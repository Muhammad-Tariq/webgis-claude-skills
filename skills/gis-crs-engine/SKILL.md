# GIS CRS & Projection Intelligence

## Purpose
Provide safe, context-aware CRS handling for GIS projects. Mixed-CRS datasets must be supported without silently mutating source data.

## Core Invariant
**Native CRS, display CRS, and analysis CRS are separate concepts.**

- **Native CRS**: authoritative CRS in which source data is stored and preserved unless persistent reprojection is explicitly requested.
- **Display CRS**: CRS used by the map/view for rendering. Different native CRS layers may coexist and be transformed for display.
- **Analysis CRS**: CRS selected for a specific spatial operation when the operation requires appropriate spatial properties or units.

Never silently overwrite native CRS merely to make layers render together.

## Mixed-CRS Workflow
1. Inspect and validate each dataset's native CRS.
2. Preserve each dataset in its native CRS.
3. Determine the map/view CRS independently.
4. Apply runtime/display transformations as supported by the selected map engine.
5. For analysis, determine operation, AOI, accuracy, units, geometry extent, datum/vertical requirements, and candidate transformations.
6. Select an appropriate analysis CRS/transformation using authoritative CRS definitions and a transformation engine such as PROJ/EPSG data available in the environment.
7. Transform analysis inputs explicitly; do not mutate source datasets.
8. Validate geometry, units, extent, and expected result.
9. Record the transformation and reasoning in the audit trail.

## CRS Intelligence
Support the full CRS ecosystem available from authoritative registries/PROJ rather than maintaining a small hard-coded EPSG list. Handle geographic, projected, local/national grids, UTM, State Plane, conformal/equal-area/equidistant/azimuthal families, vertical and compound CRS, 3D/dynamic CRS where supported, axis order, datum transformations, grid-based transformations, and custom definitions.

Do not assume a single projection family is correct globally.

## Operation-Aware Selection
Projection choice depends on the operation: display/rendering, distance, area, buffer, overlay, proximity, engineering measurements, raster analysis, terrain/elevation, temporal/spatiotemporal analysis, and 3D/vertical operations.

For distance/area/buffer work, validate that the chosen method produces required units and acceptable distortion. Geodesic methods may be preferable to reprojection in some cases.

## Explicit Reprojection
Only permanently reproject a dataset when the user explicitly requests it or a documented pipeline contract requires a derived dataset. A derived output must have its own CRS metadata and provenance. Never hide a persistent CRS change behind display logic.

## Layer Metadata
Each layer/dataset should expose: nativeCRS, displayCRS, analysisCRS (nullable), authority/EPSG where available, CRS name, projection family, datum, units, axis order, transformation pipeline/operation, source/target CRS, and accuracy information when supported.

## Anti-Pattern Remediation
Detect and remediate mixed CRS treated as identical, silent reprojection, wrong UTM zone, inappropriate EPSG:4326 planar measurement, axis-order confusion, datum transformation loss, vertical datum assumptions, and raster grid/CRS mismatch.

A remediation must explain the issue, choose a context-appropriate correction, apply it only to the analysis/display representation unless persistent reprojection is requested, and validate the result.

## Safety Rules
Never invent an EPSG code. Never select a CRS solely from country name. Never assume Web Mercator is suitable for measurement. Never silently drop Z/vertical information. Never silently change axis order. Never treat CRS metadata as cosmetic.

## Verification
After transformation verify source CRS, target CRS, explicit transformation, geometry validity, expected extent/location, units, result plausibility, source immutability, and transformation metadata.

## Related Systems
Use with skills/gis-correctness, skills/gis-data-processing, skills/webgis-map-engine, skills/postgis-engineering, skills/raster-engineering, skills/webgis-testing, contracts/crs-contract.md, and anti-patterns/mixed-crs-analysis.md.
