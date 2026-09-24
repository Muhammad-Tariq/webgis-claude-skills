# AP-GIS-002: Mixed CRS Treated as Identical

## Domain
CRS, spatial analysis, Web GIS.

## Risk
High. Different CRS datasets can look correctly aligned while producing incorrect analytical results when coordinates are treated as if they share one coordinate system.

## Trigger
Flag when code/workflow compares coordinates from different CRS without transformation, performs spatial operations across mismatched CRS, assumes EPSG equality is unnecessary, silently rewrites a dataset CRS, or permanently reprojects data solely for display.

## Correct Pattern
Maintain native CRS per dataset, display CRS per map/view, and analysis CRS per operation. Use explicit transformations and preserve source data unless persistent reprojection is explicitly requested.

## Remediation
1. Detect every input CRS.
2. Identify the operation.
3. Determine AOI and required accuracy/units.
4. Select a suitable transformation/analysis CRS using authoritative CRS definitions.
5. Transform only the representation needed for the operation.
6. Perform the operation.
7. Validate geometry, units, extent, and result.
8. Record the transformation.
9. Preserve original native CRS.

## Auto-Fix Policy
Auto-remediate when CRS metadata, operation, AOI, and required accuracy are unambiguous. Escalate when CRS is missing/ambiguous, multiple transformation paths materially differ, vertical datum matters, or accuracy cannot be established automatically.

## Validation
Use projection/spatial correctness fixtures and operation-specific tests. Verify that source data remains in its original CRS and that the result is expressed in the intended CRS/units.
