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

## Allowed fields

The validator uses an explicit allowlist. Unknown fields are rejected.

Allowed optional metadata:

- `occurrence_count`
- `independent_project_count`
- `reproducibility`
- `affected_skill`
- `regression_required`
- `privacy_review`
- `conflict_check`

## Allowed values

### schema_version

`1`

### consent_scope

`repository_learning`

### evidence_class

- `reproduced_test`
- `multi_project_pattern`
- `validated_engineering_rule`

A `multi_project_pattern` requires evidence from at least **2 independent projects**.

## Privacy boundary

The manifest must not contain raw or identifying material, including:

- project memory
- conversations
- source code
- datasets
- credentials
- customer or personal data
- project names, IDs, or URLs
- coordinates or latitude/longitude fields
- email or phone fields
- sensitive infrastructure details

The validator also scans nested objects for forbidden keys and scans text for secret-bearing patterns.

## Consent

`opt_in` must be exactly `true`.

`consent_timestamp` must be a valid calendar date in `YYYY-MM-DD` format.

A contribution cannot be considered valid without explicit opt-in.

## Validation boundary

The deterministic validator checks:

1. required fields
2. explicit allowlisted fields
3. consent
4. evidence class
5. repository destination
6. privacy-sensitive keys/content
7. reproducibility metadata
8. multi-project evidence requirements

## Promotion boundary

A valid manifest is an export package only. It does not grant acceptance into the repository and does not modify repository knowledge automatically.

See `contribution-protocol.md` and `contribution-checklist.md` before any explicit contribution.
