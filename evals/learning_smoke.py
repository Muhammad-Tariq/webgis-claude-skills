#!/usr/bin/env python3
"""Deterministic smoke checks for evidence-driven learning validation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from learning.validator import validate_candidate


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    safe = {
        "id": "LEARN-TEST-SAFE-001",
        "domain": "testing",
        "source_scope": "reproduced_test",
        "observation": "A sanitized observation can be checked deterministically.",
        "generalized_claim": "Candidate metadata should be validated before promotion.",
        "status": "CANDIDATE",
        "created_at": "2026-09-26",
        "reproducibility": "pass",
        "privacy_review": "pass",
        "conflict_check": "pass",
        "regression_required": True,
        "provenance_class": "reproduced_test",
    }
    result = validate_candidate(safe)
    require(result["status"] == "PASS", f"safe candidate rejected: {result}")

    secret = dict(safe)
    secret["observation"] = "token: super-secret-value"
    result = validate_candidate(secret)
    require(result["status"] == "FAIL", "secret-bearing candidate was not rejected")

    unvalidated = dict(safe)
    unvalidated["status"] = "ACCEPT"
    unvalidated["privacy_review"] = "pending"
    result = validate_candidate(unvalidated)
    require(result["status"] == "FAIL", "unvalidated ACCEPT candidate was not rejected")

    single_project = dict(safe)
    single_project["source_scope"] = "single_project_observation"
    single_project["provenance_class"] = "multi_project_pattern"
    result = validate_candidate(single_project)
    require(result["status"] == "FAIL", "single-project evidence claimed stronger provenance")

    print("learning validator smoke: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
