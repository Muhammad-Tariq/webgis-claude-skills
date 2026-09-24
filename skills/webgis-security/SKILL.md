# Web GIS Security

## Purpose

Use this skill when designing, implementing, reviewing, testing, or deploying a production Web GIS. Protect the browser, spatial APIs, PostGIS, GeoServer, OGC services, uploads, processing workers, object storage, GEE integrations, GeoAI inference, and multi-tenant spatial data.

The goal is defense in depth, least privilege, secure defaults, explicit trust boundaries, controlled resource usage, and recoverability.

## 1. Mandatory Preflight

Before security work:
1. Read `project-memory/STATE.md`.
2. Read `project-memory/TASKS.md`.
3. Read `project-memory/DECISIONS.md`.
4. Read `project-memory/SESSION.md`.
5. Read `project-memory/BLOCKERS.md` when present.
6. Inspect authentication, authorization, public/private endpoints, database, GeoServer, storage, worker, and frontend boundaries.
7. Review existing security tests and identify the last verified security state.

If memory conflicts with actual configuration or code, trust verified implementation and repair memory. Never expose or commit credentials during investigation.

## 2. Threat Model First

Identify assets, actors, trust boundaries, entry points, sensitive data, privileged operations, external dependencies, abuse cases, and impact of compromise.

Typical assets include user accounts, spatial datasets, private layers, customer data, model artifacts, credentials, cloud storage, GeoServer administration, and processing infrastructure.

Typical entry points include browser APIs, OGC services, uploads, remote URL imports, exports, background jobs, and administrative endpoints.

## 3. Trust Boundaries

Explicitly model:
- browser to API
- public API to private services
- API to PostGIS
- API to GeoServer
- API to object storage
- API to workers
- workers to filesystem
- application to GEE
- application to GeoAI
- tenant to tenant

Every boundary should have appropriate authentication, authorization, validation, output controls, logging, and resource limits.

## 4. Authentication

Use established mechanisms such as OIDC/OAuth 2.0 or secure application sessions. Prefer secure, HttpOnly, SameSite cookies for browser sessions where appropriate. Require HTTPS.

Never implement custom password cryptography. Never store plaintext passwords. Do not expose privileged tokens in frontend code.

## 5. Authorization

Authorization must be enforced server-side. Check user, role, tenant, project, layer, feature, and operation as required.

Never rely on hiding a layer or button in the frontend as access control.

A client-supplied tenant ID, project ID, layer ID, or AOI must never be trusted without server-side authorization.

## 6. Spatial and Tenant Authorization

For multi-tenant or spatially restricted systems define isolation explicitly using appropriate combinations of separate databases, schemas, tenant columns, Row-Level Security, GeoServer workspaces, and storage prefixes.

Test cross-tenant access explicitly. A request returning another tenant's feature is a critical security defect.

Spatial permissions may restrict users to assigned project polygons or geographic areas. Enforce these restrictions on the backend/database.

## 7. PostGIS Security

Use least-privilege database roles. Separate migration, application, read-only, and administrative privileges where appropriate.

Never use a superuser for routine API operations.

Use parameterized queries and controlled query builders. Never concatenate untrusted values into SQL.

## 8. Spatial Injection

GIS systems have injection risks beyond ordinary SQL, including CQL filters, SQL fragments, dynamic columns, sort fields, geometry expressions, CRS identifiers, and function names.

Prefer allowlists, enums, parameterized values, and server-defined field mappings. Never accept arbitrary SQL from normal API requests.

## 9. GeoServer Security

Treat GeoServer administration as highly privileged. Do not expose the admin interface publicly without strong justification and compensating controls.

Separate admin, internal service, and public OGC endpoints where possible.

Review workspaces, datastore credentials, layer permissions, service limits, WMS/WFS access, REST API access, CORS, proxy configuration, and authentication.

Disable unused services and use least-privilege datastore accounts.

## 10. OGC Service Exposure

WMS, WFS, WMTS, vector tiles, and capabilities documents can expose sensitive geometry and attributes.

Review public layers, private layers, queryable fields, feature limits, geometry precision, downloads, and filters. Do not assume a rendered map is harmless when an underlying feature service is exposed.

## 11. Sensitive Geometry and Data Minimization

Treat locations of critical infrastructure, private property, utility networks, security facilities, personal locations, endangered species, and internal projects as potentially sensitive.

Apply access control, geometry generalization, attribute minimization, resolution limits, rate limits, and auditing as appropriate.

Return only the data a client needs. Use field allowlists, pagination, simplified geometry, and generalized coordinates when appropriate.

## 12. File Upload Security

Treat all GIS uploads as untrusted. Validate actual file structure, extension/type, size, archive contents, geometry count/complexity, CRS, coordinate ranges, raster dimensions, bands, and metadata.

For archives prevent path traversal, absolute paths, symlink escapes, decompression bombs, and excessive extraction. Store uploads outside executable directories and use generated storage IDs instead of original filenames as filesystem paths.

