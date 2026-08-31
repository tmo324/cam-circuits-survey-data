"""Shared paths, data loading, and plot styling."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA = ROOT / "data" / "processed" / "cam_cell_designs.csv"
GENERATED_FIGURES = ROOT / "figures" / "generated"

TECHNOLOGY_ORDER = ["SRAM", "DRAM", "FeFET", "MTJ", "ReRAM"]

TECHNOLOGY_STYLE = {
    "SRAM": {"marker": "P", "color": "#e7b349"},
    "DRAM": {"marker": "<", "color": "black"},
    "FeFET": {"marker": "d", "color": "#89a472"},
    "MTJ": {"marker": "s", "color": "#c78cc6"},
    "ReRAM": {"marker": "^", "color": "#62b9e2"},
}

PROCESS_NODE_STYLE = {
    16: {"marker": "X", "color": "blue"},
    28: {"marker": "o", "color": "orange"},
    45: {"marker": "^", "color": "green"},
    65: {"marker": "s", "color": "red"},
    90: {"marker": "p", "color": "purple"},
    100: {"marker": "h", "color": "brown"},
    130: {"marker": "H", "color": "pink"},
    140: {"marker": "v", "color": "teal"},
    180: {"marker": "X", "color": "gray"},
    250: {"marker": "D", "color": "cyan"},
}


def configure_matplotlib() -> None:
    """Use a publication-style serif theme with portable fallbacks."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "axes.labelsize": 19,
            "xtick.labelsize": 15,
            "ytick.labelsize": 15,
            "legend.fontsize": 15,
            "axes.facecolor": "#f7fcff",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def load_designs(path: Path = PROCESSED_DATA) -> pd.DataFrame:
    """Load the cleaned design-level dataset and enforce numeric columns."""
    data = pd.read_csv(path)
    numeric_columns = [
        "manuscript_reference_number",
        "proof_reference_number",
        "states_stored",
        "bits_stored",
        "process_node_nm",
        "area_um2",
        "search_energy_fj_per_bit_per_search",
        "year",
        "information_density_bits_per_um2",
        "layout_factor_k",
        "layout_normalized_search_energy",
    ]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    return data


def reference_column(numbering: str) -> str:
    """Return the dataset column for manuscript or final-proof numbering."""
    columns = {
        "manuscript": "manuscript_reference_number",
        "proof": "proof_reference_number",
    }
    try:
        return columns[numbering]
    except KeyError as error:
        choices = ", ".join(columns)
        raise ValueError(f"numbering must be one of: {choices}") from error


def scatter_by_technology(
    ax,
    subset: pd.DataFrame,
    *,
    x: str,
    y: str,
    technology: str,
    storage_mode: str,
    label: str,
    size: float = 150,
) -> None:
    """Draw one technology and storage-mode group using the paper's encoding."""
    style = TECHNOLOGY_STYLE[technology]
    common = {
        "x": subset[x],
        "y": subset[y],
        "marker": style["marker"],
        "edgecolor": style["color"],
        "linewidth": 1.8,
        "s": size,
        "label": label,
        "zorder": 3,
    }
    if storage_mode == "Analog":
        ax.scatter(**common, color="black")
    else:
        ax.scatter(**common, facecolor="none")


def save_figure(fig, filename: str):
    """Save a generated figure and return its path."""
    GENERATED_FIGURES.mkdir(parents=True, exist_ok=True)
    output = GENERATED_FIGURES / filename
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {output.relative_to(ROOT)}")
    return output
