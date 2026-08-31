<h1 align="center">CAM Circuits Survey</h1>

<p align="center">
  <strong>Open data and reproducible figures for content-addressable memory circuits</strong>
</p>

<p align="center">
  <a href="#paper">Paper</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="REPRODUCIBILITY.md">Reproduce Artifacts</a> ·
  <a href="#citation">Citation</a>
</p>

<p align="center">
  <a href="https://github.com/tmo324/cam-circuits-survey-data/actions/workflows/ci.yml">
    <img src="https://github.com/tmo324/cam-circuits-survey-data/actions/workflows/ci.yml/badge.svg" alt="CI">
  </a>
  <a href="https://github.com/tmo324/cam-circuits-survey-data/actions/workflows/secret-scan.yml">
    <img src="https://github.com/tmo324/cam-circuits-survey-data/actions/workflows/secret-scan.yml/badge.svg" alt="Secret scan">
  </a>
  <img src="https://img.shields.io/badge/python-3.10--3.12-3776AB?logo=python&logoColor=white" alt="Python 3.10 through 3.12">
  <a href="CITATION.cff">
    <img src="https://img.shields.io/badge/citation-CFF-4B8BBE" alt="Citation CFF">
  </a>
  <a href="https://doi.org/10.1109/TCSI.2025.3527309">
    <img src="https://img.shields.io/badge/DOI-10.1109%2FTCSI.2025.3527309-blue" alt="Paper DOI">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/code-MIT-lightgrey" alt="MIT code license">
  </a>
  <a href="LICENSE-DATA.md">
    <img src="https://img.shields.io/badge/data-CC%20BY%204.0-green" alt="CC BY 4.0 data license">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/CAM-circuits-002D72" alt="CAM circuits">
  <img src="https://img.shields.io/badge/survey-open_data-7B61FF" alt="Open survey data">
  <img src="https://img.shields.io/badge/figures-reproducible-00897B" alt="Reproducible figures">
  <img src="https://img.shields.io/badge/sources-Draw.io-E67E22" alt="Draw.io sources">
</p>

<p align="center">
  <strong>41 plotted CAM designs · 13 exact published figure panels · 9 editable Draw.io sources · 6 generated tables</strong>
</p>

---

This repository is the public artifact package for a survey of content-addressable
memory circuits. It combines the canonical survey workbook, cleaned plot-ready
data, exact figure exports from the published manuscript, editable diagram
sources, Python regeneration scripts, and LaTeX table generators.

> **Project status:** archival research artifact, version 1.0. The
> `figures/published/` directory is the authoritative record of the paper-facing
> images. The `figures/generated/` directory contains reproducible outputs.

## Paper

This repository accompanies:

T. Molom-Ochir, B. Taylor, H. Li, and Y. Chen, "Advancements in
Content-Addressable Memory (CAM) Circuits: State-of-the-Art, Applications, and
Future Directions in the AI Domain," *IEEE Transactions on Circuits and Systems
I: Regular Papers*, vol. 72, no. 8, pp. 3971-3982, 2025.

- [IEEE Xplore](https://ieeexplore.ieee.org/document/10843122)
- [DOI: 10.1109/TCSI.2025.3527309](https://doi.org/10.1109/TCSI.2025.3527309)

The article PDF is not redistributed in this repository.

## Research Artifact Highlights

- **Exact paper assets:** all 13 panels used across Figs. 1-8 are retained as
  byte-preserved author exports.
- **Data-driven regeneration:** Figs. 4, 6, and 7 are rebuilt from the released
  41-record CAM design dataset.
- **Editable sources:** nine original Draw.io files are retained without
  modifying their hand-drawn contents.
- **Complete table coverage:** CSV inputs and generated LaTeX are provided for
  Tables I-VI, including ten circuit-schematic panels.
- **Traceable provenance:** the raw workbook, its main-sheet CSV export,
  processed data, formulas, and paper-to-repository mapping are documented.

## Quick Start

Python 3.10, 3.11, and 3.12 are supported.

```sh
git clone https://github.com/tmo324/cam-circuits-survey-data.git
cd cam-circuits-survey-data

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
make install-test
```

Validate the committed release artifacts:

```sh
make check
```

Regenerate the processed dataset, all figure outputs, and all six LaTeX table
fragments:

```sh
make paper
```

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the figure-by-figure and
table-by-table reproduction matrix.

## Artifact Model

| Path | Role |
|---|---|
| [`data/raw/`](data/raw/) | Canonical survey workbooks and main-sheet CSV export |
| [`data/processed/`](data/processed/) | Plot-ready and table-ready CSV data |
| [`analysis/`](analysis/) | Notebook-derived Python scripts and validation |
| [`figures/source/`](figures/source/) | Editable, byte-preserved Draw.io files |
| [`figures/published/`](figures/published/) | Exact author exports used by the manuscript |
| [`figures/generated/`](figures/generated/) | Outputs materialized by `make paper` |
| [`tables/assets/`](tables/assets/) | Circuit schematic panels used by Tables II and III |
| [`tables/generated/`](tables/generated/) | Generated LaTeX for Tables I-VI |
| [`docs/artifact_manifest.md`](docs/artifact_manifest.md) | Paper-to-repository artifact mapping |
| [`data/CODEBOOK.md`](data/CODEBOOK.md) | Column definitions, units, and derived formulas |

## Reproducibility Boundary

There are two distinct reproduction goals:

1. **Exact paper reproduction:** use the files under `figures/published/`.
   These are the original raster exports used by the manuscript.
2. **Computational regeneration:** run `make paper`. Data plots are rendered
   again from released data, while hand-drawn panels and Fig. 8 are materialized
   from the verified author exports.

Fresh Matplotlib or Draw.io exports can differ at the pixel or byte level across
font, library, operating-system, and export-tool versions. The underlying data,
labels, and artifact coverage are validated independently of those renderer
differences.

## Notebook-to-Script Map

| Original notebook | Maintained script | Main output |
|---|---|---|
| `CAM Circuits Survey PLayground.ipynb` | `analysis/explore_cam_designs.py` | Dataset summaries |
| `CAM Circuits Survey v2.0.ipynb` | `analysis/plot_cell_area.py` | Figs. 4 and 6 |
| `CAM Circuits Survey v2.0 information density.ipynb` | `analysis/plot_information_density.py` | Fig. 7(a) |
| `CAM Circuits Survey v3.0_ Energy Area.ipynb` | `analysis/plot_search_energy.py` | Fig. 7(b) |

The scripts retain the paper-facing numerical definitions while removing
notebook-only installation cells, repeated imports, abandoned experiments, and
legacy missing-file paths.

## Citation

Machine-readable citation metadata is provided in [`CITATION.cff`](CITATION.cff).

```bibtex
@article{molomochir2025cam,
  author  = {Molom-Ochir, Tergel and Taylor, Brady and Li, Hai and Chen, Yiran},
  title   = {Advancements in Content-Addressable Memory (CAM) Circuits:
             State-of-the-Art, Applications, and Future Directions in the AI Domain},
  journal = {IEEE Transactions on Circuits and Systems I: Regular Papers},
  volume  = {72},
  number  = {8},
  pages   = {3971--3982},
  year    = {2025},
  doi     = {10.1109/TCSI.2025.3527309}
}
```

## Governance and Community

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Third-Party Notices](THIRD_PARTY_NOTICES.md)

## License

Original code is released under the [MIT License](LICENSE). Data, editable
Draw.io sources, and author-created figure assets are released under
[CC BY 4.0](LICENSE-DATA.md). Bibliographic records and cited third-party works
retain their original rights.
