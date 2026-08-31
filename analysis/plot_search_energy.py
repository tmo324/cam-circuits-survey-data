"""Regenerate Fig. 7(b), layout-normalized search energy over time.

This is the cleaned script counterpart of
CAM Circuits Survey v3.0_ Energy Area.ipynb.
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
    28: (4, 8),
    30: (4, 8),
    31: (4, 8),
    35: (4, 8),
    36: (4, 8),
    47: (4, -12),
    50: (4, -12),
    52: (4, 8),
    53: (4, 8),
    59: (4, -10),
    61: (4, 8),
    63: (4, -12),
    64: (4, 8),
    66: (4, 8),
    67: (4, 8),
    68: (4, 8),
    71: (4, 8),
    72: (4, 8),
}


def plot_search_energy(data, numbering: str) -> None:
    label_column = reference_column(numbering)
    plotted = data.dropna(
        subset=[
            "storage_mode_for_plot",
            "year",
            "layout_normalized_search_energy",
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
                x="year",
                y="layout_normalized_search_energy",
                technology=technology,
                storage_mode=storage_mode,
                label=f"{technology}, {storage_mode}",
                size=160,
            )
            for row in subset.itertuples():
                reference = int(getattr(row, label_column))
                ax.annotate(
                    f"[{reference}]",
                    (row.year, row.layout_normalized_search_energy),
                    xytext=LABEL_OFFSETS.get(reference, (4, 4)),
                    textcoords="offset points",
                    fontsize=13,
                )

    ax.set_yscale("log")
    ax.set_xlabel("Year")
    ax.set_ylabel("Layout-Normalized Search\nEnergy (fJ/bit/search)")
    ax.legend(loc="upper left")
    ax.grid(True, which="major")
    save_figure(
        fig,
        "fig07b_layout_normalized_search_energy_vs_year.png",
    )


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
    plot_search_energy(load_designs(), args.numbering)


if __name__ == "__main__":
    main()
