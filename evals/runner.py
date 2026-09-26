#!/usr/bin/env python3
"""Deterministic, dependency-free evaluator for the repository's case contracts.

This runner validates case-file structure and produces a machine-readable
execution scaffold. It intentionally does not claim GIS remediation PASS
without an actual implementation adapter and validation evidence.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

STATUSES = {"PASS", "FAIL", "BLOCKED", "ESCALATE"}

# Case files have evolved from the original prose schema to a more explicit
# machine-oriented schema. These aliases keep both forms valid while enforcing
# the same semantic contract.
HEADING_ALIASES = {
    "scenario": {"scenario"},
    "expected_detection": {"expected detection", "expected_detection"},
    "expected_pattern": {"expected pattern", "expected_right_pattern"},
    "remediation": {"remediation", "remediation_class"},
    "validation": {"validation", "required validation"},
}


def parse_case(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    # Case IDs are not limited to AP-*; the repository also has GEOM-*,
    # RASTER-*, and GEOAI-* contract families.
    first = re.search(r"^#\s+([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\s+—\s+(.+)$", text, re.M)
    if not first:
        raise ValueError(f"{path}: missing case heading")

    sections: dict[str, str] = {}
    matches = list(re.finditer(r"^##\s+(.+)$", text, re.M))
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[match.group(1).strip().lower()] = text[start:end].strip()

    normalized: dict[str, str] = {}
    missing: list[str] = []

    for required, aliases in HEADING_ALIASES.items():
        match = next((sections[a] for a in aliases if a in sections), None)
        if match is None:
            missing.append(required)
        else:
            normalized[required] = match

    if missing:
        raise ValueError(f"{path}: missing sections: {', '.join(sorted(missing))}")

    remediation = normalized["remediation"]
    remediation_upper = remediation.upper()
    if not re.search(r"\b[A-C]\b", remediation_upper):
        raise ValueError(f"{path}: remediation class A/B/C not declared")

    return {
        "case_id": first.group(1),
        "title": first.group(2).strip(),
        "path": str(path),
        "sections": normalized,
        "raw_sections": sections,
    }


def scaffold_result(case: dict) -> dict:
    return {
        "case_id": case["case_id"],
        "status": "BLOCKED",
        "reason": "No execution adapter supplied; contract validation succeeded, but GIS behavior was not executed.",
        "detected_findings": [],
        "selected_pattern": None,
        "remediation_applied": False,
        "validation_results": [],
        "forbidden_behavior_detected": False,
        "evidence": [],
        "errors": [],
        "unresolved_context": ["execution_adapter"],
        "artifact_refs": [],
    }


def discover_cases(root: Path) -> list[Path]:
    return sorted((root / "cases").glob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="evals", help="Evaluation directory")
    parser.add_argument("--output", default="evals/results.json", help="Result file")
    args = parser.parse_args()

    root = Path(args.root)
    cases = discover_cases(root)
    results = []
    contract_failures = []

    for path in cases:
        if path.name == "README.md":
            continue
        try:
            case = parse_case(path)
            results.append(scaffold_result(case))
        except Exception as exc:
            contract_failures.append({"path": str(path), "error": str(exc)})

    if contract_failures:
        status = "FAIL"
    elif not cases:
        status = "BLOCKED"
    else:
        # Deliberately not PASS: execution has not occurred.
        status = "BLOCKED"

    payload = {
        "run_id": datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "runner": "evals/runner.py",
        "cases_discovered": len(results),
        "contract_failures": contract_failures,
        "cases": results,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 1 if status == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
