"""Remove only outputs that analysis/generate_all.py can recreate."""

from __future__ import annotations

from common import ROOT
from validate_artifacts import FIGURE_FILES, TABLE_FILES


def main() -> None:
    paths = [
        *(ROOT / "figures" / "generated" / name for name in FIGURE_FILES),
        *(ROOT / "tables" / "generated" / name for name in TABLE_FILES),
        ROOT / "data" / "processed" / "cam_cell_designs.csv",
    ]
    for path in paths:
        if path.is_file():
            path.unlink()
            print(f"Removed {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
