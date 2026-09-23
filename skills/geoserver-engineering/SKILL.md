---
name: geoserver-engineering
description: Design, configure, publish, secure, optimize, test, and operate production GeoServer deployments for Web GIS, OGC services, vector tiles, raster delivery, styling, and spatial APIs.
---

# GeoServer Engineering

Act as the GeoServer and OGC service engineering specialist for production Web GIS systems.

The objective is to publish spatial data reliably and efficiently while keeping configuration, security, performance, and service contracts explicit.

Do not use GeoServer automatically for every GIS backend. Use it when standards-based geospatial publishing, interoperability, map services, feature services, or GeoServer-specific capabilities provide a clear benefit.

# Mandatory preflight

Before changing GeoServer:

1. Read project memory:
   - `STATE.md`
   - `TASKS.md`
   - `DECISIONS.md`
   - `SESSION.md`
   - `BLOCKERS.md` when present
2. Inspect repository and deployment configuration.
3. Identify GeoServer version and Java/runtime requirements.
4. Identify workspaces.
5. Identify datastores.
6. Identify published layers and layer groups.
7. Identify styles.
8. Identify WMS/WFS/WMTS/vector-tile/other enabled services.
9. Identify authentication and authorization configuration.
10. Identify caching and tile infrastructure.
11. Identify PostGIS schemas/tables and raster/object-storage sources.
12. Check current service URLs and client contracts.
13. Check git status and recent relevant commits.

Never make production GeoServer changes without understanding dependencies and client expectations.

# Architecture role

GeoServer may provide:

- WMS
- WFS
- WMTS
- vector tiles
- raster services
- OGC APIs where supported/configured
- map rendering
- feature publishing
- filtering
- styling
- interoperability with GIS clients

GeoServer should generally not own:

- product/business logic
- user billing
- complex application authorization logic
- arbitrary SQL execution
- long-running ML pipelines
- general-purpose background job orchestration

Use an application API alongside GeoServer when business logic or product-specific access control is required.

# Workspace architecture

Use workspaces intentionally.

A workspace should represent a meaningful organizational boundary such as:

- project
- department
- tenant
- data domain
- environment

Avoid creating a workspace for every individual layer without a real organizational reason.

Define:

- workspace name
- namespace
- ownership
- access policy
- deployment lifecycle

Use stable names once external clients depend on them.

# Datastore architecture

Configure datastores explicitly.

Common sources:

- PostGIS
- GeoTIFF/raster
- GeoPackage
- shapefile where legacy compatibility requires it
- cloud/object-backed sources where supported

For PostGIS:

- use least-privilege credentials
- avoid database admin accounts
- configure connection pooling carefully
- keep schema/table ownership explicit
- use spatial indexes
- avoid exposing unnecessary tables

Do not publish every database table automatically.

# Layer publishing

For each published layer define:

- workspace
- datastore
- layer name
- native name
- geometry type
- native CRS
- declared CRS
- bounding box
- supported operations
- metadata
- attribution
- style
- access policy
- scale constraints where appropriate

Keep public layer names stable.

Avoid accidental publication of internal or sensitive datasets.

# CRS configuration

GeoServer CRS configuration must be intentional.

Track:

- native CRS
- declared CRS
- supported output CRS
- client display CRS
- analysis CRS

Never declare a CRS that does not match the underlying data.

For PostGIS layers:

- verify the database SRID
- verify geometry metadata
- verify GeoServer's native CRS
- verify advertised CRS
- test reprojection

Test representative features after CRS changes.

# WMS

Use WMS for:

- server-rendered cartography
- thematic maps
- raster visualization
- print-oriented map rendering
- GIS interoperability

Configure:

- supported formats
- styles
- image dimensions
- transparency
- CRS
- queryable layers
- service limits
- caching where appropriate

Avoid generating extremely large images by default.

Use scale-dependent styling and generalization for complex datasets.

# WFS

Use WFS when feature-level access is required.

Do not expose unrestricted WFS over massive datasets.

Control:

- feature limits
- filters
- output formats
- pagination where supported
- queryable attributes
- allowed operations
- access permissions

For application APIs, consider whether a dedicated spatial API is more appropriate than exposing WFS directly.

# WMTS and tiled delivery

Use tiled delivery when repeated map rendering benefits from caching.

Evaluate:

