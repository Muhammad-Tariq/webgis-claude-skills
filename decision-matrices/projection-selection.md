# Projection & CRS Selection Matrix

Projection selection is requirement-driven. Do not choose a CRS solely because it is common in a region.

| Requirement | Evaluate |
|---|---|
| Web display | map engine support, performance, supported display CRS |
| Distance | geodesic vs projected distance, distortion, units, AOI |
| Area | equal-area suitability, distortion, AOI, units |
| Buffer | local scale distortion, required radius accuracy, AOI |
| Large regional analysis | distortion across full AOI, projection family |
| Global analysis | geodesic/global equal-area/equidistant requirements |
| Engineering/local survey | authoritative local/national CRS and datum |
| Raster analysis | grid alignment, pixel size, resampling, CRS |
| Elevation | horizontal CRS plus vertical CRS/datum |
| 3D | horizontal + vertical/3D CRS compatibility |
| Temporal/dynamic CRS | epoch/time-dependent transformation requirements |

## Selection Process
1. Identify source CRS(s).
2. Identify operation and output requirements.
3. Determine AOI and spatial scale.
4. Determine required units and accuracy.
5. Discover candidate CRS/transformation operations from authoritative CRS data/PROJ.
6. Reject candidates that violate operation requirements.
7. Select and record the transformation.
8. Validate the result.

## Principle
Use the authoritative CRS registry and transformation engine available in the project/environment rather than maintaining a small manually curated list of EPSG codes.
