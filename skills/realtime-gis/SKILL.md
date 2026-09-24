# Real-Time GIS

## Purpose
Design systems that ingest, process, stream, visualize, and alert on continuously changing geospatial data.

## Mandatory Preflight
Read project memory and inspect frontend/map architecture, spatial API, PostGIS schema, stream infrastructure, authentication, deployment, and observability.

## Define Real Time
Specify event latency target, update frequency, acceptable staleness, ordering guarantees, delivery guarantees, retention, coverage, and expected event volume. Do not label polling real-time without explicit latency semantics.

## Event Model
Define event ID, entity ID, event timestamp, ingestion timestamp, geometry/location, type, payload, source, sequence/version, and quality/status. Prefer immutable events plus derived current state where auditability matters.

## Ingestion
Use the smallest suitable mechanism:
- HTTP
- WebSocket
- Server-Sent Events
- MQTT
- message queues/streams
- scheduled polling

Validate payloads and coordinates at ingestion.

## Streaming Architecture
Typical pattern:
source → broker/stream → processor → PostGIS/current state → API → map clients

For simple workloads:
source → API → PostGIS → WebSocket/SSE → clients

Choose architecture according to volume, latency, reliability, and operational needs.

## Spatial Processing
Support geofencing, point-in-polygon, nearest-feature matching, speed/distance, clustering, tracks, and alerts using indexed and bounded computations. Avoid recomputing complete history for every event.

## State and History
Separate current entity state, historical events, derived tracks, and alerts. This prevents live dashboards from scanning huge history tables on every update.

## Frontend
Use stable feature IDs, incremental updates, batching/throttling, viewport filtering, and correct WebSocket/SSE lifecycle management. Define disconnect/reconnect behavior.

## Ordering and Duplicates
Handle late, duplicate, out-of-order, missing-sequence, and clock-skewed events. Do not assume network arrival order equals event order.

## Geofencing and Alerts
Define geometry, entry/exit semantics, debounce/hysteresis, cooldown, severity, recipient, and audit record. Prevent GPS jitter from generating repeated alerts.

## Retention
Define hot data, warm history, archive, retention period, partitioning, and aggregation. High-frequency telemetry must not grow indefinitely without a retention strategy.

## Security and Privacy
Apply authentication, authorization, tenant isolation, channel access control, rate limits, encryption, location minimization, retention limits, and audit logging. Never broadcast one tenant's locations to another.

## Reliability
Design for broker/provider outage, client reconnect, duplicates, database failure, backpressure, and overload. Explicitly choose at-most-once, at-least-once, or effectively-once semantics.

## Performance
Measure ingestion throughput, end-to-end latency, connected clients, messages per client, database write latency, stream lag, map update cost, memory, CPU, and dropped/coalesced updates.

## Testing
Test invalid coordinates, burst traffic, reconnects, duplicates, ordering, stale events, geofence boundaries, authorization, tenant isolation, outages, backpressure, frontend lifecycle, and long-session memory growth.

## Definition of Done
- freshness/latency target defined
- event contract documented
- ingestion validation exists
- ordering/duplicate behavior defined
- state/history separated
- client updates incremental
- reconnect works
- authorization/tenant isolation enforced
- retention exists
- overload handled
- monitoring exists
- representative load tests pass
- project memory updated

## Project-Memory Handoff
Record event schema, transport, broker/provider, latency target, state/history design, retention, alert semantics, tests, operational limits, blockers, and exact next action.