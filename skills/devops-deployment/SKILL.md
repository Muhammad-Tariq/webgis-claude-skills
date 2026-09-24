# DevOps & Deployment

## Purpose

Use this skill to design, implement, validate, and operate production deployments for Web GIS systems. Deployment decisions must follow the project's actual requirements, architecture, traffic profile, data volume, reliability needs, security posture, team capability, and budget.

This skill is provider-neutral. It does not assume a particular VPS, cloud, container platform, framework, or managed service.

---

## 1. Mandatory Preflight

Before changing deployment infrastructure:

1. Read project memory:
   - `project-memory/STATE.md`
   - `project-memory/TASKS.md`
   - `project-memory/DECISIONS.md`
   - `project-memory/SESSION.md`
   - `project-memory/BLOCKERS.md` when present
2. Inspect repository structure and existing deployment files.
3. Check git status and recent relevant commits.
4. Identify the current frontend, API, database, GIS services, workers, storage, and external providers.
5. Determine the current verified deployment state.
6. Never replace an existing production deployment pattern without inspecting why it exists.

If memory conflicts with actual configuration, code, or deployment tests, trust verified implementation evidence and repair project memory.

---

## 2. Deployment Architecture First

Design the deployment topology before writing Dockerfiles, Compose files, CI/CD workflows, or infrastructure configuration.

Document:

- frontend runtime
- API runtime
- background workers
- job queue/broker when required
- PostGIS/database
- GeoServer or other OGC services
- object/raster storage
- reverse proxy/load balancer
- cache/CDN when useful
- DNS
- TLS certificates
- monitoring/logging
- backup targets
- external APIs/providers
- administrative access paths

Separate public, application, data, and administrative boundaries.

Prefer the simplest architecture that satisfies the requirements. Do not introduce Kubernetes, service meshes, microservices, or managed infrastructure merely because they are fashionable.

---

## 3. VPS vs Managed Cloud vs Platform

Choose infrastructure from requirements rather than habit.

Evaluate:

- expected traffic and concurrency
- CPU/RAM/storage requirements
- spatial database size and I/O
- raster/tile workload
- GPU requirements
- uptime/SLA
- geographic distribution
- backup and disaster-recovery requirements
- operational expertise
- security/compliance requirements
- deployment frequency
- observability requirements
- vendor lock-in
- monthly and annual cost

### Free-first / cost-aware policy

Prefer a genuinely free or open-source option when it is technically adequate and operationally responsible.

Do not interpret free as automatically better. Compare:

- free-tier limits
- compute/storage quotas
- bandwidth/egress costs
- API/request limits
- managed-service premiums
- backup costs
- support/SLA
- operational time
- scaling constraints
- licensing/commercial terms
- migration/vendor-lock-in risk

Record durable infrastructure choices in project memory.

---

## 4. Containerization

Use containers when they improve reproducibility, isolation, deployment consistency, or operational simplicity.

Define clear service boundaries such as:

- frontend
- API
- worker
- PostGIS
- GeoServer
- cache/queue
- reverse proxy

Avoid unnecessary containers for components that do not benefit from isolation.

Docker/Compose configurations should include:

- pinned or controlled image versions
- non-root execution where practical
- explicit ports
- persistent volumes for stateful services
- health checks
- resource limits where appropriate
- restart policies
- isolated networks
- environment-variable configuration
- no secrets committed to source control

Never treat a container filesystem as durable storage for database, GeoServer configuration, uploaded GIS files, or production raster data unless persistence is explicitly designed.

---

## 5. Frontend Deployment

Determine the runtime from the selected framework.

### React + Vite / static SPA

Use static hosting when server-side rendering is unnecessary.

Configure:

- production build
- SPA fallback routing
- asset caching
- environment-specific API URLs
- source-map policy
- compression
- cache invalidation/versioning

### Next.js

Determine whether the application requires:

- static export
- Node server
- server-side rendering
- incremental/static regeneration
- image optimization
- edge/server functions

Do not deploy a Next.js application as a static SPA if required server behavior would be lost.

