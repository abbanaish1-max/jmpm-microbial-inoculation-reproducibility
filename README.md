# JMPM Microbial-Inoculation Effects — Reproducibility Repository

**Release:** v1.0.0  
**Prepared:** 24 November 2026  
**Research object:** Reconstructed empirical analysis and scalar numerical-validation materials supporting the microbial-inoculation manuscript.

## Purpose

This repository contains the source data used for the secondary analysis, the reconstructed empirical workflow, reproducible outputs, separately documented scalar numerical-verification scripts, and manuscript figures. It is intended to make the included data-processing and analysis workflow inspectable and reusable.

This is a **secondary reanalysis of published effect-size records**, not a new field or laboratory experiment. The empirical pipeline is a transparent reconstruction because the original historical Colab notebook was not recovered. The source workbook's `lnRR` and sampling-variance `V` columns are retained as supplied; the package does not recalculate every original effect size from primary-study means, standard deviations and sample sizes.

## Repository structure

- `01_SOURCE_DATA/` — publisher-supplied Supplementary Table S1 (XLSX) and value-preserving CSV export, with source attribution.
- `02_EMPIRICAL_ANALYSIS/` — Python script, requirements, run manifests, derived CSV outputs and QA workbooks.
- `03_NUMERICAL_VALIDATION/` — scalar constant-order and variable-order numerical-verification scripts, outputs and run log. These tests do not calibrate or validate the crop–microbe–nitrogen biological model.
- `04_FIGURES/` — figures associated with the reconciled empirical results.
- `05_LICENSES/` — proposed file-scope licence mapping and release approval requirements.
- `06_CHECKSUMS/` — SHA-256 manifest for repository files (the manifest excludes its own checksum).
- `00_README/` — extended documentation, Zenodo metadata draft and upload notes.
- `CITATION.cff` — citation metadata for this versioned research object.

## Main source

Azarbad H, Junker RR. Biological and experimental factors that define the effectiveness of microbial inoculation on plant traits: a meta-analysis. *ISME Communications*. 2024;4(1):ycae122. https://doi.org/10.1093/ismeco/ycae122.

The included source workbook is the publisher-provided Supplementary Table S1 and is attributed to the original authors. The source article is distributed under CC BY 4.0. See `01_SOURCE_DATA/SOURCE_ATTRIBUTION.md` and `05_LICENSES/LICENSES.md`.

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

Please cite the version-specific Zenodo record after its publication, together with the original Azarbad and Junker (2024) source article. No Zenodo DOI has been assigned to this release yet. The final DOI will be added to the repository metadata and manuscript after the record is published.

## Licensing

This repository has mixed rights. Do not assume that every file has one common licence. Read `05_LICENSES/LICENSES.md` and `05_LICENSES/RIGHTSHOLDER_LICENCE_APPROVAL_REQUIRED.txt`. The proposed MIT licence for new scripts and CC BY 4.0 licence for new outputs/documentation require confirmation by the relevant rightsholders before public release. The source workbook remains subject to its original CC BY 4.0 terms and attribution.

## Versioning and archive

The intended initial release tag is `v1.0.0`. For each future public release, update the version, changelog, `CITATION.cff` and checksum manifest before tagging. If using Zenodo's GitHub integration, be aware that Zenodo's GitHub workflow creates a **Software** record from a GitHub release. For a repository record whose primary resource type should explicitly be **Dataset**, the authors may instead create a manual Zenodo dataset deposit and cite/link this GitHub repository in its related identifiers. See `00_README/ZENODO_UPLOAD_STEPS.md`.
