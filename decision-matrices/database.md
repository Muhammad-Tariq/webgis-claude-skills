# Database Decision Matrix

## Candidates
PostgreSQL + PostGIS, GeoPackage/SQLite, or another spatial database when justified.

## Rules
- Shared transactional spatial application: evaluate PostgreSQL/PostGIS first.
- Offline/local desktop project: evaluate GeoPackage/SQLite first.
- Large shared vector workloads: verify PostGIS indexing/query plans before introducing another database.
- Specialized database only when a documented requirement cannot be met adequately.

## Checks
Transactions, spatial operators, indexes, concurrency, CRS support, raster needs, offline use, backup/recovery, tooling, interoperability, cost.
