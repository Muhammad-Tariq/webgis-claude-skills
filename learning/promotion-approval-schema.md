# Automated Promotion Approval Policy

The repository uses a deterministic automated approval gate so learning does not depend on a human being online.

## Approval states
- `AUTO_APPROVED` — every mechanical policy gate passed.
- `BLOCKED` — at least one safety, evidence, conflict, or validation gate failed.

## Auto-approval requirements
1. pass `promotion_validator.py`
2. reference an `ACCEPT` candidate
3. have valid provenance
4. pass privacy review
5. pass conflict checks
6. pass reproducibility checks
7. contain an explicit validation plan
8. pass required regression coverage
9. target an allowlisted artifact
10. use a non-destructive `add` or `update` mode
11. identify the affected skill for updates
12. contain no raw project data or secrets

## Separation of approval and mutation
`AUTO_APPROVED` authorizes the proposal for the next controlled integration step. It does not execute arbitrary code or directly mutate repository knowledge. The integration layer must apply only the approved, validated artifact change and then run repository CI.

## Core invariant
> No human needs to be online for safe, validated learning to be approved; no approval path may bypass deterministic validation or silently mutate knowledge.