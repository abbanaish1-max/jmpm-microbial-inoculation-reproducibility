# GitHub and Zenodo publication workflow

## Recommended route for this mixed dataset + code package

1. Prepare and review this repository in GitHub first.
2. Keep it private while the authors confirm the per-file licence mapping in `05_LICENSES/`.
3. Once the rightsholders approve the licences and the content, make the repository public.
4. For a DOI whose Zenodo resource type is explicitly **Dataset**, sign in to Zenodo and create a **New upload** manually. Upload the release ZIP `JMPM_Zenodo_Reproducibility_Package_v1.0.0.zip` (or a final checksum-verified ZIP built from this repository), choose resource type Dataset, and enter the creators, description, keywords, source-paper relation and the GitHub repository URL as a related identifier. Apply the approved mixed-licence mapping and publish only after preview.
5. Copy the DOI assigned at publication into the manuscript's Data and Code Availability statement, this repository README, and `CITATION.cff`. Use the exact version DOI for this release.

## Optional GitHub-to-Zenodo automatic integration

Zenodo's GitHub integration archives a GitHub **release** as a **Software record**. Use this route if the authors also want a separately citable software release DOI:

1. Link GitHub to Zenodo through Zenodo profile menu > Linked accounts.
2. In Zenodo profile menu > GitHub, click Sync now and enable the public repository.
3. In GitHub, create a release from tag `v1.0.0` after all files and metadata are committed.
4. Wait for Zenodo to ingest the release; open the DOI shown for the release and verify its files, metadata and archival status.

Do not confuse the Software DOI from this integration with the Dataset DOI from a manual Zenodo upload. Avoid publishing two records unless the authors intentionally want both records and cross-reference them.

## Official guidance

- Zenodo account linking: https://help.zenodo.org/docs/profile/linking-accounts/
- Enable GitHub repository: https://help.zenodo.org/docs/github/enable-repository/
- Archive GitHub release (Software record): https://help.zenodo.org/docs/github/archive-software/github-upload/
- Zenodo create new upload (Dataset route): https://help.zenodo.org/docs/deposit/create-new-upload/
- Zenodo licences and mixed-licence deposits: https://help.zenodo.org/docs/deposit/describe-records/licenses/
- GitHub create release: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository

## Publication gates

- Confirm all 15 creators, author order, names, affiliations and ORCID metadata.
- Obtain rightsholder approval for the proposed MIT and CC BY licences for new content.
- Retain original source attribution and CC BY 4.0 terms for the Azarbad–Junker workbook.
- Review README claims and ensure the included scripts and outputs match the stated reproduction instructions.
- Regenerate the SHA-256 manifest after the final file changes.
- Do not state a DOI until Zenodo has published the record.