- tile matrix
- zoom levels
- grid set
- cache storage
- expiration
- invalidation
- seed/truncate operations
- storage growth

Do not pre-seed enormous areas and zoom ranges without estimating storage and processing costs.

# Vector tiles

Use vector tiles when:

- large vector datasets need interactive browser rendering
- client-side styling is valuable
- feature density is high
- repeated requests make raw GeoJSON inefficient

Evaluate:

- tile generation
- generalization
- layer naming
- attribute selection
- tile size
- caching
- zoom-dependent detail

Never include unnecessary attributes in vector tiles.

# Styling

Prefer maintainable, versioned styles.

Depending on the project use:

- SLD
- CSS styling extensions where supported
- YSLD
- other supported style formats

Keep styles aligned with:

- layer semantics
- scale
- geometry type
- accessibility
- product design

Avoid giant unmaintainable style files.

Use scale-dependent rules for dense datasets.

When styling changes are important, record them in project memory or version-controlled configuration.

# Layer groups

Use layer groups when a stable map composition is useful.

Examples:

- basemap overlays
- administrative boundaries
- utility network
- environmental layers
- project-specific thematic maps

Do not create deeply nested groups without a real need.

# Security

Treat GeoServer administration as a privileged surface.

Protect:

- GeoServer admin UI
- REST configuration API
- datastore credentials
- service endpoints
- sensitive workspaces
- internal layers

Use:

- strong authentication
- least privilege
- role-based access
- network restrictions
- reverse proxy controls
- HTTPS
- rate limiting where appropriate

Never expose GeoServer admin credentials to browser code.

Never commit credentials to Git.

# Data access security

Control publication at multiple layers:

1. network boundary
2. GeoServer authentication
3. workspace/layer permissions
4. database permissions
5. application/API authorization

Do not rely on hiding a layer from the UI as security.

For multi-tenant systems, verify that tenant boundaries cannot be bypassed through:

- WMS parameters
- WFS filters
- CQL filters
- REST endpoints
- direct datastore access

# CQL and filtering

Treat filters as untrusted input.

Validate:

- attribute filters
- spatial filters
- CQL expressions
- bbox
- feature IDs
- sort fields

Never allow arbitrary database expressions when the application does not require them.

Bound expensive filter operations.

# Performance

Analyze the complete path:

`Browser → HTTP → GeoServer → datastore → spatial query → rendering → response`

Check:

- database indexes
- geometry complexity
- query plans
- feature count
- response size
- rendering complexity
- style complexity
- reprojection cost
- cache hit rate
- network latency

Use:

- spatial indexes
- geometry generalization
- scale-dependent styling
- vector tiles
- tile caching
- response limits
- precomputed layers
- materialized views where justified

Do not attempt to solve every performance issue by increasing server memory.

# GeoWebCache / caching

When tiled delivery is appropriate:

- configure cache layers deliberately
- define grid sets
- define zoom ranges
- configure expiration
- estimate storage
- monitor cache growth
- plan invalidation

For frequently changing data, define an explicit refresh strategy.

Do not blindly cache highly dynamic or permission-sensitive data.

# Database integration

For PostGIS-backed layers:

- verify spatial indexes
- verify SRIDs
- use appropriate database roles
- avoid publishing internal tables
- use views/materialized views when they improve safety or performance
- keep database schema evolution coordinated with GeoServer configuration

When changing a PostGIS schema, inspect GeoServer dependencies before migration.

# Raster publishing

For raster/imagery:

Evaluate:

- GeoTIFF
- Cloud Optimized GeoTIFF
- pyramids/overviews
- tiling
- raster caching
- reprojection
- mosaics
- scale-dependent rendering

For large remote-sensing datasets, avoid unnecessarily copying every source into a relational database.

Use object storage or specialized raster infrastructure when more appropriate.

# Large datasets

For national/regional datasets:

Prefer:

- generalized layers
- vector tiles
- cached tiles
- server-side filtering
- spatial indexes
- precomputed products
- appropriate scale ranges

Avoid:

- unbounded WFS
- giant GeoJSON downloads
- rendering millions of complex features at every zoom
- unnecessary reprojection
- publishing raw source tables directly to the public internet

# Service limits

Configure limits appropriate to the application.

Consider:

- max features
- max rendering dimensions
- request timeout
- concurrency
- allowed formats
- upload limits
- query limits

Limits should protect reliability without breaking legitimate workflows.

# REST configuration

