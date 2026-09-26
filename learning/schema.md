# Learning Candidate Schema

A learning candidate is **non-authoritative** evidence. It is not a skill and must not be treated as validated knowledge.

## Required fields

- id
- domain
- source_scope
- observation
- generalized_claim
- status
- created_at

## Recommended fields

- evidence_summary
- occurrence_count
- independent_project_count
- reproducibility
- affected_skill
- proposed_change
- validation_plan
- privacy_review
- conflict_check
- regression_required
- provenance_class

## Status

Allowed statuses:

- `CANDIDATE`
- `ACCEPT`
- `REJECT`
- `ESCALATE`

## Provenance classes

Use one of:

- `single_project_observation`
- `multi_project_pattern`
- `reproduced_test`
- `validated_engineering_rule`
- `maintainer_reviewed`

A candidate must not claim a stronger provenance class than the evidence supports.

## Privacy requirements

A candidate must not contain:

- secrets
- credentials
- private source code
- proprietary datasets
- raw user conversations
- personal information
- unnecessary project identifiers
- sensitive coordinates

## Promotion rule

Only `ACCEPT` candidates may influence repository artifacts.

Promotion should identify the destination artifact:

- skill
- contract
- anti-pattern
- evaluation case
- fixture
- decision matrix
- documentation
- regression test

## Example

```yaml
id: LEARN-GEOSERVER-001
domain: geoserver
source_scope: multi_project_pattern
observation: "A recurring failure appeared during large raster publication."
generalized_claim: "Large raster publication should validate tiling and range-request behavior before production."
status: CANDIDATE
created_at: 2026-09-26
evidence_summary: "Observed independently in multiple projects."
occurrence_count: 12
independent_project_count: 8
reproducibility: pending
affected_skill: geoserver-engineering
proposed_change: "Add a production raster-publication validation checklist."
validation_plan: "Create deterministic contract checks and runtime validation."
privacy_review: pass
conflict_check: pending
regression_required: true
provenance_class: multi_project_pattern
```

This example is intentionally a candidate, not a claim that the rule has already been validated.
