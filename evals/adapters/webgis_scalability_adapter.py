from dataclasses import dataclass
from typing import List

@dataclass
class ScalabilityFinding:
    rule_id: str
    severity: str
    message: str
    remediation: str


def evaluate_delivery(feature_count: int, delivery: str, paginated: bool = False, vector_tiles: bool = False) -> List[ScalabilityFinding]:
    findings=[]
    if feature_count > 100000 and delivery.lower() == "geojson" and not (paginated or vector_tiles):
        findings.append(ScalabilityFinding("AP-WEBGIS-001", "HIGH", "Large feature collections are delivered as one unbounded GeoJSON payload.", "Use bounded server-side filtering, pagination, vector tiles, or an equivalent scale-appropriate delivery strategy."))
    if feature_count > 1000000 and delivery.lower() == "browser-memory":
        findings.append(ScalabilityFinding("AP-WEBGIS-002", "CRITICAL", "Client-side loading of million-scale features risks browser/resource exhaustion.", "Move filtering/generalization/tiling to the server and bound the delivered dataset."))
    return findings


def evaluate_api_limits(max_features, max_bbox_area) -> List[ScalabilityFinding]:
    findings=[]
    if max_features is None:
        findings.append(ScalabilityFinding("AP-API-001", "HIGH", "Spatial API has no explicit feature/resource limit.", "Add bounded pagination/limits and enforce server-side resource constraints."))
    if max_bbox_area is None:
        findings.append(ScalabilityFinding("AP-API-002", "MEDIUM", "Spatial API has no explicit geographic workload bound.", "Define an AOI/bbox or workload constraint appropriate to the operation."))
    return findings


def evaluate_performance_budget(measured_ms: float, budget_ms: float) -> List[ScalabilityFinding]:
    if measured_ms > budget_ms:
        return [ScalabilityFinding("AP-PERF-001", "MEDIUM", "Measured latency exceeds the declared performance budget.", "Profile the actual bottleneck, optimize the measured path, and rerun the regression test.")]
    return []
