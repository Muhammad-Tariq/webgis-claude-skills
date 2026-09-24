# GEOM-001 — Known Intersection

## Scenario
Two deterministic polygon fixtures are expected to overlap. The evaluator must distinguish fixture/schema validity from an actual computational intersection result.

## Inputs
fixtures/vector/known-intersection.geojson

## Expected Detection
Input must be valid GeoJSON with polygon geometries and required feature structure.

## Expected Pattern
Use a computational geometry engine for the actual intersection operation; do not infer the result from file naming or metadata alone.

## Remediation
A for malformed fixture structure; otherwise execution requires a geometry engine.

## Required Validation
- GeoJSON structure valid
- geometry types valid
- actual intersection computation executed when a geometry engine is available
- expected intersection geometry/result compared against the golden expectation

## Forbidden
Claiming numerical intersection correctness from schema validation alone.
