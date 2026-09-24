"""Dependency-free GeoAI validation checks.

Focuses on experiment metadata and leakage invariants. It does not train a
model or claim predictive performance without an actual ML runtime.
"""

from __future__ import annotations


def validate_experiment(metadata: dict) -> list[str]:
    required = {
        "model_id",
        "model_version",
        "input_dataset",
        "input_dataset_version",
        "prediction_unit",
        "split_strategy",
    }
    errors = []
    missing = required - set(metadata)
    if missing:
        errors.append("Missing GeoAI provenance fields: " + ", ".join(sorted(missing)))

    if metadata.get("model_id") and not metadata.get("model_version"):
        errors.append("Model version must be explicit.")

    if metadata.get("input_dataset") and not metadata.get("input_dataset_version"):
        errors.append("Input dataset version must be explicit.")

    return errors


def detect_spatial_leakage(metadata: dict) -> list[str]:
    errors = []
    strategy = str(metadata.get("split_strategy", "")).lower()
    spatial = bool(metadata.get("spatial_grouping"))
    if strategy in {"random_pixel", "random", "random_pixels"} and not spatial:
        errors.append("Random pixel split without spatial grouping may leak spatial dependence.")
    return errors


def detect_temporal_leakage(metadata: dict) -> list[str]:
    errors = []
    strategy = str(metadata.get("temporal_split_strategy", "")).lower()
    if metadata.get("temporal_data") and strategy in {"random", "random_rows", "none", ""}:
        errors.append("Temporal data lacks an explicit time-aware split strategy.")
    return errors


def evaluate(metadata: dict, case_id: str = "GEOAI-001") -> dict:
    errors = validate_experiment(metadata)
    errors.extend(detect_spatial_leakage(metadata))
    errors.extend(detect_temporal_leakage(metadata))

    return {
        "case_id": case_id,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "evidence": [
            "Checked model and input version provenance.",
            "Checked spatial split metadata.",
            "Checked temporal split metadata.",
        ],
    }


if __name__ == "__main__":
    import json
    import sys

    metadata = json.loads(sys.stdin.read())
    print(json.dumps(evaluate(metadata), indent=2))
