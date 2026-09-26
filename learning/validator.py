#!/usr/bin/env python3
"""Dependency-free validator for evidence-driven learning candidates.

The validator checks structure, privacy guardrails, provenance, and promotion
rules. It never promotes a candidate; ACCEPT only means the candidate satisfies
the repository's declared acceptance contract.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ALLOWED_STATUS = {"CANDIDATE", "ACCEPT", "REJECT", "ESCALATE"}
ALLOWED_SOURCE_SCOPE = {
    "single_project_observation",
    "multi_project_pattern",
    "reproduced_test",
}
ALLOWED_PROVENANCE = {
    "single_project_observation",
    "multi_project_pattern",
    "reproduced_test",
    "validated_engineering_rule",
    "maintainer_reviewed",
}
REQUIRED = {
    "id",
    "domain",
    "source_scope",
    "observation",
    "generalized_claim",
    "status",
    "created_at",
}

SENSITIVE_PATTERNS = (
    r"(?i)\b(api[_ -]?key|access[_ -]?token|token|secret|password|passwd)\b\s*[:=]",
    r"(?i)\b(private[_ -]?key|client[_ -]?secret)\b\s*[:=]",
    r"(?i)\b(connection[_ -]?string)\b\s*[:=]",
    r"(?i)-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
)


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _privacy_flags(candidate: dict[str, Any]) -> list[str]:
    serialized = json.dumps(candidate, ensure_ascii=False)
    return [
        pattern for pattern in SENSITIVE_PATTERNS
        if re.search(pattern, serialized)
    ]


def validate_candidate(candidate: dict[str, Any], path: str = "<memory>") -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    missing = sorted(REQUIRED - candidate.keys())
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    for field in ("id", "domain", "source_scope", "observation", "generalized_claim", "status", "created_at"):
        if field in candidate and not _is_nonempty_string(candidate[field]):
            errors.append(f"{field} must be a non-empty string")

    candidate_id = candidate.get("id", "")
    if isinstance(candidate_id, str) and not re.fullmatch(r"LEARN-[A-Z0-9]+(?:-[A-Z0-9]+)+", candidate_id):
        errors.append("id must match LEARN-<DOMAIN>-<NAME>")

    source_scope = candidate.get("source_scope")
    if source_scope not in ALLOWED_SOURCE_SCOPE:
        errors.append(f"source_scope must be one of: {', '.join(sorted(ALLOWED_SOURCE_SCOPE))}")

    status = candidate.get("status")
    if status not in ALLOWED_STATUS:
        errors.append(f"status must be one of: {', '.join(sorted(ALLOWED_STATUS))}")

    provenance = candidate.get("provenance_class")
    if provenance is not None and provenance not in ALLOWED_PROVENANCE:
        errors.append("invalid provenance_class")

    if source_scope == "single_project_observation" and provenance not in (None, "single_project_observation"):
        errors.append("single-project evidence cannot claim stronger provenance")

    privacy = candidate.get("privacy_review")
    if status == "ACCEPT":
        if privacy != "pass":
            errors.append("ACCEPT requires privacy_review=pass")
        if candidate.get("conflict_check") != "pass":
            errors.append("ACCEPT requires conflict_check=pass")
        if candidate.get("reproducibility") != "pass":
            errors.append("ACCEPT requires reproducibility=pass")
        if not _is_nonempty_string(candidate.get("validation_plan")):
            errors.append("ACCEPT requires validation_plan")
        if not _is_nonempty_string(candidate.get("proposed_change")):
            errors.append("ACCEPT requires proposed_change")
        if candidate.get("regression_required") is not False and candidate.get("regression_result") != "pass":
            errors.append("ACCEPT requires regression_result=pass when regression_required is not false")
        if candidate.get("independent_project_count", 0) < 1:
            errors.append("ACCEPT requires independent_project_count >= 1")

    if privacy == "pass" and status in {"CANDIDATE", "ACCEPT"}:
        pass
    elif privacy not in (None, "pending", "pass", "fail"):
        errors.append("privacy_review must be pending, pass, or fail")

    flags = _privacy_flags(candidate)
    if flags:
        errors.append("possible secret-bearing content detected")

    if candidate.get("occurrence_count") is not None:
        if not isinstance(candidate["occurrence_count"], int) or candidate["occurrence_count"] < 1:
            errors.append("occurrence_count must be a positive integer")

    if candidate.get("independent_project_count") is not None:
        if not isinstance(candidate["independent_project_count"], int) or candidate["independent_project_count"] < 0:
            errors.append("independent_project_count must be a non-negative integer")

    if status == "CANDIDATE" and candidate.get("privacy_review") == "pass":
        warnings.append("candidate is privacy-reviewed but remains non-authoritative until promotion criteria are met")

    return {
        "path": path,
        "id": candidate.get("id"),
        "status": "FAIL" if errors else "PASS",
        "candidate_status": status,
        "errors": errors,
        "warnings": warnings,
    }


def discover(root: Path) -> list[Path]:
    return sorted(root.glob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="learning/candidates")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    root = Path(args.root)
    files = discover(root) if root.exists() else []
    results = []

    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("candidate root must be a JSON object")
            results.append(validate_candidate(data, str(path)))
        except Exception as exc:
            results.append({
                "path": str(path),
                "id": None,
                "status": "FAIL",
                "candidate_status": None,
                "errors": [f"invalid JSON/candidate: {exc}"],
                "warnings": [],
            })

    failures = [item for item in results if item["status"] == "FAIL"]
    payload = {
        "status": "FAIL" if failures else "PASS",
        "candidate_files": len(files),
        "validated": len(results) - len(failures),
        "failures": len(failures),
        "results": results,
        "promotion_rule": "Only candidates with status=ACCEPT and all acceptance checks passing may influence repository artifacts.",
    }

    rendered = json.dumps(payload, indent=2)
    print(rendered)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
