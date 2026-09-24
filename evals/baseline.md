# Evaluation Baseline

The baseline is the set of reviewed evaluation results accepted as the current reference.

## Rules

- Baseline changes require deliberate review.
- A newly added case starts without a PASS baseline until executed and reviewed.
- Skill changes must be evaluated against relevant cases.
- Anti-pattern or remediation changes require regression evaluation.
- Do not lower expected validation requirements merely to preserve PASS status.
- Keep baseline artifacts free of secrets and sensitive project data.

## Initial Baseline State

The current cases are defined, but no execution result is claimed until an actual runner executes them.
