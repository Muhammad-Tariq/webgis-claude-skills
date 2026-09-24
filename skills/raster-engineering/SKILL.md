# Raster Engineering

## Purpose

Use this skill to design, process, validate, optimize, publish, and operate production raster workflows for Web GIS, remote sensing, terrain analysis, scientific applications, and GeoAI.

The skill covers GeoTIFF, Cloud Optimized GeoTIFF (COG), GDAL, raster tiling, pyramids/overviews, reprojection, resampling, mosaicking, DEM/DSM/DTM, STAC, object storage, raster APIs, map serving, PostGIS Raster where appropriate, and large-scale raster processing.

Raster correctness is governed by CRS, transform, resolution, extent, nodata semantics, data type, scale/offset, temporal metadata, and source provenance. Performance optimization must never silently change scientific meaning.

---

## 1. Mandatory Preflight

Before raster work:

1. Read:
   - `project-memory/STATE.md`
   - `project-memory/TASKS.md`
   - `project-memory/DECISIONS.md`
   - `project-memory/SESSION.md`
   - `project-memory/BLOCKERS.md` when present
2. Inspect existing raster assets and processing pipelines.
3. Identify source formats, CRS, resolution, bands, nodata, scale/offset, temporal coverage, and storage location.
4. Identify the intended consumer:
   - analysis
   - Web GIS visualization
   - download
   - API
   - GeoServer
   - tile service
   - GeoAI
5. Establish representative test data before optimizing.
6. Check existing tooling before introducing a new raster stack.

If project memory conflicts with actual raster metadata or verified output, trust the data/tooling and repair memory.

---

## 2. Raster Data Inventory

Every production raster should have an inventory containing, where applicable:

- dataset/source name
- source provider
- acquisition date/time
- product/processing level
- file format
- CRS/EPSG
- affine transform
- extent
- width/height
- pixel size
- band count
- band names
- data types
- nodata value
- scale/offset
- units
- vertical datum for elevation
- temporal reference
- cloud/quality metadata
- compression
- overview levels
- provenance
- license/usage restrictions

Never infer critical metadata solely from filenames.

---

## 3. Raster Formats

Choose the format according to workload.

### GeoTIFF

Use when:

- broad desktop/GIS compatibility is required
- processing workflows need a mature raster container
- local analytical workflows dominate

### Cloud Optimized GeoTIFF

Prefer COG when:

- rasters are stored in object storage
- partial/range reads are useful
- Web/cloud access is required
- tiled, multiresolution access is beneficial

Validate actual COG structure rather than assuming a .tif is cloud optimized.

### Zarr / chunked arrays

Consider for:

- multidimensional scientific data
- large time-series arrays
- analysis-heavy cloud workflows

Choose only when the ecosystem and access pattern justify it.

### PostGIS Raster

Use selectively when raster data benefits from database integration and spatial SQL.

Do not put every large raster into PostgreSQL by default. Object storage plus specialized raster serving/processing may be more appropriate.

---

## 4. GDAL-Centered Engineering

GDAL is a primary interoperability and processing tool.

Use it for tasks such as:

- inspection
- translation
- reprojection
- warping
- mosaicking
- clipping
- format conversion
- overviews
- tiling
- raster statistics
- metadata operations

Common tooling patterns may include:

- `gdalinfo`
- `gdal_translate`
- `gdalwarp`
- `gdalbuildvrt`
- `gdaladdo`
- `gdal_calc.py`
- `gdal_rasterize`
- `gdal_merge.py`

Use version-compatible commands and verify output metadata.

Do not rely on a command's exit code alone for scientific correctness.

---

## 5. Raster Metadata and Georeferencing

Before processing, verify:

- CRS
- geotransform
- pixel dimensions
- pixel size
- extent
- rotation/skew
- nodata
- band metadata
- scale/offset
- units
- vertical reference where relevant

A raster can open successfully while still being spatially wrong.