### Vue/Nuxt, Angular, Svelte/SvelteKit

Apply the same principle: identify the actual output/runtime and deploy only the runtime capabilities the application requires.

Never hard-code one framework's deployment pattern into this skill.

---

## 6. API Deployment

Support the project's chosen backend rather than forcing a framework.

Common patterns include:

- FastAPI/Django
- Node.js/NestJS/Express
- Next.js server routes
- Go services
- existing enterprise APIs

Production API deployment should define:

- process model
- workers/concurrency
- graceful shutdown
- request timeouts
- body/file-size limits
- connection pooling
- health/readiness endpoints
- structured logging
- environment configuration
- migrations
- rate limiting
- CORS policy
- authentication/authorization
- API versioning
- observability

Do not expose internal database or GIS-service ports directly to the public internet unless explicitly required.

---

## 7. PostGIS Production Deployment

Treat PostGIS as stateful production infrastructure.

Plan for:

- PostgreSQL version compatibility
- PostGIS extension/version compatibility
- persistent storage
- schema migrations
- connection pooling
- database roles and least privilege
- spatial indexes
- vacuum/analyze strategy
- storage growth
- WAL/transaction behavior
- backup/restore
- point-in-time recovery when required
- replication when justified
- monitoring
- upgrade procedures

Before production migrations:

1. back up when appropriate
2. verify migration safety
3. test against representative data
4. define rollback or forward-fix strategy
5. run the migration
6. validate schema and critical queries
7. update project memory

Never delete or rebuild production spatial data as a shortcut for an unverified migration.

---

## 8. GeoServer Production Deployment

When GeoServer is part of the system, manage it as a stateful GIS service.

Plan:

- GeoServer version
- Java/runtime compatibility
- persistent data directory
- workspaces
- stores
- layers
- layer groups
- styles
- CRS configuration
- WMS/WFS/WMTS or vector-tile services
- GeoWebCache/tile caching
- database connection pools
- service limits
- request timeouts
- security and access rules
- configuration backups

Automate configuration where practical, but validate generated configuration against the target GeoServer version.

Do not expose administrative GeoServer endpoints publicly without strong access controls.

---

## 9. Raster, Object Storage, and Large GIS Data

Separate application deployment from large geospatial data storage.

Choose storage based on:

- raster size
- object count
- read/write pattern
- archival needs
- public/private access
- bandwidth
- lifecycle policies
- backup requirements

For large rasters, consider:

- Cloud Optimized GeoTIFF
- tiled access
- pyramids/overviews
- object storage
- range requests
- server-side processing
- appropriate compression

Do not place large production datasets inside the application image.

---

## 10. Reverse Proxy, DNS, and TLS

Use a reverse proxy or managed ingress to centralize:

- HTTPS termination
- domain routing
- redirects
- security headers
- request-size limits
- rate limiting where appropriate
- compression
- WebSocket support when needed
- upstream health handling

Possible implementations include Caddy, Nginx, Traefik, cloud load balancers, or an existing enterprise gateway.

Choose based on requirements rather than preference.

DNS must be documented for:

- apex/root domain
- www or frontend hostname
- API hostname
- GIS hostname
- admin/internal hostnames when applicable

TLS must be automated and renewed reliably.

Never store private TLS keys in Git.

---

## 11. Environment Configuration and Secrets

Separate at minimum:

- local/development
- test/CI
- staging
- production

Use environment variables or a dedicated secret manager for:

- database credentials
- JWT/signing secrets
- provider API keys
- cloud credentials
- SMTP credentials
- GeoServer administrative credentials
- storage credentials

Commit only safe example configuration.

Never commit:

- passwords
- API keys
- access tokens
- private certificates/keys
- production connection strings containing credentials

If a secret is accidentally committed, treat it as compromised and rotate it.

---

## 12. CI/CD

Use automated delivery when it reduces deployment risk.

A production pipeline should generally:

