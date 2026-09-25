#!/usr/bin/env python3
"""Dependency-free CI smoke suite for deterministic GIS evaluation adapters."""

from __future__ import annotations

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


def main() -> int:
    checks: list[dict] = []

    crs = evaluate_mixed_crs_case()
    require(crs["status"] == "PASS", f"CRS adapter failed: {crs}")
    checks.append({"name": "CRS mixed-native/display separation", "status": "PASS"})

    geometry = evaluate_fixture(
        ROOT / "fixtures/vector/known-polygons.geojson",
        "GEOM-STRUCTURE-001",
    )
    require(geometry["status"] == "PASS", f"Geometry fixture validation failed: {geometry}")
    checks.append({"name": "GeoJSON fixture structure", "status": "PASS"})

    raster = evaluate_alignment(ROOT / "fixtures/raster/known-raster-alignment.json")
    require(raster["status"] == "PASS", f"Raster alignment failed: {raster}")
    checks.append({"name": "Raster grid alignment", "status": "PASS"})

    geoai_safe = evaluate(
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
    require(geoai_safe["status"] == "PASS", f"GeoAI safe case failed: {geoai_safe}")
    checks.append({"name": "GeoAI safe split/provenance", "status": "PASS"})

    geoai_leak = evaluate(
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
    require(geoai_leak["status"] == "FAIL", "GeoAI leakage detector did not flag random pixel split.")
    checks.append({"name": "GeoAI leakage detection", "status": "PASS"})

    scale = evaluate_delivery(250000, "geojson")
    require(any(f.rule_id == "AP-WEBGIS-001" for f in scale), "Large GeoJSON delivery was not detected.")
    checks.append({"name": "WebGIS large-payload detection", "status": "PASS"})

    api = evaluate_api_limits(None, None)
    require(len(api) >= 2, "Unbounded API limits were not detected.")
    checks.append({"name": "Spatial API workload bounds", "status": "PASS"})

    security = evaluate_security_headers(cors_wildcard=True, browser_secret=True)
    require(
        {f.rule_id for f in security} >= {"AP-SEC-003", "AP-SEC-004"},
        "Security adapter did not detect both configured hazards.",
    )
    checks.append({"name": "Browser security hazards", "status": "PASS"})

    latency = evaluate_latency(120.0, 200.0)
    require(latency.status == "PASS", f"Latency budget check failed: {latency}")
    regression = evaluate_regression(102.0, 100.0, 5.0)
    require(regression.status == "PASS", f"Performance regression check failed: {regression}")
    checks.append({"name": "Performance budgets/regression", "status": "PASS"})

    result = {
        "status": "PASS",
        "checks": checks,
        "note": "This smoke suite validates deterministic adapter behavior; it does not claim full GIS runtime execution.",
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
