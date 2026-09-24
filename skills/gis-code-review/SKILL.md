# GIS Code Review

## Purpose

Review GIS application code for correctness, architecture, security, performance, maintainability, and scientific validity.

This is a code-level review. Use gis-architecture-review for system-level architecture and gis-correctness for detailed analytical validation.

## Review Procedure

1. Identify changed files and their responsibilities.
2. Trace inputs to outputs.
3. Inspect boundary validation.
4. Inspect CRS/SRID and units.
5. Inspect geometry/raster handling.
6. Inspect database queries and indexes.
7. Inspect map lifecycle and rendering.
8. Inspect asynchronous work.
9. Inspect security boundaries.
10. Inspect tests and expected-result fixtures.
11. Check performance at the stated scale.
12. Report findings with evidence.

## Frontend / Map Code

Check:
- map initialization and disposal
- stable map instance lifecycle
- layer/source ownership
- unnecessary rerenders
- duplicate state
- event listener cleanup
- WebGL/resource cleanup
- feature-count handling
- vector-tile versus GeoJSON suitability
- interaction hit testing
- accessibility
- loading/error/empty states
- worker usage for expensive computation

Flag:
- map recreation on every UI state change
- millions of features in client state
- unbounded client-side spatial filtering
- duplicate API requests
- memory leaks from listeners or sources

## API / Backend

Check:
- input validation
- authorization
- spatial query semantics
- CRS handling
- GeoJSON validity
- pagination
- bounding-box filtering
- output-size limits
- async jobs
- timeouts
- retries
- stable errors
- logging without sensitive data

Flag:
- arbitrary spatial queries without limits
- giant synchronous responses
- user-controlled SQL/filter expressions
- unbounded raster processing
- provider secrets sent to clients

## PostGIS

Check:
- SRID consistency
- geometry validity
- spatial indexes
- query plans
- ST_Transform placement
- geography versus geometry choice
- bounding-box prefilters
- joins
- aggregation
- transaction boundaries
- migrations
- connection usage

For important queries inspect EXPLAIN/ANALYZE rather than assuming an index is effective.

Flag:
- functions that prevent index use without justification
- distance/area calculations in inappropriate CRS
- unindexed spatial joins
- N+1 spatial queries
- accidental full-table scans at production scale

## GeoServer / OGC

Check:
- workspace isolation
- layer/datastore configuration
- CRS
- WMS/WFS/WMTS/OGC API behavior
- filters
- style correctness
- cache configuration
- service limits
- authentication/authorization
- output format
- large-result handling

Flag unrestricted feature services and unsafe user-controlled filters.

## Raster / Remote Sensing

Check:
- CRS
- resolution
- extent
- grid alignment
- nodata
- data type
- scale/offset
- band mapping
- QA/cloud masking
- temporal windows
- resampling method
- windowed processing
- provenance

For categorical rasters, verify that resampling preserves class semantics.

## GeoAI / ML

Check:
- data provenance
- label quality
- spatial/temporal split
- leakage
- baseline
- metrics
- uncertainty
- model version
- preprocessing parity
- inference CRS/resolution
- batch/resource limits

Flag random pixel splits where they invalidate the spatial generalization claim.

## Desktop GIS

Check:
- UI-thread blocking
- worker lifecycle
- cancellation
- filesystem safety
- project persistence
- crash recovery
- native dependency handling
- packaging
- offline behavior

## Security

Check:
- auth/authz
- tenant isolation
- spatial data access
- injection
- uploads
- path traversal
- SSRF
- secrets
- rate limits
- resource exhaustion
- unsafe deserialization
- dependency vulnerabilities

## Findings

For each finding record:
- ID
- severity: critical/high/medium/low
- file/location
- evidence
- defect
- impact
- recommended fix
- validation

Do not report style preferences as defects unless they create a measurable maintenance, correctness, security, or operational problem.

## Definition of Done

A GIS code review is complete when:
- relevant changed code was inspected
- spatial semantics were considered
- findings contain evidence
- high-impact defects have remediation and validation paths
- tests or fixtures are recommended where missing
- no known critical defect is left undocumented
