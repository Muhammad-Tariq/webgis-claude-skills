# Storage Decision Matrix

## Candidates
Filesystem, object storage, PostgreSQL/PostGIS, GeoPackage/SQLite, hybrid.

## Rules
- Authoritative structured spatial transactions: PostGIS.
- Large immutable/derived rasters and files: object storage.
- Local/offline project data: GeoPackage/SQLite.
- Small application-local artifacts: filesystem may be sufficient.
- Separate authoritative data from caches and derived delivery artifacts.

## Checks
Size, access pattern, transactionality, concurrency, lifecycle, backup, versioning, security, egress, cost.
