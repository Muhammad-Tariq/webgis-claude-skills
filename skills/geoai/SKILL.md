# GeoAI Engineering

## Purpose

Use this skill when a project applies artificial intelligence or machine learning to geospatial data, including:

- satellite imagery
- aerial/drone imagery
- LiDAR and point clouds
- raster time series
- vector features
- spatial networks
- geocoded tabular data
- multimodal geospatial datasets
- GeoAI foundation models
- segmentation
- object detection
- classification
- regression
- change detection
- spatial embeddings
- geospatial retrieval
- predictive spatial analysis

The goal is to build **scientifically defensible, spatially aware, reproducible, cost-conscious, and production-ready GeoAI systems**, not merely models with high benchmark accuracy.

This skill works with:

- `skills/project-memory/SKILL.md`
- `skills/webgis-architect/SKILL.md`
- `skills/gis-data-processing/SKILL.md`
- `skills/remote-sensing/SKILL.md`
- `skills/google-earth-engine/SKILL.md`
- `skills/postgis-engineering/SKILL.md`
- `skills/spatial-api/SKILL.md`

---

## 1. Mandatory Preflight

Before implementing or changing a GeoAI workflow:

1. Read `project-memory/STATE.md`.
2. Read `project-memory/TASKS.md`.
3. Read `project-memory/DECISIONS.md`.
4. Read `project-memory/SESSION.md`.
5. Read `project-memory/BLOCKERS.md` when present.
6. Inspect the existing data pipeline, model code, training data, checkpoints, inference code, API contracts, and frontend consumers.
7. Inspect actual repository state before assuming the previous session's state is correct.
8. Identify the last verified model/data/pipeline state.
9. Continue from that verified state.

If memory conflicts with code, tests, or measured results, trust the verified implementation and repair project memory.

Never retrain, re-download, or regenerate large datasets simply because a session restarted.

---

## 2. Start With the Spatial Problem

Define the actual problem before selecting a model.

Specify:

- target phenomenon
- prediction/detection/classification objective
- spatial unit
- temporal unit
- input modalities
- target labels
- expected output
- spatial resolution
- temporal resolution
- inference extent
- acceptable latency
- acceptable error
- operational constraints
- downstream Web GIS use

Examples:

- classify crop type per field
- segment buildings from aerial imagery
- detect solar panels from drone imagery
- estimate vegetation stress
- predict drought vulnerability
- detect land-cover change
- retrieve similar geospatial locations
- estimate population density
- identify road damage

Do not start by choosing a model because it is fashionable.

---

## 3. Define the Prediction Unit

Every GeoAI task needs an explicit prediction unit.

Possible units:

- pixel
- image patch
- object
- field/polygon
- building
- road segment
- point
- grid cell
- administrative unit
- trajectory
- temporal sequence

Document:

- input geometry
- output geometry
- spatial support
- aggregation method

A model trained at pixel level should not automatically be interpreted as an object-level predictor.

---

## 4. Data Provenance and Versioning

Track every important input.

Record:

- source
- provider
- dataset/collection ID
- acquisition dates
- processing level
- spatial resolution
- spectral bands/features
- CRS
- preprocessing version
- AOI
- label source
- label version
- sampling method
- train/validation/test split version

For imagery, also record:

- sensor
- platform
- scene/image ID
- cloud/quality filtering
- calibration/scaling
- compositing method

For vector labels, record:

- source authority
- creation/edit date
- geometry validation status
- attribute schema
- class definition

Never train a production model from an undocumented dataset snapshot.

---

## 5. Spatial Data Leakage Prevention

Spatial leakage is one of the most important GeoAI failure modes.

Do not assume random train/test splitting is valid.

Neighboring pixels or overlapping patches can be highly correlated.

Consider splits by:

- geographic region
- tile
- field
- administrative unit
- acquisition scene
- date
- sensor/platform

Choose the split strategy according to the desired generalization.

Examples:

### Generalize to unseen areas

Use spatial holdout regions.

### Generalize to future dates

Use temporal holdout.

### Generalize to new fields

Split by field/object ID.

### Generalize to new sensors

Hold out sensor/platform data when appropriate.

Document the intended generalization target.

---

## 6. Label Quality

Model performance cannot exceed the reliability of its labels.

Inspect:

- class definitions
- geometry validity
- label completeness
- class imbalance
- positional accuracy
- temporal mismatch
- annotation consistency
- ambiguous samples
- duplicated samples
- conflicting labels

For remote sensing, ensure label dates are compatible with imagery dates.

Do not silently train on labels from a different phenological period unless scientifically justified.

Track label provenance.

---

## 7. Dataset Construction

