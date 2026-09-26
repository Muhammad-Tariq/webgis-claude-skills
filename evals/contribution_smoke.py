#!/usr/bin/env python3
"""Smoke tests for the privacy-safe contribution boundary."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from learning.contribution_validator import validate


BASE = {
    "schema_version": 1,
    "manifest_id": "LEARN-CONTRIBUTION-SMOKE-001",
    "opt_in": True,
    "consent_scope": "repository_learning",
    "consent_timestamp": "2026-09-26",
    "domain": "learning",
    "evidence_class": "reproduced_test",
    "generalized_claim": "A sanitized manifest can describe reusable evidence.",
    "proposed_change": "Add a regression test for contribution validation.",
    "validation_plan": "Run the deterministic validator.",
    "privacy_review": "pass",
    "conflict_check": "pass",
}


def expect_pass(manifest):
    errors = validate(manifest)
    assert not errors, errors


def expect_fail(manifest, expected):
    errors = validate(manifest)
    assert any(expected in error for error in errors), errors


expect_pass(dict(BASE))

secret = dict(BASE)
secret["generalized_claim"] = "api_key: SUPER-SECRET"
expect_fail(secret, "secret-bearing content detected")

no_opt_in = dict(BASE)
no_opt_in["opt_in"] = False
expect_fail(no_opt_in, "opt_in must be exactly true")

raw_memory = dict(BASE)
raw_memory["raw_memory"] = "private project notes"
expect_fail(raw_memory, "forbidden raw/project fields present")

print("Contribution validator smoke suite: PASS")
