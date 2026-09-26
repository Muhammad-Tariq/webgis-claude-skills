# Privacy-Safe Contribution Protocol

This protocol defines the optional boundary for exporting reusable learning evidence from a user project to the public repository.

## Default

**Local-only is the default.** No telemetry, background upload, automatic GitHub contribution, or automatic promotion is enabled by this repository.

A contribution may leave a project boundary only after explicit user or organization opt-in.

## Flow

```text
Project memory / observations
          |
          v
   Generalize locally
          |
          v
    Sanitize locally
          |
          v
  Contribution manifest
          |
          +----> local deterministic validation
          |
          v
   Human inspection
          |
          v
  Explicit contribution
          |
          v
 Maintainer review / PR
          |
          v
 Repository CI
          |
          v
 Versioned integration
```

## Export boundary

A contribution package may contain only the minimum evidence needed to explain a reusable engineering claim.

Allowed examples:

- generalized observation
- generalized claim
- domain
- evidence class
- reproducibility status
- independent-project count
- proposed repository destination
- validation plan
- regression requirement
- privacy review result
- conflict review result

Do not export:

- raw project memory
- raw conversations
- private source code
- proprietary datasets
- credentials, tokens, passwords, private keys, or connection strings
- customer information
- unnecessary project names, IDs, URLs, or infrastructure details
- sensitive coordinates or locations
- file contents copied merely as evidence

## Explicit consent

The contribution manifest must record an explicit opt-in decision. Silence, default configuration, or repository presence is not consent.

Recommended consent fields:

- `opt_in: true`
- `consent_scope: repository_learning`
- `consent_timestamp: YYYY-MM-DD`

The timestamp records when consent was granted; it does not identify the project or person.

## Local validation

Before export:

1. Generalize the observation.
2. Remove project-specific identifiers.
3. Remove secrets and credentials.
4. Remove proprietary code/data.
5. Remove sensitive coordinates and unnecessary URLs.
6. Run the deterministic contribution validator.
7. Inspect the generated manifest manually.
8. Only then perform an explicit contribution action.

## No automatic promotion

A valid contribution is still only evidence.

```text
VALID contribution
      !=
ACCEPTED repository knowledge
```

Maintainers must independently review whether the evidence is technically sound, reproducible, generalizable, non-conflicting, and suitable for a public repository.

## Organizations

An organization may choose local-only operation permanently. If it opts in, the organization remains responsible for ensuring that exported generalized evidence is permitted to leave its project boundary.

The repository does not require project telemetry to improve.

## Threat model

The protocol is designed to reduce:

- accidental secret disclosure
- proprietary-data leakage
- project-identification leakage
- unreviewed knowledge pollution
- automatic propagation of bad engineering practices
- silent changes to validated skills

It is not a substitute for organizational privacy, security, legal, or data-governance review.
