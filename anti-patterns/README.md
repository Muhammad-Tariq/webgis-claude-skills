# GIS Anti-Pattern Catalog

Anti-patterns are actionable remediation rules, not merely a list of bad practices.

## Required Lifecycle
Detection -> Why Dangerous -> Trigger -> Right Pattern -> Remediation -> Validation -> Exceptions

## Remediation Policy
- Safe: deterministic fix with no meaningful semantic ambiguity.
- Context-aware: fix requires project/data/CRS/scale inspection before applying.
- Escalate: automatic modification could alter scientific meaning, user intent, data semantics, or required accuracy.

## Catalog
- mixed-crs-analysis.md — mismatched CRS used as if identical.
- epsg4326-distance.md — angular coordinates used for inappropriate planar distance.
- giant-geojson.md — oversized feature payloads used as a rendering strategy.
- client-side-million-features.md — excessive client-side feature rendering.
- unrestricted-wfs.md — unbounded feature service requests.
- raster-full-download.md — downloading entire rasters when a bounded subset is sufficient.
- silent-reprojection.md — CRS changed without an explicit transformation contract.
- invalid-geometry.md — invalid geometries used without validation or repair policy.
- raster-grid-misalignment.md — raster operations performed on incompatible grids.
- categorical-raster-resampling.md — inappropriate interpolation of categorical classes.
- spatial-data-leakage.md — spatially correlated samples leak between train/test sets.
- temporal-data-leakage.md — future information enters model training.
- map-reinitialization.md — map instance repeatedly destroyed/recreated.
- n-plus-one-spatial-query.md — one spatial query per feature/entity.
- unbounded-raster-processing.md — processing without bounded resource/data limits.
- display-data-as-analysis-data.md — visualization representation reused as analytical source.
- provider-secret-in-browser.md — provider credentials exposed to clients.
- unrestricted-spatial-api.md — unbounded spatial API operations.
- blocking-ui-thread.md — expensive GIS work blocks the main UI thread.
- missing-job-idempotency.md — repeated processing creates duplicate side effects.
- silent-data-dropping.md — records/features/pixels dropped without explicit policy.
- unversioned-model-inference.md — inference without model/input version provenance.
- vertical-datum-assumption.md — vertical coordinates interpreted without datum definition.
- public-osm-tile-abuse.md — public tile infrastructure used beyond its permitted operational model.
- random-pixel-split-for-spatial-ml.md — random pixel splits create spatially optimistic validation.

## Adding an Anti-Pattern
Every entry must include a concrete detection rule, right pattern, remediation class, validation strategy, and exception conditions. Avoid generic software advice unless the failure mode is materially GIS-specific.
