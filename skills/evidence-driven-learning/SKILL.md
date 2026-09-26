---
name: evidence-driven-learning
description: Privacy-safe, validated learning protocol for turning recurring project evidence into reusable repository knowledge without overwriting existing skills or collecting raw project data.
---

# Evidence-Driven Learning

This skill defines how project experience can improve the repository without making the repository a raw memory store.

## Core principle

> Projects produce evidence. Validation decides what becomes reusable knowledge.

Never treat a single project observation as automatically valid global knowledge.

## Separation of concerns

Keep these layers distinct:

1. **Project Memory** — detailed state for one project.
2. **Learning Candidate** — sanitized, non-authoritative observation that may generalize.
3. **Validated Knowledge** — evidence-backed rule, pattern, anti-pattern, fixture, contract, or skill improvement.
4. **Skill Version** — the released implementation of validated knowledge.

Project memory must not be copied wholesale into repository knowledge.

## Learning pipeline

Use this flow:

```text
Project
  ↓
Observation
  ↓
Sanitize
  ↓
Deduplicate / aggregate
  ↓
Validate reproducibility and generality
  ↓
Regression / evaluation
  ↓
Accept, reject, or escalate
  ↓
Versioned repository change
```

## Non-destructive evolution

Never destructively overwrite validated knowledge.

When new evidence concerns an existing capability:

- preserve the previous behavior/history
- update the relevant skill or contract through a versioned change
- add regression coverage when behavior changes
- document why the change was made
- keep rollback possible through Git history

Create a new skill only when the capability is genuinely distinct. Do not create duplicate skills for small variations of the same responsibility.

## Evidence thresholds

Before promoting a candidate, ask:

- Is the observation reproducible?
- Is it generalizable beyond one project?
- Is there enough independent evidence?
- Does it conflict with existing knowledge?
- Can the claim be tested deterministically or with an explicit runtime adapter?
- Does it improve correctness, reliability, security, performance, usability, or scientific validity?
- Does the change introduce regressions?

Repeated evidence is useful, but frequency alone is not proof.

## Privacy rules

Never promote or transmit:

- secrets or credentials
- source code from private projects
- proprietary datasets
- customer/client information
- private coordinates or sensitive locations
- raw conversations
- personal information
- project identifiers that are not needed for the generalized lesson

Prefer derived, minimal evidence such as:

- domain
- generalized problem
- observed pattern
- anonymized outcome
- validation evidence
- test/fixture reference

## User control

Learning contribution must be explicit and controllable.

Default behavior:

- project work remains local/project-scoped
- no raw project data is uploaded to the public repository
- no automatic public contribution is assumed

A project may explicitly request a learning review, after which the system can produce sanitized candidates for validation.

## Conflict handling

If new evidence conflicts with an existing skill:

```text
New evidence
  ↓
Conflict detected
  ↓
Do not silently override
  ↓
Reproduce / compare evidence
  ↓
Escalate if unresolved
```

Existing validated knowledge remains authoritative until the new change passes the required validation.

## Output types

A learning result should be one of:

- `REJECT` — insufficient, private, unsafe, or non-generalizable
- `CANDIDATE` — promising but not yet validated
- `ACCEPT` — validated and suitable for repository integration
- `ESCALATE` — conflicting or methodology-sensitive evidence requiring review

## Repository integration

Accepted learning may become:

- a skill rule
- an anti-pattern
- an evaluation case
- a contract invariant
- a decision-matrix entry
- a fixture
- documentation
- a performance/security regression test

Do not put every accepted observation into a single large memory file. Put knowledge in the repository artifact that owns the responsibility.
