# 3D Geospatial Engineering

## Purpose

Design, implement, optimize, and validate production 3D geospatial applications covering terrain, buildings, point clouds, 3D Tiles, glTF assets, photogrammetry, BIM-adjacent spatial visualization, and globe-scale visualization.

Use this skill when 2D Web GIS is insufficient and elevation, volumetric context, realistic terrain, massive 3D datasets, or 3D spatial interaction is part of the product.

## Mandatory Preflight

Read:

- `project-memory/STATE.md`
- `project-memory/TASKS.md`
- `project-memory/DECISIONS.md`
- `project-memory/SESSION.md`
- `project-memory/BLOCKERS.md` when present

Inspect:

- frontend framework
- map/3D engine
- CRS/vertical datum
- source data
- terrain/imagery strategy
- point-cloud/building data
- API/storage architecture
- current performance evidence

## 1. Select the 3D Engine

Choose based on requirements.

### CesiumJS

Consider for:

- globe visualization
- terrain
- 3D Tiles
- time-dynamic geospatial scenes
- large-scale 3D datasets

### Three.js

Consider for:

- custom 3D visualization
- application-specific scenes
- rendering beyond conventional GIS globe workflows

### MapLibre/OpenLayers

Use their 3D capabilities when they satisfy the product without adding an unnecessary separate engine.

Do not introduce a second rendering engine without a concrete requirement.

## 2. Coordinate Systems

Document:

- horizontal CRS
- vertical CRS/datum
- ellipsoidal vs orthometric heights
- units
- local engineering coordinates
- globe/geocentric representation
- transformation pipeline

Vertical reference errors can make an otherwise correct 3D scene materially wrong.

## 3. Terrain

For terrain:

- choose an appropriate DEM source
- preserve required vertical accuracy
- generate suitable terrain pyramids/tiles
- control level of detail
- handle nodata and voids
- avoid loading full-resolution terrain unnecessarily
- validate heights against known references

Separate visualization-grade terrain from analysis-grade elevation data.

## 4. 3D Tiles and Large Scenes

For large buildings, photogrammetry, BIM-derived scenes, or point-cloud-derived models:

- use tiled streaming
- select appropriate level of detail
- define geometric error
- avoid loading the entire scene
- use spatial subdivision
- minimize unnecessary properties
- cache immutable tiles
- measure tile sizes and request patterns

Test both initial view and sustained navigation.

## 5. Point Clouds

For LiDAR/point clouds:

- classify points where useful
- preserve required attributes
- build spatial indexes
- use appropriate tiling/chunking
- stream visible regions
- use level of detail
- avoid sending raw LAS/LAZ directly to the browser when a streaming representation is more appropriate

Use the dedicated point-cloud/LiDAR skill for detailed acquisition and processing workflows.

## 6. 3D Buildings and BIM

Define semantics for:

- building identity
- floors
- heights
- roof structures
- materials
- attributes
- temporal state

Do not confuse visual 3D models with authoritative engineering/BIM data.

For BIM-adjacent integration, define a clear conversion boundary and preserve source identifiers.

## 7. Photogrammetry and Meshes

For drone/photogrammetry meshes:

- validate coordinate reference
- preserve texture relationships
- simplify only for visualization
- tile large meshes
- retain a source/high-resolution artifact separately
- document processing software/version
- verify alignment against control/reference data

Do not destroy source data through irreversible visualization optimization.

## 8. 3D Interaction

Design explicit interactions:

- camera navigation
- object selection
- hover/inspect
- measurement
- clipping/sectioning
- visibility controls
- layer filtering
- terrain exaggeration
- time controls where relevant

3D measurement must account for terrain, vertical dimension, and CRS semantics.

## 9. 3D + 2D Coordination

Synchronize:

- selected feature
- layer visibility
- filters
- time
- analysis result
- camera/extent where useful

Use stable identifiers across 2D and 3D representations.

Avoid duplicating authoritative state between renderers.

## 10. Performance

Measure:

- first 3D render
- tile latency
- frame time
- FPS
- GPU memory
- CPU
- browser memory
- visible tile count
- draw calls where available

Use:

- level of detail
- frustum/visibility culling
- tiled streaming
- progressive loading
- simplified models
- compressed assets
- cached immutable resources

Do not optimize solely for FPS if interaction latency, loading, or analytical correctness is the actual bottleneck.

## 11. Mobile and Hardware Constraints

3D can exceed low-end device limits quickly.

Define supported hardware/browser classes.

Provide graceful degradation:

- reduced terrain quality
- fewer visible layers
- 2D fallback
- simplified models
- disabled expensive effects

Never leave users with an unusable blank scene when a 2D fallback is viable.

## 12. Security and Data Access

Protect:

- private building models
- infrastructure locations
- survey data
- sensitive point clouds
- signed/private tile URLs
- download endpoints

Authorize tile/data access before expensive generation or retrieval.

Do not expose hidden source assets simply because their rendered representation is public.

## 13. Testing

Test:

- CRS/vertical datum
- terrain alignment
- model placement
- camera navigation
- object selection
- measurement
- LOD transitions
- tile loading/failure
- large-scene behavior
- memory growth
- mobile degradation
- 2D/3D state synchronization

Use representative datasets rather than toy scenes only.

## 14. Cost-Aware and Free-First Policy

Prefer open-source/free components where adequate.

Evaluate:

- self-hosted terrain/tiles
- open-source rendering engines
- object storage
- CDN/cache
- hosted 3D tile providers

Check licensing, quotas, bandwidth, storage, attribution, and commercial-use requirements.

Do not assume public terrain/imagery endpoints are unlimited production infrastructure.

## Definition of Done

- engine choice is justified
- horizontal and vertical CRS are documented
- terrain/model placement is validated
- large datasets use appropriate tiling/LOD
- 3D interactions are tested
- 2D integration is coherent
- performance is measured
- security/access control is applied
- mobile/degraded behavior is defined
- licensing/provenance is documented
- project memory is updated

## Project-Memory Handoff

Record:

- engine and rendering decisions
- CRS/vertical datum
- dataset/LOD strategy
- performance measurements
- known hardware limits
- verified tests
- exact next action
- blockers and licensing decisions

Update `STATE.md`, `TASKS.md`, `DECISIONS.md`, `SESSION.md`, `BLOCKERS.md`, and `CHANGELOG.md` as appropriate.
