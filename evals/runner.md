# Evaluation Runner Contract

## Purpose

Define how an evaluation runner executes deterministic GIS cases without coupling the repository to one specific runtime.

## Execution

1. Load case definition.
2. Resolve referenced skills, contracts, fixtures, and project context.
3. Build the case environment.
4. Run detection.
5. Compare detected anti-patterns with expected detection.
6. Resolve the expected right pattern.
7. Determine remediation class.
8. Apply remediation only when the case permits it.
9. Run required validation.
10. Check forbidden behavior.
11. Produce a structured result.
12. Persist result for regression comparison.

## Runner Principles

- deterministic inputs
- isolated case execution
- no secrets in fixtures or results
- preserve original fixtures
- record tool/library versions when available
- fail closed on missing mandatory validation
- distinguish BLOCKED from PASS
- allow ESCALATE when automation is intentionally unsafe
- never convert an unvalidated patch into PASS

## Comparison

A result passes only when:

- expected anti-pattern detection is satisfied
- right pattern is compatible
- remediation class is respected
- mandatory validation passes
- forbidden behavior is absent
- required evidence is present

## Regression

Compare current results with the repository baseline. Any new FAIL, unexpected PASS caused by weakened expectations, or changed validation behavior requires review.

## Artifacts

Store machine-readable results separately from human-readable explanations. Do not store secrets, API keys, tokens, or sensitive project data.
