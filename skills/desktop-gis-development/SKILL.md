# Desktop GIS Development

## Purpose

Engineer production-grade desktop GIS applications, plugins, offline spatial tools, scientific workstations, and desktop processing applications.

## Architecture

Prefer clear boundaries:

UI / Map Canvas
→ Application Services / Use Cases
→ GIS Domain
→ Processing Engine
→ Data Access
→ GDAL / PROJ / GEOS / PDAL / PyQGIS or selected native libraries
→ Files / GeoPackage / PostGIS / Object Storage

Keep UI code independent from spatial algorithms and provider-specific infrastructure.

## Framework Selection

Evaluate:
- Qt + PySide6/PyQt
- QGIS plugin architecture
- Electron
- Tauri
- .NET desktop
- other native/cross-platform frameworks when justified

Use the technology-decision-engine and desktop decision matrix.

### Qt / PySide / PyQt

Strong candidate for:
- native-feeling cross-platform GIS tools
- custom map canvases
- local processing
- Python GIS ecosystem integration
- GDAL/PROJ/GEOS/PDAL workflows

### QGIS Plugin

Strong candidate when:
- users already operate in QGIS
- QGIS rendering and processing should be reused
- the application is an extension rather than a standalone product

Respect QGIS plugin lifecycle, API compatibility, packaging, and version support.

### Electron / Tauri

Use when:
- web UI reuse materially reduces development cost
- desktop packaging is important
- native GIS processing can be isolated behind local services/workers

Do not place heavy raster, LiDAR, or spatial processing on the UI thread.

## Core Desktop Architecture

Separate:
- presentation
- application services
- domain/spatial logic
- data access
- processing
- background workers
- configuration
- local cache
- external integrations

Use adapters for:
- map engine
- filesystem
- database
- GDAL
- PDAL
- remote APIs
- authentication
- update services

## Map Canvas

A desktop map canvas should support, where required:
- pan/zoom
- layer tree
- visibility
- selection
- identify
- measurement
- editing
- drawing
- snapping
- coordinate display
- CRS selection
- symbology
- labels
- scale
- print/layout workflows

Do not couple analytical operations directly to rendering state.

## Local Data

Evaluate:
- GeoPackage
- SQLite
- GeoJSON for small interchange datasets
- FlatGeobuf where appropriate
- Shapefile only when compatibility requires it
- Cloud/remote sources when online behavior is required
- PostGIS for shared enterprise data

Validate:
- format
- CRS
- geometry validity
- schema
- encoding
- file size
- permissions
- locking behavior

## Raster Engineering

Support large rasters without loading entire datasets into memory.

Use:
- windowed reads
- tiling
- overviews
- COG where appropriate
- GDAL/rasterio
- background processing
- temporary storage controls

Track:
- CRS
- resolution
- extent
- nodata
- data type
- scale/offset
- band semantics

## LiDAR / Point Cloud

For large point clouds:
- use PDAL or appropriate native tooling
- stream/chunk processing
- spatial indexing
- LAS/LAZ/COPC where appropriate
- background jobs
- progress reporting
- cancellation
- temporary-file lifecycle

Do not load multi-million-point datasets into ordinary UI state.

## Background Processing

Long-running work must not block the UI.

Jobs should support:
- queued/running/completed/failed/cancelled states
- progress
- cancellation
- retry where safe
- logs
- resource limits
- temporary artifact cleanup
- persisted failure information
- recovery after application restart when practical

Examples:
- raster reprojection
- raster calculations
- mosaicking
- vector conversion
- LiDAR classification
- tiling
- GeoAI inference
- imports/exports
- spatial analysis

## Crash Recovery

For important operations:
- persist job state
- use checkpointed intermediate artifacts where useful
- make operations idempotent
- avoid destructive replacement until output validation succeeds
- preserve diagnostic logs
- recover or safely discard incomplete temporary files

A crash must not silently corrupt the source dataset.

## Offline-First

When offline capability is required:
- identify authoritative local data
- define synchronization boundaries
- cache remote metadata/data deliberately
- queue operations that can be deferred
- handle conflicts explicitly
- expose connection state
- never pretend stale data is current

## Project Files

If the application supports projects, define:
- project metadata
- layer references
- layer styles
- CRS
- map views
- analysis settings
- data-source references
- application version
- compatibility/migration rules

Avoid embedding large authoritative datasets inside project files unless that is an explicit requirement.

## Editing

For editing workflows:
- validate geometry before commit
- support undo/redo where practical
- define transaction boundaries
- prevent accidental destructive operations
- preserve attribute constraints
- handle concurrent edits for shared data
- record provenance where required

## Security

Desktop applications still require:
- input validation
- safe archive/file extraction
- path traversal protection
- untrusted dataset handling
- secure credential storage
- dependency security
- update verification
- least privilege
- safe temporary directories

Treat downloaded GIS data as untrusted input.

## Packaging and Distribution

Plan:
- supported operating systems
- native dependencies
- installer format
- code signing when required
- update mechanism
- rollback
- configuration migration
- cache migration
- user data preservation

Test clean installation, upgrade, downgrade/rollback where supported, and uninstall behavior.

## Testing

Use:
- unit tests
- spatial correctness tests
- raster fixtures
- point-cloud fixtures
- integration tests
- filesystem tests
- offline-mode tests
- crash/recovery tests
- packaging tests
- UI/E2E tests
- performance tests

Critical GIS calculations must use known-result fixtures and the GIS correctness skill.

## Performance

Measure:
- startup time
- project-open time
- layer-load time
- map interaction latency
- memory usage
- worker throughput
- raster processing time
- point-cloud processing time
- export time

Use streaming, chunking, indexes, caches, and workers based on measurements.

## Definition of Done

A desktop GIS feature is complete when:
- architecture boundaries are respected
- spatial correctness is verified
- UI remains responsive during heavy work
- cancellation/recovery behavior is defined
- data integrity is protected
- security checks pass
- tests pass
- packaging/install behavior is verified
- performance is acceptable for the verified dataset scale
- documentation and project memory are updated
