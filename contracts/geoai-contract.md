# GeoAI Contract

## Required

- model_id
- model_version
- task
- prediction_unit
- input_dataset/version
- label definition
- feature preprocessing
- CRS/resolution requirements
- training/validation/test split strategy
- metrics
- uncertainty representation
- inference constraints
- provenance

## Validation Invariants

Verify:
- no prohibited spatial/temporal leakage
- train/inference preprocessing parity
- CRS compatibility
- resolution compatibility
- label semantics
- class/target definition
- baseline comparison
- model version reproducibility

## Output

Declare:
- prediction type
- units/classes
- confidence/uncertainty
- nodata/invalid prediction behavior
- spatial extent
- output CRS
- post-processing rules
