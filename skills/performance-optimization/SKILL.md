undefined

---

## 28. Free-First and Provider Discipline

Performance optimization must not automatically introduce a paid map, tile, geocoding, routing, CDN, database, or observability provider.

Evaluate the existing free/open-source stack first:

- MapLibre/OpenLayers/Leaflet/Cesium
- PostGIS/PostgreSQL
- GeoServer/GeoWebCache
- GDAL/OGR
- browser-native caching and workers
- self-hosted reverse proxy/CDN-compatible caching
- object storage already available in the deployment

When evaluating an external provider, distinguish:

- map rendering library
- basemap provider
- tile provider
- geocoding provider
- routing provider
- GIS/OGC service
- database
- object storage
- compute/GPU
- CDN/cache
- observability platform

Check:

- free-tier limits
- request quotas
- attribution requirements
- commercial-use terms
- coverage
- freshness
- latency
- SLA
- self-hosting/offline options
- vendor lock-in
- expected traffic
- recurring cost

Public OpenStreetMap data and public OSM tile infrastructure are not the same thing. Do not treat public OSM tiles as an unlimited production API.

Record durable provider/licensing decisions in `project-memory/DECISIONS.md`.

---

## 29. No Premature Optimization

Do not:

- rewrite a framework solely for performance
- introduce a distributed cache before proving a cache bottleneck
- add a GPU before measuring CPU throughput
- replace PostGIS with another database without evidence
- add workers where transfer overhead dominates
- precompute data that must remain fresh
- add infrastructure complexity to solve an unmeasured problem

Prefer the smallest change that materially improves the measured bottleneck.

---

## 30. Production Handoff

When an optimization is verified, document:

- workload and dataset
- baseline and post-change measurements
- configuration changes
- capacity assumptions
- new operational dependencies
- cache invalidation behavior
- rollback procedure
- monitoring signal
- expected regression threshold
- cost impact

Then update project memory and commit the verified state.
