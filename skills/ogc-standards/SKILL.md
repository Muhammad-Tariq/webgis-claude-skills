# OGC Standards & Interoperability

## Purpose

Design and implement interoperable Web GIS services using OGC standards and modern OGC APIs.

Use this skill when a system publishes, consumes, validates, secures, or migrates geospatial services across different clients, servers, vendors, or organizations.

Prioritize standards only when interoperability provides real value. Do not introduce protocol complexity merely because a standard exists.

## Mandatory Preflight

Read:

1. `project-memory/STATE.md`
2. `project-memory/TASKS.md`
3. `project-memory/DECISIONS.md`
4. `project-memory/SESSION.md`
5. `project-memory/BLOCKERS.md` when present

Then inspect existing API, GeoServer, PostGIS, map-engine, frontend, and deployment decisions.

If existing implementation and memory conflict, trust verified code/tests and repair memory.

## 1. Choose the Right Standard

Evaluate the actual requirement before selecting a protocol.

Common choices:

- OGC API - Features for feature access
- OGC API - Tiles for tiled data
- OGC API - Maps for map delivery
- OGC API - Processes for asynchronous geospatial processing
- WMS for rendered map images
- WMTS for cached map tiles
- WFS for legacy/established feature-service interoperability
- WCS for coverage access
- WPS for legacy processing interoperability
- GeoJSON for lightweight feature exchange
- GML only when required by interoperability constraints
- KML when required by target software/workflows
- OGC API - Records for catalog/discovery use cases

Do not replace a working standard with a newer API solely for novelty. Document compatibility requirements.

## 2. Service Contracts

For every service define:

- endpoint/version
- advertised capabilities
- CRS support
- geometry semantics
- pagination
- filtering
- bounding-box behavior
- temporal filtering
- error format
- content types
- authentication
- authorization
- limits
- caching
- coordinate-axis behavior
- metadata/provenance

Keep contracts explicit and testable.

## 3. CRS and Axis Order

OGC interoperability frequently fails because CRS semantics are implicit.

Document:

- source CRS
- storage CRS
- service CRS
- requested CRS
- display CRS
- axis order
- units
- transformation behavior

Test representative coordinates in every supported CRS.

Never assume EPSG:4326 axis behavior is identical across every protocol/library.

## 4. WMS/WMTS/WFS

For legacy OGC services:

### WMS

Validate:

- layers
- styles
- CRS/SRS handling
- BBOX
- WIDTH/HEIGHT
- format
- transparency
- exceptions
- GetCapabilities
- GetMap
- GetFeatureInfo where used

### WMTS

Validate:

- tile matrix set
- matrix identifiers
- tile dimensions
- origin
- scale denominators
- CRS
- cache behavior

### WFS

Validate:

- feature types
- filtering
- pagination
- output formats
- CRS
- property selection
- transaction capabilities only when explicitly required

Never expose unrestricted large WFS downloads for a map-only use case.

## 5. OGC API

When using OGC APIs, treat the landing page, conformance declarations, collections, links, pagination, and content negotiation as part of the contract.

Test:

- landing page
- API definition
- conformance
- collections
- bbox filtering
- datetime filtering
- pagination
- CRS negotiation
- media types
- links
- error responses

For OGC API - Processes:

- define process inputs/outputs
- distinguish synchronous/asynchronous execution
- expose job status
- support cancellation where safe
- make execution idempotent where appropriate
- enforce resource limits

## 6. GeoServer Interoperability

When GeoServer is used:

- configure workspaces intentionally
- publish only required services
- validate GetCapabilities
- test WMS/WFS/WMTS endpoints independently
- use REST configuration carefully
- keep service configuration versioned where practical
- verify styles and CRS after deployment
- use GeoWebCache for appropriate tiled workloads

Do not expose administrative GeoServer endpoints publicly.

## 7. Client Compatibility

Test important services with at least:

- the production Web GIS client
- a second independent GIS client when interoperability matters
- direct HTTP requests
- automated contract tests

For high-value public services, test with representative QGIS/browser/API clients.

## 8. Filtering and Query Semantics

Validate spatial and attribute filters before sending them to downstream services.

Protect against:

- filter injection
- unbounded queries
- expensive spatial predicates
- unrestricted feature output
- malformed XML/JSON
- resource exhaustion

Use allowlisted filter capabilities where possible.

## 9. Metadata and Provenance

Publish enough metadata for consumers to understand:

- dataset identity
- source
- update date
- CRS
- scale/resolution
- spatial extent
- temporal extent
- responsible organization
- usage/license constraints
- processing lineage

Do not claim a service is authoritative merely because it uses an OGC protocol.

## 10. Versioning and Migration

When migrating WMS/WFS toward OGC APIs:

1. inventory current consumers
2. document existing behavior
3. define the target contract
4. preserve compatibility where required
5. implement adapters/parallel endpoints
6. contract-test both paths
7. communicate deprecation
8. remove legacy services only after consumer migration

Avoid breaking GIS clients without an explicit migration plan.

## 11. Performance

Measure:

- capabilities response
- feature request latency
- map rendering latency
- tile latency
- payload size
- cache hit rate
- concurrency
- database query cost

Use:

- pagination
- bbox filtering
- caching
- vector tiles
- generalized geometries
- response compression

Do not confuse protocol interoperability with performance.

## 12. Testing

Test:

- capabilities/conformance
- CRS
- axis order
- bbox
- datetime
- pagination
- filtering
- empty results
- invalid requests
- content negotiation
- large responses
- authorization
- caching
- service failures

Keep golden examples for critical service contracts.

## 13. Free-First and Licensing

Prefer open standards and free/open-source implementations where technically appropriate.

Do not assume an OGC standard makes underlying data freely reusable. Verify:

- dataset license
- service terms
- attribution
- API quotas
- commercial-use restrictions

Record durable interoperability/licensing decisions in project memory.

## Definition of Done

- required standard is justified
- service contract is documented
- CRS/axis behavior is tested
- capabilities/conformance is valid
- representative client compatibility is verified
- filtering/pagination/limits are enforced
- security controls are applied
- performance is measured
- provenance/license information is documented
- project memory is updated

## Project-Memory Handoff

Update:

- `STATE.md`: current interoperability state and next action
- `TASKS.md`: contract/testing/migration tasks
- `DECISIONS.md`: protocol, CRS, compatibility and licensing decisions
- `SESSION.md`: verified tests and resume point
- `BLOCKERS.md`: unresolved interoperability issues
- `CHANGELOG.md`: meaningful service changes

Never store credentials, API keys, or tokens in project memory.
