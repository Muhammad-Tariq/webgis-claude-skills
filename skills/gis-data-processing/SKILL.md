---
name: gis-data-processing
description: Design, automate, validate, transform, process, optimize, and test production GIS data pipelines for vector, raster, LiDAR, imagery, and Web GIS applications.
---

# GIS Data Processing

Act as the geospatial data-engineering specialist for production GIS and Web GIS pipelines.

The objective is to turn raw geospatial data into validated, spatially correct, efficient, traceable, and application-ready products.

Support:

- vector data
- raster data
- satellite imagery
- DEM/DSM/DTM
- LiDAR/point clouds
- tabular geospatial data
- survey data
- derived analytical products

Do not process data merely because a tool can process it. Choose the simplest reliable pipeline that satisfies accuracy, scale, reproducibility, and delivery requirements.

# Mandatory preflight

Before changing or creating a processing pipeline:

1. Read:
   - `STATE.md`
   - `TASKS.md`
   - `DECISIONS.md`
   - `SESSION.md`
   - `BLOCKERS.md` when present
2. Inspect repository structure.
3. Identify existing data directories and pipeline scripts.
4. Identify source formats and expected outputs.
5. Identify CRS/SRID requirements.
6. Identify data volumes and expected growth.
7. Identify downstream consumers:
   - PostGIS
   - GeoServer
   - Web GIS
   - APIs
   - object storage
   - analytics
   - GeoAI
8. Inspect existing automation and scheduled jobs.
9. Inspect tests and validation rules.
10. Check git status and recent relevant commits.

Never silently change CRS, geometry semantics, resolution, or data precision.

# Pipeline architecture

Prefer explicit stages:

```
Source
  ↓
Ingestion
  ↓
Inventory
  ↓
Validation
  ↓
Normalization
  ↓
CRS transformation
  ↓
Cleaning
  ↓
Processing
  ↓
Quality assurance
  ↓
Packaging/storage
  ↓
Publishing
  ↓
Verification
```

For large workflows add:

```
Queue
  ↓
Worker
  ↓
Artifact
  ↓
Metadata / provenance
```

Each stage should have a clear input, output, and failure behavior.

# Source inventory

Before processing, record:

- source name
- source type
- provider
- acquisition date
- processing date
- original filename
- format
- CRS
- spatial extent
- resolution
- feature count where applicable
- raster dimensions
- band information
- nodata
- vertical datum where relevant
- coordinate units
- accuracy/quality metadata
- license/usage constraints

Do not discard source metadata unnecessarily.

# Supported vector formats

Common inputs:

- Shapefile
- GeoPackage
- GeoJSON
- KML/KMZ
- CSV
- FlatGeobuf
- File Geodatabase
- PostGIS
- WFS/OGC APIs

Prefer modern, reliable formats for internal pipelines when possible.

Examples:

- GeoPackage for portable structured vector data
- FlatGeobuf for efficient large vector transfer
- PostGIS for authoritative relational spatial storage
- GeoJSON for interchange and small application responses

Do not use Shapefile internally when its limitations create avoidable problems.

# Supported raster formats

Common inputs:

- GeoTIFF
- Cloud Optimized GeoTIFF
- NetCDF
- JPEG/PNG when georeferencing is available
- satellite product formats

For large raster workflows evaluate:

- COG
- tiling
- overviews
- compression
- object storage
- raster services

Do not load massive imagery into memory unnecessarily.

# CRS and coordinate handling

CRS must be explicit throughout the pipeline.

Track:

- source CRS
- intermediate CRS
- storage CRS
- analysis CRS
- output CRS

Use authoritative CRS metadata.

Never infer CRS from coordinate values when reliable metadata is available.

Important distinction:

- `ST_SetSRID` assigns CRS metadata.
- `ST_Transform` changes coordinates.

Equivalent transformation rules apply outside PostGIS using GDAL/PROJ tooling.

Before transformation verify:

- source CRS
- target CRS
- datum
- axis order
- units
- required accuracy

# Vector validation

Validate:

- geometry type
- geometry validity
- CRS
- duplicate IDs
- null geometry
- empty geometry
- self-intersections
- attribute schema
- required fields
- coordinate bounds
- feature count
- encoding
- topology where required

Use appropriate tools such as:

- GDAL/OGR
- GeoPandas
- Shapely
- PostGIS

Do not blindly repair geometry without recording what changed.

# Vector cleaning

Common operations:

- remove duplicates
- normalize attributes
- fix encoding
- standardize field names
- validate geometry
- repair justified geometry errors
- explode multipart features when required
- dissolve when semantically correct
- clip
- merge
- spatial join
- reproject
- simplify
- deduplicate

Preserve source data before destructive operations.

# Attribute normalization

Define schemas explicitly.

For every output field consider:

