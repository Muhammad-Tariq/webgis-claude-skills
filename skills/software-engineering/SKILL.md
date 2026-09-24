# Software Engineering

## Purpose

Provide the general software-engineering foundation beneath the GIS-specific skills. Use this skill for architecture, implementation quality, maintainability, testing, dependency management, APIs, configuration, reliability, and delivery.

GIS skills define spatial domain behavior; this skill defines how the software should be engineered around that behavior.

## Engineering Principles

- Prefer the simplest architecture that satisfies verified requirements.
- Separate domain logic from UI, infrastructure, providers, and framework adapters.
- Make important behavior explicit, typed, testable, observable, and reversible.
- Avoid speculative microservices, abstractions, and infrastructure.
- Keep external providers behind replaceable interfaces where lock-in or testing risk matters.
- Treat configuration, migrations, schemas, API contracts, and infrastructure as versioned artifacts.
- Never hide errors that can change correctness.
- Prefer deterministic behavior for data processing and analytical workflows.
- Record architectural decisions when a choice has meaningful future consequences.

## Requirements and Scope

Before implementation, establish:
- functional requirements
- non-functional requirements
- users/roles
- workflows
- data inputs/outputs
- integrations
- performance targets
- availability expectations
- security/privacy requirements
- deployment constraints
- licensing and budget constraints
- acceptance criteria

Separate confirmed requirements from assumptions and open questions.

## Architecture Selection

Evaluate architecture from requirements rather than fashion.

Possible structures:
- modular monolith
- layered application
- clean/hexagonal architecture
- domain-driven modules
- monorepo with independently deployable applications
- service-oriented architecture
- microservices
- event-driven architecture
- batch/job architecture
- desktop layered architecture
- offline-first/local-first architecture

Use microservices only when independently scalable/deployable services, isolation, organizational boundaries, or operational requirements justify the additional complexity.

For GIS systems, keep clear boundaries between:
- presentation/UI
- application/use cases
- GIS domain logic
- spatial data access
- processing engines
- external GIS providers
- infrastructure

## Domain Boundaries

A GIS application should not bury spatial rules inside UI components or HTTP handlers.

Prefer boundaries such as:
- domain/ — spatial/business rules
- application/ — use cases and orchestration
- infrastructure/ — database, files, queues, providers
- api/ — transport and contracts
- ui/ — presentation
- workers/ — long-running processing
- tests/ — unit, integration, spatial, and end-to-end tests

Adapt names to the selected framework rather than enforcing a rigid folder layout.

## Technology Selection

Choose technologies using:
1. requirements
2. ecosystem maturity
3. GIS interoperability
4. team capability
5. performance
6. security
7. maintainability
8. deployment fit
9. licensing
10. total cost

Evaluate alternatives explicitly when the decision materially affects architecture.

Do not hard-code React, Next.js, Vue, Angular, Electron, Qt, or any other framework as a universal default.

## Code Quality

Require:
- consistent formatting/linting
- type checking where supported
- small cohesive modules
- explicit interfaces at architectural boundaries
- meaningful names
- controlled side effects
- validation at trust boundaries
- structured error handling
- no duplicated business rules
- dependency version discipline
- clear ownership of state

Avoid:
- giant components/classes
- hidden global state
- circular dependencies
- copy-paste implementations
- framework-specific logic leaking into domain code
- silent exception swallowing
- magic configuration
- unbounded recursion or resource use

## API Engineering

For APIs:
- define contracts before implementation where practical
- use appropriate HTTP semantics
- version breaking contracts
- validate input at the boundary
- return stable error structures
- define pagination/filtering/sorting explicitly
- distinguish synchronous requests from asynchronous jobs
- document authentication and authorization
- apply timeouts and resource limits
- test contract compatibility

For spatial APIs additionally use the spatial-api skill for CRS, geometry, bbox, GeoJSON, spatial predicates, large-result handling, and GIS-specific security.

