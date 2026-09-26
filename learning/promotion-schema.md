# Evidence-to-Knowledge Promotion Contract

The promotion layer converts an ACCEPTED learning candidate into a proposed repository artifact. It is a gate, not an automatic publisher.

## Promotion states

- ELIGIBLE — candidate satisfies promotion prerequisites.
- BLOCKED — one or more prerequisites are missing or unsafe.
- ESCALATE — evidence or artifact ownership requires maintainer judgment.

Promotion never means that a repository file is automatically changed.

## Required promotion prerequisites

An ACCEPT candidate must have:
- privacy review passed
- conflict check passed
- reproducibility passed
- explicit validation plan
- explicit proposed repository destination
- provenance compatible with the evidence
- at least one independent project or a reproduced test
- regression result passed when regression is required

## Artifact destinations

A promotion proposal must map to exactly one primary repository artifact:
- skill
- contract
- anti-pattern
- evaluation_case
- fixture
- decision_matrix
- documentation
- regression_test

The destination must be explicit. The promotion validator does not modify the target artifact.

## Ownership and destructive-change rules

- Existing validated knowledge must never be silently overwritten.
- A proposal that changes an existing skill must identify the affected skill.
- Conflicting knowledge must be ESCALATE, not automatically resolved.
- A new capability should create a new artifact only when an existing artifact cannot responsibly own it.
- Promotion proposals must remain traceable to the candidate ID.

## Review boundary

Candidate → validation → promotion proposal → maintainer review → repository change → CI/regression → versioned knowledge.

A validator may mark a proposal ELIGIBLE, but only an explicit maintainer-reviewed repository change can promote knowledge.

## Provenance

Promotion metadata must preserve:
- candidate ID
- evidence class/provenance
- independent project count
- reproducibility result
- validation plan
- target artifact
- whether regression coverage is required

No raw project memory, conversation, source code, proprietary dataset, secret, credential, personal data, or sensitive coordinates may enter the promotion proposal.

## Core invariant

Validated evidence may authorize a proposed knowledge change; it must never silently mutate repository knowledge.