1. validate formatting/static checks
2. run unit/integration tests
3. run GIS/spatial tests
4. build artifacts/images
5. scan dependencies/images where appropriate
6. publish versioned artifacts
7. deploy to staging
8. run smoke tests
9. require appropriate approval for production
10. deploy production
11. run post-deployment health checks
12. record release metadata

GitHub Actions is one option, not a requirement.

Avoid pipelines that silently deploy unverified main-branch changes to production unless that behavior is explicitly intended and protected.

---

## 13. Database Migrations and Releases

Treat application and schema changes as coordinated releases.

For each migration:

- identify compatibility with the current application
- consider backward-compatible expansion first
- deploy code/schema in a safe order
- validate indexes and constraints
- account for long-running locks
- verify spatial indexes
- test rollback/forward-fix
- document destructive changes

For high-risk changes, use an expand → migrate → contract pattern.

Never assume a migration is safe because it succeeds on a small development database.

---

## 14. Health Checks and Smoke Tests

Define health at multiple layers.

### Infrastructure

- container/process running
- disk space
- memory/CPU
- network reachability

### Application

- frontend loads
- API health endpoint responds
- authentication path works
- database connection works

### GIS

- PostGIS spatial query works
- GeoServer service responds
- expected layer metadata is available
- representative WMS/WFS/tile request succeeds

### Data

- critical tables exist
- spatial indexes exist
- representative features can be queried
- raster/tile source is readable

A green process status is not proof that the GIS application is healthy.

---

## 15. Observability

Collect enough telemetry to answer:

- Is the service up?
- Is it slow?
- What failed?
- Which dependency failed?
- Which release introduced the problem?
- Is storage/memory/CPU exhausted?
- Are GIS requests failing selectively?
- Are database queries degrading?

Use:

- structured application logs
- reverse-proxy logs
- database logs/metrics
- GeoServer logs/metrics
- request latency/error metrics
- job/queue metrics
- disk/storage monitoring
- uptime checks
- alerts for actionable failures

Avoid logging secrets, credentials, sensitive geometries, or unnecessary personal data.

---

## 16. Performance and Scaling

Scale based on measured bottlenecks.

### Vertical scaling

Increase CPU/RAM/storage/IO when a single service is the bottleneck.

### Horizontal scaling

Use multiple stateless API/frontend instances when traffic requires it.

Stateful GIS components need separate planning for:

- database replication
- shared storage
- GeoServer configuration/data
- tile caches
- job queues
- locks and concurrency

Use caching/CDNs where they actually reduce load.

For map-heavy applications, optimize:

- vector tile generation
- tile caching
- geometry simplification
- database spatial indexes
- query bounding boxes
- raster tiling/overviews
- API payload size
- client rendering

Do not scale infrastructure to compensate for an unoptimized spatial query.

---

## 17. Background Jobs and Workers

Long-running GIS operations should not block ordinary API requests.

Use workers/queues for tasks such as:

- large uploads
- raster processing
- GEE exports
- GeoAI inference
- tile generation
- spatial ETL
- report generation
- bulk exports

Jobs should have:

- unique IDs
- ownership/authorization
- status
- progress where meaningful
- retries
- idempotency
- timeout handling
- failure state
- logs
- cleanup policy

Never allow a user-controlled request to create unbounded background work.

---

## 18. Zero/Low-Downtime Deployment

When uptime matters:

- deploy versioned artifacts
- use health/readiness checks
- drain traffic before shutdown
- avoid incompatible schema changes
- use rolling/blue-green/canary strategies when justified
- keep rollback artifacts available
- validate after switching traffic

For small systems, a carefully sequenced restart may be safer than introducing complex orchestration.

Choose the simplest reliable strategy.

---

## 19. Backups and Disaster Recovery

Define:

- what is backed up
- backup frequency
- retention
- encryption
- off-host/off-region copy when required
- restore procedure
- recovery point objective (RPO)
- recovery time objective (RTO)

Back up at least the critical state:

- PostgreSQL/PostGIS
- GeoServer configuration/data directory
- important uploaded GIS data
- object storage metadata/data when not independently durable
- deployment configuration
- infrastructure configuration

A backup that has never been restored is not verified recovery capability.

