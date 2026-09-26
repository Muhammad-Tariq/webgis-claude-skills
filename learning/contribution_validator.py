#!/usr/bin/env python3
"""Deterministic validator for privacy-safe learning contribution manifests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from datetime import date

REQUIRED = {
    "schema_version",
    "manifest_id",
    "opt_in",
    "consent_scope",
    "consent_timestamp",
    "domain",
    "evidence_class",
    "generalized_claim",
    "proposed_change",
    "validation_plan",
}

ALLOWED_FIELDS = {
    "schema_version", "manifest_id", "opt_in", "consent_scope",
    "consent_timestamp", "domain", "evidence_class", "generalized_claim",
    "proposed_change", "validation_plan", "occurrence_count",
    "independent_project_count", "reproducibility", "affected_skill",
    "regression_required", "privacy_review", "conflict_check",
}

FORBIDDEN_KEYS = {
    "raw_memory", "raw_conversation", "source_code", "dataset", "credentials",
    "customer_data", "personal_data", "project_name", "project_id",
    "project_url", "coordinates", "latitude", "longitude", "email", "phone",
}

EVIDENCE_CLASSES = {
    "reproduced_test",
    "multi_project_pattern",
    "validated_engineering_rule",
}

SECRET_PATTERNS = [
    r"(?i)\b(api[_ -]?key|access[_ -]?token|token|secret|password)\s*[:=]",
    r"(?i)\b(private[_ -]?key|connection[_ -]?string)\s*[:=]",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
]

SENSITIVE_CONTENT_PATTERNS = [
    r"(?i)\b(client|customer|patient|employee)[-_ ]?(id|name|email)\b",
    r"(?i)\b(lat|latitude)\s*[:=].*\b(lon|lng|longitude)\s*[:=]",
]


def scalar_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    return json.dumps(value, sort_keys=True)


def validate(manifest: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED - set(manifest))
    unknown = sorted(set(manifest) - ALLOWED_FIELDS)
    if unknown:
        errors.append("unknown/unsafe fields present: " + ", ".join(unknown))
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))

    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not re.fullmatch(r"LEARN-CONTRIBUTION-[A-Z0-9-]+", str(manifest.get("manifest_id", ""))):
        errors.append("manifest_id must match LEARN-CONTRIBUTION-<NAME>")
    if manifest.get("opt_in") is not True:
        errors.append("opt_in must be exactly true")
    if manifest.get("consent_scope") != "repository_learning":
        errors.append("consent_scope must be repository_learning")
    consent_timestamp = str(manifest.get("consent_timestamp", ""))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", consent_timestamp):
        errors.append("consent_timestamp must use YYYY-MM-DD")
    else:
        try:
            date.fromisoformat(consent_timestamp)
        except ValueError:
            errors.append("consent_timestamp is not a valid calendar date")

    if manifest.get("evidence_class") not in EVIDENCE_CLASSES:
        errors.append("unsupported evidence_class")

    for field in ("generalized_claim", "proposed_change", "validation_plan"):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            errors.append(f"{field} must be a non-empty string")

    destination_terms = (
        "skill", "contract", "anti-pattern", "evaluation case",
        "fixture", "decision matrix", "documentation", "regression test",
    )
    proposed = str(manifest.get("proposed_change", "")).lower()
    if proposed and not any(term in proposed for term in destination_terms):
        errors.append("proposed_change must identify a repository destination")

    for field in ("occurrence_count", "independent_project_count"):
        if field in manifest and (
            not isinstance(manifest[field], int) or manifest[field] < 0
        ):
            errors.append(f"{field} must be a non-negative integer")

    for field in ("privacy_review", "conflict_check"):
        if field in manifest and manifest[field] not in {"pass", "pending", "fail"}:
            errors.append(f"{field} must be pass, pending, or fail")

    if manifest.get("privacy_review") == "fail":
        errors.append("privacy_review cannot be fail")
    if manifest.get("conflict_check") == "fail":
        errors.append("conflict_check cannot be fail")

    if manifest.get("reproducibility") is not None and manifest.get("reproducibility") not in {"pass", "pending", "fail"}:
        errors.append("reproducibility must be pass, pending, or fail")

    if manifest.get("regression_required") is not None and not isinstance(
        manifest["regression_required"], bool
    ):
        errors.append("regression_required must be boolean")

    if manifest.get("evidence_class") == "multi_project_pattern" and manifest.get("independent_project_count", 0) < 2:
        errors.append("multi_project_pattern requires independent_project_count>=2")

    def scan_keys(value: object) -> set[str]:
        found: set[str] = set()
        if isinstance(value, dict):
            for key, child in value.items():
                if str(key).lower() in FORBIDDEN_KEYS:
                    found.add(str(key))
                found.update(scan_keys(child))
        elif isinstance(value, list):
            for child in value:
                found.update(scan_keys(child))
        return found

    nested_forbidden = sorted(scan_keys(manifest))
    if nested_forbidden:
        errors.append("forbidden raw/project fields present: " + ", ".join(nested_forbidden))

    text = scalar_text(manifest)
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            errors.append("secret-bearing content detected")
            break
    for pattern in SENSITIVE_CONTENT_PATTERNS:
        if re.search(pattern, text):
            errors.append("potential sensitive project data detected")
            break


    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="learning/contributions")
    parser.add_argument("--output")
    args = parser.parse_args()

    root = Path(args.root)
    manifests = sorted(root.glob("*.json")) if root.exists() else []
    results = []
    for path in manifests:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            errors = validate(data)
        except (OSError, json.JSONDecodeError) as exc:
            errors = [f"read/parse error: {exc}"]
        results.append({
            "path": str(path),
            "status": "PASS" if not errors else "FAIL",
            "errors": errors,
        })

    if not manifests:
        results.append({"path": str(root), "status": "FAIL", "errors": ["no contribution manifests found"]})

    payload = {"manifests": results, "passed": all(r["status"] == "PASS" for r in results)}
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