## 13. Resource Exhaustion

Spatial operations can be computationally expensive. Protect against huge geometries, enormous multipolygons, high-resolution rasters, massive bboxes, complex intersections, unbounded WFS queries, repeated tile requests, and expensive GeoAI inference.

Use request-size limits, feature limits, geometry complexity limits, timeouts, pagination, rate limits, queues, concurrency limits, maximum raster dimensions, and maximum inference area.

Never expose unlimited expensive operations to unauthenticated users.

## 14. SSRF Protection

Web GIS backends often fetch remote rasters, imagery, WMS/WFS services, metadata, imports, or webhooks. Never blindly fetch user-supplied URLs.

Use strict allowlists where possible, protocol restrictions, DNS/IP validation, private-network blocking, redirect validation, response-size limits, and connection timeouts.

Block loopback, link-local, private network ranges, cloud metadata endpoints, and internal service networks. Revalidate after redirects and DNS resolution.

## 15. Path Traversal

Never construct filesystem paths directly from untrusted filenames, layer names, workspace names, tenant IDs, export names, or job IDs.

Use generated IDs and controlled directories. Normalize and validate paths and ensure resolved paths remain inside the intended root.

## 16. API Security

For every endpoint define authentication, authorization, allowed methods, input schema, output schema, rate limit, resource limit, timeout, and audit requirements.

Reject unexpected fields where strict validation is appropriate. Do not expose stack traces, SQL, filesystem paths, internal hostnames, or infrastructure details to clients.

## 17. Rate Limiting

Rate-limit login, password reset, search, geocoding, feature queries, exports, uploads, raster processing, GeoAI inference, and job submission as appropriate.

Consider limits by IP, user, tenant, API key, and endpoint. Use concurrency limits for expensive jobs.

## 18. Cache Security

Do not cache private responses in shared/public caches. Review browser, CDN, tile, GeoServer, and API cache behavior.

Cache keys must include relevant authorization or tenant context when needed. Never allow a private response to become publicly reusable through an incomplete cache key.

## 19. CORS and Browser Security

Configure CORS explicitly. Avoid wildcard origins for authenticated APIs.

Review HTTPS, Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, and frame protections where appropriate.

Do not add permissive CORS merely to make a GIS client work.

## 20. Secrets Management

Never commit passwords, API keys, cloud credentials, private keys, OAuth secrets, database passwords, or model-registry tokens.

Use environment variables or a secret manager. Separate local, development, staging, and production secrets. Rotate exposed credentials immediately.

Never store secrets in project memory, logs, screenshots, test fixtures, frontend bundles, or public configuration.

## 21. External Provider Keys

For geocoding, routing, basemap, satellite, cloud, or AI services, determine whether a key may safely be browser-visible.

If it must remain secret, use Browser → Backend → Provider. Apply provider-specific domain, quota, and scope restrictions where available.

## 22. Logging and Audit

Log security-relevant events without secrets:
- authentication failures/successes
- authorization failures
- sensitive-layer access
- uploads/downloads/exports
- administrative changes
- inference access
- permission changes
- suspicious patterns

Include timestamp, actor, tenant/project where applicable, action, resource, result, and correlation ID. Never log passwords, tokens, cookies, or private keys.

## 23. Monitoring

Monitor repeated authorization failures, abnormal exports, unusual uploads, expensive query spikes, suspicious URL fetching, authentication anomalies, unexpected GeoServer administration access, and cross-tenant access attempts.

## 24. Export Security

Exports are data-exfiltration paths. Protect CSV, GeoJSON, Shapefile/GeoPackage, raster, reports, and model outputs.

Authorize before generation/retrieval. Prefer short-lived download URLs, size limits, expiration, access control, and audit logging. Do not expose permanent public object-storage URLs for private data.

## 25. Background Jobs

Validate job ownership on status and result endpoints. Use unguessable IDs, tenant scoping, quotas, timeouts, and cleanup.

Workers should have only the permissions they need. Repeated client requests must not unintentionally create duplicate expensive jobs.

## 26. GeoAI Security

Protect model files, training data, uploaded imagery, inference endpoints, prediction outputs, and GPU workers.

Limit input size, inference area, batch size, concurrency, and model selection. Never allow arbitrary model paths or arbitrary code execution through an inference API.

## 27. GEE Security

Do not expose private GEE credentials in the frontend. Review project permissions, asset sharing, service accounts, export destinations, API credentials, and downstream storage permissions.

Exporting GEE data to another platform creates a new security boundary.

## 28. Data at Rest and in Transit

Use HTTPS/TLS for external and sensitive internal traffic as appropriate. Protect databases, object storage, backups, exported datasets, model artifacts, and logs. Use encryption at rest where supported.

Backups must inherit appropriate access controls.

## 29. Dependency and Supply-Chain Security