Perform restore drills appropriate to system criticality.

---

## 20. Security Hardening

Apply the security skill together with deployment work.

Check:

- firewall/network exposure
- SSH/admin access
- non-root services
- least-privilege service accounts
- secret handling
- TLS
- dependency/image patching
- public GIS endpoint exposure
- GeoServer admin protection
- database port exposure
- file upload limits
- rate limiting
- resource limits
- audit logging
- backup protection

Do not expose PostgreSQL, Redis, internal worker queues, or administrative services directly to the public internet unless explicitly required and secured.

---

## 21. Host/VPS Operations

For VPS-based deployments, establish:

- OS patching policy
- firewall rules
- SSH key-based access
- restricted administrative access
- disk monitoring
- swap strategy when appropriate
- Docker/container runtime updates
- log rotation
- backup jobs
- certificate renewal
- reboot/update procedure

Platforms such as Coolify may be used when they simplify deployment and operations, but they are implementation choices rather than architectural requirements.

---

## 22. Cost and Capacity Management

Track:

- compute
- memory
- storage
- database
- bandwidth/egress
- object storage
- tile/API provider usage
- monitoring
- backups
- domain/TLS-related costs
- paid GIS/data providers

Prefer open-source/self-hosted components when they meet the requirements, but include operational cost and maintenance effort in the comparison.

Record why a paid dependency is justified.

---

## 23. Deployment Testing

Before production:

- build from a clean environment
- verify all required environment variables
- run automated tests
- run database migrations against representative data
- verify frontend-to-API connectivity
- verify API-to-PostGIS connectivity
- verify GeoServer connectivity where applicable
- test representative map requests
- test uploads/exports
- test authentication/authorization
- test health checks
- test backup creation
- test restore for critical systems
- verify logs and alerts
- run a production smoke test after deployment

Test failure and recovery paths, not only the happy path.

---

## 24. Rollback and Incident Recovery

Every production deployment should have a documented recovery path.

Record:

- current release
- previous known-good release
- artifact/image version
- database migration state
- configuration version
- rollback limitations
- recovery commands/procedure
- data-loss implications

Prefer forward fixes for irreversible database migrations when rollback is unsafe.

During an incident:

1. stabilize the service
2. preserve evidence/logs
3. identify the failing boundary
4. mitigate user impact
5. restore service
6. validate GIS/data integrity
7. document root cause
8. record prevention actions in project memory

---

## 25. Deployment Definition of Done

A deployment task is complete only when:

- architecture is documented
- runtime/container boundaries are intentional
- environment separation is clear
- secrets are not committed
- TLS/DNS are configured appropriately
- frontend/API/GIS services are reachable as intended
- PostGIS persistence and migrations are validated
- GeoServer persistence/configuration is validated when used
- health checks exist
- smoke tests pass
- logs/monitoring are usable
- backups exist
- critical restore procedures are understood/tested
- resource limits/capacity are reasonable
- security exposure has been reviewed
- deployment and rollback procedures are documented
- costs are understood
- project memory is updated with the verified deployment state

---

## 26. Project-Memory Handoff

Before stopping:

### STATE.md
Record:
- deployment phase
- infrastructure topology
- last verified deployment step
- exact current environment
- active services
- validation performed
- blocker
- exact next action

### TASKS.md
Mark deployment tasks:
- completed
- in progress
- blocked
- next

### DECISIONS.md
Record durable choices such as:
- VPS vs managed cloud
- container strategy
- reverse proxy
- deployment platform
- database hosting
- GeoServer hosting
- storage strategy
- CI/CD strategy
- backup strategy
- scaling strategy
- paid vs free provider decisions

### SESSION.md
Record:
- work completed
- files/configuration changed
- commands or procedures validated
- failures and recovery
- exact resume point

### BLOCKERS.md
Record unresolved:
- infrastructure access
- DNS
- TLS
- quota
- provider limitations
- migration risk
- deployment failures

### CHANGELOG.md
Record meaningful deployment milestones.

Never claim a deployment is production-ready unless the required validation has actually been performed.
