"""Dependency-free raster contract and grid-alignment checks.

The adapter consumes the repository's small JSON raster fixtures. Numerical
raster operations remain explicitly blocked unless a real raster engine is
available and invoked.
"""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_RASTER_KEYS = {
    "crs",
    "width",
    "height",
    "pixel_size",
    "origin",
    "nodata",
    "datatype",
}


def load_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_raster_metadata(raster: dict) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_RASTER_KEYS - set(raster)
    if missing:
        errors.append("Missing raster metadata: " + ", ".join(sorted(missing)))

    if raster.get("width", 0) <= 0 or raster.get("height", 0) <= 0:
        errors.append("Raster dimensions must be positive.")

    pixel = raster.get("pixel_size")
    if not isinstance(pixel, list) or len(pixel) != 2:
        errors.append("pixel_size must contain x and y values.")

    origin = raster.get("origin")
    if not isinstance(origin, list) or len(origin) != 2:
        errors.append("origin must contain x and y values.")

    if not raster.get("crs"):
        errors.append("Raster CRS must be explicit.")

    return errors


def evaluate_metadata(path: str | Path, case_id: str) -> dict:
    try:
        raster = load_json(path)
        errors = validate_raster_metadata(raster)
    except Exception as exc:
        return {"case_id": case_id, "status": "FAIL", "errors": [str(exc)], "evidence": []}

    return {
        "case_id": case_id,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "evidence": [
            f"Validated raster metadata: {path}",
            f"CRS: {raster.get('crs')}",
            f"Grid: {raster.get('width')}x{raster.get('height')}",
            f"Pixel size: {raster.get('pixel_size')}",
        ],
    }


def grid_alignment(a: dict, b: dict) -> bool:
    return (
        a.get("crs") == b.get("crs")
        and a.get("pixel_size") == b.get("pixel_size")
        and a.get("origin") == b.get("origin")
    )


def _alignment_inputs(fixture: dict) -> tuple[dict | None, dict | None, dict | None]:
    # Support the canonical fixture names as well as the earlier adapter names.
    a = fixture.get("raster_a")
    b = fixture.get("raster_b") or fixture.get("raster_b_aligned")
    c = fixture.get("raster_c") or fixture.get("raster_c_misaligned")
    return a, b, c


def evaluate_alignment(path: str | Path) -> dict:
    fixture = load_json(path)
    a, b, c = _alignment_inputs(fixture)

    if not all(isinstance(x, dict) for x in (a, b, c)):
        return {
            "case_id": "AP-RASTER-001",
            "status": "FAIL",
            "errors": ["Alignment fixture must contain raster_a plus aligned and misaligned comparison rasters."],
            "evidence": [],
        }

    observed = {
        "a_b_aligned": grid_alignment(a, b),
        "a_c_aligned": grid_alignment(a, c),
    }
    expected = fixture.get("expected_alignment") or fixture.get("expected", {})

    errors = []
    if expected:
        if "a_b_aligned" in expected and observed["a_b_aligned"] != expected["a_b_aligned"]:
            errors.append(f"Observed A/B alignment {observed['a_b_aligned']} != expected {expected['a_b_aligned']}")
        if "a_c_aligned" in expected and observed["a_c_aligned"] != expected["a_c_aligned"]:
            errors.append(f"Observed A/C alignment {observed['a_c_aligned']} != expected {expected['a_c_aligned']}")

    return {
        "case_id": "AP-RASTER-001",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "observed": observed,
        "expected": expected,
        "evidence": [
            "Compared CRS, pixel size, and grid origin.",
            "No resampling or raster mutation was performed.",
        ],
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("fixture")
    parser.add_argument("--alignment", action="store_true")
    args = parser.parse_args()

    result = (
        evaluate_alignment(args.fixture)
        if args.alignment
        else evaluate_metadata(args.fixture, "RASTER-METADATA-001")
    )

    print(json.dumps(result, indent=2))
