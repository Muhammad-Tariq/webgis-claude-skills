# Spatial Data Contract

## Purpose

Define the minimum metadata and invariants required before vector spatial data is consumed by an application, service, analysis, or publication pipeline.

## Required Fields

- dataset_id
- name
- version
- geometry_type
- CRS/SRID
- dimensionality
- spatial_extent
- attribute_schema
- units
- temporal_extent when applicable
- source
- provenance
- quality_status
- nodata/null semantics
- update_frequency when applicable

## Geometry Invariants

- declared geometry type matches actual data
- declared CRS/SRID matches stored coordinates
- geometry validity rules are explicit
- empty/null geometry policy is explicit
- dimensionality is explicit
- multipart behavior is explicit

## Quality

Define:
- positional accuracy where known
- completeness
- duplicate policy
- topology expectations
- attribute constraints
- validation timestamp
- validation tool/version

## Consumption Rules

Consumers must not silently:
- change CRS without recording it
- change units
- repair invalid geometry without recording the operation
- discard features without a documented rule
- treat generalized display data as authoritative analytical data

## Versioning

Breaking changes require a new contract/data version and migration strategy.
