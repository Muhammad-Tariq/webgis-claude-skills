---
name: spatial-api
description: Design, implement, secure, validate, test, document, and optimize production spatial APIs connecting Web GIS frontends with PostGIS, GeoServer, raster services, and analytical processing.
---

# Spatial API Engineering

Act as the spatial API specialist for production Web GIS applications.

The API is the controlled boundary between the application and spatial infrastructure.

The goal is to provide APIs that are:

- spatially correct
- secure
- predictable
- performant
- versionable
- observable
- easy for frontend clients to consume
- appropriate for the size and type of geospatial data

Do not expose the database or GeoServer directly when the application requires business logic, authorization, validation, transformation, orchestration, or tenant isolation.

# Mandatory preflight

Before implementing or changing a spatial API:

1. Read project memory:
   - `STATE.md`
   - `TASKS.md`
   - `DECISIONS.md`
   - `SESSION.md`
   - `BLOCKERS.md` when present
2. Inspect repository architecture.
3. Identify frontend framework and map engine.
4. Inspect existing API routes/controllers/services.
5. Inspect database schema and PostGIS functions.
6. Inspect GeoServer services if present.
7. Identify existing API clients and response models.
8. Identify authentication and authorization.
9. Identify CRS conventions.
10. Identify data volume and expected request frequency.
11. Inspect tests.
12. Check git status and recent relevant commits.

Never create a second API pattern when an existing project convention already solves the problem.

# API architecture

Use a clear separation:

```
Web GIS Client
      |
      v
API / Application Layer
      |
      +---- Authentication / Authorization
      |
      +---- Validation
      |
      +---- Business Logic
      |
      +---- Spatial Query Layer
      |          |
      |          +---- PostGIS
      |          +---- GeoServer
      |          +---- Raster/Tile Services
      |
      +---- Processing / Job Queue
      |
      v
Response
```

The API should orchestrate the system rather than duplicate spatial engines unnecessarily.

# API technology selection

Do not force one backend framework.

Evaluate the existing project and requirements.

Possible technologies include:

- FastAPI
- Django/Django REST Framework
- Node.js
- NestJS
- Express
- Next.js route handlers/server functions
- Go
- existing backend

Choose based on:

- existing architecture
- team expertise
- GIS library support
- async workload
- performance requirements
- deployment model
- ecosystem
- maintainability

For heavy spatial computation, Python-based APIs can be useful because of the geospatial ecosystem, but do not introduce Python solely because the application contains maps.

# API boundary decisions

For every endpoint define:

- method
- path
- version
- authentication
- authorization
- input parameters
- geometry format
- input CRS
- output CRS
- filtering
- sorting
- pagination
- response limits
- error format
- caching behavior
- rate limits

Avoid ambiguous endpoints such as:

`/getData`

Prefer resource-oriented or task-oriented routes with explicit contracts.

# API versioning

Use a deliberate versioning strategy.

Possible approaches:

- URL versioning
- header versioning
- compatibility contracts

For public or long-lived APIs, prefer an explicit strategy that allows backward compatibility.

Do not break existing spatial clients without a migration path.

# Spatial input validation

Treat all client-provided spatial input as untrusted.

Validate:

- geometry type
- coordinates
- coordinate ranges
- SRID
- CRS
- bbox
- feature IDs
- attribute filters
- spatial predicates
- buffer distance
- geometry size
- feature count
- file uploads

Reject malformed or excessive requests early.

# CRS contract

Every spatial endpoint must have an explicit CRS contract.

Define:

- accepted input CRS
- default input CRS
- output CRS
- storage CRS
- analysis CRS

Never silently assume that every request is EPSG:4326.

For geometry-bearing APIs, make CRS behavior discoverable and documented.

For measurement/analysis endpoints, use an appropriate projected or geodesic operation rather than blindly calculating in display coordinates.

# GeoJSON

Use GeoJSON when it is appropriate for the response size and client workload.

Define:

- Feature
- FeatureCollection
- geometry types
- properties
- stable IDs
- CRS behavior
- null/empty geometry behavior

Do not return giant FeatureCollections when vector tiles or server-side aggregation are more appropriate.

For large datasets consider:

- pagination
- bbox filtering
- vector tiles
- streaming
- generalized geometry
- aggregated responses

# Bounding-box queries

BBox is one of the most important Web GIS API patterns.

Validate:

- minimum/maximum coordinates
- axis order
- CRS
- antimeridian behavior
- maximum bbox extent

Do not allow arbitrary requests for an entire country/world if the endpoint is intended for interactive map loading.

Use spatial indexes.

# Pagination

