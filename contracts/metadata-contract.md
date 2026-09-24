# Metadata Contract

## Purpose

Provide consistent metadata for datasets, services, models, and derived GIS products.

## Required

- identifier
- title
- description
- version
- owner/source
- license
- spatial extent
- temporal extent when applicable
- CRS
- data format
- update frequency
- lineage/provenance
- quality/limitations
- access conditions
- created/updated timestamps

## GIS Extensions

Record when relevant:
- sensor/platform
- processing level
- resolution
- bands
- nodata
- vertical datum
- point-cloud density
- model version
- analytical method

## Provenance

Derived products must identify:
- input datasets
- transformations
- processing/model versions
- parameters
- execution timestamp
- producing application/version

## Privacy and Security

Do not publish sensitive locations, credentials, internal endpoints, or restricted metadata merely because a metadata record exists.
