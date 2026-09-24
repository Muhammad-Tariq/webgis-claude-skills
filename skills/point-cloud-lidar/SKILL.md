# Point Cloud & LiDAR Engineering

## Purpose

Use this skill to design, process, validate, optimize, publish, and operate production LiDAR and point-cloud workflows for Web GIS, surveying, terrain modeling, remote sensing, 3D visualization, and GeoAI.

The skill covers LAS/LAZ, COPC, PDAL, point-cloud indexing, classification, ground extraction, DTM/DSM generation, point-cloud QA, tiling, storage, 3D delivery, and browser visualization.

Point-cloud correctness depends on coordinate reference systems, vertical reference, point attributes, classification semantics, density, acquisition metadata, and processing provenance. Never treat a visually plausible point cloud as automatically correct.

---

## 1. Mandatory Preflight

Before LiDAR work:

1. Read:
   - `project-memory/STATE.md`
   - `project-memory/TASKS.md`
   - `project-memory/DECISIONS.md`
   - `project-memory/SESSION.md`
   - `project-memory/BLOCKERS.md` when present
2. Inspect existing point-cloud assets and processing pipelines.
3. Identify source format, CRS, vertical datum, point density, attributes, classification, acquisition metadata, and intended output.
4. Establish representative tiles/areas for testing.
5. Identify whether the workflow is:
   - survey/QA
   - terrain extraction
   - visualization
   - change detection
   - volumetrics
   - object analysis
   - GeoAI
6. Verify existing tools before adding new infrastructure.

If memory conflicts with actual point-cloud metadata or verified output, trust the verified data/tool output and repair project memory.

---

## 2. Point-Cloud Inventory

Record, where available:

- source/provider
- acquisition date/time
- sensor/platform
- LAS/LAZ/COPC version
- point count
- point density
- point spacing
- CRS/EPSG
- horizontal datum
- vertical datum
- units
- extent/bounds
- return number
- number of returns
- classification
- intensity
- RGB
- GPS time
- scan angle
- scan direction
- flight line/source ID
- overlap
- processing software/version
- accuracy metadata
- license/usage restrictions

Never infer vertical datum or units from filename conventions alone.

---

## 3. LAS / LAZ / COPC

### LAS

Use for broad interoperability and standards-compatible point-cloud exchange.

### LAZ

Use when lossless point-cloud compression materially reduces storage and transfer.

### COPC

Consider COPC when:

- cloud/object storage is used
- spatially selective access is important
- large point clouds must be streamed progressively
- hierarchical spatial indexing improves access

Verify actual COPC structure and metadata rather than assuming any LAZ is COPC.

---

## 4. PDAL-Centered Processing

PDAL is a primary processing framework for production point-cloud workflows.

Typical operations include:

- metadata inspection
- reprojection
- filtering
- classification
- ground extraction
- thinning/decimation
- outlier removal
- cropping
- merging
- tiling
- rasterization
- format conversion

Use version-compatible pipelines and validate the resulting point counts, bounds, classifications, and coordinate metadata.

A successful PDAL exit code does not prove scientific or survey correctness.

---

## 5. Coordinate and Vertical Reference

Track separately:

- horizontal CRS
- vertical datum
- vertical units
- ellipsoidal vs orthometric height
- geoid model where relevant
- display CRS
- analysis CRS
- output CRS

A horizontal reprojection does not automatically solve a vertical datum transformation.

Before terrain analysis, verify that elevations are comparable.

Never silently mix datasets with different vertical references.

---

## 6. Point Attributes and Semantics

Understand each attribute before using it.

Common attributes:

- XYZ
- intensity
- return number
- number of returns
- classification
- RGB
- GPS time
- scan angle
- user data
- point source ID

Classification codes must be interpreted according to the relevant standard/source specification.

Do not assume class numbers mean the same thing across arbitrary datasets without checking metadata.

---

## 7. Classification

Common classes may include:

- unclassified
- ground
- vegetation
- buildings
- water
- noise/outliers

Classification workflows should:

1. inspect existing classes
2. preserve authoritative classes
3. define the target class
4. choose algorithm/parameters
5. run on representative tiles
6. inspect errors
7. validate counts/distribution
8. preserve provenance

Never overwrite original classification without retaining a recoverable source or derived version.

---

## 8. Ground Classification

Ground extraction is foundational for terrain products.

Consider:

- terrain type
- point density
- vegetation
- buildings
- cliffs/steep slopes
- urban structures
- algorithm
- filter window/parameters

Validate:

- missed ground points
- vegetation misclassified as ground
- building edges
- bridges
- steep terrain
- water surfaces

Ground classification errors propagate directly into DTM and derived terrain products.

---

## 9. DTM / DSM / CHM

### DTM

Generate terrain elevation from appropriate ground-classified points.

### DSM

Represent the surface including buildings, vegetation, and other above-ground objects.

### CHM

Can represent canopy height, commonly derived from DSM minus a suitable terrain surface.

For each product document:

- source classes
- interpolation/rasterization method
- resolution
- void handling
- vertical units
- CRS/datum
- smoothing
- output format