Use bounded pagination.

Possible strategies:

- offset/limit for simple datasets
- cursor/keyset pagination for large datasets

Always define:

- default page size
- maximum page size
- stable sort order

Never allow unlimited feature responses by default.

# Filtering

Support explicit, validated filters.

Examples:

- attribute filters
- bbox
- date/time
- category
- status
- spatial relationship

Never pass raw client filter strings directly into SQL.

Map user-facing filter fields to an allowlist of database fields.

# Spatial operations

Common API operations include:

- point-in-polygon
- intersection
- containment
- proximity
- buffer
- nearest feature
- route
- area
- distance
- spatial join
- aggregation
- clipping

For every operation define:

- input geometry
- CRS
- tolerance
- units
- maximum complexity
- timeout expectations
- output format

Do not run expensive operations synchronously when they can exceed normal request latency.

# Async spatial jobs

Use asynchronous jobs for:

- large raster processing
- large vector processing
- long spatial joins
- buffering huge datasets
- GeoAI inference
- batch exports
- report generation
- satellite analysis

A typical pattern:

```
POST /jobs
    ↓
job_id
    ↓
worker
    ↓
processing
    ↓
GET /jobs/{id}
    ↓
result
```

Define job states such as:

- queued
- running
- succeeded
- failed
- cancelled

Store useful provenance:

- input
- parameters
- software/model version
- timestamps
- output location
- error information

# PostGIS integration

Prefer parameterized queries.

Use:

- spatial indexes
- explicit SRIDs
- bounded queries
- database-side filtering
- database-side aggregation
- appropriate projections

Avoid:

- SQL string concatenation
- SELECT *
- loading huge datasets into application memory
- N+1 spatial queries
- unnecessary geometry serialization

Use PostGIS for authoritative spatial operations when appropriate.

# GeoServer integration

Use GeoServer when standards-based GIS services are useful.

The API may:

- proxy approved GeoServer services
- orchestrate layer access
- generate map metadata
- manage application-specific permissions
- trigger asynchronous workflows

Do not blindly proxy every GeoServer endpoint.

Do not expose GeoServer admin or configuration APIs through the public application API.

# Response design

Responses should be predictable.

For spatial resources consider:

```json
{
  "data": {},
  "meta": {
    "count": 10,
    "page": 1,
    "page_size": 10
  }
}
```

For GeoJSON endpoints, follow valid GeoJSON semantics rather than wrapping every response unnecessarily.

For errors define a consistent structure such as:

```json
{
  "error": {
    "code": "INVALID_GEOMETRY",
    "message": "The submitted geometry is invalid.",
    "details": {}
  }
}
```

Do not expose stack traces, SQL, credentials, internal paths, or sensitive implementation details.

# HTTP semantics

Use appropriate status codes.

Examples:

- 200 successful read
- 201 created
- 202 accepted asynchronous job
- 204 successful no-content operation
- 400 invalid request
- 401 unauthenticated
- 403 unauthorized
- 404 not found
- 409 conflict
- 413 oversized request
- 422 semantically invalid spatial input
- 429 rate limited
- 500 unexpected server error
- 503 dependent service unavailable

Do not return 200 for every failure.

# Authentication and authorization

Separate:

- authentication: who is the user?
- authorization: what can they access?

Authorization must be enforced server-side.

Consider:

- RBAC
- ABAC
- tenant isolation
- project-level permissions
- layer-level permissions
- feature-level restrictions where required

Never trust:

- hidden UI controls
- client-provided tenant IDs
- client-provided roles
- client-side permission checks

# Multi-tenancy

For SaaS systems:

- identify tenant from trusted authentication context
- enforce tenant filtering server-side
- validate all resource ownership
- use database-level isolation where justified
- test cross-tenant access

Do not accept a tenant ID from the browser as authoritative.

# Upload APIs

For GIS uploads validate:

- file type
- file size
- archive contents
- geometry count
- CRS
- geometry validity
- coordinate bounds
- decompression limits
- filename/path safety

Supported formats may include:

- GeoJSON
- GeoPackage
- Shapefile
- KML/KMZ
- GeoTIFF
- CSV with coordinates

Do not trust file extensions.

For server-side processing:

- isolate jobs
- restrict resources
- prevent path traversal
- sanitize extracted filenames
- use timeouts
- clean temporary files
- reject malicious or oversized archives

# Security

Protect against:

- SQL injection
- filter injection
- path traversal
- SSRF
- malicious GIS files
- resource exhaustion
- oversized geometry
- oversized bbox
- abusive spatial operations
- cross-tenant data access
- leaked provider credentials

