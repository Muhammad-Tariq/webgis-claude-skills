# Geocoding & Routing

## Purpose
Build reliable location search, address normalization, reverse geocoding, routing, travel-time, isochrone, network-accessibility, and snapping capabilities for Web GIS.

## Mandatory Preflight
Read project memory and inspect the map engine, API, spatial database, provider architecture, CRS conventions, authentication, caching, and rate limits.

## Capability Separation
Treat these independently:
- forward geocoding
- reverse geocoding
- autocomplete
- routing
- matrix routing
- isochrones
- nearest-road/network snapping
- address normalization

## Provider Selection
Evaluate coverage, address quality, road-network coverage, traffic support, latency, quotas, attribution, licensing, commercial terms, self-hosting, offline capability, and cost.

Prefer free/open-source/self-hosted options when they meet requirements. Public geocoding/routing endpoints are not assumed to be unlimited production APIs.

## Coordinate and Address Semantics
Document input/output CRS, coordinate order, language, regional bias, address components, confidence/relevance, and network reference. Validate and normalize inputs.

## Autocomplete
Use debounce, cancellation, bounded results, safe caching, geographic bias where appropriate, minimum query length where useful, and provider rate limits. Never issue uncontrolled requests on every keystroke.

## Routing
Define travel mode, network, restrictions, distance/time units, departure assumptions, route geometry, and instruction requirements. Distinguish Euclidean, geodesic, network distance, and travel time.

## Matrix and Isochrones
Bound matrix size, batch requests, cache safe repeated pairs, and avoid O(n²) browser requests. For isochrones define origin, mode, budget, network assumptions, barriers, and output resolution.

## Caching and Failure
Define normalized keys, TTL, invalidation, geographic scope, source, and privacy boundaries. Handle no results, ambiguity, timeouts, quota exhaustion, invalid coordinates, disconnected networks, and route failures explicitly.

## Security and Privacy
Protect user locations, saved places, exact coordinates, address history, and API keys. Avoid logging exact coordinates unnecessarily. Validate server-side provider targets to prevent SSRF.

## Testing
Test known addresses/coordinates, country boundaries, coordinate order, ambiguity, no-result cases, route distance/time, disconnected roads, provider failure, rate limits, caching, and authorization. Maintain representative golden cases.

## Definition of Done
- capability/provider explicitly selected
- CRS and coordinate semantics documented
- quotas/rate limits enforced
- caching/privacy defined
- failure behavior tested
- representative cases pass
- provider licensing documented
- project memory updated

## Project-Memory Handoff
Record provider, coverage assumptions, routing profile, CRS semantics, caching, quotas, costs, verified cases, blockers, and exact next action.