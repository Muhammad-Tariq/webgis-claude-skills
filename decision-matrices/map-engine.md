# Map Engine Decision Matrix

## Candidates
MapLibre GL JS, OpenLayers, Leaflet, Cesium, or another specialized engine.

## Rules
- Vector-tile/WebGL-heavy 2D visualization: evaluate MapLibre GL JS.
- Broad OGC/projection/editing/advanced GIS behavior: evaluate OpenLayers.
- Lightweight conventional maps with modest interaction needs: evaluate Leaflet.
- Terrain, globe, 3D Tiles, and 3D scenes: evaluate Cesium.
- Do not select a 2D engine for a primarily 3D requirement.

## Checks
Evaluate projection support, source/layer model, rendering model, editing, hit testing, styling, raster/OGC support, performance, mobile behavior, accessibility, licensing, and ecosystem maturity.
