# GitHub release and Zenodo publication workflow

## Current release status

The corresponding author reports that all 15 manuscript authors have provided written email approval for public release of the package and the file-scope licence mapping. The evidence summary is in `05_LICENSES/AUTHOR_APPROVAL_AND_RIGHTS_REGISTER.md`; the email correspondence is retained privately. The final licence map is `05_LICENSES/LICENSES.md`.

## Part A — Finalise and publish the GitHub repository

1. Review the root README, source attribution, author approval register, licence map, Zenodo metadata draft and checksum manifest.
2. Confirm the local GitHub Desktop working tree has no uncommitted changes and that the remote repository contains the final commit.
3. On GitHub, change the repository visibility from **Private** to **Public** only after the final content review. In repository Settings, open the Danger Zone, choose Change visibility, select Public and confirm the repository name when prompted.
4. Open the repository's Releases page and choose **Draft a new release**.
5. Create tag `v1.0.0` targeting the `main` branch. Use the title `JMPM Reproducibility Package v1.0.0`.
6. Paste the text from `00_README/GITHUB_RELEASE_NOTES_v1.0.0.md`, review the tag and target, and publish the release.
7. Open the published release and download its **Source code (zip)**. This is the versioned archive associated with tag `v1.0.0`.

GitHub's official release instructions: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository

## Part B — Create the Dataset DOI on Zenodo (recommended route)

For this mixed research-data and software package, create a manual Zenodo deposit with resource type **Dataset**:

1. Sign in to https://zenodo.org and select **New upload**.
2. Upload the GitHub release's `Source code (zip)` file.
3. Set resource type to **Dataset**, access to **Open**, and version to `1.0.0`.
4. Copy the title, description, all 15 creators in the approved author order, affiliations, keywords, funding note and related source-paper DOI from `zenodo_metadata_form.txt`.
5. In the licence field, declare both applicable licences: **CC BY 4.0** and **MIT**. Keep the path-by-path scope clear by including `05_LICENSES/LICENSES.md` and the approval register in the archive and explaining the mapping in the description.
6. Add the source article DOI `10.1093/ismeco/ycae122` with relation **IsDerivedFrom**.
7. Include the public GitHub repository URL in the related links/alternate identifier or description.
8. Preview the entire record, verify creator order, files, version, access and both licences, and publish only when every field is correct.

Zenodo supports mixed-licence records, for example software under MIT and documentation/data under CC BY: https://help.zenodo.org/docs/deposit/describe-records/licenses/

A DOI is registered upon publication. Copy both the version-specific DOI and the concept DOI from the published record.

## Part C — Update and resubmit the manuscript

After Zenodo publication:

1. Add the version-specific DOI and archive citation to the manuscript's Data and Code Availability statement and reference list.
2. Update the response to the reviewer with the repository URL, DOI and a concise description of the archived materials.
3. Update the root README and `CITATION.cff` with the Zenodo DOI. Do not change the files in the already published Zenodo version; if the archive itself needs a change after publication, issue a new version.
4. Run the final cross-check of the manuscript, reviewer response, GitHub repository and Zenodo metadata before resubmission.

## Optional GitHub-to-Zenodo integration

Zenodo's automatic GitHub workflow archives releases as **Software** records. Do not enable it for this first deposit if the intended single primary record is a **Dataset**. A separate Software DOI may be created later only if the authors intentionally want a second, separately citable record.

Official Zenodo GitHub guidance:
- https://help.zenodo.org/docs/profile/linking-accounts/
- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/
