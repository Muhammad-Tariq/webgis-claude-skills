#!/usr/bin/env python3
"""Deterministic automated approval gate for promotion proposals.

The approval engine is intentionally policy-driven: it approves only proposals
that already pass the promotion validator and satisfy the autonomous-learning
policy. It never writes repository knowledge or executes the proposed change.
"""

from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
from learning.promotion_validator import validate_proposal

AUTO_APPROVE_TARGETS = {"skill","anti-pattern","evaluation_case","fixture","decision_matrix","documentation","regression_test"}
REQUIRED_POLICY_FIELDS = {"candidate_status","provenance_class","reproducibility","privacy_review","conflict_check","validation_plan","regression_required"}

def approve_proposal(proposal: dict[str, Any], path: str = "<memory>") -> dict[str, Any]:
    validation = validate_proposal(proposal, path)
    errors = list(validation["errors"])
    if validation["status"] != "READY_FOR_REVIEW":
        errors.append("promotion validator did not return READY_FOR_REVIEW")
    missing = sorted(REQUIRED_POLICY_FIELDS - set(proposal))
    if missing: errors.append("missing automated approval fields: " + ", ".join(missing))
    if proposal.get("target_type") not in AUTO_APPROVE_TARGETS:
        errors.append("target_type is outside the automated approval allowlist")
    if proposal.get("change_mode") not in {"add","update"}:
        errors.append("only add/update changes are eligible for automated approval")
    if proposal.get("change_mode") == "update" and not proposal.get("affected_skill"):
        errors.append("automated updates require affected_skill")
    if proposal.get("candidate_status") != "ACCEPT": errors.append("candidate_status must be ACCEPT")
    if proposal.get("reproducibility") != "pass": errors.append("reproducibility must be pass")
    if proposal.get("privacy_review") != "pass": errors.append("privacy_review must be pass")
    if proposal.get("conflict_check") != "pass": errors.append("conflict_check must be pass")
    if not isinstance(proposal.get("validation_plan"), str) or not proposal["validation_plan"].strip(): errors.append("validation_plan must be non-empty")
    if proposal.get("regression_required") is True and proposal.get("regression_result") != "pass": errors.append("required regression coverage must pass")
    status = "AUTO_APPROVED" if not errors else "BLOCKED"
    return {"path":path,"promotion_id":proposal.get("promotion_id"),"candidate_id":proposal.get("candidate_id"),"status":status,"errors":errors,"approval_mode":"automated_policy","mutation_performed":False,"integration_required":status=="AUTO_APPROVED","policy_version":1}

def discover(root: Path) -> list[Path]: return sorted(root.glob("*.json"))

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--root",default="learning/promotion-proposals"); parser.add_argument("--output"); args=parser.parse_args()
    root=Path(args.root); files=discover(root) if root.exists() else []; results=[]
    for path in files:
        try:
            data=json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data,dict): raise ValueError("proposal root must be a JSON object")
            results.append(approve_proposal(data,str(path)))
        except Exception as exc:
            results.append({"path":str(path),"promotion_id":None,"candidate_id":None,"status":"BLOCKED","errors":[f"invalid JSON/proposal: {exc}"],"approval_mode":"automated_policy","mutation_performed":False,"integration_required":False,"policy_version":1})
    if not files: results.append({"path":str(root),"promotion_id":None,"candidate_id":None,"status":"BLOCKED","errors":["no promotion proposals found"],"approval_mode":"automated_policy","mutation_performed":False,"integration_required":False,"policy_version":1})
    blocked=[x for x in results if x["status"]!="AUTO_APPROVED"]
    payload={"status":"PASS" if not blocked else "FAIL","proposal_files":len(files),"auto_approved":len(results)-len(blocked),"blocked":len(blocked),"results":results,"invariant":"automated approval never mutates repository knowledge"}
    rendered=json.dumps(payload,indent=2)+"\n"; print(rendered,end="")
    if args.output: Path(args.output).parent.mkdir(parents=True,exist_ok=True); Path(args.output).write_text(rendered,encoding="utf-8")
    return 1 if blocked else 0

if __name__=="__main__": raise SystemExit(main())