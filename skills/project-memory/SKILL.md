---
name: project-memory
description: Persistent project-state and resume protocol for Claude Code. Use at the start of every task/session and before stopping work so interrupted sessions can continue from the last verified state.
---

# Project Memory

This skill provides durable, repository-backed memory for Web GIS projects. Never rely only on chat history for project continuity.

## Start-of-session protocol

Before implementing or changing code:

1. Read `STATE.md`.
2. Read `TASKS.md`.
3. Read `DECISIONS.md`.
4. Read `SESSION.md`.
5. Read `BLOCKERS.md` when present.
6. Check `git status`.
7. Inspect recent commits relevant to the current task.
8. Inspect the current implementation before assuming anything is complete.
9. Identify the last **verified** state.
10. Continue from the recorded next action.

If the project memory conflicts with the codebase, trust the codebase and tests as the source of truth, then repair the memory files.

## Resume rule

When starting after an interruption, explicitly determine:

- What was last completed and verified?
- What was in progress?
- Which files were being changed?
- What remains?
- What is blocked?
- What is the exact next action?

Do not restart completed work merely because the session is new.

## During work

Update memory when there is a meaningful change in:

- task status
- architecture
- implementation direction
- blocker
- validation/test result
- important dependency
- deployment state

Keep entries factual and concise.

## Before stopping

Always update:

- `STATE.md`: current phase, current objective, last verified step, exact next step.
- `TASKS.md`: completed, in-progress, and pending tasks.
- `SESSION.md`: what happened during this session.
- `BLOCKERS.md`: active blockers only.
- `DECISIONS.md`: durable technical decisions.
- `CHANGELOG.md`: notable user-visible or architectural changes.

Never claim a task is complete unless it was actually implemented and, where applicable, tested.

## Safe-stop record

Use this structure in `STATE.md`:

- Project
- Phase
- Objective
- Last verified step
- Files changed
- Validation performed
- Current blocker
- Exact next action
- Do-not-repeat notes

## Web GIS-specific continuity

When relevant, also record:

- frontend stack and map engine
- CRS/SRID assumptions
- PostGIS schema changes
- GeoServer workspace/layer/style changes
- API endpoints/contracts
- raster/vector data sources
- model/version information for GeoAI or remote sensing
- deployment environment
- environment variables by name only, never secret values

## Hard rules

- Never store API keys, passwords, tokens, private credentials, or secret values.
- Never overwrite project memory blindly.
- Prefer append/update with timestamps where useful.
- Keep `STATE.md` short enough to read at every session.
