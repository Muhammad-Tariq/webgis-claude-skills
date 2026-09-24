# GIS Correctness

## Purpose

Determine whether a GIS result is spatially, numerically, temporally, and scientifically meaningful—not merely whether the software runs or the map looks plausible.

Use this skill as a cross-cutting correctness gate for Web GIS, desktop GIS, spatial databases, remote sensing, GeoAI, analytics, 3D, and data-processing workflows.

## Core Rule

A visually plausible result is not evidence of GIS correctness.

Every important spatial result must be traceable to:
- a defined coordinate reference system
- explicit units
- valid source data
- documented transformations
- appropriate spatial and temporal resolution
- a defensible analytical method
- expected or independently verified results where possible

## Correctness Checklist

### CRS and Units

Verify:
- source CRS/SRID
- target CRS/SRID
- horizontal datum
- vertical datum when relevant
- axis-order assumptions
- angular versus linear units
- projected versus geographic calculations
- transformation method
- whether reprojection occurs before or after analysis

Never treat EPSG:4326 degrees as meters.

For distance, area, buffering, length, slope, volume, and other measurements, verify that the calculation CRS and units are appropriate for the geographic extent and required precision.

### Geometry Correctness

Check:
- geometry type
- validity
- empty/null geometry
- self-intersections
- ring orientation where relevant
- multipart behavior
- duplicate vertices/features where relevant
- dimensionality (2D/3D/M)
- topology assumptions

Do not silently repair geometry when the repair can change analytical meaning. Record the repair method and resulting changes.

### Raster Correctness

For raster operations verify:
- CRS
- extent
- pixel size
- grid origin/alignment
- band meaning
- data type
- nodata semantics
- scale/offset
- resampling method
- temporal acquisition
- masks
- overviews/tiling when delivery affects interpretation

Two rasters with matching CRS are not necessarily aligned. Check grid geometry before pixel-wise operations.

Do not use arbitrary resampling for categorical data. Preserve class semantics.

### Vector/Raster Interactions

Verify:
- CRS compatibility
- rasterization rules
- pixel inclusion semantics
- zonal-statistics definitions
- boundary handling
- feature-to-pixel scale relationship
- mixed-resolution effects

Document whether the operation is feature-based, cell-based, or an approximation between the two.

### Measurement Correctness

For measurements:
1. define the quantity
2. define the units
3. choose the measurement model
4. choose an appropriate CRS or geodesic method
5. validate against a known case
6. report precision consistent with the input data

Do not report false precision from coarse or uncertain spatial data.

### Spatial Relationships

Validate intended semantics for:
- intersects
- contains
- within
- covers
- overlaps
- touches
- crosses
- nearest
- distance thresholds
- buffer relationships

Check boundary behavior and geometry dimensionality where it can change the result.

### Temporal Correctness

For time-dependent analysis verify:
- acquisition timestamps
- timezone conventions
- temporal coverage
- revisit interval
- compositing period
- before/after comparability
- seasonality
- temporal leakage

Do not compare observations from incompatible periods without documenting the limitation.

### Remote Sensing Correctness

Verify:
- sensor/platform identity
- band definitions
- processing level
- scale factors/offsets
- cloud and shadow masking
- QA bands
- compositing method
- spatial resolution
- temporal window
- index formula
- training/validation data provenance
- atmospheric or radiometric assumptions when applicable

For indices such as NDVI, verify band mapping and scaling rather than assuming a dataset's band names or values are interchangeable across sensors.

### Classification and GeoAI Correctness

Verify:
- prediction unit
- label definition
- label quality
- spatial/temporal split strategy
- train/validation/test independence
- spatial leakage
- temporal leakage
- class imbalance
- baseline comparison
- appropriate metrics
- uncertainty
- domain shift
- inference CRS/resolution compatibility
- model/data/version provenance

Do not treat random pixel splits as automatically valid for spatial prediction. Use spatial or temporal separation when required by the prediction problem.

### Analytics Correctness

For spatial statistics, suitability, proximity, overlays, zonal statistics, and network analysis verify:
- analytical unit
- population/feature weighting
- distance definition
- neighborhood definition
- aggregation semantics
- normalization method
- missing-data handling
- sensitivity to thresholds/weights
- multiple-comparison or statistical assumptions where applicable

For MCDA/suitability models, document criteria, transformations, weights, constraints, and sensitivity.

### 3D Correctness

Verify:
- horizontal CRS
- vertical CRS/datum
- units
- height interpretation (ellipsoidal, orthometric, relative)
- terrain/building reference surface
- point-cloud coordinate system
- LOD/generalization effects

Do not assume a Z value has the intended physical meaning without checking its reference system.

## Display Versus Analysis

Separate:
- analytical data
- delivery/visualization data
- generalized geometry
- cached tiles
- simplified geometry

Display simplification must not silently replace authoritative analytical data.

If a map uses generalized or cached data, document the source and scale limitations.

## Expected-Result Validation

Whenever practical, create a known-result fixture for critical operations:
- known distance
- known area
- known buffer
- known intersection
- known raster statistic
- known reprojection
- known classification case

Compare actual output with tolerances appropriate to the operation.

Use both positive and negative test cases.

## Error and Uncertainty

Distinguish:
- software error
- data error
- measurement uncertainty
- model uncertainty
- approximation
- visualization artifact

Do not hide uncertainty by rounding or styling.

Report limitations that could change the user's interpretation.

## Evidence Levels

For each important result, record evidence such as:
1. input/schema validation
2. transformation validation
3. deterministic expected-result test
4. independent cross-check
5. domain/scientific validation
6. production monitoring evidence

Do not claim a stronger level of correctness than the evidence supports.

## Failure Patterns

Treat these as high-risk correctness defects:
- distance/area calculated in inappropriate units
- silent CRS mismatch
- silent reprojection
- raster grids not aligned for pixel-wise operations
- incorrect nodata handling
- categorical raster resampled continuously
- temporal mismatch presented as change
- invalid geometries used without review
- generalized display data used for analysis
- spatial or temporal leakage in ML
- training/inference resolution mismatch
- unverified band mapping or scale factors
- unverified vertical datum in 3D

## Review Procedure

For a correctness review:
1. State the analytical question.
2. Identify the prediction/measurement unit.
3. Inspect source data metadata.
4. Trace CRS and transformations.
5. Trace preprocessing and cleaning.
6. Inspect the analytical operation.
7. Check units and semantics.
8. Check temporal consistency.
9. Run known-result tests where possible.
10. Inspect uncertainty and limitations.
11. Record defects with evidence.
12. Re-run validation after fixes.

## Required Review Record

For each reviewed result record:
- question
- input datasets and versions
- CRS/SRID and units
- transformations
- method
- parameters
- expected result/tolerance when available
- observed result
- validation evidence
- uncertainty/limitations
- reviewer or automated check
- timestamp/version

## Definition of Done

GIS correctness is satisfied only when:
- spatial reference and units are verified
- source data semantics are understood
- transformations are explicit
- analytical operations match the question
- critical results have deterministic or independent validation where feasible
- uncertainty and limitations are documented
- no known high-risk correctness defect remains