GeoServer REST APIs can automate configuration, but treat them as privileged administration APIs.

Automation should be:

- idempotent
- version-controlled where possible
- environment-aware
- tested
- auditable

Never run destructive REST configuration blindly.

Before deleting or replacing resources:

1. identify dependents
2. export/backup configuration where appropriate
3. validate target environment
4. apply change
5. verify services

# Deployment

Use reproducible deployment.

Define:

- GeoServer version
- Java version
- data directory strategy
- configuration persistence
- extensions
- plugins
- reverse proxy
- HTTPS
- storage
- backup
- monitoring

Prefer immutable or declarative deployment patterns where practical.

Do not depend on undocumented manual UI changes in production.

# Environment separation

Keep development, staging, and production configuration separate.

Never copy production secrets into development.

Use environment-specific:

- database connections
- URLs
- credentials
- service limits
- cache settings
- external provider configuration

Keep secret values outside source control.

# Backups

Back up:

- GeoServer data directory/configuration
- styles
- layer metadata
- database
- relevant tile cache metadata when necessary

Test restoration.

A backup is not sufficient until restoration has been verified.

# Monitoring

Monitor:

- request rate
- response latency
- HTTP errors
- WMS render time
- WFS query time
- cache hit rate
- database connections
- memory
- CPU
- disk
- cache storage
- failed authentication
- configuration changes

Use logs and metrics to identify actual bottlenecks.

# Testing

Test at multiple levels.

### Configuration

- workspace exists
- datastore connects
- layer publishes
- CRS is correct
- style loads
- permissions work

### Service

- WMS GetCapabilities
- WMS GetMap
- WMS GetFeatureInfo where applicable
- WFS capabilities
- WFS feature query where applicable
- WMTS capabilities/tile requests
- vector tile requests where applicable

### Spatial correctness

Verify:

- CRS
- bounding boxes
- reprojection
- geometry type
- feature count
- style placement

### Security

Test:

- anonymous access
- authorized access
- unauthorized layer access
- admin endpoint protection
- tenant isolation
- filter abuse

### Performance

Test representative:

- small
- medium
- large
- complex geometry
- high-concurrency

workloads.

# Common failure modes

Investigate:

- wrong native CRS
- wrong declared CRS
- missing spatial index
- slow database query
- giant WFS response
- excessive WMS rendering
- expensive reprojection
- overly complex styles
- cache misconfiguration
- unbounded filters
- public admin endpoints
- leaked datastore credentials
- stale configuration
- accidental layer publication
- mismatched database schema
- unsupported output format
- oversized map requests

# Free-first and cost policy

Prefer open-source GeoServer and open geospatial standards when they satisfy requirements.

Evaluate total operational cost:

- compute
- memory
- storage
- tile cache
- database
- bandwidth
- monitoring
- backups
- operational maintenance

Do not assume self-hosted GeoServer is always the cheapest solution.

A managed GIS service may be justified when it materially reduces operational complexity or provides required reliability/support.

When a paid service is chosen, record:

- requirement
- alternatives evaluated
- expected usage
- cost assumptions
- migration/lock-in considerations

# Definition of done

Before declaring GeoServer work complete:

- [ ] Workspaces are intentional.
- [ ] Datastores use least privilege.
- [ ] Published layers are explicitly selected.
- [ ] CRS/native CRS are verified.
- [ ] WMS/WFS/WMTS/vector-tile choices are justified.
- [ ] Styles are maintainable and versioned where appropriate.
- [ ] Large-data strategy is defined.
- [ ] Caching strategy is defined where needed.
- [ ] Service limits are configured.
- [ ] Security boundaries are tested.
- [ ] Admin/REST surfaces are protected.
- [ ] Production deployment is reproducible.
- [ ] Monitoring is defined.
- [ ] Backup and restoration are addressed.
- [ ] Free/open-source vs paid infrastructure was evaluated.
- [ ] Critical service flows are tested.
- [ ] Project memory is updated.

# Handoff

After GeoServer changes:

1. Update `STATE.md`.
2. Update `TASKS.md`.
3. Record durable configuration decisions in `DECISIONS.md`.
4. Record blockers in `BLOCKERS.md`.
5. Update `SESSION.md`.
6. Update `CHANGELOG.md`.
7. Leave an exact next action.

Never claim a GeoServer configuration, deployment, security fix, or performance improvement is complete without verification.
