# Contribution Safety Checklist

Use this checklist before any learning evidence leaves a project boundary.

## Consent

- [ ] Explicit opt-in was given.
- [ ] `opt_in` is exactly `true`.
- [ ] `consent_scope` is `repository_learning`.
- [ ] Consent date is recorded.

## Minimization

- [ ] No raw project memory.
- [ ] No raw conversation.
- [ ] No private source code.
- [ ] No proprietary dataset content.
- [ ] No customer/personal information.
- [ ] No credentials, tokens, passwords, private keys, or connection strings.
- [ ] No sensitive coordinates.
- [ ] No unnecessary project identifiers or infrastructure details.
- [ ] No unnecessary URLs.

## Evidence

- [ ] The claim is generalized.
- [ ] The evidence class is correctly selected.
- [ ] Reproducibility is documented.
- [ ] Independent evidence is counted honestly.
- [ ] Conflicts with existing knowledge are checked.
- [ ] A repository destination is explicitly proposed.
- [ ] Regression/evaluation requirements are identified.

## Validation

- [ ] Deterministic contribution validator passes.
- [ ] Smoke tests pass.
- [ ] Human inspection is complete.
- [ ] Contribution is still treated as evidence, not accepted knowledge.
- [ ] No automatic upload or automatic promotion is enabled.

## Final boundary

**A passing manifest permits review. It does not authorize repository integration.**
