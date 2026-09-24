# Documentation Engineering

## Purpose

Use this skill to create and maintain accurate, production-grade documentation for Web GIS, spatial data, GeoAI, remote sensing, APIs, infrastructure, and project workflows.

Documentation is part of the engineering system, not an afterthought. It must remain synchronized with implementation, data contracts, deployment architecture, and project memory.

## 1. Mandatory Preflight

Before writing or changing documentation:

1. Read `project-memory/STATE.md`, `TASKS.md`, `DECISIONS.md`, `SESSION.md`, and `BLOCKERS.md` when present.
2. Read `project-memory/CHANGELOG.md` when relevant.
3. Inspect the actual implementation before documenting it.
4. Inspect package manifests, environment examples, API schemas, database migrations, deployment files, and configuration when relevant.
5. Verify commands before publishing them.
6. Never document an assumed feature as implemented.

When documentation conflicts with working code or tests, investigate the discrepancy and prefer verified implementation behavior.

## 2. Documentation Principles

Documentation should be:

- accurate
- actionable
- current
- scoped to its audience
- easy to navigate
- explicit about assumptions
- reproducible
- version-aware
- security-conscious
- GIS-aware

Prefer concrete examples over vague prose. Do not write documentation merely to increase volume.

## 3. Documentation Architecture

For a substantial Web GIS project, consider:

~~~text
README.md
docs/
  getting-started.md
  architecture.md
  frontend.md
  map.md
  spatial-api.md
  database.md
  geoserver.md
  data-pipelines.md
  remote-sensing.md
  google-earth-engine.md
  geoai.md
  deployment.md
  security.md
  testing.md
  troubleshooting.md
  operations.md
  data-dictionary.md
  api/
  adr/
  runbooks/
  guides/
~~~

Do not create every file automatically. Create documentation proportional to project complexity.

## 4. README Engineering

A production README should quickly answer:

1. What is this?
2. Who is it for?
3. What does it do?
4. What is the architecture?
5. What are the prerequisites?
6. How do I install it?
7. How do I configure it?
8. How do I run it?
9. How do I test it?
10. How do I deploy it?
11. Where are the important docs?
12. How can I contribute?

For Web GIS projects, also document the frontend framework, map engine, spatial database, GIS server, API, raster/object storage, processing services, supported data formats, and CRS/SRID conventions.

Keep the README useful as an entry point; move deep technical material into `docs/`.

## 5. Architecture Documentation

Architecture documentation should describe the real system.

Include, when applicable:

- system context
- frontend
- map engine
- API
- PostGIS
- GeoServer
- object storage
- processing workers
- queues
- remote-sensing pipelines
- GEE
- GeoAI services
- external providers
- authentication
- observability
- deployment topology

Use diagrams when they improve comprehension.

Clearly distinguish synchronous request paths, asynchronous jobs, data stores, external services, and authoritative sources.

## 6. ADRs — Architecture Decision Records

Use ADRs for decisions that are expensive or important to reverse.

Examples:

- React + Vite vs Next.js
- MapLibre vs OpenLayers
- PostGIS vs another spatial store
- GeoServer adoption
- vector tiles vs GeoJSON
- managed PostgreSQL vs self-hosted PostGIS
- GEE vs local processing
- raster storage strategy
- authentication architecture
- VPS vs managed cloud
- paid basemap vs self-hosted/open provider
- model selection for GeoAI

A useful ADR structure:

~~~markdown
# ADR-001: Map Rendering Engine

## Status
Accepted

## Context
...

## Decision
...

## Alternatives Considered
...

## Consequences
...

## Operational Notes
...

## Date
YYYY-MM-DD
~~~

Document why the decision was made, not only what was selected.

## 7. GIS Data Dictionary

For important spatial datasets, maintain a data dictionary covering:

- dataset name
- purpose
- source
- owner
- license
- update frequency
- geometry type
- dimensionality
- CRS
- SRID
- spatial extent
- temporal extent
- fields
- units
- valid ranges
- nodata values
- classification scheme
- lineage
- quality limitations
- sensitivity
- retention policy

Do not document fields that are not verified in the schema.

## 8. CRS and Spatial Documentation

CRS documentation is mandatory where spatial transformations matter.

Record:

- source CRS
- storage CRS
- display CRS
- analysis CRS
- output CRS
- EPSG/SRID
- axis-order assumptions
- transformation rules
- units
- geometry/geography decisions

Never silently assume WGS84 means every calculation should happen in EPSG:4326.

## 9. API Documentation