For derived outputs, compare:

- extent
- transform
- resolution
- CRS
- dimensions
- nodata
- expected value range

---

## 6. CRS and Reprojection

Define:

- source CRS
- processing CRS
- analysis CRS
- display CRS
- export CRS

Use reprojection only when required.

Choose a projected CRS for metric analysis when appropriate.

When warping:

- choose resampling based on data semantics
- define target resolution deliberately
- define alignment
- define nodata
- validate extent
- avoid repeated reprojection

### Resampling guidance

For categorical rasters:

- nearest-neighbor is often appropriate

For continuous rasters:

- bilinear/cubic or other suitable methods may be appropriate

For aggregation/downsampling:

- average/sum/mode may be appropriate depending on semantics

Never change resampling method without considering its effect on the scientific quantity.

---

## 7. Raster Alignment

Before pixel-wise raster operations, verify:

- CRS
- pixel size
- origin/grid alignment
- extent
- dimensions
- nodata semantics
- band structure

Misaligned grids can produce scientifically incorrect calculations even when rasters visually overlap.

Use explicit warping/alignment rather than relying on implicit library behavior.

---

## 8. Nodata and Masks

Treat nodata as data semantics, not merely a numeric value.

Distinguish:

- valid zero
- nodata
- masked pixel
- cloud
- cloud shadow
- saturated pixel
- missing observation
- outside-AOI pixel

When combining rasters:

- propagate masks intentionally
- avoid nodata arithmetic
- validate output masks
- preserve quality flags where required

Do not replace nodata with zero unless zero has the intended semantic meaning.

---

## 9. Data Types, Scale, and Precision

Understand:

- UInt8/UInt16
- Int16/Int32
- Float32/Float64
- bit-packed quality bands
- scale/offset metadata

Before converting types:

- inspect value range
- determine required precision
- detect overflow
- detect truncation
- preserve units

For scientific indices and continuous analysis, avoid unnecessary integer conversion.

---

## 10. Raster Compression

Choose compression based on data characteristics and access pattern.

Consider:

- DEFLATE
- LZW
- ZSTD where supported
- JPEG for appropriate lossy visual imagery
- predictor settings
- tile size

For scientific rasters, lossy compression requires explicit justification.

Benchmark compression ratio and read performance rather than selecting solely by habit.

---

## 11. Tiling and Block Layout

Use tiled storage for workloads involving partial reads.

Consider:

- block width/height
- internal tiling
- access window
- expected tile size
- compression
- overview structure

Tile sizes should match the serving/processing pattern.

Do not optimize block size without measuring actual read/write workloads.

---

## 12. Overviews and Pyramids

Large rasters should have appropriate overviews when they will be viewed at smaller scales.

Choose:

- overview levels
- resampling method
- storage/compression
- update strategy

Overviews reduce unnecessary full-resolution reads.

Validate that overview levels are actually present and readable by the serving stack.

---

## 13. Mosaicking

For mosaics:

1. inventory source scenes
2. verify CRS/resolution
3. normalize nodata
4. define pixel alignment
5. define overlap priority/blending
6. build a virtual mosaic when appropriate
7. materialize only when needed
8. generate overviews
9. validate seams and metadata

Prefer VRT/virtual mosaics when they avoid unnecessary duplication and the downstream stack supports them.

---

## 14. DEM / DSM / DTM Engineering

Distinguish:

- DEM as a general elevation surface
- DSM including above-ground objects
- DTM representing terrain/bare earth

Document:

- vertical datum
- horizontal CRS
- vertical units
- source resolution
- void handling

Derived products may include:

- hillshade
- slope
- aspect
- curvature
- contour
- flow direction
- flow accumulation
- watershed/catchment
- terrain ruggedness

Validate terrain outputs against known elevation behavior and edge cases.

---

## 15. Satellite Raster Workflows

For Sentinel, Landsat, MODIS/VIIRS, and similar products:

