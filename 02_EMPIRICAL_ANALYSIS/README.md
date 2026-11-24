# JMPM Microbial-Inoculation Empirical Reproducibility Package

**Version:** 1.0.0 (reconstructed analysis package; author review required before public deposit)  
**Manuscript:** *Microbial-Inoculation Effects and Fractional Dynamics: A Study-Level Secondary Analysis with Numerical Verification*

## 1. Purpose and scope

This package reproduces the empirical analyses in the JMPM major-revision manuscript from the published Azarbad and Junker (2024) Supplementary Table S1:

1. Source workbook preservation and provenance checks.
2. Variable-level missingness diagnostics.
3. Two-stage study-first aggregation by primary paper and plant-trait category.
4. 2,000-resample percentile bootstrap intervals across study-category means.
5. Five-fold study-grouped predictive benchmark for log response ratio (`lnRR`) using Ridge, Random Forest and Extra Trees.
6. A sensitivity analysis that gives each primary paper equal total training/evaluation weight.

The fractional differential-equation numerical-verification tests are maintained in the separate partial numerical package. This archive concerns the empirical dataset analysis.

## 2. Primary source and attribution

Azarbad H, Junker RR. Biological and experimental factors that define the effectiveness of microbial inoculation on plant traits: a meta-analysis. *ISME Communications*. 2024;4(1):ycae122. https://doi.org/10.1093/ismeco/ycae122

Official article and Supplementary Table S1:  
https://pmc.ncbi.nlm.nih.gov/articles/PMC11538580/

The article is published under a Creative Commons Attribution 4.0 International licence. The source XLSX is included unchanged with attribution. Any redistribution must retain the citation and comply with the source licence and any file-specific notice.

## 3. Included files

- `data/supplementary_table_s1_ycae122.xlsx` — preserved publisher supplementary workbook.
- `data/supplementary_table_s1_ycae122.csv` — value-preserving CSV export used by the reproduction script.
- `scripts/reproduce_empirical_analysis.py` — complete empirical reanalysis script.
- `outputs/missingness_summary.csv` — missingness by source variable.
- `outputs/study_category_means.csv` — one record per Paper × trait-category cell.
- `outputs/trait_summary_bootstrap.csv` — equal-study-weighted trait summaries and bootstrap intervals.
- `outputs/grouped_cv_fold_metrics.csv` — fold-level predictive metrics for both unweighted and study-balanced fitting.
- `outputs/grouped_cv_summary.csv` — model-level means and fold standard deviations.
- `outputs/grouped_cv_baseline.csv` — fold-specific primary row-level training-mean baseline and study-balanced weighted-mean sensitivity baseline, with RMSE, MAE and R².
- `outputs/feature_selection.csv` — inclusion/exclusion rationale for predictors.
- `outputs/run_manifest.json` — software, seeds, model settings, input hashes and scope limitations.
- `reports/` — QA, aggregation and grouped-CV review workbooks.

## 4. Reproduction

Python 3.13+ is recommended. Install the pinned dependencies:

```bash
python -m pip install -r requirements.txt
```

From the package root, run:

```bash
python scripts/reproduce_empirical_analysis.py \
  --input-csv data/supplementary_table_s1_ycae122.csv \
  --source-xlsx data/supplementary_table_s1_ycae122.xlsx \
  --output-dir outputs
```

The script writes all empirical outputs and `run_manifest.json` to `outputs/`.

## 5. Analysis definitions

### Study-first descriptive aggregation

For each primary paper and trait category, the script first computes the arithmetic mean of all source-row `lnRR` values in that Paper × category cell. It then computes the arithmetic mean of those study-category means across papers, giving each paper equal weight within the category.

The bootstrap resamples these study-category means with replacement within each category, using 2,000 replicates and NumPy `default_rng` seed `20261025`. Percentile limits are the 2.5th and 97.5th percentiles. The transformed quantity `100 × [exp(mean lnRR) − 1]` is a geometric-mean ratio translation, not an arithmetic mean percentage change or a causal effect.

### Grouped predictive benchmark

Target: `lnRR`.

Primary categorical predictors (11):
- `Plant_Trait_categories`
- `Plant_family_name`
- `Single_or_multiple_strains`
- `Microbial_Domain`
- `With_or_without_Stress`
- `Seeds_sterilization`
- `Microbial_Source`
- `Inoculation_method`
- `Inoculum_density`
- `Experimental_conditions`
- `Experimental_periods`

`#Study_ID` is used only as the grouping identifier for five-fold `GroupKFold`; it is never a predictor. `Paper`, `V`, the target `lnRR`, highly incomplete soil chemistry fields, high-cardinality taxonomic/cultivar fields, and the semantically mixed `Microbial_Phyla` field are excluded from the primary feature set. Missing categorical values are imputed using the most frequent category within each training fold. `Not specified` and `Not mentioned` are retained as explicit categories.

Models:
- Ridge regression: `alpha=1.0`.
- Random Forest: 400 trees, `min_samples_leaf=3`, `max_features=0.8`, seed `20261025`, `n_jobs=1`.
- Extra Trees: 400 trees, `min_samples_leaf=3`, `max_features=0.8`, seed `20261025`, `n_jobs=1`.

The standard benchmark is fitted without study weights. A separate sensitivity fit uses row weights proportional to `1 / (number of effect-size rows in that paper)`, rescaled so the mean training weight is one. The primary comparator is the ordinary training-row mean evaluated on the same held-out rows. The sensitivity comparator is the inverse-cluster-size weighted training mean, evaluated with corresponding test weights. Both fold-level baselines and all three metrics (RMSE, MAE, R²) are recorded in `grouped_cv_baseline.csv`.

No hyperparameter tuning or independent external test set is used. The benchmark is exploratory.

## 6. Data integrity and observed limitations

- 1,125 effect-size records from 71 primary studies.
- 34 columns in the source workbook.
- `lnRR` and sampling variance `V` are present for all 1,125 rows and all observed `V` values are positive.
- The workbook contains derived effect sizes and moderators. It does **not** contain the complete treatment/control means, standard deviations and sample sizes needed to independently recalculate every `lnRR` and `V` from the primary papers.
- Soil chemistry fields are highly incomplete; electrical conductivity also contains mixed types/scales and requires source-level unit harmonisation.
- Several trait categories contain only three or four studies; their descriptive intervals are unstable.
- Multiple outcomes from the same publication are dependent. `GroupKFold` prevents the same paper entering both training and test folds, but it does not recover the full within-paper sampling covariance.
- The empirical dataset does not support crop-specific nitrogen-fixation fluxes, nitrogen-use efficiency, dose optimisation, field yield claims, or calibration/identification of the fractional crop–microbe–nitrogen model.
- The reconstructed machine-learning pipeline makes the feature mapping explicit because the original empirical notebook was not present in the supplied project archive. Its results are not claimed to be an exact reproduction of the unavailable notebook.

## 7. Citation and interpretation requirements

Cite the original Azarbad and Junker (2024) article whenever using the source workbook. Describe this work as a **secondary reanalysis of published effect-size records**, not as a new field experiment or a new primary-study meta-analysis. Do not claim that the scalar fractional numerical tests validate a crop-specific biological model.

## 8. Deposit readiness

This is a reproducibility working package, not a public DOI record. Before Zenodo deposit, the authors should:
1. review the predictor set and the reconstructed pipeline;
2. approve the code licence and archive licence settings;
3. confirm author metadata and repository description;
4. verify the final checksum list after any edits;
5. publish the record and capture the version-specific and concept DOIs.
