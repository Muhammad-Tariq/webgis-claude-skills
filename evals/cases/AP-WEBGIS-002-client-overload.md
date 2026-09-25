# AP-WEBGIS-002 — Client-Side Feature Overload

## id
AP-WEBGIS-002

## domain
webgis / scalability

## scenario
A map attempts to load 2,000,000 vector features directly into browser memory.

## inputs
- feature_count: 2000000
- delivery: browser-memory
- bounded_server_delivery: false

## expected_detection
Detect client-side overload and unbounded spatial delivery.

## expected_right_pattern
Use server-side filtering/generalization, vector tiles, bounded pagination, or another scale-appropriate delivery architecture.

## remediation_class
B — Context-Aware Auto-Fix

## validation
- delivered feature volume is bounded
- browser memory remains within the declared budget
- spatial filtering remains correct
- map remains responsive under representative load

## forbidden_behavior
- sending the complete dataset to the browser
- increasing browser memory assumptions instead of fixing delivery architecture
- removing features without preserving requested spatial semantics

## pass_criteria
The proposed architecture bounds client workload and validates responsiveness with representative data.
