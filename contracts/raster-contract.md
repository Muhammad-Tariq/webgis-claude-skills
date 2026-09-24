# Raster Data Contract

## Required

- dataset_id
- version
- CRS
- extent
- width/height
- pixel size
- grid origin/alignment
- band names and semantics
- data type
- nodata
- scale/offset
- units
- acquisition/temporal metadata
- source/provenance

## Processing Invariants

For pixel-wise operations verify:
- compatible CRS
- compatible grid
- compatible resolution
- compatible extent or explicit resampling/windowing
- compatible temporal semantics

## Resampling

Declare the resampling method.
- categorical data requires class-preserving treatment
- continuous data requires an appropriate continuous method

## Quality

Record:
- cloud/quality masks when applicable
- missing-data rules
- valid value range
- processing level
- validation timestamp/tool version
