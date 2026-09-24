# Technology Decision Engine

## Purpose

Select technologies from project requirements, constraints, evidence, and lifecycle cost instead of popularity, habit, or arbitrary defaults.

This skill is the decision layer used by the project orchestrator and architecture skills.

## Decision Rules

For every material technology choice:

1. Define the problem and required capability.
2. Identify hard constraints.
3. Generate realistic alternatives.
4. Eliminate options that violate hard constraints.
5. Compare remaining options using explicit criteria.
6. Prefer the simplest adequate option.
7. Validate critical assumptions with a prototype, benchmark, or authoritative documentation.
8. Record the decision and rejected alternatives.
9. Define a reassessment trigger.

Do not choose a technology solely because:
- it is popular
- the developer already knows it
- it has the most features
- it is cloud-hosted
- it is open source
- it is paid
- it appears in an existing project

## Hard Constraints

Check applicable constraints first:
- required platform/browser/OS
- offline capability
- licensing
- data residency
- security/compliance
- interoperability standards
- required GIS formats
- required CRS/coordinate behavior
- dataset scale
- latency/throughput
- GPU/CPU requirements
- mobile/device constraints
- deployment environment
- budget
- team skills
- vendor/service availability

A candidate that fails a hard constraint is eliminated regardless of other advantages.

## Evaluation Criteria

For viable candidates evaluate, as relevant:
- functional fit
- GIS interoperability
- standards support
- correctness characteristics
- performance
- scalability
- reliability
- security
- maintainability
- developer productivity
- ecosystem maturity
- documentation quality
- testing support
- observability
- deployment complexity
- licensing
- operational cost
- lock-in/exit cost
- portability
- community/vendor support

Use criteria relevant to the decision rather than scoring every candidate mechanically.

## Evidence Quality

Prefer evidence in this order:
1. project requirements and acceptance tests
2. measured benchmark/prototype results
3. official documentation/specifications
4. source code/release history
5. reproducible technical tests
6. credible engineering experience
7. generic popularity or rankings

Record uncertainty when evidence is weak or context-dependent.

## Free-First Policy

Start with free/open-source options when they satisfy the requirements.

Do not equate free with automatically better.

For a paid option, document:
- the requirement it uniquely satisfies
- expected scale
- operational benefit
- estimated cost
- licensing implications
- migration/exit considerations
- free alternatives considered

For public/free providers, check usage policies, attribution, quotas, rate limits, commercial restrictions, and suitability for production before adopting them.

## Frontend Decision

Consider:
- React + Vite
- Next.js
- Vue/Nuxt
- Angular
- Svelte/SvelteKit
- other framework when requirements justify it

Evaluate rendering model, routing, SSR/SSG needs, application complexity, GIS library compatibility, team capability, deployment, and performance.

Do not assume a GIS application should use a framework's server rendering features simply because they exist.

## Map Engine Decision

Consider:
- MapLibre GL JS
- OpenLayers
- Leaflet
- Cesium for 3D
- other specialized engines where justified

Evaluate:
- vector-tile rendering
- raster/WMS support
- projection requirements
- editing/drawing
- high feature counts
- styling
- interaction model
- 3D terrain/buildings
- browser/device constraints
- plugin/ecosystem requirements

Use webgis-map-engine for the detailed implementation decision.

## Backend Decision

Consider:
- Python/FastAPI
- Node.js/TypeScript
- .NET
- Java/Spring
- Go
- other runtime when justified

Evaluate:
- spatial library support
- async/job workloads
- team capability
- throughput
- deployment
- observability
- type/system requirements
- ecosystem fit

## Database Decision

For spatial systems, consider:
- PostgreSQL + PostGIS
- GeoPackage/SQLite for local/offline workloads
- other spatial databases where a hard requirement exists

Evaluate:
- transactions
- spatial operators/indexes
- raster/vector support
- concurrency
- offline/local use
- scale
- interoperability
- operational burden

Do not introduce a second database merely because it has a specialized GIS feature unless the requirement justifies it.

## Raster Decision

Evaluate:
- local files/GDAL
- Cloud Optimized GeoTIFF
- object storage
- STAC catalogs
- PostGIS raster when appropriate
- cloud processing platforms
- specialized raster services

Consider data size, access pattern, update frequency, analysis locality, delivery format, metadata/provenance, and processing cost.

## Point-Cloud Decision

Evaluate:
- LAZ/LAS + PDAL
- COPC
- 3D Tiles
- object storage
- database-backed point clouds
- desktop/local processing

Choose based on acquisition, processing, delivery, spatial query, visualization, and scale requirements.

## Desktop Decision

Evaluate:
- Qt/PySide/PyQt
- QGIS plugin architecture
- Electron
- Tauri
- .NET desktop
- other native/cross-platform options

Consider offline behavior, native GIS library access, file handling, map canvas, local processing, packaging, update mechanism, memory usage, and OS support.

Use desktop-gis-development for detailed architecture.

## Realtime Decision

Evaluate:
- polling
- Server-Sent Events
- WebSockets
- MQTT
- message queues/streams
- event-driven backend

Use the simplest mechanism that satisfies freshness, bidirectional communication, delivery guarantees, concurrency, and infrastructure constraints.

## Storage Decision

Evaluate:
- local filesystem
- object storage
- PostgreSQL/PostGIS
- GeoPackage/SQLite
- hybrid storage

Separate authoritative storage from caches, derived artifacts, and delivery representations.

## Deployment Decision

Evaluate:
- single VPS
- containerized VPS
- managed platform
- Kubernetes
- cloud managed services
- on-premises
- hybrid

Prefer the least operationally complex platform that meets availability, security, scaling, and deployment requirements.

Do not introduce Kubernetes for a small application without a concrete operational requirement.

## Decision Record

Every material decision should record:

### Context
What requirement or constraint triggered the decision?

### Options
Which realistic alternatives were considered?

### Constraints
Which options were eliminated and why?

### Decision
Which technology or architecture was selected?

### Evidence
What documentation, benchmark, prototype, or test supports the decision?

### Tradeoffs
What is gained and what is sacrificed?

### Cost
Expected licensing and operational cost at the verified scale.

### Exit Strategy
How could the system migrate away if the technology becomes unsuitable?

### Reassessment Trigger
What change would cause the decision to be reviewed?

## Avoiding False Precision

Do not produce arbitrary numeric scores when evidence does not support them.

Prefer qualitative comparisons, explicit constraints, measured benchmarks, and documented tradeoffs.

If a scoring model is useful, define criteria and measurement method before scoring and preserve the underlying evidence.

## Decision Output

For a technology decision, return:

- requirement
- hard constraints
- candidates
- eliminated candidates and reasons
- selected option
- evidence
- tradeoffs
- cost/licensing
- implementation implications
- migration/exit considerations
- reassessment trigger

## Definition of Done

A technology decision is complete only when:
- the requirement is explicit
- hard constraints are checked
- credible alternatives were considered
- the choice is evidence-backed
- major tradeoffs are documented
- cost/licensing implications are understood
- implementation implications are clear
- reassessment conditions are recorded
