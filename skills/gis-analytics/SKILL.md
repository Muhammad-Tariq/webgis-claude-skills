# GIS Analytics

## Purpose

Use this skill to design, implement, validate, and explain analytical capabilities in Web GIS applications.

The skill covers deterministic spatial analysis, spatial statistics, suitability and scoring models, proximity and overlay analysis, temporal analysis, zonal statistics, clustering, network-aware analysis, raster/vector analytics, uncertainty, and decision-ready visualization.

Analytical outputs must be reproducible, spatially correct, scientifically defensible where applicable, and explicit about CRS, units, assumptions, data quality, and uncertainty.

---

## 1. Mandatory Preflight

Before implementing or changing GIS analytics:

1. Read:
   - `project-memory/STATE.md`
   - `project-memory/TASKS.md`
   - `project-memory/DECISIONS.md`
   - `project-memory/SESSION.md`
   - `project-memory/BLOCKERS.md` when present
2. Inspect the existing data model and spatial API.
3. Identify source datasets, geometry types, CRS/SRID, temporal coverage, and resolution.
4. Define the analytical question before selecting an algorithm.
5. Establish expected inputs, outputs, units, and validation method.
6. Check whether an equivalent analysis already exists before creating a duplicate implementation.

If documentation conflicts with verified code/data, trust the verified implementation and repair project memory.

---

## 2. Start With the Analytical Question

Translate vague requests into explicit analytical questions.

Examples:

- Which parcels are within 500 m of a road?
- Which locations satisfy all suitability criteria?
- Where are drought-vulnerable agricultural areas concentrated?
- Which administrative zones have the highest NDVI change?
- Where are statistically significant hotspots?
- Which features changed between two dates?
- Which candidate sites minimize travel distance while satisfying constraints?

Document:

- unit of analysis
- input datasets
- spatial relationships
- temporal window
- output geometry
- metrics
- thresholds
- assumptions
- uncertainty

Do not select an algorithm simply because it is familiar.

---

## 3. Analytical Unit and Geometry Semantics

Choose the correct prediction/analysis unit:

- point
- line
- polygon
- grid cell
- raster pixel
- administrative zone
- parcel
- road segment
- catchment
- tile
- temporal observation

Clarify whether the output represents:

- original features
- derived features
- aggregations
- continuous surfaces
- classes
- scores
- rankings
- probabilities

Preserve feature identity when downstream users need traceability.

---

## 4. CRS, Units, and Measurement

CRS is part of analytical correctness.

Before distance, area, buffering, density, or geometry operations:

- identify source CRS
- identify storage CRS
- identify analysis CRS
- identify display CRS
- choose a suitable projected CRS when planar measurement is required
- use geodesic methods when appropriate
- document units

Never assume longitude/latitude degrees are meters.

Verify:

- area units
- distance units
- raster cell size
- pixel area
- scale
- resolution
- coordinate axis order where relevant

Round results only at presentation boundaries unless analytical rounding is explicitly required.

---

## 5. Core Vector Analysis

Support common operations:

- buffer
- intersection
- union
- difference
- dissolve
- clip
- split
- merge
- spatial join
- nearest feature
- containment
- overlap
- distance
- line/polygon intersections
- point-in-polygon

For each operation:

- validate geometry
- preserve CRS
- define behavior for invalid/empty geometries
- measure computational cost
- document edge cases

Avoid unnecessary geometry explosion.

---

## 6. Proximity and Distance Analysis

Common workflows:

### Buffer

Use when the question is threshold-based proximity.

Example:

`ST_Buffer(roads, 500m)`

Confirm whether the buffer is:

- planar
- geodesic
- dissolved
- per-feature
- generalized

### Nearest feature

Use indexed nearest-neighbor strategies where supported.

Return:

- nearest feature ID
- distance
- units
- optional geometry/route

### Distance matrix

For many-to-many distances, avoid naive O(n²) computation when spatial filtering or network constraints can reduce the candidate set.

---

## 7. Overlay and Spatial Join

For overlay analysis:

1. validate geometries
2. align CRS
3. reduce candidate pairs with spatial indexes
4. perform the exact spatial predicate
5. calculate required metrics
6. preserve source identifiers
7. validate output counts/areas

For spatial joins, explicitly define:

- intersects
- contains
- within
- touches
- overlaps
- nearest
- distance threshold

Do not silently change predicates because they are faster.

---

## 8. Spatial Statistics

Use appropriate methods for the question.

Possible analyses:

- mean/median spatial summaries
- density
- nearest-neighbor analysis
- Moran's I
- Local Moran's I
- Getis-Ord Gi*
- hotspot/coldspot analysis
- kernel density estimation
- spatial autocorrelation
- geographically weighted approaches where justified

Document:

- null hypothesis
- neighborhood definition
- distance/weight matrix
- significance threshold
- multiple-testing considerations
- edge effects
- interpretation limitations

Do not call an area a statistically significant hotspot without defining the method and significance criteria.

---

## 9. Suitability and Multi-Criteria Analysis

