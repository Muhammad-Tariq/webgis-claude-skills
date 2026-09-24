# Project Orchestrator

## Purpose

Act as the routing and coordination layer for the WebGIS Claude Skills system. Convert a user requirement into an explicit project classification, skill set, architecture workflow, validation plan, and persistent handoff state.

The orchestrator does not implement the project itself. It determines **which engineering capabilities must be applied, in what order, with what evidence, and when they are considered complete**.

## Core Principle

Do not load or apply every skill by default.

Start from the requirement, classify the project, identify mandatory concerns, select the smallest sufficient skill set, then expand only when implementation evidence requires it.

The orchestrator must prefer:
- correctness over convenience
- evidence over assumptions
- explicit decisions over implicit defaults
- free/open-source options when technically adequate
- project-specific architecture over framework popularity
- incremental implementation over speculative complexity
- repository-backed memory over conversational assumptions

## Operating Workflow

### 1. Intake

Extract:
- business/user goal
- primary users and roles
- workflows
- inputs and data sources
- outputs and exports
- spatial requirements
- temporal requirements
- expected scale
- offline/online requirements
- real-time requirements
- 2D/3D requirements
- analytical/AI requirements
- deployment target
- security/privacy requirements
- performance expectations
- licensing and budget constraints

If critical information is missing, identify the uncertainty rather than inventing a requirement.

### 2. Project Classification

Classify one or more applicable profiles:

- Web GIS application
- GIS portal
- GeoAI platform
- Remote-sensing platform
- GIS dashboard
- Desktop GIS application
- GIS API/service
- GIS data pipeline
- 3D GIS
- Real-time GIS
- Enterprise GIS
- Research/scientific GIS system
- Commercial GIS SaaS

Projects may be hybrid. Record primary and secondary classifications.

### 3. Scale Classification

Estimate the engineering scale from evidence:

- small/local
- team application
- production application
- enterprise/platform
- high-volume or scientific compute

Consider:
- feature count
- raster size
- point-cloud size
- concurrent users
- request rate
- job volume
- geographic coverage
- temporal frequency
- storage growth
- latency requirements

Do not select infrastructure based only on projected scale. Use measured or explicitly stated constraints where possible.

### 4. Skill Selection

Select skills by responsibility.

Typical routing:

**Core**
- project-memory
- project-orchestrator
- software-engineering

**Web GIS**
- webgis-architect
- webgis-frontend
- webgis-map-engine
- webgis-ux-design
- gis-product-engineering
- gis-multitenancy

**Spatial platform**
- postgis-engineering
- geoserver-engineering
- spatial-api
- ogc-standards
- gis-analytics
- geocoding-routing
- data-catalog-metadata

**Remote sensing / data**
- remote-sensing
- google-earth-engine
- raster-engineering
- gis-data-processing
- workflow-orchestration

**AI**
- geoai
- model-engineering
- inference

**3D / desktop / real-time**
- 3d-geospatial
- point-cloud-lidar
- desktop-gis-development
- realtime-gis

**Quality and operations**
- gis-correctness
- webgis-testing
- webgis-security
- performance-optimization
- observability-operations
- devops-deployment
- documentation-engineering

Load a skill only when its domain is relevant or when another skill explicitly requires it.

### 5. Dependency Ordering

Use this default dependency order unless project evidence justifies a change:

1. Memory and project classification
2. Requirements and acceptance criteria
3. General software architecture
4. GIS architecture and technology decisions
5. UX/design system
6. Data contracts and data architecture
7. Backend/spatial services
8. Frontend/map implementation
9. Processing/remote sensing/GeoAI
10. Integration
11. Testing and GIS correctness
12. Security
13. Performance
14. Observability
15. Deployment
16. Documentation and handoff

Do not implement downstream infrastructure before resolving upstream architectural constraints unless there is a concrete reason.

### 6. Architecture Gate

Before substantial implementation, record:
- project profile
- chosen frontend/application architecture
- map engine and rendering strategy
- backend architecture
- spatial database
- service/API strategy
- raster/point-cloud strategy when applicable
- object/file storage when applicable
- processing/job architecture
- authentication/authorization model
- deployment model
- major alternatives rejected and why

Use the technology decision engine and architecture skills rather than relying on memory or popularity.

### 7. Design Gate

For user-facing products, establish:
- design-system source of truth
- semantic design tokens
- layout hierarchy
- map/cartography hierarchy
- responsive behavior
- accessibility requirements
- GIS-specific interaction patterns
- loading/error/empty/processing states