Build an explicit data pipeline:

```text
Source Data
   ↓
Inventory
   ↓
Validation
   ↓
Spatial/Temporal Alignment
   ↓
Preprocessing
   ↓
Label Generation
   ↓
Sampling
   ↓
Split
   ↓
Training Dataset
   ↓
Validation/Test Dataset
```

The dataset generation code should be reproducible.

Use deterministic seeds where appropriate.

Persist dataset manifests for expensive datasets.

A manifest should identify:

- sample ID
- source image/scene
- location
- label
- acquisition date
- preprocessing version
- split
- dataset version

---

## 8. Input Preprocessing

Preprocessing depends on modality.

### Optical imagery

Consider:

- radiometric scaling
- reflectance conversion
- cloud/shadow masking
- normalization
- band selection
- missing data
- seasonal compositing

### SAR

Consider:

- polarization
- orbit direction
- speckle
- calibration
- terrain effects
- incidence angle
- preprocessing consistency

### LiDAR

Consider:

- point density
- classification
- ground/non-ground separation
- DTM/DSM/CHM derivation
- voxelization
- point-cloud normalization

### Drone imagery

Consider:

- orthomosaic quality
- GSD
- illumination differences
- camera calibration
- overlap
- seam artifacts
- flight-to-flight normalization

### Vector/tabular data

Consider:

- geometry validity
- categorical encoding
- missing values
- spatial autocorrelation
- temporal consistency

Do not apply generic normalization without understanding physical units.

---

## 9. Model Selection

Choose the simplest model that satisfies the requirement.

Potential families:

### Classical ML

- Random Forest
- Gradient Boosting
- XGBoost
- LightGBM
- SVM

Useful for:

- tabular spatial features
- spectral indices
- field-level predictors
- interpretable baselines

### Deep learning

- CNN
- U-Net
- DeepLab
- SegFormer
- Vision Transformer
- object detection architectures
- temporal models

Useful for:

- image segmentation
- object detection
- complex spatial patterns

### Foundation models

Consider geospatial foundation models when they provide a meaningful advantage through:

- pretrained representations
- transfer learning
- few-shot adaptation
- embeddings
- cross-region generalization
- multimodal representations

Do not use a foundation model merely because it is newer.

Always establish a meaningful baseline.

---

## 10. Baseline Before Complexity

For most projects:

1. Build a simple baseline.
2. Measure it using the intended evaluation protocol.
3. Establish an error profile.
4. Add model complexity only when justified.

Example progression:

```text
Simple spatial/spectral baseline
        ↓
Random Forest / Gradient Boosting
        ↓
CNN / segmentation model
        ↓
Transformer / foundation model
        ↓
Fine-tuned or multimodal system
```

The progression should be evidence-driven.

Record why each additional level of complexity is justified.

---

## 11. Foundation Models and Transfer Learning

When using a geospatial foundation model:

Document:

- model name
- repository/source
- checkpoint/version
- pretraining domain
- sensor/modalities
- expected input resolution
- input normalization
- pretrained geographic coverage
- license
- hardware requirements
- fine-tuning method
- frozen/trainable layers
- training data
- downstream task

Evaluate whether the model's pretraining distribution matches the target geography and sensor.

A model pretrained on one sensor or geography may not transfer directly to another.

---

## 12. Fine-Tuning Strategy

Choose among:

- frozen encoder + trained head
- partial fine-tuning
- full fine-tuning
- parameter-efficient fine-tuning
- adapter-based approaches

Consider:

- dataset size
- GPU memory
- domain shift
- compute budget
- inference constraints
- overfitting risk

Do not fine-tune the entire model by default.

Record:

- learning rate
- batch size
- optimizer
- scheduler
- epochs/steps
- augmentation
- loss
- seed
- checkpoint policy
- early stopping criteria

---

## 13. Spatial Augmentation

Use augmentation that preserves the scientific meaning of the task.

Potential augmentations:

- rotation
- horizontal/vertical flip
- crop
- scale
- controlled brightness/contrast
- noise

Be careful with:

- orientation-sensitive road/building tasks
- multispectral band relationships
- geophysical quantities
- temporal imagery
- directional SAR effects

Never apply an augmentation simply because it improves a validation score without checking scientific validity.

---

## 14. Segmentation

For semantic or instance segmentation:

Define:

- class taxonomy
- background definition
- minimum object size
- mask encoding
- ignore/no-data policy
- tile/patch size
- overlap strategy

Metrics may include:

- IoU
- mean IoU
- Dice/F1
- precision
- recall
- class-specific metrics

For small objects, inspect boundary quality rather than relying only on aggregate scores.

