#!/usr/bin/env python3
"""Deterministic gate for evidence-to-knowledge promotion proposals.

This validator never modifies repository knowledge. READY_FOR_REVIEW means a
proposal satisfies the mechanical promotion contract and may be inspected by
a maintainer.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ALLOWED_TARGETS = {
    "skill",
    "contract",
    "anti-pattern",
    "evaluation_case",
    "fixture",
    "decision_matrix",
    "documentation",
    "regression_test",
}
ALLOWED_MODES = {"add", "update"}
ALLOWED_PROVENANCE = {
    "reproduced_test",
    "multi_project_pattern",
    "validated_engineering_rule",
    "maintainer_reviewed",
}
REQUIRED = {
    "schema_version",
    "promotion_id",
    "candidate_id",
    "candidate_status",
    "provenance_class",
    "independent_project_count",
    "reproducibility",
    "target_type",
    "target_path",
    "change_mode",
    "validation_plan",
    "regression_required",
    "privacy_review",
    "conflict_check",
}

FORBIDDEN_KEYS = {
    "raw_memory",
    "raw_conversation",
    "source_code",
    "dataset",
    "credentials",
    "customer_data",
    "personal_data",
    "project_name",
    "project_id",
    "project_url",
    "coordinates",
    "latitude",
    "longitude",
    "email",
    "phone",
}
SECRET_PATTERNS = (
    r"(?i)\b(api[_ -]?key|access[_ -]?token|token|secret|password)\s*[:=]",
    r"(?i)\b(private[_ -]?key|connection[_ -]?string)\s*[:=]",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _scan_forbidden(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_KEYS:
                found.add(str(key))
            found.update(_scan_forbidden(child))
    elif isinstance(value, list):
        for child in value:
            found.update(_scan_forbidden(child))
    return found


def validate_proposal(proposal: dict[str, Any], path: str = "<memory>") -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    missing = sorted(REQUIRED - set(proposal))
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))

    if proposal.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    if not re.fullmatch(r"PROMOTE-[A-Z0-9]+(?:-[A-Z0-9]+)+", str(proposal.get("promotion_id", ""))):
        errors.append("promotion_id must match PROMOTE-<DOMAIN>-<NAME>")

    if not re.fullmatch(r"LEARN-[A-Z0-9]+(?:-[A-Z0-9]+)+", str(proposal.get("candidate_id", ""))):
        errors.append("candidate_id must reference a learning candidate")

    if proposal.get("candidate_status") != "ACCEPT":
        errors.append("candidate_status must be ACCEPT")

    if proposal.get("provenance_class") not in ALLOWED_PROVENANCE:
        errors.append("unsupported provenance_class")

    count = proposal.get("independent_project_count")
    if not isinstance(count, int) or count < 0:
        errors.append("independent_project_count must be a non-negative integer")
    elif proposal.get("provenance_class") == "multi_project_pattern" and count < 2:
        errors.append("multi_project_pattern requires independent_project_count>=2")

    if proposal.get("reproducibility") != "pass":
        errors.append("reproducibility must be pass")

    if proposal.get("privacy_review") != "pass":
        errors.append("privacy_review must be pass")

    if proposal.get("conflict_check") == "fail":
        errors.append("conflict_check cannot be fail")
    if proposal.get("conflict_check") != "pass":
        errors.append("conflict_check must be pass before promotion review")

    target = proposal.get("target_type")
    if target not in ALLOWED_TARGETS:
        errors.append("unsupported target_type")

    target_path = proposal.get("target_path")
    if not _nonempty(target_path):
        errors.append("target_path must be a non-empty repository path")
    elif target_path.startswith("/") or ".." in Path(target_path).parts:
        errors.append("target_path must be a repository-relative safe path")

    if proposal.get("change_mode") not in ALLOWED_MODES:
        errors.append("change_mode must be add or update")

    if proposal.get("change_mode") == "update" and not _nonempty(proposal.get("affected_skill")):
        errors.append("update proposals require affected_skill")

    if not _nonempty(proposal.get("validation_plan")):
        errors.append("validation_plan must be a non-empty string")

    if not isinstance(proposal.get("regression_required"), bool):
        errors.append("regression_required must be boolean")
    elif proposal["regression_required"] and proposal.get("regression_result") != "pass":
        errors.append("regression_required=true requires regression_result=pass")

    if proposal.get("maintainer_review") not in {"pending", "approved"}:
        errors.append("maintainer_review must be pending or approved")
    if proposal.get("maintainer_review") == "approved":
        warnings.append("maintainer approval is recorded, but repository mutation remains a separate explicit change")

    forbidden = sorted(_scan_forbidden(proposal))
    if forbidden:
        errors.append("forbidden raw/project fields present: " + ", ".join(forbidden))

    serialized = json.dumps(proposal, ensure_ascii=False)
    if any(re.search(pattern, serialized) for pattern in SECRET_PATTERNS):
        errors.append("secret-bearing content detected")

    state = "READY_FOR_REVIEW" if not errors else "BLOCKED"
    return {
        "path": path,
        "promotion_id": proposal.get("promotion_id"),
        "candidate_id": proposal.get("candidate_id"),
        "status": state,
        "errors": errors,
        "warnings": warnings,
        "mutation_performed": False,
    }


def discover(root: Path) -> list[Path]:
    return sorted(root.glob("*.json"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="learning/promotion-proposals")
    parser.add_argument("--output")
    args = parser.parse_args()

    root = Path(args.root)
    files = discover(root) if root.exists() else []
    results = []

    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("proposal root must be a JSON object")
            results.append(validate_proposal(data, str(path)))
        except Exception as exc:
            results.append({
                "path": str(path),
                "promotion_id": None,
                "candidate_id": None,
                "status": "BLOCKED",
                "errors": [f"invalid JSON/proposal: {exc}"],
                "warnings": [],
                "mutation_performed": False,
            })

    if not files:
        results.append({
            "path": str(root),
            "promotion_id": None,
            "candidate_id": None,
            "status": "BLOCKED",
            "errors": ["no promotion proposals found"],
            "warnings": [],
            "mutation_performed": False,
        })

    blocked = [item for item in results if item["status"] != "READY_FOR_REVIEW"]
    payload = {
        "status": "FAIL" if blocked else "PASS",
        "proposal_files": len(files),
        "ready_for_review": len(results) - len(blocked),
        "blocked": len(blocked),
        "results": results,
        "invariant": "validator never modifies repository knowledge",
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    print(rendered, end="")
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
