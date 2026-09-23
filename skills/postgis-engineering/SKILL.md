---
name: postgis-engineering
description: Design, implement, optimize, secure, test, and migrate production PostgreSQL/PostGIS systems for Web GIS, spatial APIs, analytics, and GeoAI workloads.
---

# PostGIS Engineering

Act as the database and spatial-data engineering specialist for production Web GIS systems.

The goal is to build spatial databases that are:

- spatially correct
- query-efficient
- secure
- maintainable
- observable
- migration-safe
- scalable to the intended workload

Do not treat PostGIS as merely a place to store geometry. Design the data model, spatial indexes, queries, CRS strategy, APIs, and operational lifecycle together.

# Mandatory preflight

Before making changes:

1. Read project memory:
   - `STATE.md`
   - `TASKS.md`
   - `DECISIONS.md`
   - `SESSION.md`
   - `BLOCKERS.md` when present
2. Inspect repository structure.
3. Inspect database configuration and environment variable names.
4. Inspect existing migrations/schema.
5. Inspect ORM/query-builder configuration if present.
6. Inspect API contracts using the database.
7. Identify existing spatial tables, geometry/geography columns, and SRIDs.
8. Identify indexes and constraints.
9. Inspect existing queries before changing schema.
10. Check git status and recent relevant commits.

Never redesign an existing schema without understanding current data, queries, dependencies, and migration constraints.

# Database architecture

PostgreSQL + PostGIS is the default strong choice for relational spatial data.

Use it for:

- vector features
- spatial joins
- spatial filtering
- aggregation
- proximity queries
- geometry validation
- spatial indexing
- transactional GIS data
- authoritative spatial calculations

Do not force every workload into PostGIS.

Evaluate object storage, COGs, raster databases, tile stores, point-cloud storage, or specialized systems when the workload requires them.

# Spatial data modeling

For every spatial dataset define:

- business purpose
- geometry type
- dimensionality: 2D / Z / M / ZM
- SRID
- geometry vs geography
- source CRS
- authoritative source
- update frequency
- expected row count
- geometry complexity
- accuracy requirements
- retention requirements

Use explicit geometry types where possible.

Example:

`geometry(MultiPolygon, 32643)`

is preferable to an unconstrained geometry column when the dataset has a known type and CRS.

Avoid using generic `geometry` without a reason.

# Geometry vs geography

Choose deliberately.

## geometry

Use when:

- projected/local coordinate systems are required
- planar spatial operations are appropriate
- high-performance local calculations matter
- the application works primarily in a known projected CRS

## geography

Use when:

- global longitude/latitude data is central
- geodesic distance/area behavior is required
- cross-region geographic calculations are needed

Do not choose geography simply because coordinates are longitude/latitude.

Do not use geographic coordinates as a substitute for understanding the measurement requirements.

# CRS and SRID policy

CRS must be explicit.

Track:

- source CRS
- ingestion CRS
- storage CRS
- display CRS
- analysis CRS
- export CRS

Rules:

- Never silently assign an SRID.
- Never mix SRIDs in a spatial operation without an intentional transformation.
- Validate incoming SRIDs.
- Use `ST_Transform` for coordinate transformation.
- Use `ST_SetSRID` only to assign metadata when the coordinates are already known to be in that CRS.
- Do not confuse `ST_SetSRID` with coordinate transformation.

For measurement:

- choose a suitable projected CRS for local/regional planar analysis, or
- use geography/geodesic operations where appropriate.

Document the reasoning when accuracy is important.

# Geometry validity

Treat invalid geometry as a data-quality issue.

Use appropriate checks such as:

- `ST_IsValid`
- `ST_IsValidReason`
- `ST_MakeValid` when correction is justified

Do not blindly run `ST_MakeValid` on all data without understanding the semantic impact.

After repair, verify:

- geometry type
- topology
- area/length changes
- feature count
- expected boundaries

Define whether invalid geometries are:

- rejected
- quarantined
- automatically repaired
- accepted with warnings

# Spatial indexes

Spatial indexes are mandatory for production spatial filtering unless there is a demonstrated reason not to use one.

Evaluate:

- GiST
- SP-GiST
- B-tree for non-spatial attributes
- partial indexes
- composite indexes
- covering indexes where useful

Typical spatial index:

`CREATE INDEX ... USING GIST (geom);`

Do not add indexes blindly.

For every important index consider:

