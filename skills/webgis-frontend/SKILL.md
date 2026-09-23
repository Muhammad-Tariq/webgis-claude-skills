---
name: webgis-frontend
description: Build production-quality Web GIS frontends and dashboards using the framework and map engine selected by the architecture skill. Use for map UI, GIS interactions, layer management, spatial tools, dashboards, responsive layouts, API integration, performance, accessibility, and frontend testing.
---

# Web GIS Frontend Engineer

Build polished, production-ready Web GIS applications from the architecture selected by `webgis-architect`.

This skill is intentionally framework-neutral. Do not force React, Next.js, Vue, Angular, Svelte, or another framework when the architecture has selected a different stack.

## Relationship to the architecture skill

The architecture skill decides:

- frontend framework
- map engine
- rendering strategy
- API/service boundaries
- data flow
- deployment architecture

This skill implements that decision.

If no architecture decision exists:

1. Read project memory.
2. Inspect the existing project.
3. Invoke architectural reasoning before introducing a new frontend framework.
4. Do not rewrite the project simply to use a preferred framework.

## Mandatory preflight

Before coding:

1. Read `STATE.md`, `TASKS.md`, and `DECISIONS.md` when present.
2. Inspect repository structure.
3. Inspect package/dependency manifests.
4. Inspect existing routes/pages.
5. Inspect existing map components and GIS utilities.
6. Inspect API/service clients.
7. Inspect existing design system/component library.
8. Inspect tests.
9. Check `git status`.
10. Identify the smallest useful vertical slice.

Do not create duplicate components or services without checking existing code.

# Product-first UI design

A Web GIS is not just a map.

Design the complete user workflow:

~~~text
User goal
   ↓
Discover
   ↓
Select/filter
   ↓
Map interaction
   ↓
Inspect
   ↓
Analyze
   ↓
Act/export/share
~~~

The UI should make the primary workflow obvious.

Avoid the common failure mode:

~~~text
Huge map
+ random toolbar
+ many buttons
+ tiny unreadable panels
= poor GIS UX
~~~

Instead establish:

- clear visual hierarchy
- obvious primary actions
- contextual tools
- readable legends
- meaningful empty states
- useful loading states
- understandable errors
- responsive layout

## Dashboard composition

For an analytical GIS dashboard, consider:

- map canvas
- header/navigation
- layer panel
- legend
- search
- filter controls
- drawing/measurement tools
- feature information panel
- KPI/statistics cards
- charts
- timeline when temporal data exists
- analysis controls
- export/share actions
- notifications/status area

Do not include every component automatically. Use only what supports the workflow.

# Framework rules

## Framework selection is inherited

Respect the architecture decision.

### React
Use component composition, hooks, predictable state boundaries, controlled side effects, reusable GIS hooks, and route-level code splitting where useful.

### Next.js
Separate server-rendered/application UI, client-only map components, server/API logic, and browser-only GIS dependencies. Map libraries requiring browser APIs should be isolated appropriately.

### Vue/Nuxt
Use components and composables, with appropriate client-only handling for browser GIS libraries and clear server/client separation.

### Angular
Use components, services, dependency injection, appropriate change detection strategy, and route-level organization.

### Svelte/SvelteKit
Use components and stores where needed, with browser-only guards for GIS libraries and clear server/client separation.

## TypeScript

When TypeScript is selected:

- use strict typing
- define domain types
- type API responses
- type spatial feature properties
- avoid `any`
- validate untrusted API data at boundaries
- keep GIS types close to their domain

Avoid enormous global type files.

# Map architecture

Keep map responsibilities separate.

Prefer:

~~~text
MapShell
├── MapEngineAdapter
├── LayerManager
├── SourceManager
├── InteractionManager
├── ControlManager
├── SelectionManager
├── Popup/FeatureInspector
└── MapState
~~~

The exact structure depends on the selected map engine.

Do not tightly couple business logic to map-library internals.

## Map lifecycle

Handle:

- map initialization
- readiness
- resize
- route changes
- layer changes
- cleanup
- component unmount
- style changes
- authentication/token changes

Prevent duplicate map instances, duplicate event listeners, stale closures, leaked sources/layers, repeated network requests, and unnecessary map reinitialization.

# Layer management

Create a clear layer model.

A layer should have, where applicable:

- stable ID
- display name
- source
- type
- visibility
- opacity
- z-order
- legend metadata
- scale constraints
- filter
- loading state
- error state
- attribution
- permissions

Do not use display names as internal IDs.

Separate:

~~~text
Layer configuration
      ≠
Map engine implementation
      ≠
Backend/GIS service
~~~

This makes future migration between map engines possible.

# GIS interactions

Implement interactions as independent capabilities where practical:

- pan/zoom
- identify
- feature selection
- hover
- drawing
- editing
- measuring
- buffering
- spatial search
- bbox selection
- coordinate readout
- layer comparison
- time filtering
- geolocation when appropriate

Every interaction should have visible state, accessibility consideration, loading behavior when asynchronous, error handling, and cancellation where useful.

## Measurement correctness

Never trust browser geometry calculations blindly for production measurements.

Use the appropriate projected CRS, geodesic calculation, or backend/PostGIS calculation for the required accuracy.

Always label units and distinguish approximate from authoritative results.

# API integration

Keep API clients separate from UI components.

Prefer:

~~~text
UI
 ↓
Domain hook/service
 ↓
API client
 ↓
HTTP/GeoServer/spatial service
~~~

Not a single component containing fetching, geometry parsing, map updates, and analytics.

For API data:

- validate response shape
- handle loading
- handle errors
- handle empty results
- support cancellation where useful
- avoid duplicate requests
- cache stable data
- paginate large feature collections

## GeoJSON

For GeoJSON:

- validate geometry type
- validate properties
- respect CRS assumptions
- avoid unnecessarily large FeatureCollections
- use server-side filtering/tiling for large datasets
- avoid rendering thousands of DOM/SVG elements when WebGL/tile rendering is more appropriate

# State management

Separate state by responsibility.

### UI state
Panel visibility, selected tab, active tool, modal state.

### Map state
Center, zoom, bearing, pitch, visible layers, selected feature.

### Server state
API results, layer metadata, statistics, user data.

### Persistent application state
Saved map configuration, user preferences, project settings.

Do not put every state value into one global store.

Use the simplest state mechanism that fits.

# Performance

Performance is part of GIS architecture.

Watch for:

- excessive rerenders
- map reinitialization
- too many rendered features
- huge GeoJSON payloads
- expensive client-side geometry operations
- unnecessary API calls
- image/raster memory pressure
- unbounded chart datasets
- oversized bundles

Use where appropriate:

- code splitting
- lazy loading
- memoization
- virtualization
- clustering
- vector tiles
- server-side filtering
- pagination
- caching
- debouncing
- throttling
- Web Workers
- progressive rendering

Do not optimize by adding complexity without measuring.

## Map-specific performance

For large datasets, prefer:

~~~text
Large dataset
   ↓
Server-side filtering/generalization
   ↓
Tiles or efficient transport
   ↓
WebGL/GPU rendering
~~~

over downloading and rendering everything in the browser.

# Responsive design

Support desktop, laptop, tablet, and mobile when the product requires it.

For smaller screens:

- collapse side panels
- use bottom sheets/drawers
- prioritize primary tools
- avoid tiny map controls
- preserve touch targets
- avoid critical hover-only interactions

Do not simply shrink the desktop UI.

# Accessibility

Support keyboard navigation, visible focus, semantic controls, labels, meaningful button names, sufficient contrast, non-color-only status indicators, and accessible panels where practical.

Provide alternative textual/data views where the workflow requires it.

# Visual quality

Build a coherent design system.

Define typography hierarchy, spacing, borders/radii, elevation, icon style, component states, map/UI contrast, and light/dark behavior if required.

Avoid excessive gradients, random colors, inconsistent radii, unnecessary animation, excessive glassmorphism, tiny text, and overcrowded toolbars.

The map should remain the primary visual workspace.

# Loading, empty, and error states

Every asynchronous GIS operation should have explicit states:

~~~text
idle
 ↓
loading
 ↓
success
 ↓
empty
 ↓
error
~~~

For long-running analysis:

~~~text
queued
 ↓
processing
 ↓
completed
 ↓
failed
~~~

Show useful messages. Never expose raw stack traces or internal errors to users.

# Forms and GIS uploads

For uploads:

- validate file type
- validate size
- validate geometry
- validate CRS when possible
- show upload progress
- provide useful errors
- never trust filename/path input
- never assume uploaded data is safe

Supported formats should be deliberate, for example GeoJSON, GeoPackage, Shapefile archive, KML/KMZ, CSV with coordinates, and supported raster formats.

# Charts and analytics

Charts must stay synchronized with map state when the product requires it.

~~~text
Map filter
   ↓
Spatial query
   ↓
Dataset
   ├── Map
   └── Statistics
        ↓
      Charts
~~~

Avoid having map and dashboard independently query contradictory datasets.

For large datasets, calculate aggregates server-side.

# Testing

Cover:

### Unit
Geometry utilities, formatting, coordinate conversion, layer configuration, and state logic.

### Component
Layer panel, search, filters, feature inspector, measurement UI, dialogs/forms.

### Integration
API integration, map/layer lifecycle, selection flow, filtering, and export.

### Browser/E2E
Use Playwright or the project's selected browser automation tool for critical workflows.

Test application loading, map initialization, layer loading, search, feature selection, filters, error states, and responsive layouts where required.

Do not rely on screenshots alone for GIS correctness.

# Security

Never trust URL parameters, map filters, CQL filters, feature IDs, uploaded files, GeoJSON properties, or API responses.

Never place API secrets, database credentials, or private tokens in browser code.

Use server-side authorization for protected data.

Hiding a layer in the UI is not authorization.

# Code quality

Prefer small focused components, clear domain naming, reusable hooks/composables/services, typed APIs, explicit dependencies, predictable state, and testable utilities.

Avoid giant Map components, giant global stores, duplicated API calls, magic constants, hidden side effects, and framework-specific code spread throughout domain logic.

# Implementation workflow

For every feature:

1. Read project memory.
2. Inspect existing implementation.
3. Confirm architecture/framework/map-engine decision.
4. Define the smallest vertical slice.
5. Implement domain/data layer first when appropriate.
6. Implement UI.
7. Integrate map interaction.
8. Add loading/error/empty states.
9. Add tests.
10. Run validation.
11. Review UX.
12. Update project memory.

# Definition of done

- [ ] Follows selected architecture.
- [ ] Existing components/services reused where appropriate.
- [ ] Map lifecycle is safe.
- [ ] API responses are handled correctly.
- [ ] Loading/empty/error states exist.
- [ ] Large-data behavior is considered.
- [ ] CRS/measurement assumptions are correct.
- [ ] Responsive behavior is acceptable.
- [ ] Accessibility basics are covered.
- [ ] Security boundaries are respected.
- [ ] Tests pass.
- [ ] No unnecessary dependencies were introduced.
- [ ] Project memory is updated.

# Handoff

When the frontend is ready for the next layer:

- document API requirements
- document GIS service requirements
- document layer/source contracts
- record unresolved blockers
- update project memory
- hand database work to PostGIS skill
- hand GIS publishing work to GeoServer skill
- hand spatial analysis to the appropriate GIS/processing skill

Do not silently invent backend endpoints when the contract has not been agreed.