Do not call a DSM a DTM merely because both are elevation rasters.

---

## 10. Point Density and Coverage

Measure:

- points per square meter
- points per square foot where required
- point spacing
- density variation
- gaps
- overlap
- edge effects

For survey/engineering applications, compare observed density and coverage with project specifications.

Do not assume nominal flight density equals delivered density.

---

## 11. Tiling Strategy

Large point clouds should be spatially tiled when processing or delivery benefits from it.

Define:

- tile size
- overlap/buffer
- indexing scheme
- naming convention
- CRS
- attributes retained
- compression
- source lineage

Avoid tile seams by using appropriate overlap during neighborhood-based processing.

For derived products, document whether edge buffers were used and how duplicate/overlap points were handled.

---

## 12. Point-Cloud Indexing

Use spatial indexing appropriate to the delivery/processing stack.

Possible approaches:

- COPC hierarchy
- spatial tile index
- database spatial index
- octree/hierarchy
- catalog index

Indexing should support:

- spatial filtering
- bounding-box requests
- level-of-detail access
- progressive loading

Do not scan an entire multi-billion-point dataset for every interactive map request.

---

## 13. Outlier and Noise Handling

Identify:

- isolated points
- extreme elevation outliers
- sensor noise
- duplicate points
- invalid coordinates
- scan artifacts

Choose filters based on sensor and survey characteristics.

Never remove unusual points automatically when they may represent legitimate structures or terrain.

Record filter parameters and removed-point statistics.

---

## 14. LiDAR QA / QC

Automated QA should inspect:

- CRS
- vertical datum
- bounds
- point count
- density
- class distribution
- coordinate validity
- elevation range
- intensity range
- return statistics
- duplicate/near-duplicate behavior
- tile overlap
- gaps
- metadata completeness

Visual QA should inspect representative areas for:

- striping
- flight-line artifacts
- holes
- vegetation/ground confusion
- building classification
- terrain discontinuities
- tile seams
- spikes/noise

For survey-grade work, compare against independent checkpoints/control where available.

---

## 15. Strip and Flight-Line Quality

Where acquisition metadata permits, inspect:

- flight-line alignment
- overlap
- relative elevation differences
- striping
- systematic offsets
- scan-angle effects

If strip adjustment or calibration is required, preserve the original dataset and record the adjustment workflow.

Do not hide systematic acquisition errors with aggressive smoothing.

---

## 16. Rasterization

When converting points to rasters:

- define target resolution
- define aggregation/interpolation
- define class filters
- define nodata
- preserve CRS/vertical units
- handle tile boundaries
- validate output statistics

Common products:

- DTM
- DSM
- intensity raster
- density raster
- height-normalized surfaces
- canopy metrics

Choose resolution based on point density and analytical purpose rather than arbitrary pixel size.

---

## 17. Web GIS / 3D Delivery

For browser visualization, distinguish between:

- point-cloud inspection
- terrain visualization
- 3D buildings
- measurement
- analytical output

Possible delivery technologies include:

- COPC
- 3D Tiles
- Potree-style point-cloud streaming
- CesiumJS
- MapLibre/OpenLayers for derived 2D products

Choose the delivery format based on browser support, dataset scale, styling needs, interaction model, and infrastructure.

Do not send raw multi-million-point datasets as a single API response.

---

## 18. 3D Visualization Performance

For interactive point clouds:

- use hierarchical LOD
- stream visible regions
- cap visible point budgets
- use progressive loading
- reduce point attributes when unnecessary
- use spatial culling
- avoid loading the whole dataset
- monitor browser GPU/CPU/memory

For terrain:

- use appropriate terrain tiles/LOD
- simplify where display scale allows
- separate visualization from high-resolution analytical data

---

## 19. LiDAR + Raster Workflows

A common production pipeline is:

`Point Cloud → QA → Classification → Ground/Surface Extraction → Raster Product → Tile/Serve → Web GIS`

Keep point-cloud and raster products linked by provenance.

When generating DTM/DSM:

- preserve source tile IDs
- preserve processing parameters
- record interpolation/rasterization method
- validate seams and elevation continuity

---

## 20. LiDAR + GeoAI

For GeoAI:

- normalize heights when required
- preserve spatial coordinates
- create reproducible training tiles
- avoid spatial leakage
- define object/point labels clearly
- account for point density variation
- preserve point attributes used by the model
- version preprocessing and model configuration

Potential tasks:

- building detection
- tree detection
- powerline extraction
- pole detection
- ground classification
- object segmentation
- change detection
- infrastructure inspection

Never train or infer across mixed coordinate/vertical references without explicit normalization.

---

## 21. Change Detection

For multi-temporal point clouds:

1. harmonize CRS and vertical datum
2. validate acquisition quality
3. align datasets
4. quantify registration uncertainty
5. define comparison unit
6. calculate elevation/geometry differences
7. filter noise
8. determine meaningful change threshold
9. validate against known changes

Do not interpret small elevation differences as real change when they are within registration or measurement uncertainty.

---

## 22. Volumetric Analysis