Watch for tiling artifacts at inference boundaries.

---

## 15. Object Detection

Define:

- object classes
- minimum detectable size
- bounding-box vs polygon output
- confidence threshold
- NMS behavior
- overlap/tile strategy

Evaluate:

- precision
- recall
- F1
- AP/mAP
- size-specific performance
- geographic performance

Inspect false positives and false negatives spatially.

For geospatial products, convert detections into the correct CRS and geometry representation before downstream use.

---

## 16. Regression and Prediction

For continuous outputs:

Define:

- target variable
- units
- spatial support
- temporal support
- valid range
- uncertainty requirements

Evaluate using appropriate metrics such as:

- MAE
- RMSE
- R²
- bias
- percentile errors

Do not use R² alone.

Check residuals spatially and temporally.

A model can have acceptable global metrics while failing systematically in specific regions.

---

## 17. Classification Evaluation

For classification:

Use appropriate metrics:

- confusion matrix
- accuracy
- balanced accuracy
- precision
- recall
- F1
- per-class metrics

For imbalanced classes, report class-specific performance.

For probabilistic outputs, consider:

- calibration
- confidence distributions
- uncertainty thresholds

Do not convert every model probability into a categorical map without documenting the threshold.

---

## 18. Spatial Error Analysis

Every serious GeoAI workflow should inspect where the model fails.

Analyze errors by:

- geography
- land-cover type
- elevation
- climate zone
- season
- sensor
- acquisition date
- object size
- class
- data quality

Generate spatial error layers where possible.

Examples:

- false-positive map
- false-negative map
- residual map
- uncertainty map
- confidence map

This often reveals domain shift that aggregate metrics hide.

---

## 19. Domain Shift and Generalization

Explicitly evaluate whether the model is being deployed outside its training distribution.

Potential shifts:

- geography
- season
- sensor
- resolution
- illumination
- atmospheric conditions
- crop variety
- urban morphology
- acquisition platform

When possible, perform holdout testing on representative unseen regions or periods.

Do not claim generalization beyond the evaluated domain.

---

## 20. Inference at Scale

For large geographic extents:

- tile inputs
- use overlap where required
- batch inference
- control memory
- parallelize safely
- preserve spatial metadata
- merge outputs carefully
- validate seams
- track processing status

For raster inference:

```text
Large AOI
  ↓
Tiling
  ↓
Batch inference
  ↓
Overlap handling
  ↓
Mosaic/merge
  ↓
Spatial QA
  ↓
Final product
```

Do not load an entire country-scale raster into memory when tiling is required.

---

## 21. Model Serving Architecture

Separate model inference from the Web GIS frontend.

A common architecture:

```text
Web GIS
   ↓
Spatial API
   ↓
Inference Service
   ↓
Model Runtime
   ↓
Raster/Object Storage
   ↓
PostGIS / GeoServer / Tile Service
```

Possible inference technologies include:

- PyTorch
- TensorFlow
- ONNX Runtime
- Triton
- managed model endpoints
- serverless inference where appropriate

Choose based on:

- model type
- latency
- throughput
- GPU requirements
- deployment complexity
- cost

Do not expose model internals directly to the browser.

---

## 22. Interactive vs Batch GeoAI

Classify inference requirements.

### Interactive

User expects a result within seconds.

Prefer:

- lightweight models
- precomputed embeddings
- cached outputs
- tiled inference
- optimized model runtime
- bounded AOI

### Batch

Minutes/hours are acceptable.

Prefer:

- asynchronous jobs
- queues
- workers
- checkpointing
- resumable processing
- object storage

Do not force a batch-scale model into a synchronous HTTP request.

---

## 23. GeoAI + GEE

Use GEE where it provides strong value for:

- satellite data discovery
- filtering
- compositing
- preprocessing
- feature generation
- large-scale sampling
- temporal statistics
- export

Move to external ML infrastructure when needed for:

- custom deep learning
- GPU training
- foundation-model fine-tuning
- custom Python libraries
- advanced model architectures
- specialized inference runtimes

A common pipeline is:

```text
GEE
 ↓
Preprocessing / Feature Generation
 ↓
Training Dataset Export
 ↓
ML Training
 ↓
Model Evaluation
 ↓
Large-Scale Inference
 ↓
COG / Vector / PostGIS
 ↓
GeoServer / API
 ↓
Web GIS
```

Keep the boundary between GEE and external ML explicit.

---

## 24. GeoAI + PostGIS

Use PostGIS for:

- spatial joins
- AOI filtering
- feature retrieval
- prediction storage
- spatial indexing
- aggregation
- serving vector predictions

