# GIS Evaluation Harness

## Purpose
Provide deterministic, repeatable cases that test detection, right-pattern selection, safe remediation, and verification.

## Evaluation Loop
Case -> Context -> Expected Detection -> Expected Pattern -> Expected Remediation -> Validation -> Verdict.

## Dimensions
Detection correctness; CRS/spatial correctness; remediation correctness; data preservation; scientific validity; performance; security; contract compliance; auditability; regression safety.

## Verdicts
PASS, FAIL, BLOCKED, or ESCALATE. Never count an unvalidated patch as PASS.

## Regression Rule
Previously passing cases must remain passing after skill, contract, anti-pattern, or remediation changes.
