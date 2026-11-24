# Licence and rights map — author approval recorded

**Package:** JMPM Microbial-Inoculation Effects Reproducibility Repository  
**Version:** 1.0.0  
**Status:** Written author-team approval reported received (15/15)

This repository contains source material and project-created materials with different rights and licences. There is no single blanket licence for every file.

## File-scope licence map

| Repository path / file group | Material | Licence | Attribution / scope |
|---|---|---|---|
| `01_SOURCE_DATA/supplementary_table_s1_ycae122.xlsx` | Publisher-supplied Supplementary Table S1 workbook, included unchanged | **CC BY 4.0** | Attribute Azarbad & Junker (2024); retain source citation and licence link |
| `01_SOURCE_DATA/supplementary_table_s1_ycae122.csv` | Value-preserving CSV format export of source workbook | **CC BY 4.0** | Attribute original source and identify this as a format conversion |
| `02_EMPIRICAL_ANALYSIS/scripts/*.py` | Newly prepared empirical-analysis Python code | **MIT** | See `MIT_LICENSE.txt`; applies only to project-authored code in this path |
| `03_NUMERICAL_VALIDATION/scripts/*.py` | Newly prepared numerical-validation and source-check Python code | **MIT** | See `MIT_LICENSE.txt`; applies only to project-authored code in this path |
| `02_EMPIRICAL_ANALYSIS/outputs/`, `reports/`, run manifests and QA material | Project-generated outputs and supporting materials | **CC BY 4.0** | Attribute source-derived content where relevant and indicate modifications |
| `03_NUMERICAL_VALIDATION/outputs/`, `reports/` | Project-generated numerical test outputs and run documentation | **CC BY 4.0** | Project-authored material; numerical limitations remain documented |
| `04_FIGURES/` | Project-prepared manuscript figures | **CC BY 4.0** | Attribute source-derived data where relevant and indicate modifications |
| Repository documentation and metadata, including README files, `00_README/`, `CITATION.cff`, `CHANGELOG.md`, requirements lists and checksum manifest | Project-authored documentation and supporting files | **CC BY 4.0** | Does not change licences of third-party content or dependencies |

## Original source-data licence and attribution

Azarbad, H., & Junker, R. R. (2024). Biological and experimental factors that define the effectiveness of microbial inoculation on plant traits: a meta-analysis. *ISME Communications*, 4(1), ycae122. https://doi.org/10.1093/ismeco/ycae122.

The source article's open-access notice identifies the Creative Commons Attribution 4.0 International licence (CC BY 4.0). Supplementary Table S1 is included unchanged, with attribution. The accompanying CSV is a value-preserving format conversion. The source workbook's byte size and SHA-256 are recorded in `01_SOURCE_DATA/SOURCE_ATTRIBUTION.md`.

CC BY 4.0: https://creativecommons.org/licenses/by/4.0/  
Source article: https://academic.oup.com/ismecommun/article/4/1/ycae122

Attribution identifies the original authors and publication, links the licence, and states that the CSV is a format conversion. Nothing in this archive implies that the original authors endorse this reanalysis.

## Licence for project-created materials

The corresponding author reports that all 15 manuscript authors gave written email approval for public release of the package and the file-scope licence arrangement above. The approval summary is in `AUTHOR_APPROVAL_AND_RIGHTS_REGISTER.md`; original emails are retained privately by the corresponding author.

The **MIT License** applies only to project-authored Python scripts in the two `scripts/` directories identified above. Its full text is in `MIT_LICENSE.txt`.

The **CC BY 4.0** licence applies to project-authored non-code outputs, figures and documentation identified in the table. Users must credit the project authors, link CC BY 4.0, indicate modifications, and not imply endorsement.

## Dependencies and third-party material

Third-party Python packages and other dependencies are not relicensed by this repository. Their upstream licences and notices continue to apply. Any third-party material included in the future must be separately reviewed and attributed before release.

## Zenodo deposit

Declare both applicable licences in Zenodo:
- Creative Commons Attribution 4.0 International (CC BY 4.0)
- MIT License

Retain this file-scope mapping in the uploaded archive and describe each licence's scope in the Zenodo record. Do not place a single root-level MIT licence over the entire repository.

Official Zenodo guidance: https://help.zenodo.org/docs/deposit/describe-records/licenses/
