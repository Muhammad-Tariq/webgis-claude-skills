# GEOAI-001 — Spatial Leakage

## Scenario
A spatial prediction experiment uses nearby pixel samples and randomly splits them into training and test sets.

## Expected Detection
Flag potential spatial dependence leakage when random pixel splitting is used without spatial grouping.

## Expected Pattern
Use spatial blocks/groups or another scientifically justified validation strategy aligned with the intended deployment geography.

## Remediation
C — Escalate when study area, spatial correlation scale, block size, temporal structure, or deployment target is undefined.

## Required Validation
- model ID/version recorded
- input dataset/version recorded
- prediction unit explicit
- split strategy explicit
- spatial grouping and overlap evaluated
- deployment geography represented
- metrics retain split provenance

## Forbidden
Silently changing the split and claiming scientific equivalence; deleting difficult samples to improve metrics; claiming model performance without an executed ML evaluation.
