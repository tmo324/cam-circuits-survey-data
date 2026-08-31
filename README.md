# CAM Circuits Survey Data and Figure Sources

This repository contains the survey data, plotting scripts, editable diagram
sources, and table sources associated with:

T. Molom-Ochir, B. Taylor, H. Li, and Y. Chen, "Advancements in
Content-Addressable Memory (CAM) Circuits: State-of-the-Art, Applications, and
Future Directions in the AI Domain," IEEE Transactions on Circuits and Systems
I: Regular Papers, vol. 72, no. 8, pp. 3971-3982, 2025.
[https://doi.org/10.1109/TCSI.2025.3527309](https://doi.org/10.1109/TCSI.2025.3527309)

## What is included

- The canonical survey workbook and its main-sheet CSV export.
- A cleaned 41-record design dataset with documented derived metrics.
- Four Python scripts converted from the four exploratory notebooks.
- Byte-preserved Draw.io sources, renamed consistently.
- Exact author exports for every published figure panel.
- Data-generated versions of Figs. 4, 6, and 7.
- CSV sources and generated LaTeX for Tables I through VI.
- The BibTeX library used by the manuscript.

The article PDF is intentionally not redistributed here.

## Reproduce the artifacts

Python 3.10 or later is recommended.

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python analysis/generate_all.py
~~~

The last command prepares the data, materializes manual diagram exports,
regenerates all data plots and LaTeX tables, and validates the complete
artifact inventory.

Equivalent Make targets are available:

~~~bash
make all
make figures
make tables
make check
~~~

## Repository layout

~~~text
.
├── analysis/             # Clean Python scripts and validation
├── data/
│   ├── raw/              # Original canonical workbooks and sheet export
│   └── processed/        # Plot-ready and table-ready CSV files
├── docs/                 # Artifact map and source-selection notes
├── figures/
│   ├── source/           # Editable, byte-preserved Draw.io files
│   ├── published/        # Exact author exports used by the manuscript
│   └── generated/        # Outputs materialized by generate_all.py
├── tables/
│   ├── assets/           # Circuit schematic panels
│   └── generated/        # Rebuilt LaTeX table fragments
└── references.bib
~~~

## Notebook-to-script mapping

| Original notebook | Clean script | Main output |
|---|---|---|
| CAM Circuits Survey PLayground.ipynb | analysis/explore_cam_designs.py | Dataset summaries |
| CAM Circuits Survey v2.0.ipynb | analysis/plot_cell_area.py | Figs. 4 and 6 |
| CAM Circuits Survey v2.0 information density.ipynb | analysis/plot_information_density.py | Fig. 7(a) |
| CAM Circuits Survey v3.0_ Energy Area.ipynb | analysis/plot_search_energy.py | Fig. 7(b) |

The scripts remove notebook-only package installation, repeated imports,
display-only cells, and abandoned experiments. The numerical definitions and
paper-facing plots are retained.

## Important provenance notes

The master workbook contains both "latex numbering" and "proof numbering".
Figures 6 and 7 were exported before the bibliography was reordered during
proofing, so the labels visible in the published raster figures correspond to
manuscript_reference_number. The plotting scripts use that numbering by
default. Pass --numbering proof to the individual scripts to use final proof
numbers instead.

The cleaned design dataset has 41 plotted records. Table V has 37 displayed
rows because the plot dataset also retains two SRAM scaling points attached to
one cited design and three MTJ layout variants represented by a single Table V
row.

Figure 8 is retained as the exact author export, and its 12 application entries
are available in data/processed/cam_applications.csv. No editable timeline
source was present in the supplied archive, so generate_all.py materializes
that verified export rather than redrawing it.

See [the artifact manifest](docs/artifact_manifest.md) for the complete
paper-to-repository mapping and [the data codebook](data/CODEBOOK.md) for units
and formulas.

## Licensing

Code is released under the MIT License. Data, editable Draw.io sources, and
author-created figure assets are released under CC BY 4.0, as described in
LICENSE-DATA.md.

Before making a public release, repository owners should confirm that all
coauthors approve the selected license and that no third-party figure content
requires separate permission.

## Citation

Citation metadata is provided in CITATION.cff. GitHub can use this file to
display a ready-to-copy paper citation.
