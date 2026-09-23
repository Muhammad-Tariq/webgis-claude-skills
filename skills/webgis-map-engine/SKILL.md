---
name: webgis-map-engine
description: Design and implement production Web GIS map architecture, including map engine, basemap, tiles, geocoding, routing, layers, interactions, performance, spatial correctness, and cost-aware provider selection.
---

# Web GIS Map Engine

Act as the geospatial frontend/map-engine specialist.

The objective is to build a map experience that is spatially correct, performant, maintainable, accessible, and cost-efficient.

Do not assume one map library or provider is always correct.

## Mandatory preflight

Before implementation:

1. Read project memory:
   - `STATE.md`
   - `TASKS.md`
   - `DECISIONS.md`
   - `SESSION.md`
   - `BLOCKERS.md` when present
2. Inspect the existing frontend architecture.
3. Inspect package/dependency manifests.
4. Identify the current map engine.
5. Identify basemap/tile providers.
6. Identify vector/raster/3D data sources.
7. Inspect API contracts and CRS assumptions.
8. Inspect existing map components and state management.
9. Check git status and recent relevant commits.
10. Preserve existing architecture unless evidence supports change.

## Map stack is not one thing

Always distinguish:

1. Map rendering library
2. Basemap provider
3. Tile provider
4. Geocoding/search provider
5. Routing provider
6. GIS/OGC service
7. Spatial database
8. Raster/tile storage
9. 3D/terrain provider when applicable

Changing one does not automatically require changing the others.

# Map engine selection

Evaluate the requirements before choosing:

- MapLibre GL JS
- OpenLayers
- Leaflet
- CesiumJS
- Existing map engine

### MapLibre

Prefer when the application needs:

- WebGL rendering
- vector tiles
- modern map styling
- large interactive vector visualization
- smooth animated map interaction

### OpenLayers

Prefer when the application needs:

- advanced GIS workflows
- complex projections
- OGC-heavy integration
- WMS/WFS
- sophisticated 2D GIS interaction
- mature GIS primitives

### Leaflet

Prefer when the application needs:

- simple 2D mapping
- lightweight applications
- straightforward markers and overlays
- modest data volumes

### CesiumJS

Prefer when the application needs:

- 3D globe
- terrain
- 3D Tiles
- buildings
- point clouds
- large 3D geospatial scenes

Do not select based on popularity alone.

# Free-first provider policy

**Prefer the best viable free/open-source option first.**

A free option is preferred when it satisfies:

- functionality
- performance
- licensing
- commercial-use requirements
- reliability
- geographic coverage
- expected traffic
- operational requirements

Do not select a paid provider simply because it is easier or popular.

Evaluate paid providers when they provide a concrete benefit such as:

- guaranteed SLA
- high-volume capacity
- premium geocoding
- routing quality
- global coverage
- guaranteed uptime
- support
- commercial usage rights
- reduced operational burden

Record the reason when a paid service is selected.

## Provider evaluation

For every external provider evaluate:

| Factor | Check |
|---|---|
| License | Data and API/service terms |
| Commercial use | Allowed or restricted |
| Free tier | Requests/limits |
| Rate limits | Requests per second/day/month |
| Attribution | Required attribution |
| Coverage | Countries/regions |
| Freshness | Data update frequency |
| Performance | Latency/rendering |
| Reliability | Availability/SLA |
| Self-hosting | Possible or not |
| Vendor lock-in | Migration difficulty |
| Cost | Current and projected |
| Offline | Supported or not |

## OSM rule

OpenStreetMap data and public OSM tile servers are separate concerns.

Never treat public OSM tile infrastructure as an unlimited production tile API.

For production use, evaluate:

- appropriate OSM-compatible providers
- self-hosted tiles
- commercial providers
- usage policies
- attribution
- expected traffic

# Basemap strategy

Choose the basemap based on the application.

Possible sources include:

- OSM-derived basemaps
- self-hosted vector tiles
- commercial vector tiles
- satellite imagery
- government/open-data basemaps
- project-specific cartography

Support multiple basemaps when the product benefits from it.

Keep basemap configuration separate from application layers.

# Layer architecture

Every layer should have a stable configuration model.

Recommended fields:

- id
- name
- source
- sourceType
- layerType
- visibility
- opacity
- zIndex/order
- minZoom
- maxZoom
- filter
- style
- legend
- attribution
- loading state
- error state
- permissions

Avoid hard-coding layer behavior into UI components.

# Data rendering strategy

Use the smallest appropriate representation.

### Small vector data

GeoJSON can be appropriate for:

- small feature sets
- selected features
- search results
- temporary drawings
- small analytical outputs

### Large vector data

Prefer:

- vector tiles
- server-side filtering
- spatial indexes
- clustering
- generalized geometries
- scale-dependent rendering

Never load a national-scale dataset into the browser as one GeoJSON object.

### Raster

Consider:

- tiled raster
- COG
- WMS
- WMTS
- raster tile services
- precomputed pyramids

Choose based on resolution, access pattern, styling requirements, and volume.

### 3D

Use:

- terrain
- 3D Tiles
- point-cloud formats
- appropriate WebGL/3D rendering

Do not force 3D requirements into a 2D architecture.

# CRS and measurement correctness

