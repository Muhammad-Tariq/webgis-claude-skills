# Google Earth Engine Engineering

## Purpose

Use this skill when a Web GIS, remote-sensing, environmental, agricultural, climate, or GeoAI project requires Google Earth Engine (GEE) for large-scale geospatial analysis.

The goal is not merely to produce working GEE code. The goal is to produce **scientifically defensible, reproducible, quota-aware, maintainable, and Web GIS-ready Earth Engine workflows**.

This skill works with:

- `skills/project-memory/SKILL.md`
- `skills/webgis-architect/SKILL.md`
- `skills/gis-data-processing/SKILL.md`
- `skills/remote-sensing/SKILL.md`
- `skills/postgis-engineering/SKILL.md`
- `skills/geoserver-engineering/SKILL.md`
- `skills/spatial-api/SKILL.md`

---

## 1. Mandatory Preflight

Before implementing or changing a GEE workflow:

1. Read `project-memory/STATE.md`.
2. Read `project-memory/TASKS.md`.
3. Read `project-memory/DECISIONS.md`.
4. Read `project-memory/SESSION.md`.
5. Read `project-memory/BLOCKERS.md` when present.
6. Inspect the existing GEE scripts, exports, data contracts, and downstream consumers.
7. Check the actual repository state before assuming a task is incomplete.
8. Identify the last verified state and continue from it.

If memory conflicts with code, tests, or verified data, trust the verified implementation and repair project memory.

Never restart an existing GEE workflow from scratch merely because the current session lacks context.

---

## 2. Start With the Scientific Question

Do not begin with a collection ID or an index.

Define:

- scientific or business question
- study area/AOI
- target phenomenon
- temporal period
- required spatial resolution
- required temporal resolution
- sensor characteristics
- expected output
- acceptable uncertainty
- downstream Web GIS use
- validation strategy

Example:

> "Estimate seasonal crop vegetation stress for cotton fields in a district"

is a better starting point than:

> "Calculate NDVI from Sentinel-2."

The sensor, masking, compositing, temporal window, spatial scale, and validation method depend on the question.

---

## 3. Choose the GEE Runtime

Choose the runtime based on the workflow.

### JavaScript Code Editor

Prefer for:

- exploratory analysis
- rapid prototyping
- map visualization
- interactive layer inspection
- Code Editor workflows
- teaching/research exploration

### Python API

Prefer for:

- reproducible research pipelines
- notebooks
- integration with Python data science workflows
- automated batch processing
- orchestration outside the Code Editor
- integration with local processing and ML

Use the same scientific logic across runtimes where possible.

Do not maintain two divergent implementations without a reason.

Record the runtime choice in project memory when it materially affects reproducibility or deployment.

---

## 4. Dataset and Catalog Discovery

Before using a dataset:

1. Verify the collection ID.
2. Verify the dataset documentation.
3. Confirm temporal coverage.
4. Confirm spatial coverage.
5. Confirm spatial resolution.
6. Confirm available bands.
7. Confirm band names.
8. Confirm scale factors and offsets.
9. Confirm QA bands/classes.
10. Confirm processing level.
11. Confirm provider/source.
12. Check whether the dataset has changed, been deprecated, migrated, or versioned.
13. Record the dataset identifier and relevant version/date in project memory.

Never assume two similarly named collections are scientifically interchangeable.

Prefer authoritative GEE catalog documentation over copied snippets.

### Dataset provenance

Record:

- collection ID
- provider
- processing level
- band mapping
- QA interpretation
- scale/offset
- temporal range used
- access date when relevant
- script/repository commit

---

## 5. AOI Handling

Treat the AOI as a first-class input.

Validate:

- geometry validity
- CRS/projection metadata where relevant
- coordinate order
- expected extent
- multipart behavior
- holes
- antimeridian edge cases when applicable
- feature properties required by downstream analysis

Prefer stable AOI assets or version-controlled source data for reproducible research.

Avoid silently changing an AOI during processing.

For feature collections:

- preserve stable feature IDs
- avoid accidental property loss
- define whether analysis is per-feature or aggregate
- ensure geometry complexity is appropriate for the operation

Simplify only when scientifically and operationally justified.

---

## 6. Collection Filtering

Filter as early as possible.

Typical sequence:

1. Load collection.
2. Filter by AOI/bounds.
3. Filter by date.
4. Filter by relevant metadata.
5. Apply QA/cloud/shadow masking.
6. Apply scaling/unit conversion.
7. Add derived bands.
8. Composite or aggregate.
9. Analyze/export.

Do not carry unnecessary imagery through expensive operations.

Use the narrowest defensible temporal and spatial range.

---

## 7. Cloud, Shadow, and Quality Masking

Masking must match the sensor and scientific objective.

Consider:

- cloud probability
- cloud QA bits
- cirrus
- cloud shadow
- snow/ice
- saturation
- sensor-specific quality flags
- edge artifacts
- invalid/nodata pixels
- terrain-related artifacts where applicable

Do not treat a generic cloud-percentage metadata field as a substitute for pixel-level masking when pixel-level masking is required.

Document the masking logic.

If joining a primary image collection with a QA/cloud-probability collection:

- use stable join keys
- validate that matches exist
- handle missing QA images explicitly
- avoid silently dropping imagery unless intended

---

## 8. Scaling, Units, and Band Math

Verify the physical meaning of each input band before calculations.

Check:

- integer vs floating-point storage
- reflectance scale factors
- offsets
- temperature units
- radiance vs reflectance
- digital numbers
- QA bit encoding

Do not calculate scientific indices on unscaled values when scaling is required.

Examples include:

- NDVI
- NDWI
- EVI
- SAVI
- NDBI
- land-surface temperature
- spectral ratios
- custom biophysical metrics

Name derived bands clearly and document their units/ranges where useful.

Avoid integer truncation in calculations.

---

## 9. Compositing and Reducers

Choose the reducer based on the scientific question.

Possible approaches:

- median
- mean
- minimum
- maximum
- percentile
- quality mosaic
- medoid
- temporal interpolation
- weighted aggregation
- custom reducers

Do not default to median merely because it is common.

Consider:

- cloud residuals
- seasonal phenology
- outliers
- observation density
- temporal representativeness
- sensor characteristics
- missing observations

For temporal analysis, explicitly define the period represented by every composite.

A "monthly NDVI" layer should have a documented month definition and valid-observation policy.

---

## 10. Server-Side vs Client-Side Execution

This is a critical GEE rule.

Earth Engine objects such as:

- `ee.Image`
- `ee.ImageCollection`
- `ee.Feature`
- `ee.FeatureCollection`
- `ee.Geometry`
- `ee.Number`
- `ee.Dictionary`
- `ee.List`

represent server-side computations.

Prefer server-side operations.

Avoid unnecessary use of:

- `getInfo()`
- `evaluate()`
- client-side loops
- repeated blocking requests

### Especially avoid

Do not use `getInfo()` inside loops over many images/features.

Bad pattern:

```javascript
for (...) {
  var value = image.reduceRegion(...).getInfo();
}
```

Prefer server-side mapping/reduction or controlled batch operations.

Client-side execution is appropriate when:

- the result is genuinely needed by the application/UI
- the object is small
- the operation is intentionally interactive
- a task must be created or controlled

Keep server-side computation server-side as long as possible.

---

## 11. Core Earth Engine Operations

Use the correct abstraction for the operation.

### `map()`

Use for applying a transformation to each image/feature.

Keep mapped functions server-side and deterministic.

### `reduceRegion()`

Use for reducing pixels over a geometry.

Always consider:

- scale
- CRS
- geometry
- reducer compatibility
- maxPixels
- bestEffort
- tileScale

### `reduceRegions()`

Use for applying reductions to many features.

Control feature count, geometry complexity, scale, and output size.

### `reduceColumns()`

Use for reducing feature properties rather than raster pixels.

