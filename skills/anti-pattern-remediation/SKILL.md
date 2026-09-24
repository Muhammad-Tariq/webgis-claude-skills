# Anti-Pattern Remediation Engine

## Purpose
Turn GIS anti-pattern detection into a controlled engineering loop that can safely convert bad implementations into correct patterns.

## Core Loop
Detect -> Classify -> Explain -> Resolve -> Patch -> Validate -> Audit.

A remediation is complete only when the corrected implementation passes relevant correctness, test, security, performance, and data-contract checks.

## Finding Model
Every finding should capture anti-pattern ID, affected file/code/data/workflow, evidence, severity, confidence, affected domain, required context, right-pattern ID, auto-fix eligibility, proposed change, validation plan, and final verification status.

## Remediation Classes
### A — Safe Auto-Fix
Apply automatically when the rule is deterministic and required context is known.

Examples: explicit CRS metadata propagation; adding validation with an unambiguous contract; bounded defaults; established set-based query conversion when semantics are preserved.

### B — Context-Aware Auto-Fix
Apply only after inspecting project context, data contracts, CRS/AOI, operation semantics, and tests.

Examples: selecting an analysis CRS; replacing giant GeoJSON delivery with pagination/vector tiles; changing raster processing to windowed access; choosing categorical nearest-neighbor resampling.

### C — Escalate
Do not modify automatically when the correction could change scientific meaning, user intent, data semantics, or required accuracy.

Examples: ambiguous CRS; unavailable datum/vertical transformation; uncertain model-label semantics; destructive data migration; authorization changes with unknown requirements.

## Right-Pattern Resolution
1. Read the anti-pattern definition.
2. Resolve its linked right pattern.
3. Load related skills, contracts, and fixtures.
4. Inspect actual implementation and project architecture.
5. Determine whether required context is sufficient.
6. Choose A, B, or C.
7. Produce the smallest safe change.
8. Run targeted validation.
9. Run broader regression checks when boundaries are affected.
10. Record change and evidence in project memory.

## GIS Rules
CRS: never blindly replace one EPSG code with another. Determine operation, AOI, units, accuracy, datum, axis order, and vertical requirements. Preserve native CRS and apply display or analysis transformation explicitly.

Geometry: validate after repair/transformation. Never silently drop invalid features.

Raster: preserve CRS, extent, pixel size, origin/alignment, nodata, datatype, and resampling semantics.

GeoAI: never silently alter an experiment to hide leakage or label problems. Preserve provenance and validate spatial/temporal splits.

Web GIS: use bounded queries, server-side filtering, tiling, caching, and progressive loading when scale requires it. Do not trade correctness for rendering performance.

## Validation Gate
Identify and run applicable GIS correctness, data-contract, geometry/unit, targeted test, spatial fixture, security, performance, API/OGC, and integration checks.

A patch that merely looks plausible is not verified.

## Rollback
Auto-remediation must be reversible. Prefer small patches and preserve original state in version control. Never destroy source datasets during automatic remediation.

## Audit Trail
Record detected anti-pattern, evidence, chosen right pattern, safety rationale, files/data affected, transformation or patch, validation performed, result, and unresolved uncertainty.

## Status
Use REMEDIATED_PENDING_VALIDATION, VERIFIED, ESCALATED, or FAILED. Only VERIFIED means implementation and relevant validation agree.

## Related Systems
Project orchestrator, GIS correctness, GIS code review, Web GIS testing, Web GIS security, performance optimization, and the anti-pattern catalog.
