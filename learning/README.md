# Evidence-Driven Learning Architecture

This directory defines the controlled learning boundary between user projects and the public repository.

## Goal

Allow experience from many projects to improve the repository **without turning GitHub into a raw project-memory database**.

The repository should learn reusable engineering knowledge, not private project history.

## Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                    USER PROJECTS                        │
│  Project A · Project B · ... · Project N               │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
              Project-scoped memory
                        │
                        ▼
              Sanitized observations
                        │
                        ▼
             Learning candidate intake
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
           Reject              Candidate
                                  │
                                  ▼
                       Evidence aggregation
                                  │
                                  ▼
                      Validation / evaluation
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
                 Escalate                    Accept
                                                │
                                                ▼
                                     Versioned repository change
                                                │
                                                ▼
                                         CI / release
```

## What GitHub stores

GitHub is the source of truth for:

- reusable skills
- validated engineering rules
- contracts and invariants
- evaluation cases
- fixtures that are safe to publish
- decision matrices
- anti-patterns
- documentation
- version history

## What GitHub does not store by default

Do not place the following in this repository:

- raw project memory
- raw conversations
- private source code
- proprietary datasets
- credentials or tokens
- customer information
- unnecessary project identifiers
- sensitive coordinates or locations

## 100-project model

If 100 projects produce 500 observations, the system should not create 500 permanent memory entries.

Instead:

```text
500 observations
      ↓
sanitize
      ↓
deduplicate
      ↓
aggregate recurring patterns
      ↓
validate
      ↓
possibly 1–20 reusable changes
```

The exact reduction is evidence-dependent. The important rule is that raw observations do not become permanent repository knowledge automatically.

## Non-destructive evolution

New knowledge must not silently replace old knowledge.

For an existing skill:

```text
Skill v1
  +
validated evidence
  ↓
Skill v2
```

The previous version remains recoverable through Git history and regression coverage.

Create a separate skill only when the new responsibility is genuinely distinct.

## Contribution modes

### Local-only

The project keeps its memory and learning candidates locally. Nothing is contributed to the public repository.

### Explicit opt-in

A user or organization explicitly enables sanitized learning contribution. Only the minimum generalized evidence required for validation may leave the project boundary.

### Maintainer-reviewed integration

Accepted candidates become repository changes through the normal validation and release process.

There is no assumption that a user must become a GitHub contributor.

## Design rule

> Users do not directly teach the repository. Their projects may produce evidence; the validation system determines what is safe, generalizable, and technically justified to teach the repository.
