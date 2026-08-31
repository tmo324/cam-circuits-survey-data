"""Regenerate Fig. 7(a), CAM information density by process node.

This is the cleaned script counterpart of
CAM Circuits Survey v2.0 information density.ipynb.
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from common import (
    configure_matplotlib,
    load_designs,
    reference_column,
    save_figure,
    scatter_by_technology,
)


LABEL_OFFSETS = {
    1: (7, -13),
    29: (7, -5),
    32: (7, 3),
    33: (7, 12),
    34: (7, 5),
    35: (7, -15),
    36: (7, -15),
    47: (7, -23),
    48: (7, 14),
    52: (7, 12),
    53: (7, -12),
    54: (7, 7),
    55: (7, 13),
    57: (4, 6),
    58: (7, -5),
    59: (7, -8),
    60: (7, 9),
    61: (7, 8),
    62: (7, 8),
    63: (7, 7),
    64: (7, 5),
    66: (7, -12),
    67: (7, -14),
    68: (7, 10),
    69: (7, 10),
    70: (7, 4),
    71: (7, 6),
    72: (7, -10),
}


def plot_information_density(data, numbering: str) -> None:
    label_column = reference_column(numbering)
    plotted = data.dropna(
        subset=[
            "storage_mode_for_plot",
            "process_node_nm",
            "information_density_bits_per_um2",
        ]
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    for technology in ["SRAM", "DRAM", "ReRAM", "MTJ", "FeFET"]:
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
                y="information_density_bits_per_um2",
                technology=technology,
                storage_mode=storage_mode,
                label=f"{technology}, {storage_mode}",
                size=160,
            )
            for row in subset.itertuples():
                reference = int(getattr(row, label_column))
                ax.annotate(
                    f"[{reference}]",
                    (row.process_node_nm, row.information_density_bits_per_um2),
                    xytext=LABEL_OFFSETS.get(reference, (4, 3)),
                    textcoords="offset points",
                    fontsize=13,
                )

    for process_node in [28, 45, 65, 90, 130, 180, 250]:
        ax.axvline(process_node, color="gray", linestyle="--", linewidth=1)

    ax.set_yscale("log")
    ax.set_xlim(255, 5)
    ax.set_xlabel("Process Node (nm)")
    ax.set_ylabel("Information Density\n(storage bits/µm²)")
    ax.legend(loc="upper left")
    ax.grid(True, which="major")
    save_figure(fig, "fig07a_information_density_vs_process_node.png")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--numbering",
        choices=["manuscript", "proof"],
        default="manuscript",
        help="Reference labels. Manuscript matches the paper image.",
    )
    args = parser.parse_args()

    configure_matplotlib()
    plot_information_density(load_designs(), args.numbering)


if __name__ == "__main__":
    main()
