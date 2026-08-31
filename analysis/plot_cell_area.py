"""Regenerate Figs. 4, 6(a), and 6(b) from the survey dataset.

This is the cleaned script counterpart of CAM Circuits Survey v2.0.ipynb.
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

from common import (
    PROCESS_NODE_STYLE,
    TECHNOLOGY_ORDER,
    configure_matplotlib,
    load_designs,
    reference_column,
    save_figure,
    scatter_by_technology,
)


AREA_LABEL_OFFSETS = {
    1: (7, 13),
    29: (4, -12),
    33: (4, 8),
    34: (7, -3),
    35: (7, 14),
    36: (4, -10),
    47: (4, 7),
    48: (7, -18),
    52: (4, 6),
    53: (7, -8),
    54: (4, 3),
    55: (7, 15),
    57: (4, 3),
    58: (7, -10),
    61: (4, 7),
    62: (7, -17),
    63: (4, -10),
    64: (4, 6),
    67: (7, -10),
    69: (7, -20),
    70: (7, 5),
    71: (7, 4),
    72: (7, -7),
}


def plot_design_counts(data) -> None:
    counts = (
        data.groupby(["year", "technology"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=TECHNOLOGY_ORDER, fill_value=0)
    )

    colors = {
        "SRAM": "#33a02c",
        "DRAM": "#2477b3",
        "FeFET": "#f67f11",
        "MTJ": "#9467bd",
        "ReRAM": "#d62628",
    }

    fig, ax = plt.subplots(figsize=(8, 3))
    bottom = np.zeros(len(counts))
    for technology in TECHNOLOGY_ORDER:
        values = counts[technology].to_numpy()
        ax.bar(
            counts.index,
            values,
            bottom=bottom,
            color=colors[technology],
            edgecolor="white",
            width=0.8,
            label=technology,
        )
        bottom += values

    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Designs")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(loc="upper center", bbox_to_anchor=(0.48, 1.32), ncol=3)
    ax.grid(False)
    save_figure(fig, "fig04_cell_designs_over_time.png")


def plot_area_vs_process_node(data, numbering: str) -> None:
    label_column = reference_column(numbering)
    plotted = data.dropna(
        subset=["storage_mode_for_plot", "process_node_nm", "area_um2"]
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    legend_order = ["SRAM", "DRAM", "ReRAM", "MTJ", "FeFET"]
    for technology in legend_order:
        for storage_mode in ["Digital", "Analog"]:
            subset = plotted.loc[
                (plotted["technology"] == technology)
                & (plotted["storage_mode_for_plot"] == storage_mode)
            ]
            if subset.empty:
                continue
            scatter_by_technology(
                ax,
                subset,
                x="process_node_nm",
                y="area_um2",
                technology=technology,
                storage_mode=storage_mode,
                label=f"{technology}, {storage_mode}",
                size=160,
            )
            for row in subset.itertuples():
                reference = int(getattr(row, label_column))
                offset = AREA_LABEL_OFFSETS.get(reference, (4, 3))
                ax.annotate(
                    f"[{reference}]",
                    (row.process_node_nm, row.area_um2),
                    xytext=offset,
                    textcoords="offset points",
                    fontsize=13,
                )

    for process_node in [28, 45, 65, 90, 130, 180, 250]:
        ax.axvline(process_node, color="gray", linestyle="--", linewidth=1)

    ax.set_yscale("log")
    ax.set_xlim(255, 5)
    ax.set_xlabel("Process Node (nm)")
    ax.set_ylabel("Area (µm²)")
    ax.legend(loc="lower left")
    ax.grid(True, which="major")
    save_figure(fig, "fig06a_area_vs_process_node.png")


def scatter_by_process_node(ax, subset, process_node: int, storage_mode: str) -> None:
    style = PROCESS_NODE_STYLE[process_node]
    label = f"{process_node} nm, {storage_mode}"
    common = {
        "x": subset["year"],
        "y": subset["area_um2"],
        "marker": style["marker"],
        "edgecolor": style["color"],
        "linewidth": 1.8,
        "s": 160,
        "label": label,
        "zorder": 3,
    }
    if storage_mode == "Analog":
        ax.scatter(**common, color="black")
    else:
        ax.scatter(**common, facecolor="none")


def plot_area_vs_year(data) -> None:
    plotted = data.dropna(subset=["storage_mode_for_plot", "year", "area_um2"])
    nodes = sorted(int(node) for node in plotted["process_node_nm"].unique())

    fig, (ax_top, ax_bottom) = plt.subplots(
        2,
        1,
        sharex=True,
        figsize=(12, 6),
        gridspec_kw={"height_ratios": [1, 2], "hspace": 0.08},
    )

    for process_node in nodes:
        for storage_mode in ["Digital", "Analog"]:
            subset = plotted.loc[
                (plotted["process_node_nm"] == process_node)
                & (plotted["storage_mode_for_plot"] == storage_mode)
            ]
            if subset.empty:
                continue
            scatter_by_process_node(ax_top, subset, process_node, storage_mode)
            scatter_by_process_node(ax_bottom, subset, process_node, storage_mode)

    ax_top.set_ylim(35, 56)
    ax_bottom.set_ylim(-2, 25)
    ax_top.spines["bottom"].set_visible(False)
    ax_bottom.spines["top"].set_visible(False)
    ax_top.tick_params(bottom=False, labelbottom=False)
    ax_bottom.tick_params(top=False)

    diagonal = 0.012
    top_style = {"transform": ax_top.transAxes, "color": "black", "clip_on": False}
    ax_top.plot((-diagonal, diagonal), (-diagonal, diagonal), **top_style)
    ax_top.plot((1 - diagonal, 1 + diagonal), (-diagonal, diagonal), **top_style)
    bottom_style = {
        "transform": ax_bottom.transAxes,
        "color": "black",
        "clip_on": False,
    }
    ax_bottom.plot((-diagonal, diagonal), (1 - diagonal, 1 + diagonal), **bottom_style)
    ax_bottom.plot(
        (1 - diagonal, 1 + diagonal),
        (1 - diagonal, 1 + diagonal),
        **bottom_style,
    )

    ax_bottom.set_xlabel("Year")
    fig.supylabel("Area (µm²)", x=0.01, fontsize=19)
    handles, labels = ax_bottom.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper right",
        bbox_to_anchor=(0.985, 0.88),
        fontsize=11,
    )
    ax_top.set_yticks([40, 50])
    ax_bottom.set_yticks([0, 10, 20])
    ax_top.grid(True, zorder=1)
    ax_bottom.grid(True, zorder=1)
    save_figure(fig, "fig06b_area_vs_year.png")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--numbering",
        choices=["manuscript", "proof"],
        default="manuscript",
        help="Reference labels for Fig. 6(a). Manuscript matches the paper image.",
    )
    args = parser.parse_args()

    configure_matplotlib()
    data = load_designs()
    plot_design_counts(data)
    plot_area_vs_process_node(data, args.numbering)
    plot_area_vs_year(data)


if __name__ == "__main__":
    main()