- query pattern
- selectivity
- table size
- write frequency
- storage cost
- maintenance cost

# Query design

Prefer database-side spatial operations.

Common patterns:

- `ST_Intersects`
- `ST_Within`
- `ST_Contains`
- `ST_DWithin`
- `ST_Touches`
- `ST_Crosses`
- `ST_Overlaps`
- `ST_Centroid`
- `ST_Intersection`
- `ST_Union`
- `ST_Collect`
- `ST_Buffer`
- `ST_Transform`

Use index-friendly predicates whenever possible.

For proximity queries, prefer patterns that allow the spatial index to participate.

Do not calculate expensive geometry operations on millions of rows when a bounding-box or indexed prefilter can reduce the candidate set.

# Query performance workflow

When a spatial query is slow:

1. Reproduce the query.
2. Inspect the SQL.
3. Inspect the query parameters.
4. Run `EXPLAIN`.
5. Run `EXPLAIN ANALYZE` carefully on representative data.
6. Check whether spatial indexes are used.
7. Check row estimates.
8. Check geometry complexity.
9. Check unnecessary `ST_Transform`.
10. Check serialization/network payload size.
11. Check whether filtering can happen earlier.
12. Check whether precomputation/materialization is appropriate.
13. Re-test after the smallest targeted change.

Never optimize based only on intuition.

# Common performance failures

Investigate:

- missing GiST indexes
- invalid or unusable indexes
- sequential scans on large spatial tables
- mixed SRIDs
- repeated `ST_Transform`
- expensive functions applied before filtering
- massive GeoJSON serialization
- `SELECT *` on spatial endpoints
- unbounded spatial queries
- overly complex geometries
- unnecessary `ST_Union`
- huge buffers
- N+1 spatial queries
- client-side spatial processing that belongs in SQL
- missing pagination
- poor query statistics

# Geometry simplification

Use simplification deliberately.

Potential tools:

- `ST_Simplify`
- `ST_SimplifyPreserveTopology`
- precomputed generalized geometries
- vector tiles

Never simplify authoritative geometry destructively when exact geometry must be preserved.

Prefer:

- source/authoritative geometry
- derived display geometry

when multiple resolutions are needed.

# Large datasets

For large spatial tables:

- partition where justified
- use spatial indexes
- use appropriate statistics
- avoid unbounded responses
- use server-side filtering
- paginate
- generalize
- use vector tiles where appropriate
- precompute expensive derived products
- archive historical data when appropriate

Do not partition solely because a table is large. Partition when query patterns, lifecycle, retention, or write behavior justify it.

# Raster workloads

PostGIS can support raster workloads, but do not automatically put all imagery into the relational database.

Evaluate:

- PostGIS Raster
- Cloud Optimized GeoTIFF
- object storage
- tile services
- GeoServer
- cloud raster platforms
- GEE
- specialized raster pipelines

Choose based on:

- data size
- access pattern
- processing frequency
- transactional needs
- cost
- deployment model

# Temporal and versioned GIS data

For time-dependent datasets define:

- observation time
- valid time
- ingestion time
- version
- source
- provenance

Do not overwrite historical observations when the application requires temporal analysis.

Use appropriate indexes for common time + spatial query patterns.

# Schema design

Prefer:

- stable primary keys
- explicit constraints
- foreign keys where appropriate
- NOT NULL where required
- CHECK constraints
- unique constraints
- controlled enums/reference tables where appropriate
- timestamps
- provenance fields

For spatial tables consider:

- `id`
- `geom`
- `created_at`
- `updated_at`
- `source`
- `source_id`
- `version`

Do not add generic metadata columns without a real use case.

# Spatial relationships

Model relationships deliberately.

Examples:

- parcel → owner
- road → road segment
- administrative unit → parent unit
- sensor → observation
- field → crop season
- imagery → acquisition
- model run → prediction product

Keep business identity separate from geometry identity when necessary.

# API boundaries

Do not expose unrestricted SQL through an API.

API layers should control:

- filters
- bbox
- geometry
- IDs
- pagination
- sorting
- CRS
- response size
- allowed operations

Use parameterized queries.

Never concatenate user-controlled values directly into SQL.

For spatial APIs define:

- input CRS
- output CRS
- geometry format
- max feature count
- max bbox size
- pagination
- error behavior

# GeoJSON and serialization

Never serialize unnecessarily large spatial datasets.

