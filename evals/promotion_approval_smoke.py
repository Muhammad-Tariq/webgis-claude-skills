#!/usr/bin/env python3
"""Smoke tests for the automated promotion approval policy."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from learning.promotion_approval import approve_proposal
BASE={"schema_version":1,"promotion_id":"PROMOTE-TEST-AUTO-001","candidate_id":"LEARN-TEST-AUTO-001","candidate_status":"ACCEPT","provenance_class":"reproduced_test","independent_project_count":1,"reproducibility":"pass","target_type":"documentation","target_path":"docs/learning.md","change_mode":"add","validation_plan":"Run deterministic validation and regression checks.","regression_required":True,"regression_result":"pass","privacy_review":"pass","conflict_check":"pass","maintainer_review":"pending"}
approved=approve_proposal(BASE); assert approved["status"]=="AUTO_APPROVED"; assert approved["approval_mode"]=="automated_policy"; assert approved["integration_required"] is True; assert approved["mutation_performed"] is False
unsafe=dict(BASE); unsafe["conflict_check"]="pending"; assert approve_proposal(unsafe)["status"]=="BLOCKED"
destructive=dict(BASE); destructive["change_mode"]="delete"; assert approve_proposal(destructive)["status"]=="BLOCKED"
regression=dict(BASE); regression["regression_result"]="pending"; assert approve_proposal(regression)["status"]=="BLOCKED"
print("promotion approval smoke: PASS")