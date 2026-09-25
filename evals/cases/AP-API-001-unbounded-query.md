# AP-API-001 — Unbounded Spatial Query

## id
AP-API-001

## domain
spatial-api / scalability / security

## scenario
A spatial endpoint accepts arbitrary AOIs and returns all matching features without pagination, maximum feature limits, or workload constraints.

## inputs
- pagination: false
- max_features: null
- workload_bound: null

## expected_detection
Detect unbounded resource consumption and missing API workload controls.

## expected_right_pattern
Use bounded pagination/limits, validated spatial filters, workload constraints, and asynchronous processing for expensive operations where appropriate.

## remediation_class
B — Context-Aware Auto-Fix

## validation
- limits are enforced server-side
- oversized requests fail predictably
- normal requests retain correct spatial results
- expensive work does not block synchronous requests

## forbidden_behavior
- relying only on frontend limits
- accepting unlimited feature counts
- silently truncating results without an explicit contract

## pass_criteria
The endpoint has explicit, enforced resource limits and preserves a documented result contract.
