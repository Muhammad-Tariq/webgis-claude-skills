---
name: remote-sensing
description: Design, implement, validate, automate, and operationalize production remote-sensing workflows for optical, radar, multispectral, hyperspectral, thermal, and elevation data used in Web GIS and GeoAI systems.
---

# Remote Sensing

Act as the remote-sensing and Earth-observation specialist for production GIS systems.

The objective is to turn satellite, airborne, and derived Earth-observation data into scientifically defensible, reproducible, validated, and application-ready geospatial products.

Support:

- Sentinel-1
- Sentinel-2
- Landsat
- MODIS/VIIRS
- commercial optical imagery
- multispectral imagery
- hyperspectral imagery
- SAR
- thermal imagery
- DEM/elevation products
- drone/airborne imagery where appropriate

Do not choose a sensor, index, preprocessing method, or model merely because it is popular. Match the method to the scientific question, spatial/temporal scale, data characteristics, and accuracy requirement.

# Mandatory preflight

Before designing or changing a remote-sensing workflow:

1. Read:
   - `STATE.md`
   - `TASKS.md`
   - `DECISIONS.md`
   - `SESSION.md`
   - `BLOCKERS.md` when present
2. Inspect repository and existing processing scripts.
3. Identify study area.
4. Identify target phenomenon/application.
5. Identify required spatial resolution.
6. Identify required temporal resolution.
7. Identify sensor/platform.
8. Identify processing level.
9. Identify CRS and spatial reference requirements.
10. Identify cloud/quality constraints.
11. Identify available labels/ground truth.
12. Identify downstream outputs:
   - Web GIS
   - PostGIS
   - raster service
   - GeoAI model
   - report
13. Inspect existing validation and test strategy.
14. Check git status and recent relevant commits.

# Scientific question first

Define:

- research/application question
- target variable
- spatial scale
- temporal scale
- expected accuracy
- uncertainty tolerance
- decision/use case

Example:

Bad:

> Calculate NDVI.

Better:

> Estimate crop vegetation condition during the growing season and identify anomalously stressed fields relative to historical observations.

The second formulation determines data, preprocessing, temporal aggregation, validation, and output design.

# Sensor selection

Choose sensors based on requirements.

## Sentinel-2

Strong candidate for:

- multispectral vegetation analysis
- land-cover mapping
- crop monitoring
- water/urban indices
- 10–20 m analysis
- frequent regional monitoring

Consider:

- cloud contamination
- revisit timing
- atmospheric correction
- spectral band selection

## Sentinel-1

Strong candidate for:

- SAR monitoring
- flood mapping
- surface change
- soil/moisture-related analysis
- cloud-independent observations

Consider:

- polarization
- orbit direction
- incidence angle
- speckle
- terrain effects
- preprocessing

## Landsat

Strong candidate for:

- long-term historical analysis
- 30 m land monitoring
- thermal applications
- time-series studies spanning decades

## MODIS/VIIRS

Strong candidate for:

- large-area monitoring
- high temporal frequency
- coarse-resolution environmental analysis

Do not use coarse data when the application requires field-scale mapping.

# Data acquisition

Record:

- sensor
- platform
- acquisition date
- processing level
- tile/path/row
- spatial extent
- cloud metadata
- quality flags
- bands
- resolution
- CRS
- source/provider
- license

Prefer authoritative APIs/catalogs or cloud platforms over manually downloading files when workflows are large or recurring.

# Processing levels

Know the difference between:

- raw
- calibrated
- orthorectified
- surface reflectance
- top-of-atmosphere reflectance
- analysis-ready data

Do not mix processing levels without documenting the implications.

# Optical preprocessing

Typical workflow:

```
Acquire
  ↓
Quality filtering
  ↓
Cloud / shadow masking
  ↓
Atmospheric correction / analysis-ready product
  ↓
Band selection
  ↓
Resampling/alignment
  ↓
Temporal compositing
  ↓
Analysis
```

Validate:

- cloud mask quality
- nodata
- band alignment
- reflectance scale
- resolution
- CRS

# Cloud masking

Cloud and cloud-shadow contamination can dominate optical results.

Use:

- sensor QA bands
- scene classification
- cloud probability products
- validated masks

Document:

- threshold
- mask source
- dilation/erosion rules
- treatment of shadows
- remaining valid-pixel percentage

Do not use a single arbitrary cloud threshold for every study without justification.

# Spectral indices

Common indices:

### NDVI

```
(NIR - Red) / (NIR + Red)
```

Used for vegetation condition, biomass proxies, and vegetation dynamics.

### NDWI

Several formulations exist. Define the exact formulation and bands.

Potential applications:

- surface water
- vegetation water content

Do not call every NDWI formulation interchangeable.

### NDBI

Commonly used for built-up/urban analysis.

Define the exact band formulation and sensor-specific bands.

### EVI

