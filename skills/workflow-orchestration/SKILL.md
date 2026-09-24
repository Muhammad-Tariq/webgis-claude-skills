# GIS Workflow Orchestration

## Purpose
Design reliable multi-step workflows for GIS ingestion, ETL, raster processing, remote sensing, GeoAI, exports, publishing, and scheduled analysis.

## Mandatory Preflight
Read project memory and inspect APIs, workers, queues, storage, databases, GEE, GeoServer, and deployment architecture.

## Workflow Model
Use explicit stages such as:
queued → validated → processing → QA → publishing → completed
and explicit failure/retry states.

Define inputs, outputs, dependencies, retry policy, timeout, cancellation, idempotency, resource limits, progress, and cleanup.

## Execution Strategy
Use synchronous requests for small predictable work, background jobs for expensive work, scheduled workflows for recurring analysis, DAG/workflow engines for complex dependencies, and batch processing for large datasets.

Do not introduce a workflow engine when a simple durable queue is sufficient.

## Idempotency and Checkpoints
Identify rerunnable stages using dataset/version, parameters, code/model version, target output, and workflow version. Persist useful checkpoints for expensive stages without making checkpoints costlier than recomputation.

## Lineage and Scheduling
Track input versions, processing code/version, parameters, outputs, timestamps, environment, and model version. For schedules define timezone, duration, overlap policy, missed-run behavior, backfill, and dependency freshness.

## Resource Controls
Limit worker concurrency, database connections, CPU, RAM, GPU, temporary disk, network, and external-provider quotas.

## GIS Patterns
Imagery: discover → filter → preprocess → composite → derive → QA → publish.
Vector ETL: ingest → validate → normalize → reproject → clean → load → index → publish.
GeoAI: prepare → tile → infer → merge → validate → publish.
GeoServer: prepare → validate → publish → style → cache → smoke-test.
Reporting: query → analyze → render → export → archive.

## External Providers
For GEE, routing, geocoding, satellite catalogs, and similar services, enforce quotas, retry only safe transient failures, use backoff, distinguish permanent errors, and avoid uncontrolled parallelism.

## Recovery
A stopped workflow should resume from the last verified checkpoint where safe. Do not restart expensive completed stages after a crash without checking durable state.

## Observability
Every workflow should expose workflow/job/stage ID, status, timestamps, duration, retry count, progress, error category, and input/output references. Integrate with the observability skill.

## Failure Handling
Classify invalid input, validation failure, provider failure, timeout, quota, infrastructure failure, data corruption, and code defect. Do not endlessly retry deterministic failures.

## Testing
Test happy path, retry, timeout, cancellation, duplicate submission, partial failure, provider outage, worker restart, database/storage failure, corrupted input, concurrency, and checkpoint recovery.

## Cost-Aware Design
Prefer incremental processing, cached immutable intermediates, batching, right-sized workers, and open-source tooling when adequate. Track compute, storage, egress, provider usage, GPU, and worker idle time.

## Definition of Done
- stages explicit
- state durable
- retries safe
- idempotency defined
- checkpoints justified
- lineage recorded
- resource limits defined
- failures classified
- recovery tested
- observability integrated
- cost understood
- project memory updated

## Project-Memory Handoff
Record workflow topology, state model, checkpoint strategy, retry rules, provider dependencies, recovery evidence, blockers, and exact next action.