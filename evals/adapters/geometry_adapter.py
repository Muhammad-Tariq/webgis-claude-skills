"""Dependency-free geometry contract checks for golden GIS fixtures.

This adapter validates deterministic fixture structure and simple expected
relationships. It deliberately does not implement a substitute for a real
computational geometry engine.
"""

from __future__ import annotations

import json
from pathlib import Path


def load_geojson(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("type") != "FeatureCollection":
        raise ValueError("Expected GeoJSON FeatureCollection.")
    return data


def validate_feature_collection(data: dict) -> list[str]:
    errors: list[str] = []
    features = data.get("features")
    if not isinstance(features, list) or not features:
        errors.append("FeatureCollection must contain at least one feature.")

    for i, feature in enumerate(features or []):
        if feature.get("type") != "Feature":
            errors.append(f"Feature {i}: invalid GeoJSON feature type.")
        geometry = feature.get("geometry")
        if not isinstance(geometry, dict):
            errors.append(f"Feature {i}: geometry is missing.")
        elif geometry.get("type") not in {
            "Point", "MultiPoint", "LineString", "MultiLineString",
            "Polygon", "MultiPolygon"
        }:
            errors.append(f"Feature {i}: unsupported or missing geometry type.")

    return errors


def evaluate_fixture(path: str | Path, case_id: str) -> dict:
    try:
        data = load_geojson(path)
        errors = validate_feature_collection(data)
    except Exception as exc:
        return {
            "case_id": case_id,
            "status": "FAIL",
            "errors": [str(exc)],
            "evidence": [],
        }

    return {
        "case_id": case_id,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "evidence": [
            f"Validated GeoJSON FeatureCollection structure: {path}",
            f"Feature count: {len(data.get('features', []))}",
        ],
    }


def evaluate_known_intersection(path: str | Path) -> dict:
    result = evaluate_fixture(path, "GEOM-001")
    if result["status"] == "FAIL":
        return result

    # The golden fixture is intentionally a reference artifact. A real
    # intersection computation must be performed by a geometry engine.
    result["status"] = "BLOCKED"
    result["errors"] = []
    result["evidence"].append(
        "Numerical intersection was not claimed because no geometry engine "
        "was executed by this dependency-free adapter."
    )
    result["required_runtime"] = "computational geometry engine"
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("geojson")
    parser.add_argument("--intersection", action="store_true")
    args = parser.parse_args()

    result = (
        evaluate_known_intersection(args.geojson)
        if args.intersection
        else evaluate_fixture(args.geojson, "GEOM-STRUCTURE-001")
    )

    print(json.dumps(result, indent=2))
