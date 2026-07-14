# Data, model, score, and result licence notice

## Scope

This release provides a frozen derived benchmark snapshot for independent evaluation. It includes public split metadata, recorded-positive test labels, a frozen graph representation, model checkpoints, complete score matrices, and result tables. It does not republish every raw third-party source record.

There is intentionally no blanket data licence for the whole repository. The relevant source-specific terms and attribution obligations are recorded in data_availability/source_provenance_license_matrix.csv and data/licenses/SOURCE_LICENSES.md.

## Required handling

- Original project code in src and scripts is MIT-licensed; see LICENSE and LICENSE_SCOPE.md.
- The test-label and split artifacts are derived from a Dryad-hosted source dataset and retain the required source attribution.
- Frozen graph artifacts, checkpoints, scores, and results are mixed-source-derived materials. They should be used only with the attribution and downstream licensing terms applicable to Dryad, ChEMBL, HGNC, UniProt, and STRING components.
- No raw ChEMBL, HGNC, UniProt, STRING, or other provider database dump is claimed to be relicensed or redistributed by this package.
- The public test labels and all score matrices may be inspected and evaluated without an application process. Their public availability does not remove the duty to comply with upstream source terms.

## Archive-level licence decision before Zenodo publication

The uploader must make an explicit archive-level licence selection before publication. The recommended conservative option is to select an “Other” or source-governed licence category and link to this notice, unless the rights holder has separately confirmed a compatible release licence for the mixed derived data. A repository-wide MIT, CC0, or CC BY licence should not be selected for the full package because it would misstate the treatment of ChEMBL-derived content.

If the uploader elects to release the source-derived database portions under CC BY-SA 3.0, first confirm the attribution text and compatibility decision with the project rights holder. This local draft does not make that decision on the author’s behalf.

## Attribution

Users should cite the associated manuscript and this version-specific archive. They should also cite the original providers relevant to their use, including the Dryad dataset DOI 10.5061/dryad.wh70rxwx9, ChEMBL, HGNC, UniProt, and STRING, and follow their current conditions.
