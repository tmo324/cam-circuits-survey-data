# Reproducing the CAM Survey Artifacts

This repository supports two complementary goals: preserving the exact images
used by the paper and regenerating the data-driven artifacts from released
sources. These goals use separate directories so a fresh plot is never confused
with the archival paper image.

## 1. Environment

Python 3.10, 3.11, or 3.12 is recommended.

```sh
git clone https://github.com/tmo324/cam-circuits-survey-data.git
cd cam-circuits-survey-data

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
make install-test
```

The default installation is CPU-only and contains four runtime dependencies:
NumPy, pandas, Matplotlib, and openpyxl.

## 2. Validate the Released Artifact Set

```sh
make check
```

The checks cover:

- Python compilation and the public-release contract.
- Draw.io XML validity for all nine editable sources.
- Presence of all 13 published and generated figure panels.
- Byte equality for the eight generated panels materialized from author exports.
- Presence of ten table schematic assets and six generated LaTeX tables.
- Expected dataset sizes: 41 plotted designs, 37 Table V rows, and 12
  application entries.
- Equality of the master workbook's `main` sheet and its CSV export.
- Availability of every cited BibTeX key used by the structured artifact data.
- A known layout-normalized search-energy calculation.

## 3. Regenerate Everything

```sh
make paper
```

This command runs the complete public pipeline:

1. Rebuild `data/processed/cam_cell_designs.csv` from the canonical workbook.
2. Materialize the verified manual figure exports.
3. Replot Figs. 4, 6, and 7 from the cleaned design data.
4. Rebuild all six LaTeX table fragments.
5. Run the artifact validator.

Individual targets are also available:

```sh
make data
make figures
make tables
make check
```

## 4. Figure Reproduction Matrix

| Paper artifact | Public reproduction path | Result |
|---|---|---|
| Fig. 1, RAM and CAM operation | `analysis/sync_manual_figures.py` | Exact verified author export |
| Fig. 2, NOR and NAND matchlines | `analysis/sync_manual_figures.py` | Exact verified author export |
| Fig. 3, CAM architecture | `analysis/sync_manual_figures.py` | Exact verified author export |
| Fig. 4, cell designs over time | `analysis/plot_cell_area.py` | Fresh data-driven replot |
| Fig. 5, analog and differentiable CAM | `analysis/sync_manual_figures.py` | Exact verified author export |
| Fig. 6(a), area vs. process node | `analysis/plot_cell_area.py` | Fresh data-driven replot |
| Fig. 6(b), area vs. year | `analysis/plot_cell_area.py` | Fresh data-driven replot |
| Fig. 7(a), information density | `analysis/plot_information_density.py` | Fresh data-driven replot |
| Fig. 7(b), normalized search energy | `analysis/plot_search_energy.py` | Fresh data-driven replot |
| Fig. 8, applications timeline | `analysis/sync_manual_figures.py` | Exact verified author export |

The exact paper-facing images are always under `figures/published/`. Outputs
created or materialized by the public pipeline are under `figures/generated/`.

## 5. Table Reproduction Matrix

| Paper artifact | Structured source | Generated output |
|---|---|---|
| Table I, CAM concepts | `data/processed/table01_cam_concepts.csv` | `tables/generated/table01_cam_concepts.tex` |
| Table II, SRAM and DRAM cells | `data/processed/table02_cell_schematics.csv` | `tables/generated/table02_sram_dram_cell_schematics.tex` |
| Table III, emerging NVM cells | `data/processed/table03_nvm_cell_schematics.csv` | `tables/generated/table03_nvm_cell_schematics.tex` |
| Table IV, technology comparison | `data/processed/table04_cam_technology_comparison.csv` | `tables/generated/table04_cam_technology_comparison.tex` |
| Table V, CAM cell designs | `data/processed/table05_cam_cell_designs.csv` | `tables/generated/table05_cam_cell_designs.tex` |
| Table VI, application improvements | `data/processed/cam_applications.csv` | `tables/generated/table06_application_improvements.tex` |

To compile a standalone six-page table preview when `pdflatex` is available:

```sh
mkdir -p /tmp/cam-survey-tables
pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=/tmp/cam-survey-tables tables/preview.tex
```

The standalone preview does not load the paper bibliography, so unresolved
citation warnings are expected. A nonzero LaTeX exit code is not expected.

## 6. Exactness and Renderer Drift

The files in `figures/published/` are archival assets, not regenerated claims.
They are the exact author exports used by the manuscript source.

Fresh raster output can differ because Matplotlib, fonts, operating systems,
Draw.io versions, antialiasing, DPI, bounding-box calculations, and metadata
encoders can change. The public validator therefore checks artifact coverage,
data invariants, and exact copies of manual exports. It does not require fresh
Matplotlib renders to be byte-identical to the archival paper PNGs.

## 7. Provenance

- `data/raw/cam_survey_master.xlsx` is the canonical survey workbook.
- `data/raw/cam_survey_main_export.csv` is its direct `main`-sheet export.
- `data/CODEBOOK.md` records units, formulas, selection rules, and inferred
  fields.
- `docs/artifact_manifest.md` maps every numbered paper figure and table to its
  retained source and generator.
- `docs/source_selection.md` records which original working files were retained,
  replaced, or intentionally omitted.

When publishing a derived analysis, record the repository commit, Python and
dependency versions, operating system, and command used to generate it.