For external URL inputs, prevent SSRF by validating:

- allowed protocols
- allowed destinations
- private/internal network ranges
- redirects
- DNS rebinding risks

Never allow arbitrary URLs to be fetched by the server unless the feature explicitly requires it and is safely constrained.

# Rate limiting

Rate limits should reflect endpoint cost.

Cheap endpoints may have higher limits.

Expensive operations should have stricter controls.

Consider separate limits for:

- map metadata
- feature queries
- search
- geocoding proxy
- routing
- spatial analysis
- uploads
- asynchronous job creation

Do not use one global rate limit for every endpoint without considering workload.

# Caching

Cache when data and authorization semantics permit.

Candidates:

- map metadata
- public feature queries
- tiles
- lookup tables
- static configuration
- analytical products

Do not cache private responses across users without correct cache keys.

Include:

- tenant
- user/role where relevant
- CRS
- bbox
- filters
- version
- time range

in cache identity where necessary.

# Performance

Analyze:

```
Browser
  ↓
Network
  ↓
API
  ↓
Database/GIS service
  ↓
Spatial computation
  ↓
Serialization
  ↓
Network
  ↓
Browser
```

Measure:

- latency
- database time
- GIS service time
- serialization time
- response size
- cache hit rate
- request rate
- error rate

Use:

- spatial indexes
- pagination
- server-side filtering
- aggregation
- generalized geometry
- vector tiles
- caching
- asynchronous jobs

Do not solve slow APIs only by increasing server resources.

# Observability

Track:

- request count
- latency
- status codes
- slow spatial operations
- database latency
- GeoServer latency
- cache hits/misses
- job duration
- upload failures
- rate-limit events

Use request IDs/correlation IDs for multi-service debugging.

Log enough context to reproduce issues but never log secrets.

# Documentation

Every non-trivial spatial endpoint should document:

- purpose
- authentication
- parameters
- geometry format
- CRS
- units
- limits
- response
- errors
- examples
- performance expectations where relevant

OpenAPI is preferred when compatible with the project.

# Testing

### Unit

Test:

- CRS handling
- validation
- filter parsing
- permission rules
- pagination
- response transformation

### Integration

Test:

- API ↔ PostGIS
- API ↔ GeoServer
- API ↔ storage
- API ↔ job workers

### Spatial correctness

Test:

- intersection
- containment
- distance
- buffer
- transformation
- bbox
- invalid geometry
- empty geometry

### Security

Test:

- unauthorized access
- tenant isolation
- SQL injection attempts
- filter injection
- SSRF
- path traversal
- oversized requests
- rate limits

### E2E

Test critical user workflows from browser to API to spatial backend.

# Failure handling

External GIS dependencies can fail.

Handle:

- database unavailable
- GeoServer unavailable
- tile provider unavailable
- geocoding provider unavailable
- routing provider unavailable
- worker unavailable
- timeout
- rate limit
- malformed data

Return useful errors without exposing internal details.

For asynchronous jobs, persist failure state and actionable error information.

# Cost-aware API policy

Prefer open-source infrastructure and free/low-cost providers when they meet requirements.

Evaluate:

- compute
- database
- bandwidth
- external API calls
- geocoding
- routing
- tile services
- storage
- worker execution

Avoid expensive provider calls when equivalent local/open-source processing is practical.

Cache or batch expensive external requests where licensing and freshness allow.

Do not optimize for lowest cost at the expense of correctness, security, or required reliability.

# API quality checklist

Before declaring an endpoint complete:

- [ ] Contract is explicit.
- [ ] Authentication is defined.
- [ ] Authorization is enforced server-side.
- [ ] CRS behavior is explicit.
- [ ] Input validation exists.
- [ ] Spatial indexes are used where required.
- [ ] Pagination/response limits exist.
- [ ] Expensive operations have limits or async processing.
- [ ] SQL is parameterized.
- [ ] GeoServer admin surfaces are not exposed.
- [ ] Uploads are safely validated.
- [ ] Rate limits are appropriate.
- [ ] Caching behavior is intentional.
- [ ] Errors are consistent.
- [ ] Observability exists.
- [ ] Tests cover spatial correctness and security.
- [ ] Documentation exists.
- [ ] Project memory is updated.

# Handoff

After API changes:

1. Update `STATE.md`.
2. Update `TASKS.md`.
3. Record durable API/architecture decisions in `DECISIONS.md`.
4. Record blockers in `BLOCKERS.md`.
5. Update `SESSION.md`.
6. Update `CHANGELOG.md`.
7. Leave the exact next action.

Never claim an API is complete without testing the real spatial boundary it serves.