### Joins

Use joins for matching collections or metadata by stable keys.

Validate join results instead of assuming every primary record has a match.

### Temporal aggregation

Build explicit temporal bins:

- daily
- weekly
- dekadal
- monthly
- seasonal
- annual

Record the temporal definition.

---

## 12. Scale, Projection, and Pixel Alignment

Never ignore projection semantics.

Explicitly consider:

- native dataset projection
- analysis CRS
- requested scale
- resampling behavior
- reprojection
- pixel alignment
- mixed-resolution bands
- aggregation vs resampling

Do not casually call `reproject()` to force a desired visualization or resolution.

Understand the distinction between:

- visualization scale
- reduction scale
- export scale
- native pixel resolution

For multi-sensor workflows, document how datasets are aligned.

A nominal "10 m" output does not automatically mean the information content is 10 m.

---

## 13. Aggregation Limits and Performance

Earth Engine operations can fail because of memory, aggregation, or computation limits.

When appropriate, evaluate:

- `maxPixels`
- `bestEffort`
- `tileScale`
- geometry simplification
- smaller AOIs
- temporal chunking
- spatial tiling
- reduced intermediate data
- fewer bands
- earlier filtering
- server-side mapping

Do not increase `maxPixels` blindly.

Do not use `bestEffort` as a silent substitute for scientifically required resolution.

Do not increase `tileScale` without understanding the performance tradeoff.

When a computation fails, diagnose whether the problem is:

- data volume
- geometry complexity
- reducer design
- excessive aggregation
- unbounded collection
- client-side execution
- unsuitable scale
- export size
- quota/task limits

---

## 14. Sampling and Statistics

For training, validation, or statistical analysis:

- define the sampling population
- avoid spatial leakage
- consider temporal leakage
- balance classes where scientifically appropriate
- document sample size
- use deterministic random seeds where supported
- preserve sample IDs
- separate training/validation/test data appropriately

For spatial modeling, random pixel splits can produce overoptimistic accuracy when neighboring pixels are highly correlated.

Prefer spatially or temporally independent validation when the scientific question requires generalization across space/time.

---

## 15. Classification and Machine Learning

For classification workflows:

1. Define target classes.
2. Verify label quality.
3. Prepare predictor bands/features.
4. Normalize/scale only when required by the model.
5. Build training samples.
6. Split data using a defensible strategy.
7. Train model.
8. Validate on held-out data.
9. Calculate relevant metrics.
10. Inspect spatial error patterns.
11. Export the classification with metadata.

Relevant metrics may include:

- overall accuracy
- producer's accuracy
- user's accuracy
- precision
- recall
- F1
- confusion matrix
- class-specific accuracy

Do not report only overall accuracy for imbalanced multi-class problems.

---

## 16. Temporal and Change Analysis

For change detection:

Define:

- baseline period
- comparison period
- temporal compositing strategy
- minimum valid observations
- change metric
- threshold
- uncertainty handling

Potential approaches:

- image differencing
- normalized difference change
- trend analysis
- seasonal anomaly
- harmonic/temporal models
- breakpoint detection
- classification comparison

Do not interpret every spectral difference as physical change.

Account for:

- seasonality
- phenology
- cloud contamination
- sensor differences
- atmospheric effects
- acquisition timing
- processing differences

---

## 17. GEE and Web GIS Integration

GEE is usually the analysis engine, not automatically the application backend.

Define the downstream delivery contract.

Possible outputs:

### Raster

- GeoTIFF
- Cloud Optimized GeoTIFF where appropriate
- GEE Asset
- map tiles/visualization layers where appropriate

### Vector

- GeoJSON
- Shapefile
- CSV with geometry
- database-ready features

### Web GIS

Possible pipeline:

```text
GEE
  ↓
Analysis / Export
  ↓
Object Storage / PostGIS / Processing
  ↓
GeoServer / Spatial API
  ↓
Web GIS Frontend
```

For large rasters, do not automatically export giant GeoTIFFs directly into a web application.

