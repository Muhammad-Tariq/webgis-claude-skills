from dataclasses import dataclass

@dataclass
class PerformanceResult:
    status: str
    metric: str
    observed: float
    budget: float
    message: str


def evaluate_latency(observed_ms: float, budget_ms: float) -> PerformanceResult:
    status = "PASS" if observed_ms <= budget_ms else "FAIL"
    return PerformanceResult(status, "latency_ms", observed_ms, budget_ms, "Observed latency is within the declared budget." if status == "PASS" else "Observed latency exceeds the declared budget.")


def evaluate_regression(current: float, baseline: float, allowed_degradation_pct: float = 5.0) -> PerformanceResult:
    if baseline == 0:
        return PerformanceResult("BLOCKED", "regression_pct", 0.0, allowed_degradation_pct, "Cannot compute percentage regression from a zero baseline.")
    degradation = ((current - baseline) / baseline) * 100.0
    status = "PASS" if degradation <= allowed_degradation_pct else "FAIL"
    return PerformanceResult(status, "regression_pct", degradation, allowed_degradation_pct, "Within allowed regression budget." if status == "PASS" else "Performance regression exceeds the allowed budget.")
