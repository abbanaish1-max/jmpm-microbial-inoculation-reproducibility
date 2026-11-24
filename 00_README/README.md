# JMPM Microbial-Inoculation Effects: Reconstructed Empirical Analysis and Numerical-Validation Reproducibility Package

**Version:** 1.0.0  
**Prepared:** 24 November 2026  
**Resource type proposed for Zenodo:** Dataset (mixed research-data and software package)  
**Status:** Deposit-ready draft; Zenodo DOI not yet registered.

## Purpose

This archive supports the manuscript *Microbial-Inoculation Effects and Fractional Dynamics: A Study-Level Secondary Analysis with Numerical Verification*. It combines the original published secondary source file, reconstructed empirical analysis materials, the separately documented scalar numerical-validation materials, and the figures associated with the reconciled manuscript.

## Contents

- `01_SOURCE_DATA/`: original Azarbad–Junker Supplementary Table S1 workbook and a value-preserving CSV export.
- `02_EMPIRICAL_ANALYSIS/`: reconstructed Python analysis script, dependencies, run manifests, output CSVs, and QA workbooks.
- `03_NUMERICAL_VALIDATION/`: numerical-validation scripts, dependencies, run log, and the three output CSV files.
- `04_FIGURES/`: the four figures used in the reconciled empirical Results section.
- `05_LICENSES/`: attribution, licence mapping, and a proposed software licence requiring author/rightsholder confirmation.
- `06_CHECKSUMS/`: SHA-256 manifest covering the archive files (excluding the manifest itself).

## Primary source and attribution

Azarbad H, Junker RR. Biological and experimental factors that define the effectiveness of microbial inoculation on plant traits: a meta-analysis. *ISME Communications*. 2024;4(1):ycae122. https://doi.org/10.1093/ismeco/ycae122.

The primary workbook is the publisher-supplied Supplementary Table S1 from the article above. The article is distributed under the Creative Commons Attribution 4.0 International licence (CC BY 4.0); the source workbook is included unchanged with attribution. Source article: https://pmc.ncbi.nlm.nih.gov/articles/PMC11538580/

## Empirical analysis overview

The source workbook has 1,125 effect-size rows, 34 columns and 71 primary studies. The workflow performs: (1) source integrity and structure checks; (2) missingness diagnostics; (3) two-stage study-first aggregation by paper and plant-trait category; (4) 2,000 within-category percentile-bootstrap resamples of paper–category means using NumPy PCG64 `default_rng` seed `20261025`; and (5) five-fold GroupKFold prediction holding out complete primary studies.

The main categorical prediction feature set has 11 variables. Study identifiers are used only for grouping, not as predictors. Preprocessing is fitted within training folds. Ridge, Random Forest and Extra Trees are evaluated against matched training-mean baselines. Study-balanced fitting is a sensitivity analysis. See `02_EMPIRICAL_ANALYSIS/README` (if present) and the script/run manifest for full settings; the script itself contains the definitive executable configuration.

## Numerical-validation scope

The numerical scripts reproduce the stated scalar constant-order L1 and selected terminal-time variable-order tests. They are synthetic numerical benchmarks with known/reference solutions. They do not validate a crop-specific biological model, estimate microbial nitrogen-fixation rates, or constitute field calibration.

## Reproduction

### Empirical workflow

From the archive root, install the empirical requirements:

```bash
python -m pip install -r 02_EMPIRICAL_ANALYSIS/requirements.txt
python 02_EMPIRICAL_ANALYSIS/scripts/reproduce_empirical_analysis.py \
  --input-csv 01_SOURCE_DATA/supplementary_table_s1_ycae122.csv \
  --source-xlsx 01_SOURCE_DATA/supplementary_table_s1_ycae122.xlsx \
  --output-dir /path/to/reproduced_outputs
```

### Numerical validation

Install the numerical requirements and consult the run log and script usage before execution:

```bash
python -m pip install -r 03_NUMERICAL_VALIDATION/requirements.txt
python 03_NUMERICAL_VALIDATION/scripts/numerical_validation.py --help
```

The original Colab notebook was unavailable. Therefore the empirical code is a transparent reconstructed workflow rather than a claim of exact historical notebook reproduction.

## Important interpretation limits

1. Published `lnRR` and marginal sampling-variance `V` are source-derived fields; they are not recomputed from all primary-study treatment/control means, standard deviations and sample sizes because these are not all supplied in S1.
2. The dataset contains substantial missingness in soil covariates and is not a matched longitudinal dataset of inoculant abundance, soil mineral nitrogen and plant nitrogen uptake.
3. The grouped machine-learning benchmark is exploratory, uses 71 study clusters, was not tuned via nested cross-validation, and has no independent external test set. Models did not outperform matched mean baselines.
4. Several plant-trait categories contain only three or four studies; their intervals are unstable.
5. Scalar numerical-verification tests do not validate the proposed crop–microbe–nitrogen model or justify crop-, country- or dose-specific recommendations.

## Licensing

- **Original source workbook and derivative source-data citation:** CC BY 4.0, with attribution to Azarbad and Junker (2024).
- **New scripts:** MIT is proposed as a permissive software licence, but it is not activated in this draft until the relevant copyright holders authorise it. The final Zenodo record must state the approved software licence.
- **New derived outputs, figures and documentation:** proposed CC BY 4.0, subject to author confirmation.
- Third-party software dependencies remain under their own licences.

Zenodo supports mixed-licence records. Before publishing, select the approved licences and retain the file/folder mapping in `05_LICENSES/LICENSES.md`. Do not treat the proposed MIT licence as effective unless author/rightsholder approval is confirmed.

## Citation

Please cite the exact Zenodo version DOI after publication. A DOI has not yet been reserved or registered. Once published, update the `CITATION.cff`, manuscript Data and Code Availability statement, and response-to-reviewers document with the version-specific DOI and concept DOI.

## Archive integrity

Verify files using `06_CHECKSUMS/SHA256SUMS.txt`. The original S1 workbook's independently verified SHA-256 is:

`595a888363862e153b30e875e3fa88260dfcc8b862addd2332f205f93d321f03`

## Authors

Creators are listed in `zenodo_metadata_draft.json` and `CITATION.cff` in the order approved in the manuscript. Affiliation 1 is Mewar University, India; affiliation 2 is Aliko Dangote University of Science and Technology, Nigeria. Only the corresponding author's ORCID was available in the manuscript metadata.
