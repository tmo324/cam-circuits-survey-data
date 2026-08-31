"""Create the design-level CSV used by the paper's data figures."""

from __future__ import annotations

import numpy as np
import pandas as pd

from common import ROOT


RAW_DATA = ROOT / "data" / "raw" / "cam_survey_main_export.csv"
OUTPUT_DATA = ROOT / "data" / "processed" / "cam_cell_designs.csv"


def numeric(series: pd.Series) -> pd.Series:
    """Convert a source column to numeric values without hiding missing data."""
    return pd.to_numeric(series, errors="coerce")


def prepare_designs(raw: pd.DataFrame) -> pd.DataFrame:
    """Select surveyed designs and compute the two normalized metrics."""
    selected = raw.loc[raw["latex numbering"].notna()].copy()

    storage_reported = selected["storage of bits"].astype("string").str.strip()
    storage_reported = storage_reported.replace("", pd.NA)

    designs = pd.DataFrame(
        {
            "source_row": selected.index + 2,
            "citation_key": selected["Unique label"].astype("string"),
            "manuscript_reference_number": numeric(selected["latex numbering"]),
            "proof_reference_number": numeric(selected["proof numbering"]),
            "paper_title": selected["paper title"].astype("string"),
            "cam_concept": selected["CAM/TCAM/ACAM/dCAM"].astype("string"),
            "cell_structure": selected["cell structure"].astype("string"),
            "technology": selected["technology type"].astype("string"),
            "process_node_nm": numeric(selected["Process Node nm"]),
            "area_um2": numeric(selected["Area (µm²)"]),
            "search_energy_fj_per_bit_per_search": numeric(
                selected["search energy"]
            ),
            "year": numeric(selected["year"]),
            "storage_mode_reported": storage_reported,
            "states_stored": numeric(selected["States storage"]),
            "nonvolatile": selected["non-volatility"].astype("string"),
        }
    )

    # Four rows have a blank storage-mode cell in the final workbook. The
    # original notebooks exclude those rows from storage-mode grouped plots.
    # Preserve that behavior for exact provenance, while making the likely
    # digital interpretation available as a separate, explicit field.
    designs["storage_mode_inferred"] = designs["storage_mode_reported"].isna()
    designs["storage_mode_for_plot"] = designs["storage_mode_reported"]
    designs["storage_mode_interpreted"] = designs["storage_mode_reported"].fillna(
        "Digital"
    )

    designs["bits_stored"] = np.log2(designs["states_stored"])
    designs["information_density_bits_per_um2"] = (
        designs["bits_stored"] / designs["area_um2"]
    )

    # Convert the process node from nm to µm before squaring it. This is the k
    # used in Fig. 7(b): k = cell area / (process node in µm)^2.
    process_node_um2 = (designs["process_node_nm"] / 1000.0) ** 2
    designs["layout_factor_k"] = designs["area_um2"] / process_node_um2
    designs["layout_normalized_search_energy"] = (
        designs["search_energy_fj_per_bit_per_search"]
        / designs["layout_factor_k"]
    )

    designs = designs.sort_values(
        ["year", "technology", "citation_key", "area_um2"],
        kind="stable",
    ).reset_index(drop=True)
    return designs


def main() -> None:
    raw = pd.read_csv(RAW_DATA)
    designs = prepare_designs(raw)
    if len(designs) != 41:
        raise RuntimeError(f"Expected 41 plotted design records, found {len(designs)}")

    OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
    designs.to_csv(OUTPUT_DATA, index=False, float_format="%.12g")
    print(f"Wrote {OUTPUT_DATA.relative_to(ROOT)} ({len(designs)} rows)")


if __name__ == "__main__":
    main()
