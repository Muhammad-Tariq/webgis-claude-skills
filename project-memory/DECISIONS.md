# Decisions

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