For suitability models:

1. define objective
2. define criteria
3. normalize criteria
4. define weights
5. define constraints
6. combine criteria
7. classify/threshold results
8. validate
9. expose assumptions to users

A common weighted model is:

`S = Σ(w_i × x_i)`

where:

- `x_i` is normalized criterion value
- `w_i` is its weight
- weights should be documented and typically normalized

Separate:

- hard constraints
- soft preferences
- derived scores

Do not present a subjective score as an objective fact.

---

## 10. Sensitivity Analysis

For weighted or threshold-based models, test whether conclusions change when assumptions change.

Vary:

- criterion weights
- thresholds
- normalization methods
- exclusion criteria
- spatial resolution
- temporal window

Report whether outputs are:

- stable
- moderately sensitive
- highly sensitive

Sensitivity analysis is especially important for site selection, risk scoring, vulnerability indices, and composite indicators.

---

## 11. Raster Analytics

Common raster operations:

- zonal statistics
- reclassification
- focal statistics
- neighborhood analysis
- raster algebra
- slope/aspect
- terrain derivatives
- distance surfaces
- suitability surfaces
- change detection
- anomaly analysis

Validate:

- CRS
- resolution
- alignment
- extent
- nodata
- data type
- scale/offset
- temporal compatibility

For raster-to-raster math, confirm that grids are aligned before calculation.

---

## 12. Zonal Statistics

For polygon summaries over raster data, explicitly define:

- zones
- raster
- statistic
- nodata behavior
- pixel inclusion rule
- resolution
- aggregation method

Possible statistics:

- count
- sum
- mean
- median
- minimum
- maximum
- standard deviation
- percentiles

Document whether partial pixels are included and how weighting is handled.

---

## 13. Temporal and Change Analysis

For time-series analysis:

- define baseline
- define comparison period
- align temporal resolution
- account for missing observations
- apply consistent preprocessing
- preserve acquisition metadata
- distinguish seasonal variation from actual change

Common methods:

- difference
- percentage change
- anomaly
- trend
- rolling statistics
- change-point detection
- pre/post comparison
- temporal composites

For satellite data, keep cloud/shadow and quality masking consistent across periods.

---

## 14. Land-Cover and Classification Analytics

For classification workflows:

- define classes
- create representative training data
- prevent spatial/temporal leakage
- establish train/validation/test separation
- select appropriate features
- establish a baseline model
- evaluate with a confusion matrix
- report class-specific metrics

Useful metrics:

- overall accuracy
- precision
- recall
- F1
- IoU
- producer's accuracy
- user's accuracy
- balanced accuracy

Do not rely on overall accuracy alone for imbalanced classes.

---

## 15. Clustering and Pattern Detection

For clustering:

- define the objective
- choose features
- normalize where necessary
- choose spatial/non-spatial distance
- determine cluster count or density parameters
- validate cluster stability

Possible approaches:

- DBSCAN/HDBSCAN
- k-means
- hierarchical clustering
- spatially constrained clustering

A visual cluster is not automatically a statistically meaningful spatial cluster.

---

## 16. Network and Accessibility Analysis

When analysis depends on travel rather than Euclidean distance, use a network model.

Examples:

- nearest hospital by road travel
- service area
- drive-time isochrone
- shortest path
- accessibility index
- road connectivity

Distinguish:

- Euclidean distance
- geodesic distance
- network distance
- travel time

Do not substitute straight-line distance for travel distance when the decision depends on actual network movement.

---

## 17. Analytical Architecture

Choose where computation belongs.

### Browser

Use for:

- small interactive calculations
- display-only measurements
- lightweight filtering
- UI previews

### API

Use for:

- business-specific analysis
- controlled spatial operations
- reusable analytical endpoints
- authorization-aware computation

### PostGIS

Use for:

- indexed spatial joins
- vector overlays
- proximity
- aggregations
- spatial SQL
- transactional analytical queries

### Raster/processing workers

Use for:

- large raster operations
- heavy ETL
- batch analysis
- long-running computation

### GEE

Use when:

- analysis depends on large Earth-observation archives
- cloud-scale remote sensing processing is appropriate

### GeoAI/GPU

Use for:

- inference
- segmentation
- object detection
- large model execution

Do not move computation to the browser merely because it is technically possible.

---

## 18. Analytical API Design

For every analytical endpoint define:

- endpoint purpose
- input schema
- geometry schema
- CRS contract
- temporal parameters
- thresholds
- weights
- output schema
- units
- precision
- error behavior
- authorization
- computational limits

Example pattern:

`POST /api/v1/analysis/suitability`

Request:

- AOI
- criteria
- weights
- constraints
- resolution

Response:

- result layer/reference
- score metadata
- criteria contributions
- processing status
- provenance

Expensive analysis should return a job ID rather than block an HTTP request indefinitely.

---

## 19. Map + Chart Synchronization

Analytical dashboards should keep spatial and statistical views synchronized.

Examples:

