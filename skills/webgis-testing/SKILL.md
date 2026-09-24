# Web GIS Testing

## Purpose

Use this skill to validate production Web GIS applications across frontend, maps, spatial APIs, PostGIS, GeoServer, data pipelines, remote sensing, Google Earth Engine, GeoAI, security, accessibility, performance, and end-to-end workflows.

A successful HTTP response or rendered map is not sufficient. Test both **software behavior and spatial correctness**.

## 1. Mandatory Preflight

Before testing:

1. Read `project-memory/STATE.md`.
2. Read `project-memory/TASKS.md`.
3. Read `project-memory/DECISIONS.md`.
4. Read `project-memory/SESSION.md`.
5. Read `project-memory/BLOCKERS.md` when present.
6. Inspect the current implementation and existing tests.
7. Identify the stack, spatial services, CRS/SRID contracts, and last verified state.
8. Run relevant existing tests before modifying them.

If memory conflicts with executable behavior, trust code and verified test results, then repair memory. Never remove or weaken tests merely to obtain a passing suite.

## 2. Testing Pyramid

Use the lowest effective level first:

- unit tests for isolated logic
- integration tests for service/data boundaries
- spatial/scientific tests for geographic correctness
- end-to-end tests for user workflows
- visual regression for stable UI states
- performance tests for scale-sensitive paths
- security tests for exposed boundaries

Do not force every test into E2E.

## 3. GIS Test Fixtures

Maintain small deterministic fixtures:

- known points/polygons
- small GeoJSON
- representative PostGIS rows
- test GeoServer layers
- small raster samples
- representative GeoAI patches
- known GEE outputs

Every important fixture should have an expected result.

Include boundary cases and empty/null cases.

Never use production data as the default automated test database.

## 4. CRS and Coordinate Testing

Test the complete CRS contract:

- source CRS
- storage SRID
- API CRS
- analysis CRS
- display CRS
- export CRS

Verify:

- SRID metadata
- coordinate order
- longitude/latitude order
- transformation accuracy
- units
- bounding boxes
- axis-order behavior

Explicitly test for degree/meter confusion and incorrect reprojection.

Visual alignment alone does not prove numerical correctness.

## 5. Geometry Testing

Test:

- validity
- empty/null geometry
- polygons and multipolygons
- ring orientation where relevant
- self-intersections
- intersects
- contains
- within
- overlaps
- touches
- crosses
- distance
- nearest-neighbor

Include points on boundaries and geometries near boundaries.

## 6. Measurement Testing

For distance, area, perimeter, and bearing:

- test underlying calculations
- verify units
- verify geodesic vs planar behavior
- verify calculation CRS
- compare against known values
- use documented tolerances

Never test only the formatted value shown in the UI.

## 7. Map UI and Lifecycle Testing

Test:

- initialization
- initial extent
- basemap
- layers
- visibility
- opacity
- z-order
- legend
- zoom/pan
- resize
- selection
- popup
- drawing
- editing
- measurement
- route/navigation changes
- unmount/remount

Detect:

- duplicate map instances
- duplicate listeners
- duplicate sources
- stale event handlers
- memory leaks
- orphaned workers
- stale requests

Repeated navigation must not multiply map resources.

## 8. Layer Testing

Test stable layer IDs and:

- source registration
- visibility
- opacity
- ordering
- filters
- scale constraints
- legends
- loading state
- error state
- permissions
- attribution

Removing a layer must clean up associated resources.

Test repeated toggling and layer replacement.

## 9. Frontend Component Testing

Test GIS components such as:

- MapShell
- LayerPanel
- Legend
- Search
- FeatureInspector
- DrawTool
- MeasurementTool
- FilterPanel
- TimeSlider
- AnalysisPanel
- ChartPanel
- ExportDialog
- UploadDialog

Cover normal, loading, empty, error, disabled, and unauthorized states.

## 10. API Contract Testing

Verify:

- method
- route
- request schema
- response schema
- status codes
- pagination
- filtering
- sorting
- GeoJSON structure
- CRS contract
- error schema

Test malformed input, missing parameters, invalid spatial filters, unauthorized requests, and oversized requests.

Use OpenAPI as a contract when available, but test actual runtime behavior.

## 11. GeoJSON Testing

Verify:

- valid JSON
- Feature/FeatureCollection structure
- geometry type
- coordinates
- properties
- feature IDs
- bbox where applicable
- expected CRS behavior

Test empty collections, null geometry, malformed geometry, unexpected properties, and large collections.

## 12. PostGIS Testing

Use an isolated database/schema.

Test:

- migrations
- seed data
- CRUD
- spatial indexes
- spatial predicates
- joins
- bbox filtering
- nearest-neighbor queries
- geometry validation
- GeoJSON serialization

For performance-sensitive queries, verify query plans and index usage.

## 13. GeoServer Testing

Test:

- workspace
- datastore
- layer publication
- CRS
- WMS
- WFS
- vector tiles where used
- styles
- layer groups
- capabilities
- filters
- authentication
- caching

For WMS verify layer, CRS, bbox, image dimensions, and style.

For WFS verify features, attributes, geometry, filters, pagination, and CRS.

