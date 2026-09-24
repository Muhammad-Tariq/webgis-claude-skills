# Performance Optimization

## Purpose

Use this skill to diagnose, design, measure, and improve Web GIS performance across the browser, map engine, API, PostGIS, GeoServer, raster/remote-sensing pipelines, object storage, workers, and infrastructure.

Performance work must be evidence-driven. Do not optimize based on intuition alone, and do not trade correctness, security, accessibility, or scientific validity for superficial speed.

---

## 1. Mandatory Preflight

Before performance changes:

1. Read:
   - `project-memory/STATE.md`
   - `project-memory/TASKS.md`
   - `project-memory/DECISIONS.md`
   - `project-memory/SESSION.md`
   - `project-memory/BLOCKERS.md` when present
2. Inspect the current architecture and deployment.
3. Identify the user-visible performance target.
4. Establish a baseline before changing code/configuration.
5. Inspect recent relevant commits.
6. Identify whether the bottleneck is frontend, network, API, database, GIS server, raster pipeline, worker, storage, or infrastructure.
7. Preserve verified behavior while optimizing.

If project memory conflicts with measurements or implementation, trust measured/verified behavior and repair memory.

---

## 2. Performance Is a System Property

Model the request path:

```
User
 ↓
Browser/UI
 ↓
Map renderer
 ↓
CDN/reverse proxy/cache
 ↓
API
 ↓
PostGIS / GeoServer / processing service
 ↓
Object storage / raster / external provider
```

For each path measure:

- latency
- throughput
- payload size
- CPU
- memory
- database execution time
- network transfer
- rendering time
- cache hit rate
- concurrency
- error rate

Optimize the actual bottleneck rather than the most visible component.

---

## 3. Define Performance Budgets

Create explicit budgets appropriate to the product.

Examples:

- initial page load
- time to interactive
- first meaningful map render
- first useful layer
- map pan/zoom responsiveness
- API latency
- spatial query latency
- tile latency
- feature inspection latency
- chart update latency
- export completion time
- memory usage
- bundle size
- raster processing duration

Record:

- target
- current baseline
- measurement method
- environment
- dataset size
- expected concurrency

Do not treat a benchmark without its dataset, environment, and workload as universally representative.

---

## 4. Measure Before and After

Use reproducible measurements.

Capture:

- p50
- p95
- p99 when useful
- minimum/maximum where meaningful
- requests per second
- payload size
- browser frame rate/render timing
- database execution time
- cache hit/miss
- CPU/memory
- queue depth

Compare equivalent workloads.

A performance claim should state:

- what was measured
- where
- against what baseline
- under what workload
- what changed

Never claim an optimization is successful merely because the code looks cleaner.

---

## 5. Frontend Performance

Optimize the application without sacrificing GIS usability.

### Bundle strategy

- code-split heavy GIS modules
- lazy-load advanced analysis tools
- avoid importing entire libraries when smaller imports are possible
- remove unused dependencies
- use production builds
- compress assets
- cache immutable assets
- measure bundle size

### Rendering

Avoid unnecessary:

- component rerenders
- map instance recreation
- layer recreation
- source recreation
- event listener duplication
- expensive derived state
- DOM overlays for thousands of features

Keep map rendering state separate from unrelated UI state where appropriate.

### Data fetching

- request only needed fields
- use bounding boxes
- paginate
- debounce search
- cancel stale requests
- cache stable responses
- avoid duplicate requests
- prefetch only when evidence supports it

---

## 6. Map Rendering Performance

Choose rendering strategy based on dataset size and interaction requirements.

### Small vector datasets

GeoJSON may be appropriate.

Optimize:

- geometry simplification
- feature properties
- coordinate precision
- feature count
- update frequency

### Large vector datasets

Prefer:

- vector tiles
- server-side filtering
- spatial indexing
- generalized geometries
- appropriate tile resolution

Do not send millions of features as one GeoJSON response.

### Raster

Use:

- tiled imagery
- pyramids/overviews
- appropriate resolution
- COG/range requests when suitable
- server-side reprojection only when necessary

### 3D

For Cesium or similar systems:

- use appropriate level-of-detail
- stream rather than load everything
- simplify geometry
- avoid excessive entity counts
- use 3D Tiles or equivalent when appropriate

---

## 7. PostGIS Query Optimization

Treat PostGIS as a primary performance boundary.

For slow queries:

1. reproduce the query
2. inspect `EXPLAIN`
3. inspect `EXPLAIN ANALYZE`
4. verify spatial indexes
5. inspect row estimates
6. check geometry complexity
7. check joins and filters
8. check sorting/grouping
9. inspect query frequency
10. compare alternative query plans

Common optimizations:

- GiST/SP-GiST indexes
- appropriate B-tree indexes for attributes
- composite indexes where justified
- bounding-box filtering
- `ST_Intersects`/spatial predicates with indexed geometries
- geometry simplification
- precomputed derived values
- materialized views
- partitioning for suitable temporal/large datasets
- query result caching

Do not add indexes blindly. Measure write overhead and storage impact.

---

