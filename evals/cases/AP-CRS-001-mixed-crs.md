# AP-CRS-001 — Mixed CRS

## Scenario
Roads use EPSG:4326 and parcels use EPSG:32642. Both must display together; later the user requests a 500 m buffer.

## Expected Detection
Different native CRS is detected, but is not itself treated as an error.

## Expected Pattern
Preserve native CRS per layer; use a separate display CRS; select an appropriate analysis CRS or geodesic method for the 500 m operation.

## Remediation
B — Context-Aware Auto-Fix.

## Validation
Native CRS unchanged; display transformation explicit; analysis units are meters; buffer is plausible; transformation recorded.

## Forbidden
Permanent reprojection merely for display; planar degree arithmetic; invented EPSG codes.