Track:

- source CRS
- storage CRS
- display CRS
- analysis CRS
- output CRS

Do not assume the map display CRS is appropriate for measurement.

For area/distance:

- use an appropriate projected CRS or geodesic calculation
- label units
- distinguish approximate client-side measurement from authoritative server-side analysis
- use PostGIS for authoritative spatial calculations when appropriate

Never silently mix SRIDs.

# Map state architecture

Separate:

### UI state

- panels
- dialogs
- active tools
- layer-panel state

### Map state

- center
- zoom
- bearing
- pitch
- active layers
- selection
- drawing state

### Server state

- API responses
- loading
- errors
- cached datasets

### Persistent state

- saved map views
- user preferences
- project configuration

Avoid putting all map state into one global object without clear ownership.

# Interaction architecture

Support only interactions required by the product, such as:

- pan/zoom
- identify
- click selection
- hover
- drawing
- editing
- measurement
- buffer
- spatial search
- bbox search
- coordinate readout
- geolocation
- compare/swipe
- time filtering
- layer filtering

Map interactions must have predictable precedence.

For example:

- drawing mode should capture drawing gestures
- selection mode should not conflict with drawing
- hover should not create expensive network calls for every pointer event
- measurement tools should clearly indicate units

# Map lifecycle

Prevent:

- duplicate map instances
- duplicate event listeners
- memory leaks
- repeated source registration
- repeated layer registration
- stale event handlers
- unnecessary map recreation

Initialize the map once where possible.

Update sources/layers/state rather than recreating the entire map.

Clean up listeners and resources when components unmount.

# Performance

Measure before optimizing.

Watch:

- initial map load
- time to first render
- tile latency
- feature count
- geometry complexity
- source count
- layer count
- style complexity
- network payload size
- browser memory
- FPS during interaction

Use:

- vector tiles
- clustering
- server-side filtering
- geometry simplification
- spatial indexes
- lazy loading
- scale-dependent visibility
- caching
- debouncing
- throttling
- WebGL rendering
- progressive loading

Avoid rendering thousands of DOM markers when a GPU/tile-based approach is appropriate.

# API integration

The map client should not contain business logic that belongs to the API.

Keep separate modules for:

- API client
- map adapter
- layer management
- source management
- selection
- measurement
- feature inspection

Define contracts for:

- bbox
- CRS
- pagination
- filters
- geometry
- feature IDs
- error responses

Validate API data before rendering.

# Geocoding and routing

Treat geocoding and routing as independent provider decisions.

Evaluate free/open-source/self-hosted options first.

For geocoding consider:

- Nominatim-compatible infrastructure
- commercial geocoding APIs
- authoritative local datasets
- self-hosted search infrastructure

For routing consider:

- OSRM
- GraphHopper
- Valhalla
- commercial routing APIs

Choose based on:

- geography
- routing modes
- traffic requirements
- request volume
- latency
- licensing
- operational complexity
- accuracy

Do not expose provider API keys in browser code unless the provider explicitly supports a safe public-key model.

# Accessibility

Provide:

- keyboard-accessible controls
- visible focus states
- labels for map controls
- non-map alternatives for critical information
- accessible legends
- readable contrast
- meaningful loading/error states

Do not make the map the only way users can access critical data.

# Security

Treat map inputs as untrusted.

Validate:

- uploaded GeoJSON
- coordinates
- bbox values
- feature IDs
- filters
- style expressions
- external URLs

Never expose:

- private provider keys
- database credentials
- GeoServer admin credentials
- internal service endpoints

UI visibility is not authorization.

# Testing

Test:

### Unit

- layer configuration
- CRS conversion helpers
- measurement utilities
- coordinate formatting
- filters
- map-state reducers

### Integration

- layer loading
- source registration
- API-to-map rendering
- selection
- filtering
- measurement

### E2E

Use browser automation for critical flows:

- map loads
- layer toggle
- search
- identify
- drawing
- measurement
- filtering
- export
- responsive behavior

Include failure cases:

- tile provider unavailable
- API unavailable
- malformed geometry
- empty result
- slow network
- invalid CRS
- rate limit

# Definition of done

Before declaring map work complete:

- [ ] Correct map engine selected for requirements.
- [ ] Basemap provider evaluated.
- [ ] Free/open-source alternatives evaluated.
- [ ] Paid provider justification documented if used.
- [ ] Licensing and attribution checked.
- [ ] Expected traffic and provider limits considered.
- [ ] CRS strategy verified.
- [ ] Layer architecture is modular.
- [ ] Large datasets are not blindly loaded into GeoJSON.
- [ ] Map lifecycle is leak-free.
- [ ] Loading/error/empty states exist.
- [ ] Accessibility requirements are covered.
- [ ] Security boundaries are respected.
- [ ] Critical interactions are tested.
- [ ] Project memory is updated.

# Handoff

After map architecture or implementation changes:

1. Update `STATE.md`.
2. Update `TASKS.md`.
3. Record durable decisions in `DECISIONS.md`.
4. Record the current session in `SESSION.md`.
5. Record blockers in `BLOCKERS.md`.
6. Update `CHANGELOG.md`.
7. Leave an exact next action for the next Claude Code session.

Never claim completion without verification.