Document spatial APIs with endpoint, HTTP method, authentication, parameters, request schema, response schema, CRS, geometry rules, bbox behavior, pagination, filtering, sorting, errors, rate limits, and examples.

For spatial responses, explicitly document GeoJSON geometry type, coordinate reference assumptions, feature IDs, properties, precision, and null behavior.

Never document an endpoint without verifying its implementation or OpenAPI contract.

## 10. PostGIS Documentation

Document:

- schemas
- tables
- geometry columns
- SRIDs
- spatial indexes
- important relationships
- materialized views
- triggers
- extensions
- migrations
- retention
- backup strategy

For complex spatial queries, document the purpose and important performance assumptions.

## 11. GeoServer Documentation

Document:

- workspace structure
- stores
- layers
- layer groups
- CRS
- styles
- WMS/WFS/WMTS usage
- vector tile configuration
- GeoWebCache behavior
- access restrictions
- environment differences
- REST automation
- data-directory backup strategy

For important layers, identify source, published name, workspace, CRS, style, service exposure, and access policy.

Avoid documenting secrets or administrator credentials.

## 12. Raster, Remote Sensing, and GEE Documentation

Document scientific processing as reproducible methodology.

Include:

- sensor/dataset
- dataset version
- acquisition period
- AOI
- cloud/shadow masking
- preprocessing
- scale factors
- compositing
- indices
- classification
- thresholds
- sampling
- validation
- accuracy metrics
- exports
- resolution
- projection
- nodata
- limitations

For GEE, document dataset IDs, collection versions where applicable, filters, reducers, scale, projection, `maxPixels`, `tileScale`, export configuration, task behavior, and quota assumptions.

Do not document a scientific result without preserving enough methodology to reproduce it.

## 13. GeoAI / ML Documentation

Every production model should have a model record covering:

- model name and version
- task
- input data
- prediction unit
- target
- features
- preprocessing
- training region
- validation region
- temporal split
- spatial split
- metrics
- uncertainty
- known failure modes
- inference scale
- hardware requirements
- serving endpoint
- model artifact location
- license
- provenance

Explicitly document leakage prevention for spatial or temporal data.

Do not claim generalization beyond the evaluated geography or time period.

## 14. Deployment Documentation

Deployment documentation should be executable by another engineer.

Include:

- prerequisites
- environment variables
- DNS
- TLS
- containers
- services
- ports
- volumes
- migrations
- startup order
- health checks
- deployment commands
- smoke tests
- rollback
- backups
- restore
- monitoring

For Docker/Compose deployments, document service dependencies without embedding secrets.

## 15. Environment Variables and Secrets

Document variable names, not secret values.

~~~text
DATABASE_URL=
GEOSERVER_URL=
GEOSERVER_WORKSPACE=
STORAGE_BUCKET=
API_BASE_URL=
GEE_PROJECT=
~~~

Use safe placeholders.

Never commit API keys, passwords, private tokens, cloud credentials, database credentials, or service-account private keys.

## 16. Runbooks

Create runbooks for operational events that require repeatable response.

Examples:

- PostGIS unavailable
- GeoServer unavailable
- tiles failing
- GEE jobs stuck
- worker queue backlog
- disk nearly full
- certificate expiry
- failed migration
- failed deployment
- broken DNS
- raster ingestion failure
- model inference failure
- provider outage

A runbook should include:

1. Symptoms
2. Checks
3. Diagnosis
4. Recovery
5. Verification
6. Escalation
7. Prevention

## 17. Troubleshooting Documentation

Organize by symptom.

For a blank map, check browser console, network requests, map initialization, style URL, tile response, CRS configuration, layer visibility, CORS, authorization, and provider quota/status.

For a GeoServer failure, check workspace, datastore, layer status, CRS, source connectivity, style, service limits, and logs.

Troubleshooting should be diagnostic, not a random list of commands.

## 18. User-Facing GIS Documentation

Technical users and end users need different documentation.

User guides should explain:

- search
- layers
- legends
- filters
- drawing
- measurement
- analysis
- time controls
- feature inspection
- exports
- sharing

Use domain language appropriate to the audience.

## 19. Documentation for Analytical Results

Every important analytical output should expose enough context to prevent misinterpretation.

Include:

- what was calculated
- input data
- date/time
- spatial resolution
- method
- units
- classification
- uncertainty
- limitations
- source
- processing version

An NDVI map, for example, should communicate the index, period, resolution/context, and interpretation rather than merely saying "Vegetation Health."

## 20. Changelog Engineering

Record meaningful changes using categories such as Added, Changed, Fixed, Security, Deprecated, and Removed.

Do not generate noisy entries for trivial edits.