Review frontend/backend packages, GIS libraries, GDAL/PROJ, GeoServer, database extensions, ML frameworks, containers, and OS packages.

Use lockfiles, dependency scanning, pinned versions where appropriate, trusted sources, and image scanning. Regression-test critical geospatial library upgrades.

## 30. Container and Deployment Security

For containers, run non-root where possible, minimize images, keep secrets outside images, restrict capabilities, isolate networks, limit resources, scan images, and pin important base versions.

Separate public-facing services from administrative services.

## 31. Network Architecture

Prefer explicit segmentation:

Internet → Reverse Proxy/WAF → Web/API → Private Network → PostGIS / GeoServer / Workers / Storage

Do not expose PostGIS directly to the public internet without compelling justification and strong controls. Restrict GeoServer and database administration to trusted networks.

## 32. Backup and Recovery

Maintain backups for databases, spatial data, object storage, configurations, models, and GeoServer settings where appropriate.

Test restoration and define RPO, RTO, retention, ownership, and recovery procedures. A backup that has never been restored is not a verified recovery strategy.

## 33. Security Testing

Use unit, integration, API, E2E, dependency, static-analysis, container, and controlled penetration testing as appropriate.

Important cases include unauthorized layer access, cross-tenant access, malicious uploads, oversized geometry, SQL/filter injection, SSRF, path traversal, rate-limit bypass, private cache leakage, and export authorization.

Never perform destructive security testing against production without explicit authorization and safeguards.

## 34. Incident Response

When a security issue is discovered:
1. Contain the affected path.
2. Preserve relevant evidence.
3. Determine scope.
4. Rotate compromised credentials.
5. Patch the root cause.
6. Invalidate affected sessions/tokens where necessary.
7. Restore from trusted backups if required.
8. Verify the fix.
9. Document the incident.
10. Add tests and controls to prevent recurrence.

Do not hide security failures by deleting logs or suppressing alerts.

## 35. Review by Change Type

### Frontend
Review XSS, unsafe HTML, token handling, exposed secrets, and CORS assumptions.

### API
Review authentication, authorization, validation, rate/resource limits, injection, and error leakage.

### PostGIS
Review privileges, SQL construction, RLS, migrations, and tenant isolation.

### GeoServer
Review public layers, admin exposure, datastore credentials, filters, and service limits.

### Data pipeline
Review file handling, SSRF, path traversal, resource limits, and sensitive-data exposure.

### GeoAI
Review input limits, model access, job authorization, resource exhaustion, and output privacy.

### Deployment
Review network exposure, secrets, containers, TLS, firewall rules, backups, and monitoring.

## 36. Definition of Done

- [ ] Threat model exists for material systems.
- [ ] Trust boundaries are identified.
- [ ] Authentication is appropriate.
- [ ] Authorization is enforced server-side.
- [ ] Spatial/tenant isolation is tested.
- [ ] Database privileges follow least privilege.
- [ ] GeoServer administration is protected.
- [ ] Public OGC exposure is intentional.
- [ ] Spatial injection risks are controlled.
- [ ] Uploads are validated and isolated.
- [ ] SSRF/path traversal protections exist where relevant.
- [ ] Resource-exhaustion limits exist.
- [ ] Rate limiting exists for sensitive/expensive operations.
- [ ] Cache behavior cannot leak private data.
- [ ] CORS/browser security is intentional.
- [ ] Secrets are externalized and protected.
- [ ] Sensitive exports are authorized and auditable.
- [ ] Background jobs enforce ownership.
- [ ] External provider credentials are protected.
- [ ] Logs do not contain secrets.
- [ ] Dependency/container security is addressed.
- [ ] Backups and recovery are tested.
- [ ] Security tests pass.
- [ ] Project memory is updated.

Do not claim production security merely because HTTPS or authentication exists.

## 37. Project-Memory Handoff

Before ending security work, update:

### STATE.md
Record security phase, last verified control, changed files, validation, blocker, and exact next action.

### TASKS.md
Record controls implemented, tests added, vulnerabilities fixed, and remaining work.

### DECISIONS.md
Record durable decisions such as authentication, tenant isolation, GeoServer exposure, upload architecture, network segmentation, secret management, and rate/resource limits.

### SESSION.md
Record checks performed, findings, fixes, test results, and exact resume point.

### BLOCKERS.md
Record unresolved findings, provider limitations, dependency vulnerabilities, infrastructure issues, and pending reviews.

Never store secrets, credentials, tokens, or private keys in project memory.

## 38. Handoff Summary

Record:
- threat model
- protected assets
- trust boundaries
- authentication
- authorization
- tenant/spatial isolation
- PostGIS controls
- GeoServer exposure
- upload controls
- SSRF/path protections
- rate/resource limits
- secret management
- security tests
- monitoring
- backup/recovery status
- known findings
- current blocker
- last verified state
- exact next action

The next agent must inspect actual configuration and run relevant security tests before trusting this summary.
