# Spatial API Contract

## Required

- API version
- endpoint
- operation
- authentication/authorization
- input schema
- output schema
- CRS behavior
- geometry format
- units
- pagination
- filtering
- sorting
- bbox semantics
- limits
- error format

## Spatial Rules

Declare:
- accepted CRS/SRID
- output CRS
- geometry validation
- coordinate order
- distance/area units
- spatial predicate semantics

## Resource Safety

Define:
- maximum features
- maximum payload
- timeout
- maximum processing area/extent
- job limits for asynchronous processing
- rate/resource limits

## Compatibility

Breaking spatial or schema changes require API versioning or a documented compatibility strategy.
