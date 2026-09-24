# Point Cloud Decision Matrix

## Candidates
LAS/LAZ, COPC, PDAL, 3D Tiles, object storage, database-backed approaches, desktop processing.

## Rules
- Processing pipelines: evaluate PDAL with LAS/LAZ.
- Cloud/browser streaming of large point clouds: evaluate COPC and/or 3D Tiles depending on visualization architecture.
- Local/offline workflows: evaluate LAS/LAZ plus PDAL.
- Database storage only when spatial query/integration requirements justify it.

## Checks
Point count, density, attributes, spatial indexing, streaming, LOD, CRS/vertical datum, processing versus visualization needs.
