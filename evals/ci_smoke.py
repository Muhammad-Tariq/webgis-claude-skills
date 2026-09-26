#!/usr/bin/env python3
"""Dependency-free CI smoke suite for deterministic GIS evaluation adapters."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from evals.adapters.api_security_adapter import evaluate_security_headers, evaluate_spatial_api
from evals.adapters.crs_adapter import evaluate_mixed_crs_case
from evals.adapters.geoai_adapter import evaluate
from evals.adapters.geometry_adapter import evaluate_fixture
from evals.adapters.performance_adapter import evaluate_latency, evaluate_regression
from evals.adapters.raster_adapter import evaluate_alignment
from evals.adapters.webgis_scalability_adapter import evaluate_api_limits, evaluate_delivery


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_check(name: str) -> dict:
    if name == "crs":
        result = evaluate_mixed_crs_case()
        require(result["status"] == "PASS", f"CRS adapter failed: {result}")
        return {"name": "CRS mixed-native/display separation", "status": "PASS"}

    if name == "geometry":
        result = evaluate_fixture(
            ROOT / "fixtures/vector/known-polygons.geojson",
            "GEOM-STRUCTURE-001",
        )
        require(result["status"] == "PASS", f"Geometry fixture validation failed: {result}")
        return {"name": "GeoJSON fixture structure", "status": "PASS"}

    if name == "raster":
        result = evaluate_alignment(ROOT / "fixtures/raster/known-raster-alignment.json")
        require(result["status"] == "PASS", f"Raster alignment failed: {result}")
        return {"name": "Raster grid alignment", "status": "PASS"}

    if name == "geoai-safe":
        result = evaluate(
            {
                "model_id": "ci-model",
                "model_version": "1.0.0",
                "input_dataset": "ci-fixture",
                "input_dataset_version": "1",
                "prediction_unit": "polygon",
                "split_strategy": "spatial_holdout",
                "spatial_grouping": True,
            }
        )
        require(result["status"] == "PASS", f"GeoAI safe case failed: {result}")
        return {"name": "GeoAI safe split/provenance", "status": "PASS"}

    if name == "geoai-leakage":
        result = evaluate(
            {
                "model_id": "ci-model",
                "model_version": "1.0.0",
                "input_dataset": "ci-fixture",
                "input_dataset_version": "1",
                "prediction_unit": "pixel",
                "split_strategy": "random_pixel",
                "spatial_grouping": False,
            }
        )
        require(result["status"] == "FAIL", "GeoAI leakage detector did not flag random pixel split.")
        return {"name": "GeoAI leakage detection", "status": "PASS"}

    if name == "scalability":
        findings = evaluate_delivery(250000, "geojson")
        require(
            any(f.rule_id == "AP-WEBGIS-001" for f in findings),
            "Large GeoJSON delivery was not detected.",
        )
        return {"name": "WebGIS large-payload detection", "status": "PASS"}

    if name == "api":
        findings = evaluate_api_limits(None, None)
        require(len(findings) >= 2, "Unbounded API limits were not detected.")
        return {"name": "Spatial API workload bounds", "status": "PASS"}

    if name == "security":
        findings = evaluate_security_headers(cors_wildcard=True, browser_secret=True)
        require(
            {f.rule_id for f in findings} >= {"AP-SEC-003", "AP-SEC-004"},
            "Security adapter did not detect both configured hazards.",
        )
        return {"name": "Browser security hazards", "status": "PASS"}

    if name == "performance":
        latency = evaluate_latency(120.0, 200.0)
        require(latency.status == "PASS", f"Latency budget check failed: {latency}")
        regression = evaluate_regression(102.0, 100.0, 5.0)
        require(regression.status == "PASS", f"Performance regression check failed: {regression}")
        return {"name": "Performance budgets/regression", "status": "PASS"}

    raise ValueError(f"Unknown check: {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        choices=[
            "crs",
            "geometry",
            "raster",
            "geoai-safe",
            "geoai-leakage",
            "scalability",
            "api",
            "security",
            "performance",
            "all",
        ],
        default="all",
    )
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    names = [
        "crs",
        "geometry",
        "raster",
        "geoai-safe",
        "geoai-leakage",
        "scalability",
        "api",
        "security",
        "performance",
    ]
    selected = names if args.check == "all" else [args.check]

    checks = []
    for name in selected:
        checks.append(run_check(name))

    result = {
        "status": "PASS",
        "check_scope": args.check,
        "checks": checks,
        "note": "This smoke suite validates deterministic adapter behavior; it does not claim full GIS runtime execution.",
    }
    rendered = json.dumps(result, indent=2)
    print(rendered)

    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