## 8. Spatial Query Design

Avoid expensive operations on unnecessarily large geometries.

Prefer:

- coarse filtering before expensive predicates
- spatial index candidates first
- appropriate geometry precision
- smaller analysis windows
- pre-simplified display geometries
- generalized layers for small scales

Be careful with:

- `ST_Union` over huge feature sets
- repeated `ST_Intersection`
- large buffers
- distance calculations across unbounded datasets
- repeated reprojection inside queries
- per-row expensive raster/vector operations

For measurement and scientific analysis, optimization must not change the intended result.

---

## 9. API Performance

Design spatial APIs to minimize unnecessary transfer and computation.

Use:

- pagination
- bbox filters
- attribute filters
- field selection
- simplified representations
- vector tiles for large map layers
- compression
- conditional requests
- caching
- asynchronous jobs for expensive operations

Avoid:

- returning entire datasets
- deeply nested unnecessary responses
- repeated database queries
- N+1 spatial queries
- synchronous long-running raster/GeoAI jobs

Keep API contracts stable while optimizing internals.

---

## 10. GeoServer Performance

For GeoServer workloads, inspect:

- datastore connection pools
- spatial indexes
- layer complexity
- SLD rendering complexity
- WMS image dimensions
- WFS feature counts
- GeoWebCache/tile cache hit rates
- JVM memory
- request concurrency
- timeout settings

Prefer cached/tiled delivery for heavily requested map visualization.

For large vector layers, evaluate:

- vector tiles
- scale-dependent styling
- generalized datasets
- attribute minimization
- spatial filtering

For WMS, avoid generating unnecessarily large images.

For WFS, never expose unrestricted massive feature downloads when the use case only requires map visualization.

---

## 11. Tile Strategy

Choose tile architecture deliberately:

- raster tiles
- vector tiles
- dynamic WMS
- cached WMS/WMTS
- self-hosted tile service
- external provider

Evaluate:

- tile size
- zoom levels
- feature density
- styling complexity
- cacheability
- generation cost
- storage cost
- update frequency

For vector tiles:

- simplify geometries by zoom
- select only required attributes
- use appropriate tile extent/buffer
- avoid excessive feature duplication
- measure tile size

For raster tiles:

- choose appropriate image format
- build overviews
- cache frequently requested areas
- avoid unnecessary reprojection

---

## 12. Raster and Remote-Sensing Performance

For satellite/remote-sensing workflows:

- process only the AOI
- filter imagery before expensive operations
- mask clouds/shadows efficiently
- use appropriate scale
- avoid unnecessary band retention
- composite only required periods
- export at scientifically justified resolution
- tile large rasters
- use overviews/pyramids
- avoid repeatedly downloading the same source data

For GEE:

- keep computation server-side
- avoid unnecessary `getInfo()`
- reduce data before export
- use `tileScale`, `maxPixels`, and `bestEffort` only when appropriate
- avoid redundant exports
- reuse intermediate results where practical

Optimization must preserve scientific meaning.

---

## 13. Large Dataset Strategy

Classify data by scale before choosing delivery:

| Scale | Typical strategy |
|---|---|
| Small | GeoJSON / API response |
| Medium | filtered GeoJSON / server-side query |
| Large vector | vector tiles / generalized layers |
| Very large vector | tiled/partitioned services |
| Small raster | direct raster service |
| Large raster | COG/tiles/overviews/object storage |
| Huge analysis | batch processing/workers/GEE |

Do not use a single delivery format for every scale.

---

## 14. Caching

Use caching at the correct layer.

Possible layers:

- browser cache
- CDN
- reverse proxy
- API response cache
- PostGIS/materialized results
- GeoServer tile cache
- object storage
- worker result cache

For every cache define:

- key
- TTL
- invalidation
- scope
- authorization implications
- stale-data tolerance
- storage limit

Never cache user-private spatial responses in a shared cache without safe authorization-aware keys.

---

## 15. Network and Payload Optimization

Reduce unnecessary bytes.

Use:

- gzip/Brotli where appropriate
- compact JSON
- GeoJSON property selection
- vector tiles
- image compression
- HTTP caching
- HTTP/2 or HTTP/3 where supported
- CDN delivery for static assets

Do not compress already-compressed formats unnecessarily.

For spatial data, coordinate precision and geometry simplification can materially reduce payloads, but must remain within accuracy requirements.

---

## 16. Search, Geocoding, and Routing

External providers can become performance bottlenecks.

Apply:

- debounce
- request cancellation
- caching
- local result reuse
- bounded query scope
- provider timeout
- fallback behavior
- quota monitoring

Do not hammer a free public geocoder/routing service with uncontrolled autocomplete traffic.

Respect provider usage policies and rate limits.

---

## 17. Web Workers and Client-Side GIS

Move expensive browser computation off the main thread when appropriate.

Good candidates:

- geometry processing
- large GeoJSON parsing
- spatial filtering
- client-side clustering
- raster calculations
- format conversion

Use workers only when their overhead is justified.

Avoid transferring enormous objects repeatedly between the main thread and worker.

