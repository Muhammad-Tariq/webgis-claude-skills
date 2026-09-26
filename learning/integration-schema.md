# Controlled Integration Contract

The integration layer converts an `AUTO_APPROVED` promotion proposal into a deterministic `INTEGRATION_READY` plan.

## Rules
- Approval must be `AUTO_APPROVED`.
- Target path must be repository-relative and belong to an allowlisted artifact directory.
- Target type and target path must agree.
- Only `add` and `update` changes are supported.
- The engine never executes proposal-supplied code.
- The engine never copies raw project memory, secrets, or proprietary data.
- The engine itself does not mutate repository knowledge.
- Repository CI must run after an applied change.

## Safety boundary
`INTEGRATION_READY` means the proposal passed the integration policy. It is not a license to execute arbitrary commands.

## Core invariant
> Automated approval can authorize learning, but integration remains deterministic, bounded, auditable, and CI-verified.