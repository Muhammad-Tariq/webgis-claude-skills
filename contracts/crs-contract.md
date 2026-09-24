# CRS Contract

## Purpose
Define invariants for CRS-aware GIS applications and mixed-CRS projects.

## Required Concepts
| Field | Meaning |
|---|---|
| nativeCRS | Authoritative CRS of the stored/source dataset |
| displayCRS | CRS used by the map/view for rendering |
| analysisCRS | CRS selected for a particular analysis operation |
| transformation | Explicit operation/pipeline between CRS definitions |

## Invariants
1. Native CRS must not change during display transformation.
2. Different native CRS layers may coexist in one project.
3. Display transformation must not be represented as permanent data reprojection.
4. Analysis CRS must be selected from the operation and spatial context.
5. CRS transformations must be explicit and reproducible.
6. EPSG/authority identifiers must never be fabricated.
7. Axis order must follow the CRS and library contract.
8. Datum transformations must be explicit when material to accuracy.
9. Vertical/3D CRS information must not be silently discarded.
10. Persistent reprojection creates a derived dataset with new CRS metadata and provenance.

## Mixed-CRS Example
Dataset A: nativeCRS = EPSG:4326.
Dataset B: nativeCRS = EPSG:32642.
Both may be displayed in a common map/view CRS while retaining their native CRS.

A 500 m buffer must not be computed by blindly applying planar degree arithmetic to EPSG:4326. The system must select an appropriate measurement approach/analysis CRS, perform the operation, validate it, and preserve the original layers.

## Audit Information
For every non-trivial transformation record source CRS, target CRS, authority identifiers, transformation operation/pipeline, reason, operation, units, accuracy information when supported, validation result, and whether source data was mutated.

## Failure Conditions
Reject or escalate when CRS is missing/ambiguous, reliable transformation cannot be established, available transformation cannot satisfy required accuracy, vertical datum is required but unavailable, geometry becomes invalid, or the result cannot be validated.
