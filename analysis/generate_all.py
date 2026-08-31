"""Regenerate processed data, figures, and tables, then validate them."""

from __future__ import annotations

import generate_tables
import plot_cell_area
import plot_information_density
import plot_search_energy
import prepare_data
import sync_manual_figures
import validate_artifacts
from common import configure_matplotlib, load_designs


def main() -> None:
    prepare_data.main()
    sync_manual_figures.main()

    configure_matplotlib()
    data = load_designs()
    plot_cell_area.plot_design_counts(data)
    plot_cell_area.plot_area_vs_process_node(data, "manuscript")
    plot_cell_area.plot_area_vs_year(data)
    plot_information_density.plot_information_density(data, "manuscript")
    plot_search_energy.plot_search_energy(data, "manuscript")

    generate_tables.main()
    validate_artifacts.main()


if __name__ == "__main__":
    main()
