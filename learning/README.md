# Evidence-Driven Learning Architecture

This directory defines the controlled learning boundary between user projects and the public repository.

## Goal

Allow experience from many projects to improve the repository **without turning GitHub into a raw project-memory database**.

## Autonomous architecture

```text
USER PROJECTS
     ↓
sanitized observations
     ↓
learning candidate
     ↓
validation / evaluation
     ↓
ACCEPT candidate
     ↓
promotion proposal
     ↓
automated approval
   ├── BLOCKED → stop
   └── AUTO_APPROVED
          ↓
controlled integration
          ↓
CI / release
```

## Autonomous approval

The learning system does not require a human to be online for normal, low-risk, validated learning.

A proposal is automatically approved only when all deterministic gates pass:

- candidate status is `ACCEPT`
- provenance is valid
- reproducibility passes
- privacy review passes
- conflict check passes
- validation plan exists
- required regression coverage passes
- target artifact is allowlisted
- change is non-destructive
- no secrets or raw project data are present

Anything outside this policy is blocked rather than guessed.

## Safety boundary

Approval and mutation remain separate. `AUTO_APPROVED` authorizes the proposal for the next controlled integration step; it does not execute arbitrary code or silently rewrite repository knowledge.

## What GitHub stores

GitHub is the source of truth for:

- reusable skills
- validated engineering rules
- contracts and invariants
- evaluation cases
- safe fixtures
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

## Design rule

> Projects produce evidence. Validation and automated approval determine what is safe, generalizable, and technically justified to teach the repository.
