# AP-ML-001 — Spatial ML Leakage

## Scenario
Nearby pixel samples are randomly split into training and test sets.

## Expected Detection
Spatial dependence can make random pixel splitting over-optimistic.

## Expected Pattern
Spatially separated blocks/groups or another justified spatial validation strategy.

## Remediation
C — Escalate when block size, study area, temporal structure, and deployment target are undefined.

## Validation
Split strategy explicit; leakage measured; deployment geography represented; metrics include split provenance.