- name
- type
- nullable
- units
- allowed values
- source field
- transformation rule

Avoid accidental type conversion.

Examples:

- numeric strings should not silently become null
- dates should use consistent formats
- categorical values should be normalized
- units should be explicit

# Spatial joins

For spatial joins define:

- predicate
- target layer
- join layer
- CRS
- duplicate handling
- aggregation rule
- boundary behavior

Common predicates:

- intersects
- within
- contains
- nearest
- touches

Be explicit about boundary semantics.

# Raster processing

For raster workflows define:

- bands
- resolution
- extent
- CRS
- nodata
- data type
- scale/offset
- resampling method
- compression

Choose resampling based on data semantics.

Examples:

- nearest neighbor for categorical classes
- bilinear for continuous surfaces
- cubic when appropriate for visual/continuous data

Never choose resampling solely for visual appearance when analytical correctness matters.

# Raster calculations

Common operations:

- band math
- NDVI
- NDWI
- NDBI
- terrain derivatives
- reclassification
- masking
- clipping
- mosaicking
- resampling
- compositing
- zonal statistics

Record formulas and assumptions.

For scientific/analytical products, store:

- input dataset IDs
- processing parameters
- formula/version
- timestamp
- software version
- output metadata

# Satellite imagery

For satellite workflows record:

- sensor
- platform
- acquisition date
- processing level
- bands
- spatial resolution
- cloud information
- QA bands
- atmospheric correction status
- CRS
- tile/path identifiers when applicable

Do not compare imagery products without checking processing level and resolution.

# DEM / DSM / DTM

Distinguish:

- DEM
- DSM
- DTM

Before processing verify:

- vertical datum
- horizontal CRS
- units
- resolution
- voids
- interpolation method

Possible derived products:

- slope
- aspect
- hillshade
- contours
- watershed
- flow direction
- flow accumulation
- viewshed

Use an appropriate projected CRS for terrain calculations when required by accuracy.

# LiDAR and point clouds

For LiDAR workflows track:

- LAS/LAZ version
- point density
- classification
- return information
- coordinate system
- vertical datum
- acquisition date
- accuracy
- tile index

Possible processing:

- ground classification
- filtering
- thinning
- rasterization
- DSM
- DTM
- canopy metrics
- building extraction
- point-cloud tiling

Do not load massive point clouds entirely into memory.

Use spatial tiling and streaming/chunked processing.

# Large data strategy

For large datasets use:

- tiling
- chunking
- streaming
- spatial indexing
- parallel workers
- intermediate artifacts
- resumable jobs
- object storage
- COG
- vector tiles
- generalized datasets

Avoid:

- loading entire datasets into RAM
- creating huge temporary files without cleanup
- unnecessary format conversions
- repeated full-dataset scans

Estimate resource requirements before processing.

# GDAL / OGR

Use GDAL/OGR for robust command-line geospatial processing where appropriate.

Typical operations:

- translate
- warp
- rasterize
- vector conversion
- clipping
- merging
- tiling
- metadata inspection

Keep command parameters explicit and reproducible.

Avoid shell command construction with untrusted user input.

Validate paths and arguments before execution.

# GeoPandas / Shapely

Use for:

- vector transformations
- spatial joins
- data cleaning
- exploratory processing
- moderate-sized datasets

Do not assume GeoPandas is suitable for every large dataset.

For database-scale workloads prefer PostGIS.

For very large raster workloads prefer GDAL/raster pipelines or specialized infrastructure.

# PostGIS loading

When loading into PostGIS:

1. Validate source.
2. Confirm target schema.
3. Confirm target CRS.
4. Load into staging when appropriate.
5. Validate row/feature counts.
6. Validate geometry.
7. Build/verify indexes.
8. Apply constraints.
9. Promote to production tables.
10. Record provenance.

Prefer staging tables for high-risk imports.

Never replace authoritative production data without validation.

# GeoServer publishing

After processing, publish only verified outputs.

Before publishing verify:

- CRS
- geometry type
- schema
- extent
- data freshness
- spatial index
- permissions
- style
- performance

Do not automatically publish every processed artifact.

# Raster/object storage

For large outputs consider:

- object storage
- COG
- tile pyramids
- raster catalogs
- metadata indexes

Store metadata separately from large binary artifacts when useful.

Use stable artifact identifiers.

# Provenance

Every important derived dataset should be traceable to its inputs.

Record:

- source IDs
- input paths/URIs
- processing software
- software version
- pipeline version
- parameters
- CRS
- timestamp
- operator/job ID
- output ID

For scientific workflows, provenance is part of the data product.

# Reproducibility

Pipelines should be reproducible.

Prefer:

- version-controlled scripts
- pinned dependencies where practical
- explicit parameters
- deterministic operations where possible
- recorded input versions
- containerized environments for complex pipelines

