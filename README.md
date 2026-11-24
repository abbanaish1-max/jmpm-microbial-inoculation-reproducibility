# JMPM Microbial-Inoculation Effects — Reproducibility Repository

**Release:** v1.0.0  
**Prepared:** 24 November 2026  
**Research object:** Reconstructed empirical analysis and scalar numerical-validation materials supporting the microbial-inoculation manuscript.

## Purpose

This repository contains the source data used for the secondary analysis, the reconstructed empirical workflow, reproducible outputs, separately documented scalar numerical-verification scripts, and manuscript figures. It is intended to make the included data-processing and analysis workflow inspectable and reusable.

This is a **secondary reanalysis of published effect-size records**, not a new field or laboratory experiment. The empirical pipeline is a transparent reconstruction because the original historical Colab notebook was not recovered. The source workbook's `lnRR` and sampling-variance `V` columns are retained as supplied; the package does not recalculate every original effect size from primary-study means, standard deviations and sample sizes.

## Repository structure

- `00_README/` — extended documentation, Zenodo metadata draft, GitHub release notes and upload instructions.
- `01_SOURCE_DATA/` — publisher-supplied Supplementary Table S1 workbook and value-preserving CSV export, with source attribution.
- `02_EMPIRICAL_ANALYSIS/` — Python script, requirements, run manifests, outputs and QA workbooks.
- `03_NUMERICAL_VALIDATION/` — scalar constant-order and variable-order numerical-verification scripts, outputs and run log. These tests do not calibrate or validate the crop–microbe–nitrogen biological model.
- `04_FIGURES/` — figures associated with the reconciled empirical results.
- `05_LICENSES/` — file-scope licence map, MIT licence text and author approval register.
- `06_CHECKSUMS/` — SHA-256 manifest for repository files (the manifest excludes its own checksum).
- `CITATION.cff` — citation metadata for this versioned research object.

## Main source

Azarbad H, Junker RR. Biological and experimental factors that define the effectiveness of microbial inoculation on plant traits: a meta-analysis. *ISME Communications*. 2024;4(1):ycae122. https://doi.org/10.1093/ismeco/ycae122.

The included source workbook is the publisher-provided Supplementary Table S1. The source article is distributed under CC BY 4.0. The workbook is included unchanged with attribution; the accompanying CSV is a value-preserving format conversion. See `01_SOURCE_DATA/SOURCE_ATTRIBUTION.md` and `05_LICENSES/LICENSES.md`.

## Reproduce the empirical analysis

Python 3.13+ is recommended. From the repository root:

```bash
python -m pip install -r 02_EMPIRICAL_ANALYSIS/requirements.txt
python 02_EMPIRICAL_ANALYSIS/scripts/reproduce_empirical_analysis.py \
  --input-csv 01_SOURCE_DATA/supplementary_table_s1_ycae122.csv \
  --source-xlsx 01_SOURCE_DATA/supplementary_table_s1_ycae122.xlsx \
  --output-dir 02_EMPIRICAL_ANALYSIS/outputs_reproduced
```

See `02_EMPIRICAL_ANALYSIS/README.md` and `02_EMPIRICAL_ANALYSIS/metadata/run_manifest.json` for the methods, feature set, seeds, model settings and limitations. Reproduced outputs can be compared with the archived files in `02_EMPIRICAL_ANALYSIS/outputs/`.

## Reproduce the scalar numerical checks

```bash
python -m pip install -r 03_NUMERICAL_VALIDATION/requirements.txt
python 03_NUMERICAL_VALIDATION/scripts/numerical_validation.py \
  --output-dir 03_NUMERICAL_VALIDATION/outputs_reproduced
```

See `03_NUMERICAL_VALIDATION/README.md` before interpreting these numerical tests.

## Key limitations

1. The original empirical notebook and exact historical predictor mapping were unavailable; this is a transparent reconstructed pipeline, not a bit-for-bit rerun of that notebook.
2. The workbook contains `lnRR` and `V`, but not the complete primary-study treatment/control means, standard deviations and sample sizes required to recalculate every effect size from first principles.
3. The 71-study grouped predictive benchmark is exploratory, without nested tuning or an independent external test set.
4. The empirical dataset does not identify crop-specific nitrogen-fixation fluxes, nitrogen-use efficiency, yield response, or parameters of the proposed fractional crop–microbe–nitrogen model.
5. The scalar numerical tests verify selected numerical schemes on specified test problems; they do not constitute empirical or biological validation of the crop model.

## Citation

Please cite the version-specific Zenodo record after its publication, together with the original Azarbad and Junker (2024) source article. The Zenodo DOI has not yet been assigned to this release. The corresponding author will update the repository citation metadata and manuscript after publication.

## Licensing and author approval

This repository uses a **mixed-licence arrangement**; do not assume that all files have one common licence:

- **Original source workbook and its value-preserving CSV export:** CC BY 4.0, with attribution to Azarbad and Junker (2024) and an indication that the CSV is a format conversion.
- **Project-authored Python scripts** in `02_EMPIRICAL_ANALYSIS/scripts/` and `03_NUMERICAL_VALIDATION/scripts/`: MIT License.
- **Project-authored figures, derived outputs, QA materials and documentation:** CC BY 4.0.

The corresponding author reports that all 15 manuscript authors have provided written email approval for public release and this file-scope licence arrangement. The approval register is `05_LICENSES/AUTHOR_APPROVAL_AND_RIGHTS_REGISTER.md`; the original emails are retained privately. Third-party software dependencies remain under their respective upstream licences. The complete file map and licence terms are in `05_LICENSES/LICENSES.md` and `05_LICENSES/MIT_LICENSE.txt`.

## Versioning and archive

The initial release tag is `v1.0.0`. For each future public release, update the version, changelog, `CITATION.cff` and checksum manifest before tagging. The recommended DOI route for this mixed research dataset and code archive is a manual Zenodo deposit with resource type **Dataset**. See `00_README/ZENODO_UPLOAD_STEPS.md`.