Store model metadata with predictions where appropriate:

- model version
- inference timestamp
- confidence
- uncertainty
- input dataset version
- processing version

Do not overwrite previous model results when temporal/model versioning matters.

---

## 25. Raster Output Engineering

For production raster predictions:

Prefer appropriate cloud-native delivery patterns.

Consider:

- Cloud Optimized GeoTIFF
- internal tiling
- overviews
- compression
- nodata
- correct CRS
- metadata
- object storage
- raster tile services

For very large outputs, do not create one enormous monolithic file unless the delivery system requires it.

Validate that visualization resolution does not imply model resolution.

---

## 26. Uncertainty and Confidence

Where practical, expose uncertainty.

Possible approaches:

- model probability
- entropy
- ensemble variance
- Monte Carlo dropout
- prediction intervals
- calibration
- confidence thresholds

Distinguish:

- model confidence
- prediction uncertainty
- data quality
- epistemic uncertainty
- aleatoric uncertainty

Do not describe a probability score as guaranteed real-world probability unless calibration supports that interpretation.

---

## 27. Explainability

Use explainability when it supports a real decision.

Possible techniques:

- feature importance
- permutation importance
- SHAP
- saliency
- attention inspection
- counterfactual analysis
- class activation methods

For spatial models, combine model explanations with spatial error analysis.

Do not present saliency maps as causal explanations.

---

## 28. Reproducibility

Record:

- code repository commit
- model/checkpoint version
- dataset version
- label version
- preprocessing version
- train/validation/test split
- random seed
- hyperparameters
- framework version
- CUDA/runtime version where relevant
- hardware
- inference parameters
- postprocessing parameters

Persist:

- dataset manifest
- training configuration
- model metadata
- evaluation results
- model artifact checksum where practical

A production prediction should be traceable to the model and data versions that generated it.

---

## 29. Experiment Tracking

For meaningful experiments, record:

- experiment ID
- hypothesis
- dataset version
- model
- configuration
- metrics
- runtime
- compute cost
- checkpoint
- qualitative observations

Compare experiments using the same evaluation protocol.

Do not select a model based on a single metric when deployment requirements include latency, memory, cost, or geographic robustness.

---

## 30. Cost and Free-First Policy

Prefer the best viable free/open-source option first.

Evaluate:

- open-source model availability
- pretrained checkpoints
- local inference
- free/public datasets
- GEE access and quotas
- GPU availability
- CPU inference feasibility
- object storage costs
- API/inference costs
- expected prediction volume
- commercial licensing
- model/checkpoint license
- dataset license
- vendor lock-in

Use paid infrastructure when concrete requirements justify it, such as:

- production GPU throughput
- SLA
- large-scale inference
- managed model serving
- required proprietary data
- operational reliability

Do not choose an expensive foundation model when a simpler model meets the requirement.

Record material cost/licensing decisions in `project-memory/DECISIONS.md`.

---

## 31. Licensing and Model Governance

Before production use, verify:

- model license
- dataset license
- pretrained checkpoint license
- commercial-use restrictions
- attribution requirements
- redistribution restrictions
- geographic restrictions
- derivative-model requirements

Do not assume "open source" means unrestricted commercial use.

Record important license decisions.

---

## 32. Security

Never commit:

- API keys
- service-account credentials
- private model registry tokens
- cloud secrets
- database passwords

Validate uploaded geospatial data before processing.

Protect inference APIs against:

- oversized inputs
- malicious files
- path traversal
- SSRF
- resource exhaustion
- unauthorized model access
- unauthorized data access

Apply authentication and authorization before exposing private predictions or model endpoints.

---

## 33. Monitoring

Production GeoAI requires more than uptime monitoring.

Monitor:

### System

- latency
- throughput
- memory
- GPU utilization
- failures
- queue depth

### Data

- missing bands
- invalid geometry
- input distribution
- resolution changes
- temporal coverage
- sensor changes

### Model

- confidence drift
- prediction distribution
- error metrics when labels arrive
- geographic drift
- class distribution changes

### Cost

- compute
- storage
- inference requests
- export volume

Create alerts for meaningful degradation.

---

## 34. Model Versioning

Never silently replace a production model.

Track:

- model version
- training dataset version
- code commit
- configuration
- metrics
- deployment date
- status

Use explicit model promotion:

```text
Experimental
   ↓
Validated
   ↓
Candidate
   ↓
Production
   ↓
Retired
```

Keep rollback capability where practical.

---

## 35. Testing

Test at multiple levels.

### Data tests

- expected bands/features
- schema
- CRS
- geometry validity
- missing values
- label ranges

### Preprocessing tests