- selecting a map polygon updates charts
- selecting a chart category highlights map features
- changing a time slider updates both map and statistics
- changing an analysis parameter updates result metadata

Use stable feature IDs and explicit application state.

Avoid hidden coupling between chart and map components.

---

## 20. Result Provenance

Every important analytical result should be traceable.

Record:

- source datasets
- dataset versions
- acquisition dates
- processing version
- algorithm/method
- parameters
- CRS
- resolution
- weights
- thresholds
- model version where applicable
- execution time
- creator/user when appropriate

For reproducible research, preserve the exact configuration used to produce the result.

---

## 21. Uncertainty and Confidence

Where analytical uncertainty exists, expose it.

Possible representations:

- confidence score
- standard error
- probability
- prediction interval
- class uncertainty
- sensitivity range
- data-quality flag

Never convert uncertainty into false precision.

For decision-support systems, distinguish:

- measured value
- modeled estimate
- prediction
- score
- recommendation

The system should make those semantics visible to users.

---

## 22. Validation and QA

Validate analytical outputs using:

- known test cases
- synthetic geometries
- independent reference data
- manual spot checks
- conservation checks
- area/length consistency
- expected feature counts
- known distance cases
- statistical sanity checks
- raster alignment checks

For overlays, verify that output geometry and area behavior are plausible.

For suitability models, test extreme cases where criteria should clearly produce high/low results.

---

## 23. Performance-Aware Analytics

Analytical correctness comes first, but design for scale.

Use:

- spatial indexes
- candidate filtering
- bounding boxes
- precomputed summaries
- materialized views
- generalized geometries
- raster pyramids
- tiled outputs
- asynchronous jobs
- caching
- incremental processing

Never run a global expensive analysis synchronously because it works on a development sample.

---

## 24. Security and Authorization

Analytics can expose sensitive spatial information.

Enforce:

- tenant isolation
- row/feature-level authorization
- AOI restrictions
- dataset permissions
- rate limits
- resource limits
- output access controls

Prevent users from using analytical endpoints to infer protected features or download unrestricted datasets.

Validate user-supplied:

- geometries
- SQL-like filters
- CQL filters
- expressions
- raster parameters
- feature IDs
- bounding boxes

Do not interpolate untrusted analytical expressions directly into SQL or GIS-service requests.

---

## 25. Reproducibility and Versioning

Version:

- analytical algorithms
- weights
- thresholds
- normalization methods
- datasets
- configuration
- model versions
- code

When an analytical result changes, determine whether the cause was:

- source data update
- algorithm change
- parameter change
- CRS/resolution change
- dependency change
- bug fix

Do not silently overwrite important analytical results without traceability.

---

## 26. Cost-Aware Analytics

Prefer the least expensive architecture that satisfies analytical requirements.

Use:

- PostGIS for efficient indexed spatial SQL
- cached/materialized results for repeated analysis
- GEE when cloud-scale EO processing is appropriate
- open-source GIS libraries when adequate
- batch processing for non-interactive workloads

Paid APIs, hosted analytics, GPU infrastructure, or managed services should be justified by concrete requirements.

Consider:

- compute time
- database load
- storage
- provider quotas
- egress
- GPU cost
- operational complexity

---

## 27. Testing

Test:

### Geometry

- valid/invalid
- empty
- multipolygon/multiline
- boundary cases
- CRS transformations

### Analytical logic

- known distances
- expected buffers
- overlay areas
- weighted scores
- threshold boundaries
- temporal calculations
- raster statistics

### API

- input validation
- authorization
- large AOIs
- malformed geometry
- timeout behavior
- async jobs

### Scientific workflows

- preprocessing consistency
- train/test separation
- metric calculation
- reproducibility

### UI

- parameter changes
- result updates
- map/chart synchronization
- loading/progress
- error states

---

## 28. Analytical Definition of Done

An analytical feature is complete only when:

- the analytical question is explicit
- input datasets are identified
- CRS and units are documented
- method and assumptions are documented
- thresholds/weights are explicit
- output semantics are clear
- uncertainty is represented where relevant
- representative validation exists
- performance is acceptable for intended scale
- authorization is enforced
- provenance is recorded
- API/UI integration is tested
- results are reproducible where required
- project memory is updated

---

## 29. Project-Memory Handoff

Before stopping:

### STATE.md
Record:
- current analytical feature
- method
- last verified result
- dataset/version
- parameters
- exact next action

### TASKS.md
Record:
- analysis implementation
- validation
- performance
- visualization
- documentation status

### DECISIONS.md
Record durable choices such as:
- analytical method
- CRS
- normalization
- weights
- thresholds
- statistical method
- raster resolution
- aggregation strategy

### SESSION.md
Record:
- experiments
- measurements
- output validation
- failed approaches
- exact resume point

### BLOCKERS.md
Record:
- missing datasets
- unclear methodology
- computational constraints
- provider limitations
- unresolved scientific questions

### CHANGELOG.md
Record meaningful analytical features and verified result changes.

Never present a model-derived score, statistical result, or suitability output as authoritative without documenting its method and limitations.
