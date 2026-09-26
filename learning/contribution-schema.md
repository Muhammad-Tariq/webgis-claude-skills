# Contribution Manifest Schema

A contribution manifest is a sanitized, reviewable description of reusable learning evidence.

It is **not** raw project memory and is not itself repository knowledge.

## Required fields

- `schema_version`
- `manifest_id`
- `opt_in`
- `consent_scope`
- `consent_timestamp`
- `domain`
- `evidence_class`
- `generalized_claim`
- `proposed_change`
- `validation_plan`

## Allowed values

### schema_version
`1`

### consent_scope
`repository_learning`

### evidence_class
- `reproduced_test`
- `multi_project_pattern`
- `validated_engineering_rule`

### proposed_change
Must identify a repository destination such as a skill, contract, anti-pattern, evaluation case, fixture, decision matrix, documentation page, or regression test.

## Privacy boundary

The manifest must not contain raw:

- project memory
- conversations
- source code
- datasets
- credentials
- customer information
- sensitive coordinates
- unnecessary project identifiers

Optional evidence metadata may include:

- `occurrence_count`
- `independent_project_count`
- `reproducibility`
- `affected_skill`
- `regression_required`
- `privacy_review`
- `conflict_check`

## Consent

`opt_in` must be exactly `true`. A contribution cannot be considered valid without explicit opt-in.

## Promotion boundary

A valid manifest is an export package only. It does not grant acceptance into the repository and does not modify repository knowledge automatically.