---

## 18. Background Processing

Use asynchronous jobs for:

- large spatial joins
- raster processing
- GeoAI inference
- report generation
- bulk exports
- tile generation
- large file ingestion

Workers should expose measurable states:

`queued → running → completed`

and:

`queued → running → failed`

Add:

- retry policy
- timeout
- idempotency
- cancellation where safe
- progress reporting
- cleanup

---

## 19. Memory and Resource Management

Watch for:

- browser memory growth
- detached map layers
- duplicate listeners
- unreleased object URLs
- unbounded caches
- database connection exhaustion
- GeoServer/JVM memory pressure
- worker memory leaks
- oversized Docker containers
- temporary raster accumulation

Long-running map applications should be tested through repeated pan/zoom/filter/layer cycles.

---

## 20. Performance vs Correctness

Never optimize away:

- CRS correctness
- measurement accuracy
- geometry validity
- scientific preprocessing
- authorization
- tenant isolation
- audit requirements
- data provenance
- required map precision

For geospatial analysis, distinguish:

- display simplification
- analytical simplification

Display simplification may be acceptable at small scales. Analytical simplification requires explicit scientific justification.

---

## 21. Performance Regression Testing

Create repeatable workloads for:

- representative map loads
- common spatial queries
- API endpoints
- vector tile requests
- WMS requests
- raster operations
- GeoAI inference
- GEE exports
- large uploads

Track performance over time.

Useful regression gates include:

- p95 API latency
- p95 spatial query latency
- maximum acceptable tile size
- maximum browser memory
- bundle-size ceiling
- render/frame-time budget
- export duration

Do not create arbitrary thresholds without representative baseline data.

---

## 22. Profiling and Diagnostics

Use the appropriate profiler for the boundary:

### Browser
- Performance panel
- memory profiler
- network waterfall
- framework profiler

### API
- request tracing
- application profiling
- database timing

### PostgreSQL/PostGIS
- `EXPLAIN ANALYZE`
- query statistics
- index usage
- locks
- connection statistics

### GeoServer
- request logs
- JVM metrics
- datastore metrics
- tile-cache metrics

### Infrastructure
- CPU
- RAM
- disk I/O
- network
- container metrics

Do not profile production destructively. Prefer representative staging workloads when profiling can materially affect service performance.

---

## 23. Performance Architecture Patterns

Prefer patterns that match workload:

### Public map portal
CDN → cached tiles → lightweight API → PostGIS/GeoServer

### Analytical dashboard
Frontend → API → PostGIS/worker → cached analytical results

### Remote-sensing platform
Frontend → API → job queue → GEE/local processing → object storage → map service

### GeoAI application
Frontend → API → inference worker/GPU → raster/vector output → tiled delivery

These are starting patterns, not mandatory architectures.

---

## 24. Cost-Aware Optimization

Performance improvements have costs.

Evaluate:

- extra compute
- RAM
- database storage
- tile storage
- CDN
- egress
- managed caching
- GPU
- provider API usage
- operational complexity

Prefer optimizations that improve performance without unnecessary recurring cost.

A free optimization such as a proper spatial index should normally be exhausted before buying larger infrastructure for the same bottleneck.

Do not choose a paid provider solely because it appears faster in an unrepresentative benchmark.

---

## 25. Optimization Workflow

Use this sequence:

1. Define user-visible performance problem.
2. Establish baseline.
3. Identify bottleneck.
4. Form a measurable hypothesis.
5. Implement the smallest appropriate change.
6. Run regression tests.
7. Re-measure the same workload.
8. Compare correctness and performance.
9. Evaluate cost/complexity.
10. Keep or revert the change.
11. Record the result in project memory.

Never accumulate speculative optimizations without measuring them.

---

## 26. Performance Definition of Done

Performance work is complete when:

- baseline was measured
- bottleneck was identified
- optimization has a clear hypothesis
- functional/spatial correctness remains intact
- regression tests pass
- before/after measurements exist
- representative dataset/workload was used
- resource impact is understood
- cost impact is understood
- cache behavior is understood where relevant
- production monitoring can detect regression
- project memory records the verified result

---

## 27. Project-Memory Handoff

Before stopping:

### STATE.md
Record:
- performance phase
- target metric
- baseline
- last verified optimization
- current bottleneck
- exact next action

### TASKS.md
Record:
- profiling tasks
- optimization tasks
- regression tasks
- completed/in-progress/blocked state

### DECISIONS.md
Record durable choices such as:
- vector tiles vs GeoJSON
- caching strategy
- database indexing strategy
- raster format/delivery strategy
- tile architecture
- CDN/provider decisions
- performance budgets

### SESSION.md
Record:
- measurements
- tools/workloads used
- changes made
- validation results
- failed experiments
- exact resume point

### BLOCKERS.md
Record unresolved:
- dataset scale
- provider quota
- hardware limits
- unexplained latency
- database locks
- rendering bottlenecks

### CHANGELOG.md
Record meaningful performance improvements and verified benchmark changes.

Never claim performance is improved without a comparable measurement.
