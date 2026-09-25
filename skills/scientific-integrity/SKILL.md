# Scientific Integrity Gate

## Purpose

Prevent an agent or automated research workflow from changing scientific methodology merely to improve reported model metrics.

## Core Invariant

> The system must never modify scientific methodology solely to artificially improve model metrics.

The objective is a scientifically valid estimate of performance, not the largest possible benchmark score.

## Allowed Changes

Methodology changes are allowed when justified independently of the observed metric, including correcting leakage, invalid splits, preprocessing inconsistency, label or spatial alignment errors, documented domain shift, sampling bias, statistical validity, or operational requirements.

Every material change must record what changed, why, supporting evidence, affected versions, before/after metrics, and validation performed.

## Forbidden Metric-Gaming

Reject or escalate changes whose primary justification is metric improvement when they compromise validity, including changing spatial/temporal splits solely because the score increases, removing difficult samples, moving validation/test data into training, selecting the test set after seeing results, changing evaluation population/geography without predefined justification, preprocessing leakage, repeated methodology changes until a target score is reached, suppressing unfavorable results, changing labels/classes solely to improve scores, or silently changing metric definitions/thresholds after seeing results.

## Decision Procedure

1. Identify the scientific problem being corrected.
2. State the intended generalization/deployment target.
3. Determine whether the change is justified independently of the observed metric.
4. Check leakage, selection bias, data exclusion, and evaluation-population changes.
5. Record the proposed change and rationale.
6. Compare old and new protocols.
7. Validate the new protocol.
8. Preserve original experiment lineage.
9. Escalate ambiguous cases.

## Enforcement

Apply this gate before selecting final experiments, promoting models, comparing model versions, accepting methodology-changing remediation, reporting benchmark results, or declaring GeoAI work complete.

A metric-gaming change must never receive PASS merely because the resulting score is higher.

## Definition of Done

- [ ] Evaluation protocol is explicit and versioned.
- [ ] Generalization target is explicit.
- [ ] Material methodology changes have documented rationale.
- [ ] Leakage and selection-bias checks pass.
- [ ] Original and changed experiment lineage is preserved.
- [ ] Metric changes are not the sole justification for methodology changes.
- [ ] Ambiguous scientific changes are escalated.
- [ ] Final metrics are traceable to the exact evaluation protocol that produced them.
