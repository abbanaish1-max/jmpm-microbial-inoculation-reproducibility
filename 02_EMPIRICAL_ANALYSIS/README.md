# JMPM Microbial-Inoculation Effects: Reconstructed Empirical Analysis

**Version:** 1.0.0 — author-team release approval recorded  
**Prepared:** 24 November 2026

## Purpose and scope

This package reconstructs the empirical analyses in the JMPM major-revision manuscript from the published Azarbad and Junker (2024) Supplementary Table S1. The workflow includes source workbook checks, variable-level missingness, two-stage study-first aggregation by paper and plant-trait category, 2,000-resample percentile bootstrap intervals, five-fold study-grouped prediction for `lnRR`, and an equal-paper-weight sensitivity analysis.

The original historical Colab notebook was not recovered. This is a transparent reconstruction, not a bit-for-bit historical notebook rerun. The separate scalar fractional numerical-verification tests are in `03_NUMERICAL_VALIDATION/` and are not empirical or biological validation of the crop–microbe–nitrogen model.

## Source and attribution

Azarbad H, Junker RR. Biological and experimental factors that define the effectiveness of microbial inoculation on plant traits: a meta-analysis. *ISME Communications*. 2024;4(1):ycae122. https://doi.org/10.1093/ismeco/ycae122.

The source XLSX is included unchanged in `01_SOURCE_DATA/` under the source article's CC BY 4.0 terms, with attribution. The CSV is a value-preserving format conversion. Retain the citation, licence link and conversion notice.

## Included files

Paths are relative to the repository root:
- `01_SOURCE_DATA/supplementary_table_s1_ycae122.xlsx` — publisher supplementary workbook.
- `01_SOURCE_DATA/supplementary_table_s1_ycae122.csv` — value-preserving CSV export.
- `02_EMPIRICAL_ANALYSIS/scripts/reproduce_empirical_analysis.py` — empirical reanalysis script.
- `02_EMPIRICAL_ANALYSIS/outputs/` — missingness, study-category, bootstrap, grouped-CV and baseline outputs.
- `02_EMPIRICAL_ANALYSIS/metadata/run_manifest.json` and `outputs/run_manifest.json` — software, seeds, model settings, hashes and limitations.
- `02_EMPIRICAL_ANALYSIS/reports/` — QA, aggregation and grouped-CV review workbooks.
- `02_EMPIRICAL_ANALYSIS/requirements.txt` — Python dependencies.

## Reproduction

Run from repository root with Python 3.13+:

```bash
python -m pip install -r 02_EMPIRICAL_ANALYSIS/requirements.txt
python 02_EMPIRICAL_ANALYSIS/scripts/reproduce_empirical_analysis.py \
  --input-csv 01_SOURCE_DATA/supplementary_table_s1_ycae122.csv \
  --source-xlsx 01_SOURCE_DATA/supplementary_table_s1_ycae122.xlsx \
  --output-dir 02_EMPIRICAL_ANALYSIS/outputs_reproduced
```

## Analysis definitions

For each primary paper and trait category, the script first computes the mean of source-row `lnRR` values within that Paper × category cell. It then averages those study-category means across papers, giving each paper equal weight within the category. The bootstrap resamples these study-category means within category using 2,000 replicates and NumPy `default_rng` seed `20261025`. The transformed quantity `100 × [exp(mean lnRR) − 1]` is a geometric-mean ratio translation, not an arithmetic mean percentage change or causal effect.

The grouped predictive target is `lnRR`. The 11 prespecified categorical predictors are listed in the executable script. `#Study_ID` is used only as the GroupKFold grouping variable, not as a predictor. Imputation and model preprocessing are fitted within training folds. Ridge, Random Forest and Extra Trees are compared with matched training-mean baselines. The benchmark is exploratory: no nested tuning or independent external test set is used.

## Data integrity and limitations

- 1,125 effect-size records from 71 primary studies and 34 source columns.
- `lnRR` and sampling variance `V` are source-provided and are not recalculated from all primary-study means, standard deviations and sample sizes.
- Soil chemistry fields are highly incomplete; electrical conductivity has mixed types/scales requiring source-level harmonisation.
- Some trait categories contain only three or four studies, so their intervals are unstable.
- GroupKFold prevents the same primary study entering train and test folds but does not recover within-paper sampling covariance.
- The empirical dataset does not support crop-specific nitrogen-fixation fluxes, nitrogen-use efficiency, dose optimisation, field-yield claims, or calibration of the fractional crop–microbe–nitrogen model.

## Licence and author approval

The project-authored Python script in `02_EMPIRICAL_ANALYSIS/scripts/` is licensed under MIT. Project outputs, QA material, run manifests and documentation are licensed under CC BY 4.0. The source workbook and CSV conversion retain the source attribution and CC BY 4.0 terms. The corresponding author reports written email approval from all 15 manuscript authors for public release and this file-scope arrangement. See `05_LICENSES/LICENSES.md` and `05_LICENSES/AUTHOR_APPROVAL_AND_RIGHTS_REGISTER.md`. Third-party dependencies remain under their upstream licences.