Evaluate:

- COG
- tiling
- pyramids/overviews
- object storage
- raster tile services
- GeoServer
- API-generated statistics
- vector tiling

For large vector outputs, evaluate:

- PostGIS
- vector tiles
- GeoServer
- spatial APIs

---

## 18. Export Engineering

Every export should have explicit parameters.

Record:

- source dataset
- processing version
- AOI
- date range
- bands
- scale
- CRS
- region
- file format
- file dimensions where applicable
- nodata policy
- output destination
- description/task name
- shard/file dimensions when relevant

Choose the destination deliberately:

- Drive for small/manual research outputs
- Cloud Storage for automated pipelines and larger artifacts
- Earth Engine Assets for reusable GEE-native datasets
- downstream object storage/database for Web GIS production delivery

Do not use Drive as an implicit production data lake.

---

## 19. Task Management

Treat exports as jobs.

For batch workflows:

- create deterministic task names
- record task parameters
- avoid duplicate submissions
- track task state
- detect failures
- retry only when safe
- preserve failed-task diagnostics
- separate transient failures from invalid jobs

Use idempotent export generation where possible.

A rerun should not unexpectedly create conflicting datasets or overwrite validated outputs.

---

## 20. Reproducibility

A GEE workflow should be reproducible from recorded inputs.

Record:

- script/repository commit
- GEE runtime
- collection IDs
- dataset versions where available
- AOI version
- date range
- filter parameters
- cloud/QA thresholds
- masking logic
- scaling logic
- formulas
- reducer
- scale
- CRS
- random seed
- training dataset/version
- model parameters
- export parameters

Do not rely on undocumented Code Editor state.

If a research result matters, make the exact analysis configuration recoverable.

---

## 21. Cost, Quotas, and Free-First Policy

GEE may be usable within applicable free access or project quotas, but it is **not an unlimited free production compute platform**.

Before committing a production workflow to GEE, evaluate:

- current account/project terms
- computation quotas
- concurrent task limits
- export limits
- storage limits/cost
- API usage
- commercial/project requirements
- expected workload
- data egress
- operational reliability
- alternative open-source/local/cloud processing

Prefer GEE when it provides a strong fit for the required large-scale Earth observation computation.

Use local or other cloud processing when it is more appropriate for:

- unrestricted production workloads
- custom GPU/ML pipelines
- private data
- deterministic infrastructure requirements
- specialized libraries unavailable in GEE
- workloads exceeding practical GEE limits

Record material cost/quota decisions in `project-memory/DECISIONS.md`.

Never describe GEE as "free unlimited compute."

---

## 22. Security and Data Governance

Never hard-code:

- API secrets
- service-account private keys
- passwords
- tokens
- private credentials

Do not publish private assets or sensitive geometries accidentally.

For sensitive projects:

- separate public and private assets
- restrict project/asset permissions
- minimize exported sensitive data
- review sharing settings
- avoid exposing internal asset IDs through public APIs when inappropriate

Remember that exporting data from GEE into another system changes the security boundary.

---

## 23. Scientific QA

Before accepting a result, verify:

### Data QA

- expected imagery exists
- expected date range is covered
- AOI is correct
- cloud/QA masking behaves correctly
- no unexpected empty periods

### Numerical QA

- units are correct
- expected value ranges hold
- nodata is handled
- derived bands are numerically plausible

### Spatial QA

- alignment is correct
- no unexpected shifts
- boundaries behave correctly
- resolution is appropriate
- artifacts are inspected

### Temporal QA

- dates are correct
- composites represent the intended periods
- seasonal effects are understood

### Validation QA

- validation data are independent enough for the objective
- metrics are appropriate
- errors are spatially inspected
- uncertainty is documented

Never treat successful task completion as proof of scientific correctness.

---

## 24. Testing

Where practical, test GEE workflows at multiple levels.

### Unit-level logic

Test:

- date calculations
- band selection
- masking predicates
- index formulas
- class mappings
- property transformations

