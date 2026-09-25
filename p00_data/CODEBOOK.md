# Data codebook

## Raw data

raw/cam_survey_master.xlsx is the canonical workbook. The file
raw/cam_survey_main_export.csv is a direct export of its main worksheet.
The two have the same 179 rows and 33 columns in the supplied archive.

raw/cam_applications_sources.xlsx contains the working bibliography used for
the applications timeline. The paper-facing 12-entry subset is cleaned in
processed/cam_applications.csv.

## Design-level processed data

processed/cam_cell_designs.csv contains the 41 records selected by a nonblank
latex numbering field in the master sheet.

| Column | Meaning |
|---|---|
| source_row | One-based spreadsheet row including the header row |
| citation_key | BibTeX key used by the manuscript |
| manuscript_reference_number | Reference label embedded in Figs. 6 and 7 |
| proof_reference_number | Reference number after IEEE proof reordering |
| paper_title | Source paper title from the master sheet |
| cam_concept | CAM, TCAM, analog CAM, or differentiable CAM classification |
| cell_structure | Reported transistor, capacitor, or device configuration |
| technology | SRAM, DRAM, ReRAM, MTJ, or FeFET |
| process_node_nm | Fabrication process node in nanometers |
| area_um2 | Cell area in square micrometers |
| search_energy_fj_per_bit_per_search | Search energy in fJ/bit/search |
| year | Publication year |
| storage_mode_reported | Digital or Analog value from the source sheet |
| storage_mode_for_plot | Reported mode used by the original plotting logic |
| storage_mode_interpreted | Blank reported modes explicitly interpreted as Digital |
| storage_mode_inferred | True when the interpreted mode was not reported |
| states_stored | Number of representable cell states |
| bits_stored | Base-2 logarithm of states_stored |
| information_density_bits_per_um2 | Stored bits divided by cell area |
| layout_factor_k | Cell area divided by squared process node in micrometers |
| layout_normalized_search_energy | Search energy divided by layout_factor_k |

The two derived metrics are:

~~~text
bits_stored = log2(states_stored)
information_density_bits_per_um2 = bits_stored / area_um2

process_node_um = process_node_nm / 1000
layout_factor_k = area_um2 / process_node_um^2
layout_normalized_search_energy =
    search_energy_fj_per_bit_per_search / layout_factor_k
~~~

Rows with a blank reported storage mode remain excluded from the grouped plots,
matching the original notebooks. Their likely digital interpretation is
recorded separately so future analyses can make a deliberate choice.

## Table data

- table01_cam_concepts.csv generates Table I.
- table02_cell_schematics.csv indexes the assets used by Table II.
- table03_nvm_cell_schematics.csv indexes the assets used by Table III.
- table04_cam_technology_comparison.csv generates Table IV.
- table05_cam_cell_designs.csv reproduces the 37 displayed rows in Table V.
- cam_applications.csv generates Table VI and documents Fig. 8.