- preserve acquisition metadata
- apply sensor/product-specific scaling
- apply quality/cloud/shadow masks
- select required bands
- harmonize resolution only when justified
- align temporal observations
- preserve source provenance

For indices such as NDVI/NDWI/NDBI/EVI/SAVI:

- document band mapping
- document scaling
- document masking
- document formula/version
- validate expected value ranges

Do not mix incompatible product levels or band definitions without explicit harmonization.

---

## 16. Raster Algebra and Derived Products

For pixel-wise calculations:

1. verify alignment
2. verify units
3. verify masks
4. define numerical behavior
5. calculate
6. validate value range
7. write metadata/provenance

Watch for:

- divide-by-zero
- overflow
- NaN/Inf
- nodata propagation
- mixed units
- integer truncation

Derived products should state the input datasets and formula.

---

## 17. STAC and Raster Cataloging

Use STAC when searchable catalog metadata is valuable.

A useful STAC item can expose:

- geometry
- temporal metadata
- asset URLs
- media types
- CRS
- resolution
- band information
- processing metadata
- cloud/quality information

Keep catalog metadata consistent with actual raster metadata.

STAC is a catalog/API convention, not a replacement for raster storage.

---

## 18. Object Storage

For large raster collections, object storage is often preferable to application-local disk.

Design for:

- stable asset identifiers
- immutable/versioned objects where appropriate
- range requests
- lifecycle policies
- access controls
- encryption
- backups
- metadata/catalog integration

Separate:

- raw data
- intermediate products
- validated products
- published products
- temporary processing artifacts

Do not mix temporary and authoritative data without lifecycle rules.

---

## 19. Raster Serving Architecture

Choose the serving pattern based on requirements.

Possible options:

- GeoServer WMS/WMTS
- COG + range requests
- dynamic tile services
- raster tile APIs
- STAC + COG
- specialized raster APIs
- pre-generated tiles

For each layer define:

- source
- CRS
- visualization style
- min/max scaling
- nodata behavior
- tile strategy
- cache strategy
- access policy

Do not expose raw high-resolution rasters to every client when tiled or windowed delivery is sufficient.

---

## 20. Web GIS Raster Visualization

Optimize the browser for:

- tiled delivery
- appropriate display resolution
- progressive loading
- color ramps
- transparency
- legends
- min/max controls
- temporal sliders
- layer opacity
- nodata visualization

Separate:

- visualization stretch
- analytical values

A display contrast adjustment must not alter the underlying scientific dataset.

---

## 21. Raster API Design

A raster API should explicitly define:

- dataset identifier
- spatial extent
- CRS
- resolution/scale
- time
- bands
- resampling
- output format
- nodata behavior
- authentication
- limits

For large requests, prefer asynchronous jobs or bounded windows.

Never permit arbitrary unbounded raster extraction from protected datasets.

---

## 22. Processing Pipelines

Use a reproducible pipeline:

`Source → Inventory → Validate → Normalize → Align → Process → QA → Package → Publish → Verify`

Pipeline properties should include:

- idempotency
- deterministic configuration
- versioned code
- versioned inputs
- explicit parameters
- retry behavior
- intermediate artifact management
- provenance
- logs
- QA reports

A failed job should not silently publish partial output as authoritative.

---

## 23. Large-Scale Processing

For large raster workloads:

- process by tiles/windows
- avoid loading entire rasters into memory
- use streaming/windowed reads
- use chunking
- use multiprocessing/workers where appropriate
- use cloud-scale processing when justified
- exploit overviews for low-resolution work
- avoid repeated full-scene scans

Choose memory strategy based on raster dimensions and data type.

---

## 24. Raster + PostGIS

Use PostGIS for:

- AOI management
- vector/raster relationships
- metadata
- spatial indexing
- analytical queries

Use specialized raster/object storage when:

- rasters are very large
- object access is dominant
- cloud-native delivery is required

