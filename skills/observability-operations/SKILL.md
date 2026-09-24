# Web GIS Observability & Operations

## Purpose

Make production Web GIS systems observable, diagnosable, and operationally reliable across frontend, APIs, PostGIS, GeoServer, workers, raster pipelines, GeoAI services, storage, and infrastructure.

Observability is not the same as logging. The system should expose enough evidence to answer what failed, where, why, who was affected, and whether recovery succeeded.

## Mandatory Preflight

Read project memory and inspect the deployment architecture before adding telemetry.

At minimum:

- `STATE.md`
- `TASKS.md`
- `DECISIONS.md`
- `SESSION.md`
- `BLOCKERS.md` when present

## 1. Define Service Boundaries

Identify:

- frontend
- API
- authentication
- PostGIS
- GeoServer
- tile cache
- object storage
- processing workers
- GEE integration
- GeoAI inference
- external providers

Give each important boundary a health signal and ownership.

## 2. Three Pillars

### Metrics

Track meaningful signals such as:

- request count
- latency
- p50/p95/p99
- error rate
- active users/jobs
- tile latency
- database latency
- queue depth
- job duration
- cache hit rate
- CPU
- memory
- disk
- network
- GPU where applicable

### Logs

Logs should be:

- structured
- timestamped
- correlated
- useful for diagnosis
- free of secrets and unnecessary sensitive spatial data

Include:

- request/job ID
- service
- operation
- outcome
- duration
- error category

### Traces

Use traces for cross-service workflows such as:

frontend → API → PostGIS/GeoServer → worker → object storage.

Propagate correlation IDs consistently.

## 3. GIS-Specific Telemetry

Capture useful GIS dimensions:

- layer/service identifier
- dataset version
- CRS where relevant
- query type
- bbox size/category rather than sensitive raw coordinates
- feature count bucket
- tile z/x/y only when privacy/security permits
- raster dimensions bucket
- processing stage
- job type

Avoid logging sensitive coordinates or protected geometry unnecessarily.

## 4. Health Checks

Separate:

- liveness: process is running
- readiness: service can accept work
- dependency health: required database/storage/service is reachable

Do not make liveness depend on every external dependency.

For GIS services, check representative operations where useful:

- PostGIS query
- GeoServer capabilities/request
- tile cache
- object storage
- worker queue

Keep health checks lightweight.

## 5. Alerting

Alert on user-impacting or actionable conditions:

- sustained high error rate
- p95/p99 latency breach
- database connection exhaustion
- queue backlog
- repeated job failures
- disk/storage pressure
- memory exhaustion
- tile service degradation
- certificate expiration
- provider quota exhaustion

Avoid noisy alerts that have no clear response.

Every alert should have an owner and runbook.

## 6. SLOs and Error Budgets

For important services define:

- service level indicator
- target
- measurement window
- error budget
- escalation threshold

Examples:

- API availability
- p95 spatial-query latency
- tile success rate
- analysis-job completion rate

Do not invent SLOs without considering actual product requirements.

## 7. GIS Failure Diagnosis

When a map is blank, diagnose systematically:

1. browser request
2. authentication/authorization
3. API response
4. tile/WMS request
5. GeoServer status
6. database query
7. CRS/extent
8. styling
9. cache
10. data availability

For missing features, distinguish:

- no data
- filter mismatch
- CRS mismatch
- geometry validity
- authorization
- service failure
- rendering/style issue

## 8. Database Observability

Monitor:

- slow queries
- active sessions
- locks
- connection pool
- cache hit behavior
- index usage
- storage growth
- replication where used

Use query fingerprints or normalized query identifiers rather than logging sensitive full query payloads.

## 9. GeoServer Observability

Monitor:

- request volume
- WMS/WFS/WMTS latency
- errors
- JVM memory
- thread usage
- datastore connections
- tile-cache behavior

Correlate expensive requests with layer/style/query configuration.

## 10. Async Jobs

Every long-running GIS/GeoAI/raster job should expose:

- job ID
- status
- created time
- started time
- completed/failed time
- progress where meaningful
- retry count
- error category
- output reference

Make retries safe through idempotency where possible.

## 11. Incident Response

Define:

- severity
- detection
- containment
- diagnosis
- mitigation
- recovery
- verification
- post-incident review

Do not delete evidence during incident cleanup.

Document recurring failure modes and their fixes.

## 12. Deployment and Change Correlation

Every deployment should be traceable to:

- version/commit
- configuration change
- migration
- dependency update

When performance or errors change, correlate telemetry with the deployment timeline.

## 13. Privacy and Security

Do not put these into ordinary logs unless explicitly required and protected:

- access tokens
- passwords
- API keys
- private geometries
- exact sensitive coordinates
- personal data
- private dataset contents

Use redaction and retention policies.

Telemetry itself is production data and needs access control.

## 14. Cost-Aware Observability

Avoid collecting high-cardinality or high-volume telemetry without purpose.

Control:

- log retention
- trace sampling
- metric cardinality
- payload capture
- dashboard count
- storage

Prefer open standards and self-hosted/open-source observability where appropriate, but choose managed services when operational requirements justify them.

## 15. Testing

Test:

- health endpoints
- alert conditions
- trace propagation
- structured logs
- failure recovery
- queue/job failures
- database outages
- GeoServer outages
- storage failures
- provider failures

Include observability checks in deployment validation.

## Definition of Done

- service boundaries are documented
- meaningful metrics exist
- structured logs exist
- cross-service correlation works
- health/readiness checks exist
- important alerts have runbooks
- GIS-specific failure diagnosis is documented
- secrets/sensitive spatial data are protected
- telemetry cost is controlled
- incident/recovery procedures are tested
- project memory is updated

## Project-Memory Handoff

Record:

- observability architecture
- important metrics/SLOs
- alert/runbook decisions
- known failure modes
- deployment correlation method
- monitoring gaps
- exact next action

Update `STATE.md`, `TASKS.md`, `DECISIONS.md`, `SESSION.md`, `BLOCKERS.md`, and `CHANGELOG.md` as appropriate.
