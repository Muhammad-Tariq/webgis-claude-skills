# Vector Data Contract

## Required

- geometry type
- CRS/SRID
- dimensionality
- feature identifier
- attribute schema
- nullability
- domain constraints
- geometry validity rule
- spatial extent
- units for measured fields

## Validation

Verify:
- geometry type
- SRID
- validity
- required attributes
- unique identifiers
- value ranges
- duplicate policy
- topology rules when required

## Delivery

Declare whether the representation is:
- authoritative
- analytical
- generalized
- cached
- visualization-only

Never silently use a visualization representation for authoritative analysis.
