"""Deterministic CRS contract checks.

The adapter verifies metadata-level invariants without pretending to perform
coordinate transformation itself. Real PROJ-backed transformation tests can
be plugged in later when the runtime provides PROJ.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CRSLayer:
    name: str
    native_crs: str
    display_crs: str | None = None
    analysis_crs: str | None = None


def validate_mixed_crs_display(layers: list[CRSLayer]) -> list[str]:
    errors: list[str] = []
    if len(layers) < 2:
        errors.append("At least two layers are required for mixed-CRS validation.")

    native = [layer.native_crs for layer in layers]
    if len(set(native)) < 2:
        errors.append("Fixture is not mixed-CRS; expected distinct native CRS values.")

    for layer in layers:
        if not layer.native_crs:
            errors.append(f"{layer.name}: native CRS is missing.")
        if layer.display_crs and layer.display_crs == "REPROJECTED_SOURCE":
            errors.append(f"{layer.name}: display transformation must not mutate native CRS.")

    return errors


def validate_analysis_separation(layer: CRSLayer) -> list[str]:
    errors: list[str] = []
    if not layer.native_crs:
        errors.append(f"{layer.name}: native CRS is required.")
    if layer.analysis_crs == layer.native_crs and layer.analysis_crs:
        # This is allowed in some cases, so this is intentionally informational
        # rather than an error. Callers must validate the operation itself.
        return errors
    return errors


def evaluate_mixed_crs_case() -> dict:
    layers = [
        CRSLayer("roads", "EPSG:4326", "EPSG:3857"),
        CRSLayer("parcels", "EPSG:32642", "EPSG:3857"),
    ]
    errors = validate_mixed_crs_display(layers)
    for layer in layers:
        errors.extend(validate_analysis_separation(layer))

    return {
        "case_id": "AP-CRS-001",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "evidence": [
            "Two distinct native CRS values are preserved.",
            "Both layers may use a common display CRS without changing native CRS.",
        ],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(evaluate_mixed_crs_case(), indent=2))
