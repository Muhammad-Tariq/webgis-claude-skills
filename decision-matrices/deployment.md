# Deployment Decision Matrix

## Candidates
Single VPS, containers on VPS, managed platform, Kubernetes, cloud managed services, on-premises, hybrid.

## Rules
- Small/medium production GIS application: evaluate containerized VPS or managed platform before Kubernetes.
- Enterprise multi-service platform: evaluate managed services or Kubernetes when operational requirements justify them.
- Regulated/on-premise requirement: evaluate on-premises or hybrid.
- Large raster/GeoAI compute: evaluate workload-specific cloud/compute services.

## Checks
Availability, scaling, security, networking, backups, observability, rollback, team operations, cost, vendor lock-in.