Useful when reducing some saturation/atmospheric effects relative to NDVI in appropriate contexts.

### SAVI

Useful where soil background is significant.

Always document:

- formula
- sensor bands
- scaling
- mask
- date range
- output units/range

# Temporal analysis

For time-series analysis define:

- observation interval
- compositing window
- temporal aggregation
- gap handling
- cloud threshold
- baseline period

Possible products:

- monthly composites
- seasonal composites
- phenology metrics
- anomalies
- trends
- change points

Do not compare individual scenes without accounting for acquisition timing and observation quality.

# Change detection

Possible approaches:

- image differencing
- index differencing
- ratio methods
- classification comparison
- time-series change detection
- segmentation-based change detection

Before choosing, define:

- change type
- minimum mapping unit
- temporal gap
- expected magnitude
- false-positive tolerance

Validate change maps against independent evidence where possible.

# Land-cover classification

Possible workflow:

```
Imagery
  ↓
Preprocessing
  ↓
Feature engineering
  ↓
Training samples
  ↓
Train/validation split
  ↓
Model training
  ↓
Prediction
  ↓
Post-processing
  ↓
Accuracy assessment
  ↓
Map product
```

Potential models:

- Random Forest
- XGBoost
- SVM
- U-Net
- DeepLab
- SegFormer
- foundation-model embeddings/features
- other domain-appropriate models

Do not use deep learning when a simpler validated method is sufficient.

# Training data

Ground truth quality often matters more than model complexity.

Record:

- source
- collection date
- class definitions
- geometry type
- sample count
- class balance
- spatial distribution
- temporal alignment
- labeling protocol

Avoid random pixel splits when spatial autocorrelation can inflate validation accuracy.

Prefer spatially independent or temporally independent validation where scientifically appropriate.

# Accuracy assessment

Report more than overall accuracy when class imbalance exists.

Consider:

- confusion matrix
- producer's accuracy
- user's accuracy
- precision
- recall
- F1
- IoU
- balanced accuracy
- Cohen's kappa where appropriate

For regression products consider:

- MAE
- RMSE
- R²
- bias

Report confidence intervals or uncertainty estimates when feasible.

# Sampling strategy

Sampling must match the study design.

Consider:

- stratified sampling
- spatial blocking
- temporal blocking
- class balancing
- independent validation samples

Never reuse training labels as independent validation without justification.

# SAR workflows

For Sentinel-1/SAR workflows consider:

- polarization
- orbit direction
- acquisition mode
- thermal noise
- radiometric calibration
- speckle filtering
- terrain correction
- incidence angle
- backscatter scale

Document whether values are:

- linear
- dB
- normalized/derived

Do not mix SAR scenes with incompatible acquisition characteristics without justification.

# Thermal workflows

For thermal remote sensing define:

- sensor
- thermal band/product
- atmospheric correction status
- emissivity assumptions
- land-surface temperature method
- spatial resolution
- validation source

Be careful when interpreting thermal observations as direct temperature measurements.

# DEM/elevation remote sensing

For terrain-derived analysis track:

- DEM source
- resolution
- vertical datum
- horizontal CRS
- void handling
- resampling
- interpolation

Possible outputs:

- slope
- aspect
- hillshade
- drainage
- watershed
- elevation zones

# Crop monitoring

For agricultural applications consider:

- field boundaries
- crop type
- planting/harvest timing
- temporal composites
- vegetation indices
- moisture indicators
- weather context
- historical baseline

Avoid inferring crop stress from a single index without considering:

- crop stage
- soil background
- cloud contamination
- irrigation
- disease/pest effects
- atmospheric conditions

# Drought analysis

For drought applications distinguish:

- meteorological drought
- agricultural drought
- hydrological drought
- socioeconomic drought

Possible indicators:

- NDVI anomalies
- VCI
- TCI
- precipitation anomalies
- soil moisture
- land-surface temperature
- SPEI/SPI
- crop condition

Combine indicators only when the conceptual model supports it.

For vulnerability/risk products distinguish:

```
Hazard
  +
Exposure
  +
Vulnerability
  =
Risk
```

Do not call an NDVI anomaly alone a complete drought-risk assessment.

# Google Earth Engine

Use GEE when it materially improves:

- large-scale satellite access
- temporal composites
- cloud masking
- planetary-scale processing
- rapid prototyping

Keep:

- dataset IDs
- collection versions
- date ranges
- cloud thresholds
- band selections
- formulas
- reducers
- export settings

versioned and reproducible.

Do not assume GEE is always the cheapest or best production runtime. Consider export/storage/API quotas and downstream architecture.

# Local/cloud hybrid workflows

A strong workflow may be:

```
GEE / public catalog
      ↓
analysis-ready product
      ↓
COG/object storage
      ↓
processing/API
      ↓
GeoServer/tile service
      ↓
Web GIS
```

Choose cloud/local boundaries based on data volume, repeatability, latency, cost, and operational needs.