- scaling
- masking
- feature calculations
- normalization
- deterministic outputs

### Model tests

- model loads
- expected input/output shape
- deterministic inference where expected
- checkpoint compatibility

### Spatial tests

- correct georeferencing
- output extent
- tile boundaries
- geometry validity
- no spatial shift

### API tests

- authentication
- validation
- inference request/response schema
- error handling
- timeout behavior

### Regression tests

Maintain representative fixtures and compare:

- metrics
- sample predictions
- output schema
- spatial statistics

Avoid using a full production-scale dataset for every code change.

---

## 36. Failure Handling

When GeoAI fails:

1. Capture the exact error.
2. Identify whether it is data, preprocessing, model, GPU, dependency, memory, API, or spatial.
3. Reproduce on the smallest representative dataset.
4. Verify the input contract.
5. Verify preprocessing consistency.
6. Check model/checkpoint compatibility.
7. Inspect resource usage.
8. Fix the root cause.
9. Re-run targeted tests.
10. Validate that the fix did not change scientific meaning.
11. Update project memory.

Do not hide model failures by silently dropping difficult samples.

Do not change evaluation methodology merely to make the metrics improve.

---

## 37. Common Anti-Patterns

Avoid:

- random pixel splits with severe spatial autocorrelation
- training on leaked validation/test data
- undocumented labels
- mixing incompatible sensor preprocessing
- ignoring CRS or spatial resolution
- evaluating only global accuracy
- reporting only one metric
- using a foundation model without a baseline
- fine-tuning everything by default
- treating confidence as calibrated probability without evidence
- ignoring geographic domain shift
- loading country-scale imagery into memory
- synchronous HTTP inference for batch jobs
- exposing model endpoints without authentication
- committing model/cloud credentials
- silently replacing production models
- ignoring model/dataset licenses
- choosing paid infrastructure without a concrete requirement
- claiming production readiness from a notebook demo

---

## 38. Definition of Done

A GeoAI implementation is complete only when:

- [ ] The spatial prediction problem is explicit.
- [ ] Prediction unit and spatial support are defined.
- [ ] Input and label provenance are documented.
- [ ] Dataset construction is reproducible.
- [ ] Spatial/temporal leakage has been considered.
- [ ] A defensible baseline exists where appropriate.
- [ ] Model selection is justified.
- [ ] Training configuration is recorded.
- [ ] Evaluation methodology matches deployment goals.
- [ ] Spatial error analysis is performed.
- [ ] Domain shift has been considered.
- [ ] Inference architecture is appropriate.
- [ ] Large-scale inference is safe and resumable where needed.
- [ ] Output CRS/georeferencing is correct.
- [ ] Prediction metadata/model versioning is implemented.
- [ ] Uncertainty/confidence is handled appropriately.
- [ ] Security controls are present.
- [ ] Licensing has been checked.
- [ ] Cost/compute requirements are understood.
- [ ] Representative tests pass.
- [ ] Production monitoring requirements are defined where applicable.
- [ ] Project memory is updated.

Do not claim completion because a model trains successfully or because a benchmark score looks good.

---

## 39. Project-Memory Handoff

Before ending a GeoAI task, update project memory.

### STATE.md

Record:

- active model/workflow
- dataset version
- last verified training/inference step
- files changed
- validation performed
- current blocker
- exact next action

### TASKS.md

Record:

- completed experiments
- active experiment/task
- next experiment
- failed jobs
- pending validation

### DECISIONS.md

Record durable decisions such as:

- model family
- baseline selection
- foundation model selection
- dataset/label strategy
- spatial split strategy
- preprocessing
- inference architecture
- GEE vs external processing
- serving architecture
- cost/licensing decision

### SESSION.md

Record:

- experiments executed
- metrics obtained
- model/checkpoint used
- data version
- important observations
- exact resume point

### BLOCKERS.md

Record unresolved:

- missing labels
- GPU limitations
- model compatibility
- dataset access
- licensing questions
- inference failures
- scientific uncertainty

Never store credentials, tokens, or private keys in project memory.

---

## 40. Handoff Summary

When handing a GeoAI task to another session or agent:

```text
GeoAI task:
Prediction unit:
Target:
Input datasets:
Label dataset/version:
Spatial split:
Temporal split:
Preprocessing:
Baseline:
Model/checkpoint:
Training configuration:
Evaluation protocol:
Metrics:
Spatial error findings:
Inference architecture:
Output format:
Model version:
Cost/licensing:
Last verified result:
Current blocker:
Exact next action:
```

The next agent must inspect the actual repository, dataset manifests, model artifacts, and evaluation outputs before trusting this summary.
