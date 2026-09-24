# Golden GIS Fixtures

## Purpose

Small deterministic datasets with known expected results for validating GIS implementations.

These fixtures are intentionally simple. They are not representative production datasets; they are correctness references.

## Fixture Groups

### Vector
- known-points.geojson
- known-polygons.geojson
- known-buffer.geojson
- known-intersection.geojson

### Projection
- known-wgs84-points.geojson

### Raster
- known-raster.json
- known-raster-alignment.json

## Expected Results

### Distance
Known points are defined so tests can verify units and calculation method. Tests must state whether the expected result is planar or geodesic.

### Buffer
Buffer tests must verify CRS/units before comparing geometry area or distance.

### Intersection
Intersection tests verify predicate and boundary semantics.

### Raster
Raster fixtures verify:
- dimensions
- pixel size
- origin
- CRS
- nodata
- expected cell values
- alignment compatibility

## Rules

- Keep fixtures tiny and deterministic.
- Do not change expected results casually.
- Any intentional fixture change requires updating the documented expected result and changelog.
- Tests should fail loudly when CRS/SRID or units are wrong.