For API responses:

- select only required columns
- simplify when display geometry is sufficient
- paginate
- use bounding-box filtering
- use vector tiles for large interactive datasets
- consider compressed responses

Separate:

- database geometry
- API representation
- frontend rendering representation

# Security

Protect the database from:

- SQL injection
- unsafe spatial filters
- malicious geometries
- oversized queries
- resource exhaustion
- unauthorized spatial access
- cross-tenant data leakage
- exposed database credentials

Use:

- parameterized queries
- least-privilege database users
- separate migration/runtime roles where appropriate
- row-level security where justified
- tenant isolation
- query limits
- connection pooling
- auditing for sensitive systems

Never store passwords, connection strings, or API secrets in Git or project memory.

# Multi-tenancy

For SaaS applications decide explicitly:

- shared schema
- shared tables with tenant ID
- separate schemas
- separate databases

For shared spatial tables:

- enforce tenant isolation at the database/API boundary
- consider row-level security
- index tenant + spatial query patterns when appropriate
- test cross-tenant leakage

Never rely solely on frontend filtering for tenant isolation.

# Migrations

All production schema changes must be migration-safe.

Before migration:

1. Identify dependent code.
2. Identify existing data.
3. Estimate migration duration.
4. Consider locking behavior.
5. Plan rollback or recovery.
6. Test against representative data.
7. Deploy compatible application/schema changes where needed.

Prefer additive migrations for high-risk production changes.

Avoid destructive operations without explicit migration planning.

# Seed and fixture data

Keep development/test GIS data:

- small enough for fast tests
- representative of real geometry complexity
- valid
- CRS-correct
- non-sensitive

Do not commit confidential production datasets.

# Testing

Test:

### Schema

- geometry type
- SRID
- constraints
- indexes
- foreign keys

### Spatial correctness

- intersections
- containment
- distance
- area
- length
- CRS transformations
- geometry validity

### Query performance

Use representative datasets and verify important plans.

### API integration

Test:

- bbox filtering
- pagination
- CRS handling
- invalid geometry
- empty results
- authorization
- maximum limits

### Regression

Keep known spatial edge cases as tests.

Examples:

- antimeridian
- invalid polygons
- multipolygons
- empty geometries
- null geometry
- mixed SRIDs
- very large polygons
- duplicate features

# Observability

For production spatial systems monitor:

- query latency
- slow queries
- connection pool usage
- database CPU
- memory
- disk usage
- index growth
- table growth
- failed queries
- API response size
- spatial endpoint usage

Log enough context to diagnose spatial issues without logging secrets or sensitive data.

# Backup and recovery

For production:

- configure PostgreSQL backups
- verify PostGIS extension compatibility
- test restore procedures
- define RPO/RTO
- protect backups
- monitor backup success

A backup that has never been restored is not a verified recovery strategy.

# Cost-aware database policy

Prefer open-source PostgreSQL/PostGIS when it meets requirements.

Optimize total cost, not only database licensing.

Consider:

- managed database cost
- compute
- storage
- backup storage
- network egress
- replicas
- monitoring
- operational labor
- scaling requirements

Self-hosting is not automatically cheaper if operational complexity becomes excessive.

Use managed PostgreSQL when reliability, backups, scaling, or operational simplicity justify the cost.

# Definition of done

Before declaring PostGIS work complete:

- [ ] Data model is explicit.
- [ ] Geometry type is appropriate.
- [ ] SRID/CRS strategy is documented.
- [ ] Geometry vs geography choice is justified.
- [ ] Geometry validity behavior is defined.
- [ ] Spatial indexes exist where required.
- [ ] Important queries were inspected.
- [ ] Query plans were checked for performance-sensitive paths.
- [ ] API response sizes are bounded.
- [ ] Security boundaries are defined.
- [ ] Migration strategy is safe.
- [ ] Representative spatial tests exist.
- [ ] Production observability is considered.
- [ ] Backup/recovery requirements are addressed.
- [ ] Project memory is updated.

# Handoff

After database work:

1. Update `STATE.md`.
2. Update `TASKS.md`.
3. Record schema/architecture decisions in `DECISIONS.md`.
4. Record migration risks in `BLOCKERS.md` when applicable.
5. Update `SESSION.md`.
6. Update `CHANGELOG.md`.
7. Record the exact next action.

Never claim a migration, optimization, or spatial correctness fix is complete without verification.
