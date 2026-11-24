#!/usr/bin/env python3
"""Reproduce the JMPM microbial-inoculation empirical reanalysis from the S1 CSV.

The S1 CSV is a value-preserving export of the published Supplementary Table S1 XLSX.
This script reproduces:
  1) variable missingness diagnostics;
  2) Paper × plant-trait two-stage aggregation;
  3) 2,000-resample study-level percentile bootstrap intervals;
  4) five-fold GroupKFold prediction benchmarks with 11 prespecified categorical fields;
  5) row-level and study-balanced evaluation, with both matched row-mean and weighted-mean baselines.

It does not recalculate the source lnRR or V from primary-paper treatment/control means,
because those raw means, SDs and sample sizes are not columns in Supplementary Table S1.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


FEATURES = [
    "Plant_Trait_categories",
    "Plant_family_name",
    "Single_or_multiple_strains",
    "Microbial_Domain",
    "With_or_without_Stress",
    "Seeds_sterilization",
    "Microbial_Source",
    "Inoculation_method",
    "Inoculum_density",
    "Experimental_conditions",
    "Experimental_periods",
]
TRAIT_ORDER = [
    "Flower Traits",
    "Leaf Traits",
    "Shoot Traits",
    "Root Traits",
    "Seeds Traits",
    "Overall Plant Growth Traits",
    "Fruit Traits",
    "Nodulation Traits",
]
BOOTSTRAP_SEED = 20261025
N_BOOTSTRAP = 2000
MODEL_SEED = 20261025


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def is_missing(v: str | None) -> bool:
    return v is None or str(v).strip().upper() in {"", "NA", "N/A", "NULL"}


def read_csv(path: Path):
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    if not rows:
        raise ValueError(f"No data rows found in {path}")
    required = {"Paper", "#Study_ID", "Plant_Trait_categories", "lnRR", "V"}
    missing = required.difference(fields)
    if missing:
        raise ValueError(f"Required fields missing: {sorted(missing)}")
    return fields, rows


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def variable_missingness(fields, rows):
    output = []
    for col in fields:
        vals = [r.get(col) for r in rows]
        missing = sum(is_missing(v) for v in vals)
        nonmissing = [v for v in vals if not is_missing(v)]
        output.append({
            "variable": col,
            "n_rows": len(rows),
            "nonmissing_n": len(nonmissing),
            "missing_n": missing,
            "missing_pct": round(100.0 * missing / len(rows), 4),
            "unique_nonmissing_values": len(set(nonmissing)),
        })
    return output


def study_category_aggregation(rows):
    grouped = defaultdict(list)
    study_row_counts = Counter()
    for r in rows:
        paper = r["Paper"]
        study_row_counts[paper] += 1
        key = (paper, r["Plant_Trait_categories"])
        grouped[key].append(float(r["lnRR"]))

    study_category_rows = []
    by_trait = defaultdict(list)
    for (paper, trait), values in sorted(grouped.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        mean_val = statistics.mean(values)
        median_val = statistics.median(values)
        by_trait[trait].append(mean_val)
        study_category_rows.append({
            "Paper": paper,
            "Trait_category": trait,
            "effect_size_rows_in_cell": len(values),
            "study_category_mean_lnRR": mean_val,
            "study_category_median_lnRR": median_val,
        })

    # Preserve deterministic trait iteration order and RNG stream.
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    trait_summary = []
    for trait in TRAIT_ORDER:
        vals = np.asarray(by_trait[trait], dtype=float)
        boots = np.empty(N_BOOTSTRAP, dtype=float)
        for b in range(N_BOOTSTRAP):
            boots[b] = rng.choice(vals, size=len(vals), replace=True).mean()
        source_rows = sum(
            d["effect_size_rows_in_cell"] for d in study_category_rows
            if d["Trait_category"] == trait
        )
        trait_summary.append({
            "trait_category": trait,
            "study_count": int(len(vals)),
            "effect_size_rows": int(source_rows),
            "mean_study_level_lnRR": float(vals.mean()),
            "bootstrap_95_lower": float(np.quantile(boots, 0.025)),
            "bootstrap_95_upper": float(np.quantile(boots, 0.975)),
            "geometric_mean_ratio_translation_pct": float(100.0 * (math.exp(float(vals.mean())) - 1.0)),
            "median_study_level_lnRR": float(np.median(vals)),
            "bootstrap_resamples": N_BOOTSTRAP,
            "bootstrap_seed": BOOTSTRAP_SEED,
        })
    return study_category_rows, trait_summary, study_row_counts


def new_models():
    return {
        "Ridge": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(
            n_estimators=400, min_samples_leaf=3, max_features=0.8,
            random_state=MODEL_SEED, n_jobs=1
        ),
        "Extra Trees": ExtraTreesRegressor(
            n_estimators=400, min_samples_leaf=3, max_features=0.8,
            random_state=MODEL_SEED, n_jobs=1
        ),
    }


def grouped_cv(rows, study_row_counts):
    X = np.asarray([
        [np.nan if is_missing(r.get(col)) else str(r.get(col)) for col in FEATURES]
        for r in rows
    ], dtype=object)
    y = np.asarray([float(r["lnRR"]) for r in rows], dtype=float)
    groups = np.asarray([str(r["#Study_ID"]) for r in rows], dtype=object)

    cv = GroupKFold(n_splits=5)
    fold_outputs = []
    summary = []
    baseline_outputs = []

    for train_idx, test_idx in cv.split(X, y, groups):
        fold_no = len(baseline_outputs) + 1
        train_groups = set(groups[train_idx])
        test_groups = set(groups[test_idx])
        overlap = len(train_groups.intersection(test_groups))

        # Study-balanced weights are inverse numbers of effect-size rows per paper.
        w_train = np.asarray(
            [1.0 / study_row_counts[rows[i]["Paper"]] for i in train_idx], dtype=float
        )
        w_train *= len(w_train) / w_train.sum()
        w_test = np.asarray(
            [1.0 / study_row_counts[rows[i]["Paper"]] for i in test_idx], dtype=float
        )

        # Primary comparator: ordinary training-row mean, evaluated on the same held-out rows.
        row_training_mean = float(np.mean(y[train_idx]))
        row_base_pred = np.full(len(test_idx), row_training_mean, dtype=float)

        # Sensitivity comparator: inverse-cluster-size weighted training mean, evaluated
        # with the corresponding test weights so each primary study has equal total weight.
        weighted_training_mean = float(np.average(y[train_idx], weights=w_train))
        weighted_base_pred = np.full(len(test_idx), weighted_training_mean, dtype=float)
        baseline_outputs.append({
            "fold": fold_no,
            "train_studies": len(train_groups),
            "test_studies": len(test_groups),
            "test_rows": len(test_idx),
            "train_test_group_overlap": overlap,
            "row_level_training_mean": row_training_mean,
            "row_level_baseline_RMSE": float(np.sqrt(mean_squared_error(y[test_idx], row_base_pred))),
            "row_level_baseline_MAE": float(mean_absolute_error(y[test_idx], row_base_pred)),
            "row_level_baseline_R2": float(r2_score(y[test_idx], row_base_pred)),
            "study_balanced_training_mean": weighted_training_mean,
            "study_balanced_baseline_row_RMSE": float(np.sqrt(mean_squared_error(y[test_idx], weighted_base_pred))),
            "study_balanced_baseline_row_MAE": float(mean_absolute_error(y[test_idx], weighted_base_pred)),
            "study_balanced_baseline_row_R2": float(r2_score(y[test_idx], weighted_base_pred)),
            "study_balanced_baseline_RMSE": float(np.sqrt(mean_squared_error(y[test_idx], weighted_base_pred, sample_weight=w_test))),
            "study_balanced_baseline_MAE": float(mean_absolute_error(y[test_idx], weighted_base_pred, sample_weight=w_test)),
            "study_balanced_baseline_R2": float(r2_score(y[test_idx], weighted_base_pred, sample_weight=w_test)),
        })

        for name, model in new_models().items():
            # Training-fold mode imputation and one-hot encoding are fitted only on train.
            pipe = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ("model", model),
            ])

            # Unweighted reconstruction.
            pipe.fit(X[train_idx], y[train_idx])
            pred = pipe.predict(X[test_idx])
            unweighted = {
                "row_RMSE": float(np.sqrt(mean_squared_error(y[test_idx], pred))),
                "row_MAE": float(mean_absolute_error(y[test_idx], pred)),
                "row_R2": float(r2_score(y[test_idx], pred)),
            }

            # Study-balanced sensitivity: equal total training and test weight per paper.
            pipe_w = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ("model", new_models()[name]),
            ])
            pipe_w.fit(X[train_idx], y[train_idx], model__sample_weight=w_train)
            pred_w = pipe_w.predict(X[test_idx])
            weighted = {
                "row_RMSE": float(np.sqrt(mean_squared_error(y[test_idx], pred_w))),
                "row_MAE": float(mean_absolute_error(y[test_idx], pred_w)),
                "row_R2": float(r2_score(y[test_idx], pred_w)),
                "study_balanced_RMSE": float(np.sqrt(mean_squared_error(y[test_idx], pred_w, sample_weight=w_test))),
                "study_balanced_MAE": float(mean_absolute_error(y[test_idx], pred_w, sample_weight=w_test)),
                "study_balanced_R2": float(r2_score(y[test_idx], pred_w, sample_weight=w_test)),
            }

            fold_outputs.append({
                "model": name,
                "fold": fold_no,
                "n_test_rows": len(test_idx),
                "n_train_studies": len(train_groups),
                "n_test_studies": len(test_groups),
                "train_test_group_overlap": overlap,
                **{f"unweighted_{k}": v for k, v in unweighted.items()},
                **{f"study_weighted_{k}": v for k, v in weighted.items()},
            })

    # Model-wise means and fold SDs.
    for name in ["Ridge", "Random Forest", "Extra Trees"]:
        subset = [r for r in fold_outputs if r["model"] == name]
        def m(key):
            vals = np.asarray([r[key] for r in subset], dtype=float)
            return float(vals.mean()), float(vals.std(ddof=1))
        summary.append({
            "model": name,
            "unweighted_row_RMSE_mean": m("unweighted_row_RMSE")[0],
            "unweighted_row_RMSE_fold_SD": m("unweighted_row_RMSE")[1],
            "unweighted_row_MAE_mean": m("unweighted_row_MAE")[0],
            "unweighted_row_MAE_fold_SD": m("unweighted_row_MAE")[1],
            "unweighted_row_R2_mean": m("unweighted_row_R2")[0],
            "unweighted_row_R2_fold_SD": m("unweighted_row_R2")[1],
            "study_weighted_RMSE_mean": m("study_weighted_study_balanced_RMSE")[0],
            "study_weighted_RMSE_fold_SD": m("study_weighted_study_balanced_RMSE")[1],
            "study_weighted_MAE_mean": m("study_weighted_study_balanced_MAE")[0],
            "study_weighted_MAE_fold_SD": m("study_weighted_study_balanced_MAE")[1],
            "study_weighted_R2_mean": m("study_weighted_study_balanced_R2")[0],
            "study_weighted_R2_fold_SD": m("study_weighted_study_balanced_R2")[1],
        })
    return fold_outputs, summary, baseline_outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--source-xlsx", default=None)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    csv_path = Path(args.input_csv)
    xlsx_path = Path(args.source_xlsx) if args.source_xlsx else None
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    fields, rows = read_csv(csv_path)
    miss = variable_missingness(fields, rows)
    write_csv(out_dir / "missingness_summary.csv", list(miss[0].keys()), miss)

    study_category_rows, trait_summary, study_row_counts = study_category_aggregation(rows)
    write_csv(out_dir / "study_category_means.csv", list(study_category_rows[0].keys()), study_category_rows)
    write_csv(out_dir / "trait_summary_bootstrap.csv", list(trait_summary[0].keys()), trait_summary)

    cv_folds, cv_summary, baseline = grouped_cv(rows, study_row_counts)
    write_csv(out_dir / "grouped_cv_fold_metrics.csv", list(cv_folds[0].keys()), cv_folds)
    write_csv(out_dir / "grouped_cv_summary.csv", list(cv_summary[0].keys()), cv_summary)
    write_csv(out_dir / "grouped_cv_baseline.csv", list(baseline[0].keys()), baseline)

    feature_decisions = [
        ("Plant_Trait_categories","INCLUDE","Complete; 8 trait categories."),
        ("Plant_family_name","INCLUDE","Complete; 11 botanical families; reduced dimensionality."),
        ("Single_or_multiple_strains","INCLUDE","Complete; single strain versus consortium."),
        ("Microbial_Domain","INCLUDE","Complete; broad bacterial/fungal domain."),
        ("With_or_without_Stress","INCLUDE","Complete; experimental stress context."),
        ("Seeds_sterilization","INCLUDE","Complete; includes explicit 'Not mentioned' level."),
        ("Microbial_Source","INCLUDE","2.5% missing; training-fold mode imputation."),
        ("Inoculation_method","INCLUDE","0.9% missing; training-fold mode imputation."),
        ("Inoculum_density","INCLUDE","Categorical level only; not absolute dose."),
        ("Experimental_conditions","INCLUDE","Complete; sterilized/unsterilized/field."),
        ("Experimental_periods","INCLUDE","0.9% missing; categorical period bins."),
        ("#Study_ID","GROUP ONLY","GroupKFold grouping variable; never a predictor."),
        ("Paper","EXCLUDE","Publication identifier; identity leakage risk."),
        ("lnRR","TARGET","Prediction outcome."),
        ("V","EXCLUDE","Sampling variance, not a biological moderator."),
        ("Microbial_Phyla","EXCLUDE","Contains 'Consortium' as a non-phylum category."),
        ("Taxonomic class/order/family/genus/species/strain","DESCRIPTIVE ONLY","Missingness and sparse levels."),
        ("Plant model/genus/Latin name/cultivar","DESCRIPTIVE OR SENSITIVITY","Higher-cardinality/overlapping taxonomic information."),
        ("Duration_of_incubation_group","EXCLUDE","Mixed numeric/category encoding and most observations unspecified."),
        ("Soil chemistry fields","EXCLUDE","High missingness; electrical conductivity also needs unit harmonisation."),
    ]
    write_csv(out_dir / "feature_selection.csv",
              ["variable","decision","reason"],
              [dict(variable=a, decision=b, reason=c) for a,b,c in feature_decisions])

    source_hash = sha256_file(xlsx_path) if xlsx_path and xlsx_path.is_file() else None
    manifest = {
        "analysis": "JMPM microbial-inoculation empirical reanalysis",
        "input_csv": csv_path.name,
        "input_csv_sha256": sha256_file(csv_path),
        "source_xlsx": xlsx_path.name if xlsx_path else None,
        "source_xlsx_bytes": xlsx_path.stat().st_size if xlsx_path and xlsx_path.is_file() else None,
        "source_xlsx_sha256": source_hash,
        "n_rows": len(rows),
        "n_studies": len({r["#Study_ID"] for r in rows}),
        "n_variables": len(fields),
        "features": FEATURES,
        "target": "lnRR",
        "bootstrap_resamples": N_BOOTSTRAP,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "models_seed": MODEL_SEED,
        "cv": "5-fold GroupKFold by #Study_ID",
        "models": {
            "Ridge": {"alpha": 1.0},
            "Random Forest": {"n_estimators":400,"min_samples_leaf":3,"max_features":0.8,"random_state":MODEL_SEED,"n_jobs":1},
            "Extra Trees": {"n_estimators":400,"min_samples_leaf":3,"max_features":0.8,"random_state":MODEL_SEED,"n_jobs":1},
        },
        "preprocessing": "Most-frequent categorical imputation and one-hot encoding fitted within each training fold.",
        "baselines": {
            "primary_row_level": "Unweighted mean of training-fold lnRR rows; evaluated on the same held-out rows.",
            "study_balanced_sensitivity": "Inverse-cluster-size weighted mean of training-fold lnRR rows; evaluated with inverse-cluster-size test weights."
        },
        "study_balance_sensitivity": "Fit and evaluate using row weights proportional to 1 / effect-size rows per primary paper.",
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scikit_learn": sklearn.__version__,
        "limitations": [
            "The supplied XLSX contains lnRR and V but not all raw treatment/control means, SDs and sample sizes needed to recompute the individual effect sizes.",
            "The original empirical notebook and exact historical predictor mapping were unavailable; this is a transparent reconstructed pipeline.",
            "Only 71 study clusters are available; no nested hyperparameter tuning or independent external test set is used.",
            "This dataset does not calibrate crop-specific nitrogen-fixation fluxes, NUE, yield response, or the proposed fractional crop model."
        ],
    }
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({
        "rows": len(rows),
        "studies": len({r["#Study_ID"] for r in rows}),
        "study_category_cells": len(study_category_rows),
        "outputs": sorted(p.name for p in out_dir.iterdir()),
        "source_xlsx_sha256": source_hash,
    }, indent=2))


if __name__ == "__main__":
    main()
