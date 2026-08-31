"""Check that every published figure and table has a retained artifact."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
import filecmp
import re
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

from common import ROOT
from sync_manual_figures import MANUAL_EXPORTS


DRAWIO_FILES = [
    "annotated_figures_1.drawio",
    "annotated_figures_2.drawio",
    "fig01_ram_vs_cam.drawio",
    "fig02_matchline_architectures.drawio",
    "fig03_cam_architecture_peripherals.drawio",
    "fig05_analog_vs_differentiable_cam.drawio",
    "survey_paper_structure.drawio",
    "table02_03_cam_cell_designs.drawio",
    "table03_cam_cell_designs_v2.drawio",
]

FIGURE_FILES = [
    "fig01a_ram_operation.png",
    "fig01b_cam_operation.png",
    "fig02a_nor_type_cam.png",
    "fig02b_nand_type_cam.png",
    "fig03_cam_architecture_peripherals.png",
    "fig04_cell_designs_over_time.png",
    "fig05a_analog_cam_operation.png",
    "fig05b_differentiable_cam_operation.png",
    "fig06a_area_vs_process_node.png",
    "fig06b_area_vs_year.png",
    "fig07a_information_density_vs_process_node.png",
    "fig07b_layout_normalized_search_energy_vs_year.png",
    "fig08_cam_applications_timeline.png",
]

TABLE_ASSETS = [
    "table02_dram_binary.png",
    "table02_dram_ternary.png",
    "table02_sram_binary.png",
    "table02_sram_ternary.png",
    "table03_fefet_analog.png",
    "table03_fefet_ternary.png",
    "table03_mtj_ternary.png",
    "table03_reram_analog.png",
    "table03_reram_differentiable.png",
    "table03_reram_ternary.png",
]

TABLE_FILES = [
    "table01_cam_concepts.tex",
    "table02_sram_dram_cell_schematics.tex",
    "table03_nvm_cell_schematics.tex",
    "table04_cam_technology_comparison.tex",
    "table05_cam_cell_designs.tex",
    "table06_application_improvements.tex",
]


def require_files(paths) -> None:
    missing = [str(path.relative_to(ROOT)) for path in paths if not path.is_file()]
    empty = [
        str(path.relative_to(ROOT))
        for path in paths
        if path.is_file() and path.stat().st_size == 0
    ]
    if missing or empty:
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if empty:
            details.append("empty: " + ", ".join(empty))
        raise RuntimeError("; ".join(details))


def normalize_sheet_cell(value: object) -> str:
    """Normalize scalar types that Excel and CSV readers infer differently."""
    if pd.isna(value):
        return ""
    text = str(value).strip()
    try:
        return format(Decimal(text).normalize(), "f")
    except InvalidOperation:
        return text


def main() -> None:
    drawio = [ROOT / "figures" / "source" / name for name in DRAWIO_FILES]
    published = [ROOT / "figures" / "published" / name for name in FIGURE_FILES]
    generated = [ROOT / "figures" / "generated" / name for name in FIGURE_FILES]
    table_assets = [ROOT / "tables" / "assets" / name for name in TABLE_ASSETS]
    tables = [ROOT / "tables" / "generated" / name for name in TABLE_FILES]
    require_files(drawio + published + generated + table_assets + tables)

    for path in drawio:
        ET.parse(path)

    for filename in MANUAL_EXPORTS:
        published_file = ROOT / "figures" / "published" / filename
        generated_file = ROOT / "figures" / "generated" / filename
        if not filecmp.cmp(published_file, generated_file, shallow=False):
            raise RuntimeError(f"Manual export changed while syncing: {filename}")

    designs = pd.read_csv(ROOT / "data" / "processed" / "cam_cell_designs.csv")
    table_05 = pd.read_csv(
        ROOT / "data" / "processed" / "table05_cam_cell_designs.csv"
    )
    applications = pd.read_csv(
        ROOT / "data" / "processed" / "cam_applications.csv"
    )
    if len(designs) != 41:
        raise RuntimeError(f"cam_cell_designs.csv has {len(designs)} rows, expected 41")
    if len(table_05) != 37:
        raise RuntimeError(f"Table V has {len(table_05)} rows, expected 37")
    if len(applications) != 12:
        raise RuntimeError(f"Application data has {len(applications)} rows, expected 12")

    workbook = pd.read_excel(
        ROOT / "data" / "raw" / "cam_survey_master.xlsx",
        sheet_name="main",
    )
    csv_export = pd.read_csv(
        ROOT / "data" / "raw" / "cam_survey_main_export.csv"
    )
    if workbook.shape != csv_export.shape or list(workbook) != list(csv_export):
        raise RuntimeError("The raw workbook main sheet and CSV export differ in shape")
    workbook_normalized = workbook.map(normalize_sheet_cell)
    export_normalized = csv_export.map(normalize_sheet_cell)
    changed_cells = int(
        workbook_normalized.ne(export_normalized).to_numpy().sum()
    )
    if changed_cells:
        raise RuntimeError(
            f"Workbook main sheet and CSV export differ in {changed_cells} cells"
        )

    bib_text = (ROOT / "references.bib").read_text(encoding="utf-8")
    bib_keys = set(
        re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib_text, flags=re.IGNORECASE)
    )
    citation_sources = [
        "table01_cam_concepts.csv",
        "table02_cell_schematics.csv",
        "table03_nvm_cell_schematics.csv",
        "table05_cam_cell_designs.csv",
        "cam_applications.csv",
    ]
    cited_keys = set()
    for filename in citation_sources:
        citation_data = pd.read_csv(
            ROOT / "data" / "processed" / filename
        )
        cited_keys.update(citation_data["citation_key"].dropna())
    missing_bib_keys = sorted(cited_keys - bib_keys)
    if missing_bib_keys:
        raise RuntimeError(
            "Citation keys missing from references.bib: "
            + ", ".join(missing_bib_keys)
        )

    sram_2 = designs.loc[designs["citation_key"] == "SRAM_2"].iloc[0]
    expected = 0.7 / (22.4 / (0.1**2))
    actual = sram_2["layout_normalized_search_energy"]
    if not np.isclose(actual, expected):
        raise RuntimeError(
            f"Layout-normalized energy check failed: {actual} != {expected}"
        )

    print("Artifact validation passed")
    print(f"  Draw.io sources: {len(drawio)}")
    print(f"  Published figure panels/exports: {len(published)}")
    print(f"  Generated figure panels/exports: {len(generated)}")
    print(f"  Table schematic assets: {len(table_assets)}")
    print(f"  Generated LaTeX tables: {len(tables)}")
    print(f"  Design records: {len(designs)}")
    print("  Workbook main sheet matches its CSV export")
    print(f"  Referenced BibTeX keys checked: {len(cited_keys)}")


if __name__ == "__main__":
    main()
