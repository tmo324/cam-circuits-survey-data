"""Materialize hand-drawn author exports in figures/generated."""

from __future__ import annotations

import shutil

from common import GENERATED_FIGURES, ROOT


MANUAL_EXPORTS = [
    "fig01a_ram_operation.png",
    "fig01b_cam_operation.png",
    "fig02a_nor_type_cam.png",
    "fig02b_nand_type_cam.png",
    "fig03_cam_architecture_peripherals.png",
    "fig05a_analog_cam_operation.png",
    "fig05b_differentiable_cam_operation.png",
    "fig08_cam_applications_timeline.png",
]


def main() -> None:
    source_dir = ROOT / "figures" / "published"
    GENERATED_FIGURES.mkdir(parents=True, exist_ok=True)
    for filename in MANUAL_EXPORTS:
        source = source_dir / filename
        destination = GENERATED_FIGURES / filename
        shutil.copy2(source, destination)
        print(f"Wrote {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
