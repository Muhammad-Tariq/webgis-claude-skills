# Decisions

## 2026-09-26
- Add an evidence-driven learning layer without changing the authority of existing skills.
- Keep project memory, learning candidates, validated repository knowledge, and released skills as separate layers.
- Do not treat GitHub as a raw project-memory database.
- Learning candidates must be privacy-reviewed, generalized, validated, and regression-protected before repository integration.
- New evidence must not destructively overwrite existing validated skills; use versioned evolution and preserve rollback through Git history.
- Create a new skill only when a capability is genuinely distinct; extend an existing skill when the responsibility is the same.
- Do not enable automatic telemetry or public project uploads as part of the learning foundation.

## 2026-09-23
- Use repository-backed Markdown files for durable project memory.
- Treat the codebase and tests as the source of truth when memory conflicts with implementation.
- Keep project memory separate from secrets and never store credential values.
- Build domain-specific Web GIS skills rather than installing a large unrelated skill collection.
- Do not treat React + TypeScript as a universal requirement; framework choice is requirements-driven.
- Use a project orchestrator to route only relevant skills.
- Put general software engineering beneath GIS-specific domain skills.
- Make GIS correctness an explicit cross-cutting gate rather than assuming ordinary software tests prove spatial correctness.
- Use an evidence-based technology decision engine with free-first evaluation and documented tradeoffs.
