# Project State

## Project
WebGIS Claude Skills

## Phase
Controlled evidence-to-knowledge promotion

## Objective
Build a reusable, production-oriented Claude Code skill system for Web GIS, GIS portals, GeoAI, remote sensing, spatial software, desktop GIS, 3D, real-time GIS, testing, security, deployment, persistent project resumption, and controlled evidence-driven learning.

## Last Verified Step
Implemented and verified the deterministic evidence-to-knowledge promotion gate.

Verified components:
- promotion contract
- deterministic promotion validator
- promotion proposal fixture
- promotion validator smoke tests
- CI promotion-validation job

Latest verified CI:
- Run #56
- ID: 36225850078
- Head SHA: d561a91e0416d91d94b88ac2687268a417f6d714
- Conclusion: success

## Validation Performed
- Verified CI Run #56 completed successfully.
- Promotion validation is now a required CI quality gate.
- Promotion proposals cannot mutate repository knowledge.
- Promotion requires an ACCEPT candidate, passed privacy/conflict/reproducibility checks, explicit target artifact, regression evidence when required, and maintainer review state.
- The workflow remains explicit-review based; no automatic repository promotion or telemetry is enabled.

## Current Blocker
None for the verified promotion gate.

## Exact Next Action
Implement the controlled promotion proposal generator. It should consume an accepted learning candidate plus explicit artifact intent and produce a sanitized promotion proposal for review. It must refuse non-ACCEPT candidates, preserve candidate provenance, avoid raw project data, and never mutate repository artifacts.

## Do-Not-Repeat
- Do not treat raw project memory as repository knowledge.
- Do not automatically overwrite validated skills with new observations.
- Do not collect or upload raw project data, conversations, secrets, or proprietary datasets.
- Do not rebuild the repository from scratch.
- Do not overwrite existing project files without inspecting them.
- Do not add duplicate skills when an existing skill already covers the responsibility.
- Do not hard-code a framework or provider without a requirements-based decision.
- Do not claim GIS correctness without explicit CRS, units, data, and validation evidence.
- Do not treat a valid contribution manifest as accepted repository knowledge.
- Do not enable telemetry or public contribution without explicit opt-in.
- Do not let a promotion validator or generator mutate repository knowledge.
