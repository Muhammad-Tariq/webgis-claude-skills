#!/usr/bin/env python3
"""Generate a sanitized promotion proposal from an ACCEPT learning candidate.

The generator performs no repository mutation. It copies only validated
promotion metadata and explicit artifact intent into the proposal.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from learning.promotion_validator import validate_proposal


def build_proposal(
    candidate: dict[str, Any],
    target_type: str,
    target_path: str,
    change_mode: str,
    affected_skill: str | None = None,
) -> dict[str, Any]:
    if candidate.get("status") != "ACCEPT":
        raise ValueError("candidate must have status=ACCEPT before proposal generation")

    candidate_id = str(candidate.get("id", ""))
    if not candidate_id.startswith("LEARN-"):
        raise ValueError("candidate id is invalid")

    proposal_id = "PROMOTE-" + candidate_id.removeprefix("LEARN-")
    proposal: dict[str, Any] = {
        "schema_version": 1,
        "promotion_id": proposal_id,
        "candidate_id": candidate_id,
        "candidate_status": "ACCEPT",
        "provenance_class": candidate.get("provenance_class", candidate.get("source_scope")),
        "independent_project_count": candidate.get("independent_project_count", 0),
        "reproducibility": candidate.get("reproducibility"),
        "target_type": target_type,
        "target_path": target_path,
        "change_mode": change_mode,
        "validation_plan": candidate.get("validation_plan"),
        "regression_required": candidate.get("regression_required", True),
        "regression_result": candidate.get("regression_result", "pass"),
        "privacy_review": candidate.get("privacy_review"),
        "conflict_check": candidate.get("conflict_check"),
        "maintainer_review": "pending",
    }

    if affected_skill:
        proposal["affected_skill"] = affected_skill

    result = validate_proposal(proposal)
    if result["status"] != "READY_FOR_REVIEW":
        raise ValueError("generated proposal failed promotion validation: " + "; ".join(result["errors"]))

    return proposal


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--target-type", required=True)
    parser.add_argument("--target-path", required=True)
    parser.add_argument("--change-mode", choices=("add", "update"), default="add")
    parser.add_argument("--affected-skill")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    candidate = json.loads(Path(args.candidate).read_text(encoding="utf-8"))
    proposal = build_proposal(
        candidate,
        args.target_type,
        args.target_path,
        args.change_mode,
        args.affected_skill,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "READY_FOR_REVIEW", "promotion_id": proposal["promotion_id"], "mutation_performed": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
