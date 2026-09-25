# Evaluation Case Schema

## Required Fields

Each evaluation case must have:

- id
- domain
- scenario
- inputs
- expected_detection
- expected_right_pattern
- remediation_class
- validation
- forbidden_behavior
- pass_criteria

## Optional Fields

- required_context
- fixtures
- related_skills
- related_contracts
- severity
- confidence_threshold
- escalation_conditions
- regression_tags

## Result Schema

Every run should emit:

- case_id
- run_id
- timestamp
- status
- detected_findings
- selected_pattern
- remediation_applied
- validation_results
- forbidden_behavior_detected
- evidence
- errors
- unresolved_context
- artifact_refs

## Status Values

PASS, FAIL, BLOCKED, ESCALATE.

A PASS requires all mandatory pass criteria and validation checks to succeed.


## Scientific Integrity Requirements

Methodology-sensitive evaluation cases should declare:

- methodology_change
- methodology_change_rationale
- evaluation_protocol_version
- generalization_target
- metric_gaming_risk
- required_escalation

A case must not PASS solely because a remediation produces a higher metric.
