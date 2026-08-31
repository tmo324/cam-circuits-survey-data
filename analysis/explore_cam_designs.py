"""Inspect the survey dataset from the command line.

This is the cleaned script counterpart of CAM Circuits Survey PLayground.ipynb.
"""

from __future__ import annotations

import argparse

import pandas as pd

from common import load_designs


def print_summary(data: pd.DataFrame) -> None:
    """Print the checks that are most useful when extending the survey."""
    year_min = int(data["year"].min())
    year_max = int(data["year"].max())
    energy_rows = int(data["search_energy_fj_per_bit_per_search"].notna().sum())

    print(f"Design records: {len(data)}")
    print(f"Unique cited papers: {data['citation_key'].nunique()}")
    print(f"Publication years: {year_min} to {year_max}")
    print(f"Records with search energy: {energy_rows}")
    print("\nRecords by technology:")
    counts = data["technology"].value_counts().reindex(
        ["SRAM", "DRAM", "ReRAM", "MTJ", "FeFET"]
    )
    print(counts.fillna(0).astype(int).to_string())
    print("\nRecords by year and technology:")
    print(pd.crosstab(data["year"].astype(int), data["technology"]).to_string())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--show-inferred",
        action="store_true",
        help="Print records whose plotting storage mode was inferred as Digital.",
    )
    args = parser.parse_args()

    data = load_designs()
    print_summary(data)
    if args.show_inferred:
        columns = [
            "citation_key",
            "cell_structure",
            "technology",
            "storage_mode_reported",
            "storage_mode_for_plot",
            "storage_mode_interpreted",
        ]
        print("\nStorage-mode inferences:")
        inferred = data.loc[data["storage_mode_inferred"], columns]
        print(inferred.to_string(index=False))


if __name__ == "__main__":
    main()
