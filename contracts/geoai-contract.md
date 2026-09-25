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


## Scientific Integrity Invariants

- Evaluation protocol must be explicit and versioned.
- Methodology must not be changed solely to improve reported metrics.
- Material methodology changes require documented scientific or operational rationale.
- Original experiment results and lineage must be preserved.
- Changes to splits, sampling, labels, preprocessing boundaries, evaluation population, thresholds, or metric definitions require explicit review when made after results exist.
- A higher metric does not prove improvement when the evaluation protocol changed.
- Ambiguous methodology changes must be escalated.