### Data-contract tests

Verify:

- expected bands exist
- expected properties exist
- collection is non-empty
- output schema is stable

### Spatial tests

Verify:

- output footprint
- CRS/projection expectations
- pixel dimensions where relevant
- sample locations

### Regression tests

Keep small, deterministic test AOIs or sample assets where feasible.

Compare:

- expected band names
- feature counts
- summary statistics
- known sample values
- classification metrics

Avoid full-country/full-global tests for every code change.

---

## 25. Failure Handling

When a GEE workflow fails:

1. Capture the exact error.
2. Identify whether it is client-side, server-side, quota, data, export, or scientific.
3. Reproduce with the smallest representative AOI/time range.
4. Reduce complexity systematically.
5. Verify the scientific logic did not change as a workaround.
6. Fix the root cause.
7. Re-run targeted validation.
8. Record durable blockers or decisions in project memory.

Do not solve memory errors by randomly changing parameters until the task succeeds.

---

## 26. Common Anti-Patterns

Avoid:

- `getInfo()` inside large loops
- unbounded ImageCollections
- giant geometries passed unnecessarily into every operation
- undocumented cloud masks
- incorrect scale factors
- arbitrary `reproject()`
- blindly using `bestEffort`
- blindly increasing `maxPixels`
- exporting massive rasters without a delivery strategy
- random pixel train/test splits when spatial leakage matters
- mixing incompatible sensors without normalization
- silently changing AOIs
- hard-coded credentials
- duplicate export tasks
- treating GEE success as scientific validation
- treating public/free access as unlimited production capacity

---

## 27. Definition of Done

A GEE implementation is complete only when:

- [ ] Scientific/business objective is explicit.
- [ ] AOI is validated and versioned where needed.
- [ ] Dataset IDs and relevant versions are documented.
- [ ] Temporal and spatial filters are explicit.
- [ ] QA/cloud/shadow masking is scientifically justified.
- [ ] Scale factors and units are correct.
- [ ] Server-side execution is used appropriately.
- [ ] Reducers and compositing methods match the question.
- [ ] Projection/scale behavior is understood.
- [ ] Performance limits have been considered.
- [ ] Export parameters are explicit.
- [ ] Export tasks are deterministic/idempotent where practical.
- [ ] Reproducibility metadata is recorded.
- [ ] Scientific QA has been performed.
- [ ] Validation is appropriate to the objective.
- [ ] Downstream Web GIS delivery is defined when applicable.
- [ ] Security and asset permissions are reviewed.
- [ ] Quota/cost implications are understood.
- [ ] Tests or representative validation checks pass.
- [ ] Project memory is updated.

Do not claim completion because a script merely runs without errors.

---

## 28. Project-Memory Handoff

Before ending work on a GEE task, update project memory with:

### STATE.md

Record:

- current GEE workflow
- last verified step
- files changed
- validation performed
- current blocker
- exact next action

### TASKS.md

Record:

- completed GEE tasks
- active task
- next task
- failed/retry items

### DECISIONS.md

Record durable decisions such as:

- JavaScript vs Python API
- dataset/collection selection
- masking strategy
- temporal compositing method
- projection/scale choice
- GEE vs local/cloud processing
- export architecture
- quota/cost decision

### SESSION.md

Record:

- what was actually done
- tests/exports executed
- important observations
- exact resume point

### BLOCKERS.md

Record unresolved:

- quota problems
- unavailable datasets
- failed exports
- permissions
- API issues
- scientific uncertainties

Never store credentials, tokens, or private keys in project memory.

---

## 29. Handoff Summary

When handing work to another session or agent, provide enough information to resume without rediscovery:

```text
GEE workflow:
AOI:
Datasets:
Date range:
Masking:
Derived variables:
Composite/reducer:
Scale/CRS:
Validation:
Exports:
Downstream destination:
Quota/cost considerations:
Last verified result:
Current blocker:
Exact next action:
```

The next agent should inspect the repository and actual GEE implementation before trusting this summary.