Do not duplicate huge raster datasets in both PostgreSQL and object storage without a clear reason.

---

## 25. Raster + GeoAI

For GeoAI pipelines:

- tile inference inputs consistently
- preserve CRS/geotransform
- maintain nodata/masks
- define overlap strategy
- handle edge effects
- merge predictions correctly
- preserve confidence/probability bands
- version model and preprocessing
- validate spatial alignment

For segmentation/detection outputs, ensure prediction geometry maps back to the source raster correctly.

---

## 26. Raster Quality Assurance

Automated QA should inspect:

- CRS
- dimensions
- extent
- transform
- resolution
- band count
- dtype
- nodata
- value range
- NaN/Inf
- mask percentage
- expected coverage
- file integrity
- overviews
- compression
- COG structure when required

Visual QA should inspect representative areas for:

- seams
- reprojection artifacts
- resampling artifacts
- nodata boundaries
- unexpected clipping
- incorrect color/stretch
- alignment problems

---

## 27. Performance and Cost

Measure:

- processing time
- memory
- storage size
- compression ratio
- read latency
- tile latency
- cache hit rate
- egress
- worker utilization

Prefer free/open-source tooling when it meets requirements.

Avoid expensive repeated processing by using:

- VRTs
- cached intermediates
- derived products
- overviews
- object storage
- incremental updates
- server-side processing

Paid raster providers or hosted processing should be justified by coverage, reliability, scale, or operational requirements.

---

## 28. Security

Protect raster infrastructure against:

- unauthorized downloads
- path traversal
- malicious file uploads
- decompression/resource exhaustion
- untrusted GDAL inputs
- SSRF through remote raster URLs
- public bucket exposure
- leaked signed URLs
- excessive extraction requests

Use:

- allowlisted formats
- file-size/pixel limits
- isolated processing workers
- access controls
- signed/short-lived URLs where appropriate
- resource quotas
- audit logging

Never process arbitrary remote URLs with privileged raster tooling without validation.

---

## 29. Testing

Test:

### Metadata

- CRS
- transform
- resolution
- dimensions
- bands
- nodata
- scale/offset

### Processing

- reprojection
- resampling
- mosaicking
- clipping
- raster algebra
- nodata propagation
- overviews

### Scientific

- expected value ranges
- known index values
- elevation sanity
- alignment
- temporal consistency

### Serving

- tile requests
- window reads
- API limits
- GeoServer responses
- authorization

### Resilience

- corrupt input
- missing band
- invalid CRS
- oversized raster
- worker failure
- interrupted processing

---

## 30. Raster Definition of Done

A raster feature/pipeline is complete when:

- source metadata is known
- CRS/transform/resolution are verified
- nodata semantics are explicit
- data type and units are correct
- processing is reproducible
- output metadata is validated
- scientific assumptions are documented
- QA passes
- serving/storage strategy matches scale
- performance is measured
- security limits are applied
- provenance is preserved
- representative visualization has been checked
- project memory is updated

---

## 31. Project-Memory Handoff

Before stopping:

### STATE.md
Record:
- raster phase
- source/output dataset
- last verified processing step
- metadata validation
- exact next action

### TASKS.md
Record:
- ingestion
- processing
- QA
- publishing
- optimization status

### DECISIONS.md
Record durable choices such as:
- GeoTIFF vs COG
- compression
- tile/block size
- overview strategy
- CRS
- resampling
- object storage
- STAC/catalog strategy
- raster serving architecture

### SESSION.md
Record:
- commands/workflows executed
- input/output assets
- measurements
- QA results
- failures
- exact resume point

### BLOCKERS.md
Record:
- missing imagery
- storage constraints
- GDAL/tool compatibility
- provider limitations
- unresolved metadata/scientific issues

### CHANGELOG.md
Record meaningful raster pipeline and serving changes.

Never claim a raster is production-ready until metadata, spatial correctness, QA, and serving behavior have been verified.