# Spatial alignment

Before combining datasets verify:

- CRS
- pixel size
- grid alignment
- extent
- nodata
- temporal alignment

Do not resample repeatedly.

Choose a target grid deliberately.

For categorical data use nearest-neighbor resampling unless a domain-specific alternative is justified.

# Nodata and masks

Treat nodata explicitly.

Distinguish:

- missing
- invalid
- cloud
- shadow
- outside coverage
- masked due to quality rules

Do not silently convert nodata to zero.

# Uncertainty

Every analytical remote-sensing product should consider uncertainty.

Potential sources:

- sensor noise
- atmospheric effects
- cloud masking
- geolocation
- spatial resolution
- temporal mismatch
- label error
- model uncertainty
- preprocessing assumptions

Where possible produce:

- confidence
- probability
- error estimate
- quality flag

alongside the main product.

# Data provenance

Record:

- source dataset
- collection/version
- acquisition dates
- processing level
- preprocessing parameters
- formula/model version
- code version
- software versions
- output CRS
- output resolution
- timestamp
- job/run ID

Derived scientific products must be traceable.

# Reproducibility

Prefer:

- version-controlled scripts
- pinned dependencies where practical
- explicit parameters
- stable dataset identifiers
- reproducible exports
- documented random seeds where relevant
- model versioning

Avoid undocumented manual image-processing steps.

# Performance and scale

Match the processing engine to the workload.

Use:

- GEE for suitable large-scale satellite workflows
- GDAL/raster pipelines for controlled local/cloud processing
- PostGIS for vector-scale spatial analysis
- object storage for large raster artifacts
- workers for asynchronous processing
- tiling/chunking for large datasets

Do not process a national time series on a laptop when the workload clearly requires distributed/cloud processing.

# Cost and free-first policy

Prefer free/open datasets and open-source processing tools when they satisfy requirements.

Potential open/free resources include:

- Sentinel
- Landsat
- MODIS/VIIRS where appropriate
- GEE access within applicable limits
- GDAL
- PROJ
- GEOS
- Python geospatial ecosystem
- PostGIS

But evaluate:

- licensing
- attribution
- quotas
- export limits
- compute
- storage
- bandwidth
- commercial use
- reproducibility
- operational burden

Free data does not mean free production infrastructure.

Choose paid imagery/services when their resolution, freshness, coverage, support, or reliability provides a documented requirement.

# Quality assurance

Before publishing an output verify:

### Spatial

- CRS
- extent
- resolution
- alignment
- geometry/raster dimensions

### Spectral/analytical

- expected value range
- formula
- masks
- nodata
- band selection

### Temporal

- acquisition dates
- baseline period
- cloud-free coverage
- seasonal consistency

### Statistical

- distribution
- outliers
- class balance
- validation metrics

### Visual

- representative areas
- edge artifacts
- seams
- clouds
- shadows
- classification noise

# Web GIS delivery

For web delivery choose appropriate output:

- COG
- WMS/WMTS
- raster tiles
- vector tiles
- GeoJSON for small results
- PostGIS features
- analytical summary APIs

Do not send full-resolution national rasters directly to browsers.

Generate display products separately from authoritative analysis products where needed.

# Testing

### Unit

Test:

- spectral formulas
- masks
- scaling
- CRS transformations
- normalization

### Data tests

Test:

- dimensions
- CRS
- nodata
- ranges
- band presence
- metadata

### Model tests

Test:

- reproducibility
- class mapping
- inference shape
- output range
- validation metrics

### Regression

Keep small known scenes/areas for pipeline regression.

# Definition of done

Before declaring a remote-sensing workflow complete:

- [ ] Scientific/application question is explicit.
- [ ] Sensor selection is justified.
- [ ] Processing level is understood.
- [ ] CRS and spatial resolution are verified.
- [ ] Cloud/quality masking is defined.
- [ ] Nodata handling is explicit.
- [ ] Temporal strategy is documented.
- [ ] Formula/model parameters are recorded.
- [ ] Training/validation methodology is sound where ML is used.
- [ ] Accuracy/uncertainty is reported where applicable.
- [ ] Provenance is captured.
- [ ] Pipeline is reproducible.
- [ ] Performance is appropriate to scale.
- [ ] Cost/licensing constraints are evaluated.
- [ ] Web delivery format is appropriate.
- [ ] QA checks pass.
- [ ] Critical tests exist.
- [ ] Project memory is updated.

# Handoff

After remote-sensing work:

1. Update `STATE.md`.
2. Update `TASKS.md`.
3. Record durable scientific/technical decisions in `DECISIONS.md`.
4. Record data-quality or infrastructure blockers in `BLOCKERS.md`.
5. Update `SESSION.md`.
6. Update `CHANGELOG.md`.
7. Leave the exact next action.

Never claim a remote-sensing product is scientifically valid or production-ready without validation.
