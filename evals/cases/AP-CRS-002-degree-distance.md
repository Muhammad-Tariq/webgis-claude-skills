# AP-CRS-002 — Degree Distance

## Scenario
Code calculates distance from longitude/latitude deltas and reports meters.

## Expected Detection
Inappropriate planar distance on geographic coordinates.

## Expected Pattern
Use geodesic calculation or context-appropriate projected analysis CRS.

## Remediation
B — Context-Aware Auto-Fix.

## Validation
Units are meters; method matches AOI/accuracy; reference fixture validates result; source coordinates remain unchanged.