Avoid manual undocumented GIS desktop steps in production pipelines.

# Idempotency

A pipeline should safely handle reruns where practical.

Define:

- input identity
- output identity
- overwrite behavior
- partial failure behavior
- temporary artifacts
- retry behavior

Do not create duplicate datasets every time a job is retried.

# Incremental processing

For recurring data:

- identify changed inputs
- process only required tiles/features
- preserve unchanged outputs
- update indexes/catalogs
- invalidate dependent caches

Avoid full reprocessing when incremental processing is safe and reliable.

# Job orchestration

For long-running processing use jobs/workers.

Track:

- job ID
- status
- progress
- start time
- end time
- worker
- inputs
- parameters
- outputs
- errors

Use retries only for retryable failures.

Do not retry deterministic data-validation failures indefinitely.

# Error handling

Classify failures:

### Input errors

- missing file
- corrupt file
- invalid CRS
- invalid geometry
- unsupported format

### Processing errors

- tool failure
- memory exhaustion
- disk exhaustion
- timeout

### Infrastructure errors

- storage unavailable
- database unavailable
- worker unavailable

### Data-quality errors

- unexpected schema
- missing attributes
- wrong feature count
- suspicious extent

Make errors actionable.

# Quality assurance

Every production pipeline should have measurable QA.

Examples:

- feature count comparison
- raster dimension comparison
- extent comparison
- CRS validation
- geometry validity percentage
- null/duplicate checks
- attribute completeness
- value range checks
- checksum/file integrity
- visual spot checks where appropriate

Define acceptance thresholds.

Do not declare success merely because the processing command exited with code 0.

# Data comparison

For updates compare:

- feature count
- geometry count
- extent
- attribute changes
- area/length changes
- raster statistics
- checksum where appropriate

For scientific products consider:

- mean
- min/max
- standard deviation
- distribution changes

Unexpected changes should trigger review.

# Temporary data

Manage temporary files deliberately.

Use:

- dedicated temporary directories
- unique job IDs
- cleanup policies
- storage quotas

Never allow temporary processing paths to become unbounded.

# Security

Treat uploaded GIS data as untrusted.

Protect against:

- path traversal
- malicious archives
- decompression bombs
- oversized files
- malicious geometry
- command injection
- unsafe GDAL drivers
- SSRF through remote data sources
- resource exhaustion

Sandbox high-risk processing where appropriate.

Never pass untrusted strings directly into shell commands.

# Cost-aware processing

Prefer open-source tools such as:

- GDAL
- PROJ
- GEOS
- PostGIS
- GeoPandas
- Shapely
- PDAL

when they satisfy requirements.

Do not choose cloud processing solely because the dataset is geospatial.

Evaluate:

- compute
- storage
- network transfer
- processing frequency
- operational effort
- parallelism
- managed-service cost

For large workloads, compare local/self-hosted processing against cloud/GEE or managed services using actual data volume and runtime estimates.

# Performance measurement

Measure:

- processing time
- CPU
- memory
- disk
- network
- output size
- feature count
- raster size
- worker utilization

Optimize the bottleneck rather than adding infrastructure blindly.

# Testing

### Unit

Test:

- CRS helpers
- schema normalization
- geometry validation
- formulas
- parameter validation

### Integration

Test:

- source ingestion
- GDAL/OGR commands
- PostGIS loading
- GeoServer publication
- object storage

### Data QA

Test:

- counts
- CRS
- geometry validity
- extents
- attributes
- raster statistics

### Regression

Maintain representative fixtures for known edge cases.

# Definition of done

Before declaring a GIS processing pipeline complete:

- [ ] Source metadata is captured.
- [ ] CRS is explicit and verified.
- [ ] Input validation exists.
- [ ] Geometry/schema validation exists.
- [ ] Processing parameters are reproducible.
- [ ] Large datasets use appropriate chunking/tiling/streaming.
- [ ] Output QA is measurable.
- [ ] Provenance is recorded.
- [ ] Pipeline is rerunnable/idempotent where practical.
- [ ] Temporary data is managed.
- [ ] Security controls exist for untrusted inputs.
- [ ] Performance was measured.
- [ ] Cost/operational trade-offs were considered.
- [ ] Downstream PostGIS/GeoServer/API integration is verified.
- [ ] Tests exist for critical processing logic.
- [ ] Project memory is updated.

# Handoff

After pipeline work:

1. Update `STATE.md`.
2. Update `TASKS.md`.
3. Record durable processing decisions in `DECISIONS.md`.
4. Record data-quality or infrastructure blockers in `BLOCKERS.md`.
5. Update `SESSION.md`.
6. Update `CHANGELOG.md`.
7. Leave an exact next action.

Never claim a dataset or pipeline is production-ready without validating the actual output.