Test the deployed service rather than assuming configuration succeeded.

## 14. Raster Testing

Verify:

- dimensions
- CRS
- affine transform/georeferencing
- bounds
- resolution
- bands
- band names
- datatype
- nodata
- value ranges
- compression when relevant

For scientific rasters test representative pixel values and summary statistics.

For tiled/COG outputs test tile continuity and required overviews/range access.

## 15. Remote-Sensing Testing

Test:

- collection/date filters
- cloud/shadow masks
- scale factors
- band selection
- index formulas
- compositing
- temporal aggregation
- nodata
- spatial alignment

Use small deterministic scenes/fixtures. A rendered NDVI layer is not evidence that the NDVI calculation is correct.

## 16. Google Earth Engine Testing

Test:

- collection availability
- AOI
- date filters
- QA/cloud masking
- band names
- scaling
- reducers
- output schema
- export parameters

Use small AOIs for regression tests. Avoid using `getInfo()` as a substitute for proper server-side testing.

Record dataset/script versions for scientifically important outputs.

## 17. GeoAI Testing

Test:

```
Input
  ↓
Preprocessing
  ↓
Model
  ↓
Postprocessing
  ↓
Spatialization
  ↓
Storage
  ↓
API
  ↓
Map
```

Verify:

- input shape
- normalization
- CRS/georeferencing
- checkpoint compatibility
- output shape
- confidence
- thresholds
- vectorization/rasterization
- spatial alignment
- metadata

Use representative model fixtures and compare predictions/statistics where exact bitwise equality is inappropriate.

## 18. Spatial Regression Testing

Traditional snapshots are insufficient.

Use spatial assertions such as:

- bounds
- feature count
- centroid
- area tolerance
- distance tolerance
- overlap ratio
- IoU
- raster statistics
- sample pixel values
- geometry equality within tolerance

Document the scientific or engineering reason for each tolerance.

## 19. Visual Regression

Use browser automation for stable visual states:

- initial map
- layer panel
- selected feature
- popup
- analysis result
- charts
- responsive layouts
- error states

Control viewport, browser, fixtures, map extent, animations, and network dependencies.

Do not use visual snapshots to prove numerical correctness. Mock unstable third-party map tiles when necessary.

## 20. End-to-End Workflows

Use Playwright or an equivalent browser automation framework where appropriate.

Cover workflows such as:

### Viewer
Open → map loads → layer toggle → search → select → inspect.

### Analysis
Open tool → draw/select AOI → parameters → submit → job/result → inspect → export.

### Upload
Select file → validate → upload → process → publish/display → verify metadata.

### Authentication
Sign in → access protected resource → verify authorization → sign out → verify access revocation.

Test both success and failure paths.

## 21. Third-Party Services

External dependencies may include:

- basemap providers
- geocoders
- routing services
- GEE
- GeoServer
- cloud storage
- satellite catalogs

Do not make the entire test suite depend on their live availability.

Prefer mocks/fixtures/local services for most tests and retain a smaller set of real integration tests for critical contracts.

## 22. Accessibility

Test:

- keyboard navigation
- focus order
- visible focus
- labels
- dialogs
- legends
- contrast
- non-color information
- screen-reader labels
- error messages

Provide non-map alternatives for important information where practical, such as tables, text summaries, accessible charts, and downloads.

## 23. Security Testing

Test:

- authentication
- authorization
- tenant isolation
- input validation
- SQL injection resistance
- filter injection
- path traversal
- SSRF
- malicious GIS files
- oversized payloads
- resource exhaustion
- CORS/CSRF where applicable
- secret exposure

Never use production credentials in tests.

## 24. File Upload Testing

For GeoJSON, Shapefile, KML, GeoPackage, raster, and point-cloud uploads test:

- supported type
- MIME/type validation
- malformed files
- oversized files
- missing companion files
- invalid CRS
- invalid geometry
- empty datasets
- duplicate features
- malicious content
- decompression bombs
- path traversal

Verify uploads cannot escape their intended processing/storage boundary.

## 25. Performance Testing

Measure rather than guess.

### Frontend
- initial load
- map initialization
- layer load
- interaction latency
- rendering time
- memory growth

### API
- p50/p95/p99 latency where useful
- throughput
- error rate

### Database
- query latency
- query plan
- index usage
- connection behavior

### GIS services
- WMS/WFS/tile latency
- cache hit rate

### GeoAI
- preprocessing
- inference
- postprocessing
- GPU/CPU utilization
- throughput

Do not optimize without measurements.

## 26. Large-Data Testing

Create controlled scale tests for:

- many features
- large geometries
- large rasters
- many layers
- concurrent users
- large bboxes
- complex filters
- long time series

Verify predictable degradation and test pagination, vector tiling, raster tiling, filtering, and caching.

## 27. Resilience Testing

Test failures of:

- API
- PostGIS
- GeoServer
- GEE jobs
- model workers
- tile providers
- network
- storage
- authentication
- upstream responses

The application should show useful errors, preserve safe state, support retry where appropriate, prevent duplicate expensive submissions, and avoid corruption.

## 28. Async Job Testing

