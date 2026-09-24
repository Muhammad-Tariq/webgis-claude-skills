# AP-WEBGIS-001 — Giant GeoJSON

## Scenario
A web map downloads and renders a very large feature collection as one GeoJSON payload.

## Expected Detection
Oversized client delivery/rendering is a scalability anti-pattern.

## Expected Pattern
Use an architecture appropriate to scale: vector tiles, server-side filtering/pagination, generalized geometry, or another bounded strategy.

## Remediation
B — Context-Aware Auto-Fix.

## Validation
Request/payload bounds explicit; visual semantics preserved; resource use acceptable; no undocumented feature loss.
