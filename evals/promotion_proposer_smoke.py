#!/usr/bin/env python3
"""Smoke tests for controlled promotion proposal generation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from learning.promotion_proposer import build_proposal


BASE = {
    "id": "LEARN-TEST-PROMOTION-001",
    "source_scope": "reproduced_test",
    "provenance_class": "reproduced_test",
    "status": "ACCEPT",
    "independent_project_count": 1,
    "reproducibility": "pass",
    "validation_plan": "Run deterministic validation.",
    "privacy_review": "pass",
    "conflict_check": "pass",
    "regression_required": True,
    "regression_result": "pass",
}


proposal = build_proposal(
    BASE,
    "regression_test",
    "evals/cases/AP-LEARNING-001-unvalidated-auto-learning.md",
    "update",
    "evidence-driven-learning",
)
assert proposal["candidate_id"] == BASE["id"]
assert proposal["maintainer_review"] == "pending"
assert proposal["mutation_performed"] if "mutation_performed" in proposal else True
assert "observation" not in proposal
assert "generalized_claim" not in proposal

blocked = dict(BASE)
blocked["status"] = "CANDIDATE"
try:
    build_proposal(
        blocked,
        "documentation",
        "docs/learning.md",
        "add",
    )
except ValueError as exc:
    assert "status=ACCEPT" in str(exc)
else:
    raise AssertionError("non-ACCEPT candidate was allowed to generate a proposal")

print("promotion proposer smoke: PASS")