For long-running GIS/GeoAI jobs test:

- submission
- job ID
- queued/running/success/failure
- cancellation
- retry
- timeout
- duplicate submission
- result retrieval

Verify idempotency so repeated client requests do not unintentionally create duplicate jobs.

## 29. Data Pipeline Testing

Test:

Source → Ingestion → Validation → Transformation → Processing → QA → Storage → Publishing → API → Frontend

Verify schema, counts, CRS, geometry validity, attributes, raster metadata, output paths, and provenance.

Use checksums or stable metadata where appropriate.

## 30. Cross-System Contract Testing

Define explicit contracts for:

- frontend ↔ API
- API ↔ PostGIS
- API ↔ GeoServer
- pipeline ↔ GeoServer
- model ↔ API

Include geometry type, SRID, schemas, null behavior, filter semantics, and error responses.

Contract tests should fail clearly when an upstream change breaks a downstream assumption.

## 31. Environment and Isolation

Test separately across local, development, and staging. Production should normally receive only safe smoke/read-only checks.

Use:

- isolated databases
- test schemas
- temporary storage
- test GeoServer workspaces
- test buckets/prefixes
- synthetic users

Never allow automated tests to corrupt production data.

## 32. CI/CD Testing

A typical pipeline:

```
Commit
 ↓
Lint
 ↓
Type Check
 ↓
Unit Tests
 ↓
Integration Tests
 ↓
Build
 ↓
Spatial/Data Validation
 ↓
E2E
 ↓
Security Checks
 ↓
Deploy
 ↓
Smoke Tests
```

Use staged suites. Expensive geospatial, E2E, and scale tests do not need to run on every commit if earlier checks provide adequate feedback.

## 33. Targeted Testing by Change

### Frontend change
Run type checks, component tests, relevant E2E, and visual tests.

### Map-engine change
Run lifecycle, layer, interaction, CRS, measurement, and E2E tests.

### API change
Run unit, contract, integration, security, and relevant E2E tests.

### PostGIS change
Run migrations, spatial integration, performance, and API contract tests.

### GeoServer change
Run configuration, WMS/WFS, style/layer, and integration tests.

### Remote-sensing/GEE change
Run preprocessing, scientific validation, and output metadata tests.

### GeoAI change
Run preprocessing, model-load, inference, spatial-output, regression, API, and E2E tests.

## 34. Debugging Failures

When a test fails:

1. Capture the exact failure.
2. Reproduce independently.
3. Classify it as code, test, fixture, environment, dependency, data, timing, or spatial.
4. Find the smallest failing case.
5. Fix the root cause.
6. Re-run the smallest relevant test.
7. Re-run broader regression tests.
8. Update the test only when intended behavior genuinely changed.
9. Record durable decisions/blockers.

Do not weaken assertions or increase timeouts blindly.

## 35. Flaky Tests

Track:

- test name
- failure frequency
- environment
- suspected cause
- owner
- mitigation
- permanent fix

Do not permanently quarantine a flaky test without investigating it.

## 36. Test Organization

Prefer:

```
tests/
  unit/
  integration/
  spatial/
  api/
  e2e/
  visual/
  performance/
  fixtures/
```

Use behavioral names such as `selecting-a-field-centers-map.spec.ts`.

Keep fixtures small and understandable.

## 37. Definition of Done

A Web GIS feature is sufficiently tested when:

- [ ] Relevant unit tests exist.
- [ ] Integration boundaries are covered.
- [ ] Spatial correctness is tested.
- [ ] CRS/SRID behavior is tested.
- [ ] Geometry edge cases are covered.
- [ ] API contracts are tested.
- [ ] Map lifecycle is tested where applicable.
- [ ] Important user workflows have E2E coverage.
- [ ] Error states are tested.
- [ ] Security-sensitive paths are tested.
- [ ] Performance-sensitive paths have measurements.
- [ ] Large-data behavior is considered.
- [ ] Accessibility is tested for important workflows.
- [ ] External dependencies are isolated appropriately.
- [ ] CI validation passes.
- [ ] Scientific outputs have representative validation where applicable.
- [ ] No tests were weakened/skipped without documented justification.
- [ ] Project memory is updated.

Unit-test success alone does not establish production readiness.

## 38. Project-Memory Handoff

Before ending testing work:

### STATE.md
Record current testing phase, last verified suite, changed files, validation results, blockers, and exact next action.

### TASKS.md
Record tests added/fixed, failures, pending validation, and next test target.

### DECISIONS.md
Record test architecture, fixture strategy, spatial tolerance policy, E2E framework, CI tiers, mocking strategy, and performance thresholds.

### SESSION.md
Record tests actually executed, results, failures/root causes, and exact resume point.

### BLOCKERS.md
Record unresolved flaky tests, unavailable services, environment problems, data-quality issues, and regressions.

Never store credentials or secrets.

## 39. Handoff Summary

Record:

- test scope
- application/component
- tests added/changed
- fixtures
- unit results
- integration results
- spatial validation
- E2E results
- performance results
- security checks
- known flaky tests
- current blocker
- last verified state
- exact next action

The next agent must inspect and execute the relevant test suite before trusting this summary.
