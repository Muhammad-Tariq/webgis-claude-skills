# AP-RASTER-001 — Raster Grid Misalignment

## Scenario
Two rasters share CRS and resolution but have different grid origins; a cell-by-cell operation is requested.

## Expected Detection
Same CRS/resolution does not imply identical pixel grids.

## Expected Pattern
Explicit grid alignment with documented resampling policy.

## Remediation
B — Context-Aware Auto-Fix.

## Validation
Alignment known; resampling explicit; categorical data uses nearest-neighbor when applicable; extent/nodata preserved.
