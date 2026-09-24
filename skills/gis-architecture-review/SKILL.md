# GIS Architecture Review

## Purpose

Inspect an existing GIS system and identify architectural defects, risks, unnecessary complexity, and missing boundaries using evidence from requirements and implementation.

## Review Method

1. Understand requirements and project profile.
2. Inspect repository structure and actual implementation.
3. Identify runtime/data flows.
4. Inspect architecture boundaries.
5. Compare implementation against selected technology decisions.
6. Check scale assumptions.
7. Check spatial correctness boundaries.
8. Check security, performance, observability, and deployment concerns.
9. Produce actionable findings.
10. Validate fixes.

## Review Categories

### Architecture
Check:
- separation of UI, application, domain, infrastructure
- module boundaries
- dependency direction
- coupling
- circular dependencies
- provider isolation
- configuration ownership
- synchronous versus asynchronous work

### GIS Architecture
Check:
- map engine lifecycle
- authoritative versus display data
- CRS ownership
- spatial service boundaries
- PostGIS usage
- GeoServer/OGC exposure
- raster/point-cloud delivery
- processing architecture
- analytical versus visualization data

### Scale
Check:
- feature counts
- raster sizes
- point-cloud sizes
- concurrent users
- request/job rates
- storage growth
- geographic and temporal coverage

Flag designs that transfer large datasets to the browser or perform unbounded spatial work synchronously.

### Reliability
Check:
- retries
- timeouts
- idempotency
- job recovery
- database transactions
- provider failure
- backup/recovery
- health/readiness
- graceful degradation

### Security
Check:
- authentication
- authorization
- tenant isolation
- spatial data exposure
- upload handling
- SQL/filter injection
- SSRF/path traversal
- secret handling
- resource exhaustion

### Performance
Check:
- spatial indexes
- query plans
- map rendering
- tile strategy
- caching
- API payloads
- raster windows
- worker utilization
- network transfer

## Finding Format

For each finding record:

- ID
- severity: critical/high/medium/low
- category
- evidence
- affected component
- impact
- recommended fix
- validation method
- confidence

Severity is an engineering impact classification, not a subjective quality score.

## Evidence Rules

Do not report architecture problems based only on assumptions.

Prefer:
1. executable behavior
2. code/configuration evidence
3. measured performance
4. database query plans
5. deployment/runtime evidence
6. documented requirements

If evidence is missing, state the uncertainty and request or create the appropriate validation.

## Common GIS Architecture Defects

Check explicitly for:
- giant GeoJSON responses
- client-side rendering of millions of features
- unrestricted WFS
- synchronous long-running raster analysis
- map reinitialization on ordinary state changes
- duplicated map state
- direct database access from UI
- analytical queries without spatial indexes
- public services without resource limits
- authoritative data mixed with visualization caches
- silent CRS transformations
- raster processing without grid/alignment controls
- GeoAI inference without model/version provenance
- no job recovery for long processing
- provider credentials exposed in browser code

## Output

Return:
1. architecture summary
2. project profile
3. major data/runtime flows
4. findings ordered by engineering severity
5. quick fixes
6. structural fixes
7. validation plan
8. unresolved risks
9. architecture decision updates required

## Definition of Done

The architecture review is complete when:
- actual implementation was inspected
- requirements were considered
- findings have evidence
- recommended changes are actionable
- critical/high risks have validation plans
- resulting decisions are recorded in project memory