## Database Engineering

Require:
- versioned migrations
- explicit schemas
- constraints where useful
- transaction boundaries
- indexes justified by access patterns
- query-plan inspection for important queries
- connection/resource limits
- backup/recovery strategy for production

For PostGIS, defer spatial modeling, CRS/SRID, geometry validity, spatial indexing, and spatial query correctness to postgis-engineering and gis-correctness.

## Configuration and Secrets

Separate:
- code
- environment configuration
- deployment configuration
- secrets

Never commit:
- API keys
- passwords
- private tokens
- credentials
- production certificates

Use secret managers or deployment-provided secret stores when available. Memory files must contain environment variable names or references, never secret values.

## Error Handling and Resilience

Classify failures:
- validation
- domain/business
- dependency/provider
- database
- network
- authentication/authorization
- resource exhaustion
- configuration
- deployment
- data quality

Errors should preserve actionable context without exposing secrets or sensitive data.

For external providers:
- set timeouts
- handle retries selectively
- use bounded exponential backoff where appropriate
- distinguish retryable from permanent failures
- support degraded behavior where requirements permit
- make provider failure observable

Never retry non-idempotent operations blindly.

## Background Work

Use workers/jobs for:
- large raster processing
- GeoAI inference
- imports/exports
- tiling
- ETL
- long spatial analysis
- batch processing

Jobs should have:
- stable IDs
- state transitions
- progress where meaningful
- cancellation semantics
- retries
- idempotency
- resource limits
- persisted failure state
- observable logs/metrics

Use workflow-orchestration for multi-stage pipelines.

## Testing Strategy

Use layered tests:
- unit tests
- integration tests
- API contract tests
- database tests
- spatial correctness tests
- end-to-end tests
- security tests
- performance/load tests

Test behavior at the lowest useful layer, but verify critical cross-layer behavior end-to-end.

For GIS, ordinary unit tests are insufficient for CRS, geometry, raster alignment, measurement, and analytical semantics.

## Dependency Management

For every important dependency:
- pin or constrain versions appropriately
- understand transitive dependencies
- check licensing
- track security advisories
- remove unused dependencies
- avoid duplicate libraries that solve the same concern
- document unusual native/system dependencies

When selecting a provider, consider portability and exit cost.

## Observability

Production systems should expose appropriate:
- structured logs
- metrics
- traces where useful
- health/readiness checks
- job status
- dependency health
- error correlation IDs

Use observability-operations for GIS-specific telemetry and operational design.

## Security

Apply:
- least privilege
- authentication and authorization
- input validation
- secure defaults
- dependency security
- secret management
- safe file handling
- rate/resource limits
- audit logging where required

Use webgis-security for spatial data isolation, GIS uploads, GeoServer/OGC exposure, spatial injection, and GIS-specific threat modeling.

## Performance

Measure before optimizing.

Establish:
- latency targets
- throughput targets
- dataset-size assumptions
- memory/CPU limits
- frontend render budgets
- database query budgets
- processing-job expectations

Use performance-optimization for GIS rendering, spatial queries, raster, remote sensing, API, and large-dataset optimization.

## Documentation

Maintain documentation for:
- architecture
- decisions
- setup
- configuration
- APIs
- data contracts
- deployment
- operations
- user workflows
- known limitations

Update documentation as part of the implementation loop, not as an afterthought.

## Code Review Gate

Every significant change should be reviewed for:
1. correctness
2. architecture
3. security
4. performance
5. test coverage
6. maintainability
7. observability
8. documentation
9. licensing/dependency impact

GIS changes additionally require GIS correctness review.

## Definition of Done

A software-engineering work unit is done only when:
- requirements and acceptance criteria are satisfied
- implementation is integrated into the intended architecture
- relevant tests pass
- error and security behavior is addressed
- performance is acceptable for the verified scale
- documentation/configuration is updated
- no secrets are introduced
- project memory records the verified state and exact next action
