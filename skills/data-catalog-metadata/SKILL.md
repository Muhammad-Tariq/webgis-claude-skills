# Spatial Data Catalog & Metadata

## Purpose
Design discoverable, trustworthy, searchable, and interoperable catalogs for spatial datasets, services, imagery, LiDAR, analytical products, and GeoAI outputs.

## Mandatory Preflight
Read STATE.md, TASKS.md, DECISIONS.md, SESSION.md, and BLOCKERS.md when present. Inspect existing data models, APIs, storage, GeoServer/OGC services, processing pipelines, and documentation.

## Core Metadata
Record where applicable:
- title, abstract, keywords
- owner/provider and contact
- source, lineage, processing history
- license and access constraints
- acquisition and update dates
- spatial and temporal extent
- geometry type, CRS, scale/resolution
- format, size, version
- quality indicators
- preview/thumbnail
- service URL or data reference

## Spatial Discovery
Support search by text, keyword, bbox/geometry, administrative area, time, dataset type, provider, resolution, CRS, license, and access level. Keep spatial search server-side and indexed.

## Dataset Lifecycle
Track:
discovered → registered → validated → published → updated → deprecated → archived

Preserve versions when analytical reproducibility matters.

## Remote-Sensing and LiDAR Metadata
For imagery record sensor, platform, acquisition time, processing level, bands, quality/cloud information, resolution, nodata, scale/offset, and source identifiers.

For LiDAR record acquisition method, density, classification, horizontal/vertical accuracy, CRS/vertical datum, tiling, and processing version.

## Service Metadata
For WMS/WFS/WMTS/OGC API services record endpoint, service type, capabilities/conformance, supported CRS, collections/layers, formats, access policy, provider, update frequency, and terms.

## Quality and Provenance
Distinguish source data, transformed data, derived indicators, model predictions, and visualization products. Record provenance through the processing chain.

## Catalog API
Define stable contracts for dataset search, spatial/temporal search, dataset detail, metadata retrieval, preview, download/service access, and version history. Use pagination and bounded spatial queries.

## Access Control
Metadata may be public while data is restricted. Support public, private, tenant-specific, and restricted datasets without exposing private paths, credentials, or sensitive geometry.

## Validation
Validate required metadata, CRS identifiers, extents, dates, licenses, service links, file references, geometry extents, and dataset/version identifiers.

## Interoperability
Evaluate standards according to consumers and requirements:
- STAC for spatiotemporal assets
- OGC API - Records
- ISO 19115-family metadata
- DCAT for broader catalog integration

## Performance and Cost
Index text, dates, spatial extents, and dataset types. Do not load entire catalogs into browsers. Prefer open standards/open-source catalog components when adequate and document managed-service requirements.

## Definition of Done
- metadata model defined
- spatial/temporal discovery works
- provenance represented
- access rules enforced
- metadata validated
- versions traceable
- service/data links tested
- interoperability requirements addressed
- project memory updated

## Project-Memory Handoff
Record metadata schema, catalog architecture, standards, indexing, validation rules, known gaps, and exact next action in STATE.md, TASKS.md, DECISIONS.md, SESSION.md, BLOCKERS.md, and CHANGELOG.md as appropriate. Never store secrets.