Keep `project-memory/CHANGELOG.md` aligned with the repository's user/developer-facing changelog when both exist.

## 21. Versioning and Compatibility

Document compatibility between:

- frontend
- API
- database schema
- GeoServer
- map styles
- data schemas
- model versions
- processing pipelines

For breaking changes, state what changed, who is affected, migration required, and rollback considerations.

## 22. Documentation from Code

When useful, derive documentation from authoritative sources:

- OpenAPI
- database migrations/schema
- TypeScript types
- JSON Schema
- GeoServer configuration
- Docker Compose
- CI workflows
- environment templates

Generated documentation must have a clear source of truth.

Avoid maintaining duplicate definitions that can drift.

## 23. Documentation Validation

Verify:

- links
- commands
- file paths
- endpoint examples
- environment variable names
- configuration names
- database/table references
- CRS/SRID values
- code examples
- deployment steps

For high-value documentation, use CI checks where practical.

Examples include Markdown lint, link checking, OpenAPI validation, example-command smoke tests, and schema/documentation consistency checks.

## 24. Screenshots and Visual Documentation

Screenshots should be current, representative, readable, properly cropped, and linked to the correct workflow.

For Web GIS screenshots, capture meaningful states:

- initial map
- layer panel
- selected feature
- analysis result
- responsive/mobile view
- error state where relevant

Do not keep outdated screenshots after major UI changes.

## 25. Documentation and Design Systems

When a project has a `DESIGN.md` or design system, document:

- visual direction
- token source
- component library
- responsive rules
- accessibility rules
- GIS-specific interaction patterns

Keep design intent and implementation synchronized.

## 26. Documentation and Project Memory

Project memory is not a replacement for product documentation.

Use:

- `project-memory/` for agent/session continuity
- `docs/` for durable engineering/product knowledge
- `README.md` for project entry point
- ADRs for durable architectural decisions
- runbooks for operations
- changelog for meaningful change history

Cross-reference rather than duplicate long sections.

## 27. Documentation Maintenance Loop

For significant implementation changes:

`Change → Verify → Update Docs → Validate Docs → Update Memory → Commit`

Examples:

- new API endpoint → API docs + README if user-visible + changelog
- new layer → layer/data documentation + GeoServer docs if applicable
- CRS change → data dictionary + API docs + ADR
- deployment change → deployment docs + runbook + changelog
- UI redesign → DESIGN.md + screenshots + user guide
- model update → model card/methodology + reproducibility notes

## 28. Documentation Review

Review from three perspectives.

### Developer
Can another developer run and extend the system?

### Operator
Can another engineer deploy, monitor, recover, and troubleshoot it?

### User
Can the intended user understand and complete the workflow?

If any perspective is missing, documentation is incomplete for a production system.

## 29. Cost-Aware Documentation

Prefer approaches that minimize maintenance:

- source-generated API docs
- reusable templates
- shared definitions
- concise runbooks
- automated validation
- canonical sources

Do not introduce a paid documentation platform unless a concrete requirement justifies it.

Prefer open formats such as Markdown where practical.

## 30. Security and Privacy

Documentation must not leak sensitive information.

Never publish:

- credentials
- private tokens
- internal secrets
- private customer geometry
- sensitive coordinates
- confidential datasets
- proprietary model artifacts

Sanitize logs and examples before committing them.

Clearly distinguish public, internal, and restricted documentation where required.

## 31. Documentation Definition of Done

Documentation work is complete when:

- implementation has been inspected
- intended audience is clear
- source of truth is identified
- instructions are actionable
- GIS assumptions are documented
- CRS/SRID behavior is explicit where relevant
- API/data contracts are accurate
- deployment/recovery steps are documented when applicable
- examples have been verified
- security-sensitive values are excluded
- links and paths are checked
- stale documentation is removed or updated
- project memory is updated

## 32. Project-Memory Handoff

Before stopping:

### STATE.md
Record documentation phase, documents changed, last verified documentation state, validation performed, and exact next action.

### TASKS.md
Record documentation tasks, missing docs, validation tasks, and cleanup work.

### DECISIONS.md
Record documentation architecture, source-of-truth decisions, ADR conventions, and generated versus hand-maintained documentation.

### SESSION.md
Record files inspected, documentation updated, validation performed, unresolved documentation drift, and exact resume point.

### BLOCKERS.md
Record missing implementation information, unverified commands, unavailable screenshots, and unresolved schema/API discrepancies.

### CHANGELOG.md
Record meaningful documentation changes.

Never mark documentation complete merely because Markdown files exist. Verify that the documented system matches the actual system.
