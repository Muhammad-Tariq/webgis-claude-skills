#!/usr/bin/env python3
"""Plan and validate controlled integration of an AUTO_APPROVED proposal.

The engine is deliberately plan-first: it never executes arbitrary code and
never edits repository files. It emits a deterministic integration plan that
the CI integration workflow can consume.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
from learning.promotion_approval import approve_proposal

ALLOWED_ROOTS = {
    "skills/": "skill",
    "contracts/": "contract",
    "evals/cases/": "evaluation_case",
    "fixtures/": "fixture",
    "decision-matrices/": "decision_matrix",
    "docs/": "documentation",
    "learning/": "documentation",
}

def target_allowed(target_type: str, target_path: str) -> bool:
    return any(target_path.startswith(prefix) and target_type == kind for prefix, kind in ALLOWED_ROOTS.items())

def build_integration_plan(proposal: dict[str, Any], path: str = '<memory>') -> dict[str, Any]:
    approval = approve_proposal(proposal, path)
    errors = list(approval['errors'])
    target_path = proposal.get('target_path', '')
    target_type = proposal.get('target_type')
    if not target_allowed(str(target_type), str(target_path)):
        errors.append('target_path is not allowed for target_type')
    if Path(str(target_path)).is_absolute() or '..' in Path(str(target_path)).parts:
        errors.append('target_path must remain repository-relative')
    status = 'INTEGRATION_READY' if not errors and approval['status'] == 'AUTO_APPROVED' else 'BLOCKED'
    return {
        'status': status,
        'promotion_id': proposal.get('promotion_id'),
        'candidate_id': proposal.get('candidate_id'),
        'target_type': target_type,
        'target_path': target_path,
        'change_mode': proposal.get('change_mode'),
        'approval_status': approval['status'],
        'mutation_performed': False,
        'requires_ci_after_change': status == 'INTEGRATION_READY',
        'errors': errors,
        'integration_policy_version': 1,
    }

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--proposal', required=True); p.add_argument('--output', required=True); a=p.parse_args()
    proposal=json.loads(Path(a.proposal).read_text(encoding='utf-8'))
    plan=build_integration_plan(proposal, a.proposal)
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(plan, indent=2))
    return 0 if plan['status']=='INTEGRATION_READY' else 1

if __name__=='__main__': raise SystemExit(main())