# RASTER-001 — Known Raster Alignment

## Scenario
Raster A and B are intentionally aligned. Raster C has the same CRS and pixel size but a shifted origin.

## Inputs
fixtures/raster/known-raster-alignment.json

## Expected Detection
The evaluator must distinguish CRS/resolution equality from actual grid alignment.

## Expected Pattern
Require explicit grid alignment before cell-by-cell raster analysis.

## Remediation
B — Context-Aware Auto-Fix when the analysis operation and resampling policy are known.

## Required Validation
- A/B reported aligned
- A/C reported misaligned
- CRS and pixel size checked
- origin/grid transform checked
- resampling policy explicit before any alignment operation

## Forbidden
Treating same CRS and resolution as proof of pixel alignment; silently resampling categorical data with an inappropriate interpolator.
