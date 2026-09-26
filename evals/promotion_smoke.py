#!/usr/bin/env python3
"""Deterministic smoke checks for the evidence-to-knowledge promotion gate."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from learning.promotion_validator import validate_proposal


BASE = {
    "schema_version": 1,
    "promotion_id": "PROMOTE-TEST-SMOKE-001",
    "candidate_id": "LEARN-TEST-SMOKE-001",
    "candidate_status": "ACCEPT",
    "provenance_class": "reproduced_test",
    "independent_project_count": 1,
    "reproducibility": "pass",
    "target_type": "regression_test",
    "target_path": "evals/cases/AP-LEARNING-001-unvalidated-auto-learning.md",
    "change_mode": "update",
    "affected_skill": "evidence-driven-learning",
    "validation_plan": "Run deterministic regression validation.",
    "regression_required": True,
    "regression_result": "pass",
    "privacy_review": "pass",
    "conflict_check": "pass",
    "maintainer_review": "pending",
}


def expect_ready(proposal):
    result = validate_proposal(proposal)
    assert result["status"] == "READY_FOR_REVIEW", result
    assert result["mutation_performed"] is False


def expect_blocked(proposal, text):
    result = validate_proposal(proposal)
    assert result["status"] == "BLOCKED", result
    assert any(text in error for error in result["errors"]), result


expect_ready(dict(BASE))

not_accept = dict(BASE)
not_accept["candidate_status"] = "CANDIDATE"
expect_blocked(not_accept, "candidate_status must be ACCEPT")

missing_regression = dict(BASE)
missing_regression["regression_result"] = "pending"
expect_blocked(missing_regression, "regression_result=pass")

conflict = dict(BASE)
conflict["conflict_check"] = "pending"
expect_blocked(conflict, "conflict_check must be pass")

unsafe_target = dict(BASE)
unsafe_target["target_path"] = "../skills/unsafe.md"
expect_blocked(unsafe_target, "safe path")

secret = dict(BASE)
secret["validation_plan"] = "token: SECRET"
expect_blocked(secret, "secret-bearing content detected")

update_without_owner = dict(BASE)
update_without_owner.pop("affected_skill")
expect_blocked(update_without_owner, "affected_skill")

print("promotion validator smoke: PASS")