For stockpiles, excavation, fill, and earthworks:

- define base/reference surface
- define comparison surface
- align CRS/vertical datum
- define AOI
- calculate cut/fill
- report units
- quantify uncertainty
- preserve input surfaces

Avoid volume calculations from misaligned surfaces or incompatible vertical datums.

---

## 23. Storage and Object Management

For large point-cloud collections, consider object storage with:

- immutable source assets
- derived products
- tile/index metadata
- lifecycle rules
- access controls
- versioning where required
- backup strategy

Separate:

- raw point clouds
- normalized point clouds
- classified point clouds
- derived terrain products
- temporary processing outputs

Do not overwrite authoritative source data during processing.

---

## 24. Processing Architecture

Choose processing placement by scale:

### Local/desktop

Suitable for:

- small datasets
- exploratory QA
- survey inspection

### Worker/server

Suitable for:

- repeatable ETL
- scheduled processing
- medium/large datasets
- API-triggered jobs

### Distributed/cloud

Suitable when:

- datasets are very large
- many tiles process independently
- throughput requirements justify orchestration

Do not introduce distributed infrastructure when a single well-designed worker can handle the workload reliably.

---

## 25. Pipeline Design

Use a reproducible flow:

`Ingest → Inventory → Validate → Normalize → Tile → Classify → Derive → QA → Package → Publish → Verify`

Pipeline properties:

- deterministic configuration
- idempotency
- versioned code
- versioned source
- explicit parameters
- retry behavior
- intermediate artifact handling
- logs
- QA reports
- provenance

A failed tile should not silently produce a partial authoritative dataset.

---

## 26. Performance

Measure:

- points processed per second
- points per tile
- memory usage
- disk I/O
- CPU utilization
- processing duration
- output size
- query latency
- point-cloud streaming latency
- browser memory/GPU use

Optimize with:

- spatial tiling
- indexing
- LAZ/COPC
- streaming/windowed processing
- LOD
- parallel workers
- attribute reduction
- caching

Do not trade away classification or terrain accuracy merely to increase throughput.

---

## 27. Security

Protect point-cloud infrastructure against:

- unauthorized survey-data downloads
- malicious uploads
- oversized/decompression attacks
- path traversal
- SSRF through remote point-cloud URLs
- public object-storage exposure
- excessive extraction requests
- unsafe processing workers

Apply:

- format allowlists
- file-size/point-count limits
- isolated workers
- access control
- signed/short-lived URLs where appropriate
- quotas
- audit logging

Survey and infrastructure point clouds may contain sensitive physical information; expose only what the user is authorized to access.

---

## 28. Cost-Aware Policy

Prefer free/open-source tooling when it meets requirements.

Common open-source choices may include:

- PDAL
- GDAL
- PostgreSQL/PostGIS
- open-source 3D/Web GIS libraries

Evaluate paid services based on:

- processing scale
- hosted infrastructure
- SLA
- storage
- bandwidth/egress
- operational burden
- specialized capabilities

Record durable cost/licensing decisions in project memory.

---

## 29. Testing

Test:

### Data

- LAS/LAZ parsing
- COPC structure
- CRS
- vertical datum
- bounds
- point counts
- attributes
- classifications

### Processing

- reprojection
- classification
- ground extraction
- tiling
- filtering
- rasterization
- DTM/DSM generation

### QA

- density
- gaps
- seams
- elevation ranges
- class distributions
- known checkpoints

### Serving

- bounding-box requests
- progressive loading
- LOD
- access control
- large-area behavior

### Resilience

- corrupt files
- missing metadata
- oversized inputs
- worker failure
- interrupted processing
- partial tile failure

---

## 30. Definition of Done

A point-cloud/LiDAR feature is complete when:

- source metadata is known
- horizontal and vertical references are verified
- point attributes are understood
- density/coverage are measured
- processing is reproducible
- classifications are validated
- derived surfaces are validated
- QA/QC passes
- storage/indexing strategy matches scale
- Web GIS delivery is tested where applicable
- performance is measured
- security limits are enforced
- provenance is preserved
- project memory is updated

---

## 31. Project-Memory Handoff

Before stopping:

### STATE.md
Record:
- LiDAR phase
- source/output assets
- last verified processing step
- QA status
- exact next action

### TASKS.md
Record:
- ingestion
- classification
- terrain derivation
- QA
- publishing
- optimization

### DECISIONS.md
Record:
- LAS/LAZ/COPC
- PDAL pipeline
- CRS/vertical datum
- tile size
- classification method
- rasterization method
- 3D delivery strategy
- storage/indexing architecture

### SESSION.md
Record:
- datasets processed
- pipeline/configuration used
- measurements
- QA findings
- failed approaches
- exact resume point

### BLOCKERS.md
Record:
- missing control data
- vertical datum uncertainty
- processing limits
- storage constraints
- visualization limitations

### CHANGELOG.md
Record meaningful LiDAR/point-cloud processing and delivery changes.

Never claim LiDAR or survey data is production-ready until coordinate references, density, classification, QA, and representative outputs have been verified.
