# Evaluation Adapters

Adapters execute domain-specific checks that the generic runner cannot infer from Markdown alone.

## Current

- crs_adapter.py — deterministic mixed-CRS metadata/invariant checks.

## Adapter Rules

1. Keep fixtures deterministic.
2. Separate metadata/invariant validation from numerical transformation validation.
3. Never claim a PROJ-backed transformation test unless the runtime actually executed the transformation.
4. Emit structured evidence.
5. Preserve source fixture data.
6. Return PASS only when all checks required by the adapter have executed successfully.

## Planned

- geometry adapter
- raster adapter
- spatial-ML adapter
- Web GIS scalability adapter
- security adapter
- API/OGC contract adapter