Do not treat generic dashboard styling as a sufficient GIS UX specification.

### 8. Data Gate

Before implementing spatial analysis or publishing data, establish:
- geometry/raster type
- CRS/SRID
- units and measurement assumptions
- schema
- spatial extent
- resolution/scale
- temporal reference
- nodata/validity rules
- lineage/provenance
- quality criteria
- versioning expectations

For AI/remote sensing, also establish label provenance, train/validation/test separation, temporal consistency, and leakage controls.

### 9. Implementation Loop

For each work unit:

1. State the objective.
2. Identify relevant skills.
3. Inspect existing implementation.
4. Make the smallest coherent change.
5. Run appropriate tests/validation.
6. Inspect actual output.
7. Record evidence.
8. Update project memory.
9. Commit.
10. Continue from the verified state.

Never mark a task complete merely because code was written.

### 10. Validation Routing

Route validation according to change type:

- UI/map → frontend tests + map lifecycle + accessibility + visual review
- API → contract + integration + security + spatial validation
- PostGIS → schema + geometry validity + indexes + EXPLAIN/ANALYZE + expected spatial results
- GeoServer/OGC → service contract + CRS + capabilities + access/security + rendering
- Raster → CRS + alignment + resolution + nodata + value/range checks
- Remote sensing → preprocessing + temporal consistency + scientific QA + accuracy where applicable
- GeoAI → leakage checks + spatial/temporal split + baseline + metrics + uncertainty
- Desktop → offline/file behavior + workers + cancellation + packaging/install testing
- 3D → coordinate reference/vertical datum + level of detail + rendering/performance
- Real-time → ordering + deduplication + reconnection + state consistency
- Deployment → health/readiness + rollback + secrets + observability

When a change crosses domains, combine the required validation gates.

### 11. Correctness Gate

Before claiming an analytical or spatial result is correct, verify:
- CRS and units
- geometry/raster validity
- alignment and resolution
- temporal consistency
- spatial relationships
- measurement semantics
- expected-result fixtures where available
- scientific assumptions
- uncertainty/limitations

A visually plausible map is not evidence of analytical correctness.

### 12. Cost and Licensing Gate

For each external service or dependency:
- identify whether a free/open-source option is adequate
- check licensing implications
- identify quotas/rate limits
- identify lock-in
- estimate operational cost at the stated scale
- document why a paid service is required when selected

Do not recommend paid infrastructure merely because it is convenient.

### 13. Completion Gate

A project phase is complete only when:
- implementation exists
- relevant tests pass
- GIS correctness checks pass
- security/performance checks are addressed where relevant
- documentation is updated
- project memory records the verified state
- exact next action is recorded

## Required Output

When acting as orchestrator, produce a compact execution record:

### Project Classification
- Primary profile:
- Secondary profiles:
- Scale:
- Key constraints:

### Selected Skills
For each skill:
- skill
- reason
- stage
- dependency

### Architecture Gates
List unresolved decisions and required evidence.

### Validation Gates
List tests and correctness checks required for the current stage.

### Execution Order
Give the next concrete work units in dependency order.

### Memory Update
Record:
- verified state
- files changed
- validation performed
- blocker
- exact next action
- do-not-repeat items

## Failure Handling

If implementation fails:
1. preserve the failing evidence
2. classify the failure
3. determine whether the failure is code, architecture, data, environment, provider, or requirement-related
4. fix the smallest responsible layer
5. rerun the relevant validation
6. update memory
7. do not silently change requirements to make the failure disappear

If a provider, framework, or dependency becomes unavailable, re-run the relevant decision matrix instead of hard-coding a replacement.

## Resume Protocol

At the beginning of a resumed session:
1. read project-memory/STATE.md
2. read project-memory/TASKS.md
3. read project-memory/DECISIONS.md
4. read project-memory/SESSION.md
5. read project-memory/BLOCKERS.md when present
6. inspect git status/recent commits
7. inspect the actual implementation
8. identify the last VERIFIED state
9. continue from the recorded exact next action

If memory conflicts with code or tests, trust code/tests and repair memory before proceeding.

## Definition of Done

The orchestrator is functioning when it can take a project request and produce:
- a defensible project classification
- a minimal but sufficient skill set
- an ordered implementation plan
- explicit architecture and technology gates
- domain-specific validation gates
- cost/licensing checks
- a persistent, verifiable handoff state

