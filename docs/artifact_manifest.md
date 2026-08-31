# Published artifact manifest

This manifest was checked against all 12 pages of the supplied article PDF.
The repository retains either an editable source plus export, or structured
data plus a generator, for every numbered figure and table.

## Figures

| Paper artifact | Published export | Editable source or data | Reproduction path |
|---|---|---|---|
| Fig. 1, basic RAM and CAM operation | fig01a_ram_operation.png, fig01b_cam_operation.png | figures/source/fig01_ram_vs_cam.drawio | analysis/sync_manual_figures.py |
| Fig. 2, NOR and NAND matchline architectures | fig02a_nor_type_cam.png, fig02b_nand_type_cam.png | figures/source/fig02_matchline_architectures.drawio | Manual Draw.io export, then sync |
| Fig. 3, CAM architecture and peripherals | fig03_cam_architecture_peripherals.png | figures/source/fig03_cam_architecture_peripherals.drawio | Manual Draw.io export, then sync |
| Fig. 4, cell designs over time | fig04_cell_designs_over_time.png | data/processed/cam_cell_designs.csv | analysis/plot_cell_area.py |
| Fig. 5, analog and differentiable CAM operation | fig05a_analog_cam_operation.png, fig05b_differentiable_cam_operation.png | figures/source/fig05_analog_vs_differentiable_cam.drawio | Manual Draw.io export, then sync |
| Fig. 6(a), area vs process node | fig06a_area_vs_process_node.png | data/processed/cam_cell_designs.csv | analysis/plot_cell_area.py |
| Fig. 6(b), area vs year | fig06b_area_vs_year.png | data/processed/cam_cell_designs.csv | analysis/plot_cell_area.py |
| Fig. 7(a), information density | fig07a_information_density_vs_process_node.png | data/processed/cam_cell_designs.csv | analysis/plot_information_density.py |
| Fig. 7(b), layout-normalized search energy | fig07b_layout_normalized_search_energy_vs_year.png | data/processed/cam_cell_designs.csv | analysis/plot_search_energy.py |
| Fig. 8, CAM applications timeline | fig08_cam_applications_timeline.png | data/processed/cam_applications.csv; no editable timeline file was found | Verified author export, then sync |

All paths in the published-export column are under figures/published. The same
filenames are materialized under figures/generated.

## Tables

| Paper artifact | Structured source | Schematic source, if applicable | Generated artifact |
|---|---|---|---|
| Table I, CAM concepts | table01_cam_concepts.csv | Not applicable | table01_cam_concepts.tex |
| Table II, SRAM and DRAM cells | table02_cell_schematics.csv | table02_03_cam_cell_designs.drawio, four PNG assets | table02_sram_dram_cell_schematics.tex |
| Table III, emerging NVM cells | table03_nvm_cell_schematics.csv | table03_cam_cell_designs_v2.drawio, six PNG assets | table03_nvm_cell_schematics.tex |
| Table IV, technology comparison | table04_cam_technology_comparison.csv | Not applicable | table04_cam_technology_comparison.tex |
| Table V, CAM cell designs | table05_cam_cell_designs.csv | Not applicable | table05_cam_cell_designs.tex |
| Table VI, application improvements | cam_applications.csv | Not applicable | table06_application_improvements.tex |

Structured sources are under data/processed, schematic PNGs are under
tables/assets, Draw.io files are under figures/source, and generated table
fragments are under tables/generated.

## Additional retained Draw.io files

The user requested that every hand-drawn file be retained. The two annotated
figure files and the survey-structure diagram are therefore preserved even
though they are not direct final-paper figure sources:

- figures/source/annotated_figures_1.drawio
- figures/source/annotated_figures_2.drawio
- figures/source/survey_paper_structure.drawio
