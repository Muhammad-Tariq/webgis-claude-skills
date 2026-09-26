#!/usr/bin/env python3
"""Smoke tests for controlled integration planning."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from learning.integration_engine import build_integration_plan
BASE={
 "schema_version":1,"promotion_id":"PROMOTE-TEST-INTEGRATION-001","candidate_id":"LEARN-TEST-INTEGRATION-001","candidate_status":"ACCEPT","provenance_class":"reproduced_test","independent_project_count":1,"reproducibility":"pass","target_type":"documentation","target_path":"docs/learning.md","change_mode":"add","validation_plan":"Run deterministic checks.","regression_required":True,"regression_result":"pass","privacy_review":"pass","conflict_check":"pass","maintainer_review":"pending"
}
ready=build_integration_plan(BASE)
assert ready['status']=='INTEGRATION_READY'
assert ready['mutation_performed'] is False
assert ready['requires_ci_after_change'] is True
bad=dict(BASE); bad['target_path']='scripts/run.py'
assert build_integration_plan(bad)['status']=='BLOCKED'
bad2=dict(BASE); bad2['change_mode']='update'; bad2['affected_skill']='evidence-driven-learning'; bad2['target_path']='skills/evidence-driven-learning/SKILL.md'
assert build_integration_plan(bad2)['status']=='INTEGRATION_READY'
print('integration engine smoke: PASS')