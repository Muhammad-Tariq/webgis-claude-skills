<div align="center">

# WebGIS Claude Skills

### The engineering operating system for GIS software, GeoAI & spatial applications

<p>
  <a href="https://github.com/Muhammad-Tariq/webgis-claude-skills"><img src="https://img.shields.io/github/stars/Muhammad-Tariq/webgis-claude-skills?style=for-the-badge" alt="GitHub stars"></a>
  <a href="https://github.com/Muhammad-Tariq/webgis-claude-skills/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue?style=for-the-badge" alt="Apache 2.0"></a>
  <a href="https://github.com/Muhammad-Tariq/webgis-claude-skills"><img src="https://img.shields.io/github/last-commit/Muhammad-Tariq/webgis-claude-skills?style=for-the-badge" alt="Last commit"></a>
</p>

<p>
  <b>Architecture</b> · <b>GeoAI</b> · <b>Remote Sensing</b> · <b>PostGIS</b> · <b>GeoServer</b> · <b>OGC</b> · <b>3D GIS</b> · <b>Testing</b> · <b>Security</b> · <b>Performance</b> · <b>Evidence-Driven Learning</b>
</p>

</div>

---

## What is this?

**WebGIS Claude Skills** is a repository-backed engineering skill system for building reliable GIS software with AI coding agents.

It is designed to help an agent move from:

**Requirement → Architecture → Design → Data Contracts → Implementation → Validation → Security → Performance → Documentation → Persistent Memory**

The goal is not simply to generate GIS code. The goal is to make the agent reason about **spatial correctness, scientific validity, scalability, security, cost, reproducibility, production operations, and validated learning**.

### Why it exists

GIS applications fail in ways that ordinary software assistants often miss:

- incorrect CRS or measurement assumptions
- invalid geometry and raster misalignment
- spatial/temporal leakage in GeoAI
- huge GeoJSON payloads and browser overload
- unbounded spatial APIs
- insecure GeoServer/OGC exposure
- provider-secret leakage
- expensive cloud choices without requirements
- scientifically invalid methodology chosen because it improves a metric

This repository turns those concerns into **skills, contracts, anti-patterns, decision matrices, fixtures, executable evaluations, persistent project memory, and a controlled evidence-driven learning pipeline**.

---

## Visual workflow

<p align="center">
  <img src="docs/assets/engineering-loop.svg" alt="WebGIS Claude Skills engineering loop" width="96%">
</p>

> The visual is intentionally part of the repository homepage so the project communicates its architecture before a visitor reads the details.

---

## Visual architecture

<p align="center">
  <img src="docs/assets/system-architecture.svg" alt="WebGIS Claude Skills system architecture" width="96%">
</p>

## GIS technology stack

<p align="center">
  <img src="docs/assets/gis-stack.svg" alt="GIS technology stack supported by the repository" width="96%">
</p>

## Scientific integrity

<p align="center">
  <img src="docs/assets/scientific-integrity.svg" alt="Scientific integrity gate" width="96%">
</p>

## Engineering loop

```text
                        USER REQUIREMENT
                               │
                               ▼
                    ┌────────────────────┐
                    │ PROJECT ORCHESTRATOR│
                    └──────────┬─────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ARCHITECTURE       DESIGN SYSTEM    DATA CONTRACTS
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                        IMPLEMENTATION
                               │
                               ▼
                    ┌────────────────────┐
                    │ QUALITY EVALUATION │
                    ├────────────────────┤
                    │ GIS Correctness    │
                    │ Scientific Integrity│
                    │ API / Security     │
                    │ Scalability        │
                    │ Performance        │
                    │ Regression         │
                    └──────────┬─────────┘
                               ▼
                         VERIFIED STATE
                               │
                               ▼
                        PROJECT MEMORY
```

---

## Core capabilities

| Capability | Purpose |
|---|---|
| **Project Orchestrator** | Classify projects, select skills, order work, and enforce gates |
| **Project Memory** | Resume interrupted work from the last verified state |
| **Evidence-Driven Learning** | Turn sanitized recurring project evidence into validated, versioned repository knowledge |
| **Software Engineering** | Architecture, modularity, APIs, resilience, testing, documentation |
| **Web GIS** | Frontend, map engines, GIS UX, APIs, spatial services |
| **PostGIS / GeoServer** | Spatial data modeling, indexing, OGC services, publishing |
| **Remote Sensing / GEE** | Satellite processing, temporal analysis, reproducible workflows |
| **GeoAI** | Spatial ML, foundation models, leakage controls, deployment |
| **GIS Correctness** | CRS, units, geometry, raster alignment, analytical validity |
| **Security** | Threat modeling, access control, resource protection, secrets |
| **Performance** | Measured budgets, profiling, large-data strategies, regression |
| **Evaluation Harness** | Deterministic cases, adapters, PASS/FAIL/BLOCKED/ESCALATE |
| **Anti-Pattern Remediation** | Detect → explain → correct → validate → regression-protect |

---

## Scientific integrity details

A core rule of the system is:

> **The system must never modify scientific methodology merely to artificially improve model metrics.**

A higher F1, IoU, accuracy, R², or other score does not automatically mean a better model when the evaluation protocol changed or became less valid.

The system instead records:

- methodology
- scientific rationale
- evaluation protocol
- dataset/model versions
- before/after metrics
- validation evidence
- experiment lineage

Ambiguous methodology changes are escalated rather than silently accepted.

---


## Evidence-driven learning

The repository can evolve from experience across many projects without treating GitHub as a raw memory database.

The controlled model is:

Project memory
→ Sanitized observation
→ Learning candidate
→ Deduplication / aggregation
→ Privacy + generalization checks
→ Validation / regression
→ Versioned repository knowledge

**Project memory stays project-scoped by default.** Raw conversations, private source code, proprietary datasets, secrets, customer data, and sensitive locations are not repository learning inputs.

A new observation must not silently overwrite an existing skill. If it belongs to an existing capability, the skill evolves through a versioned, validated change. A separate skill is created only when the responsibility is genuinely distinct.

See learning/README.md, learning/schema.md, and learning/PRIVACY.md.

## CRS intelligence

The system explicitly separates:

**Native CRS ≠ Display CRS ≠ Analysis CRS**

This allows datasets with different native coordinate reference systems to coexist in the same map without mutating their source data.

Permanent reprojection is treated as a deliberate data transformation, not a side effect of visualization.

---

## Evaluation architecture

The repository includes executable evaluation building blocks for:

```text
CRS
 ↓
Geometry
 ↓
Raster
 ↓
GeoAI
 ↓
Scientific Integrity
 ↓
Web GIS Scalability
 ↓
Spatial API
 ↓
Security
 ↓
Performance
 ↓
Learning Safety
 ↓
Regression
```

Evaluation results distinguish:

- **PASS**
- **FAIL**
- **BLOCKED**
- **ESCALATE**

A plausible patch is never treated as verified without the required validation.

---

## Anti-pattern remediation

The system is designed to do more than document bad patterns.

```text
Anti-pattern
     ↓
Detection
     ↓
Classification
     ↓
Explain risk
     ↓
Select correct pattern
     ↓
Auto-fix when safe
     ↓
Validate
     ↓
Regression protection
```

Examples include:

- giant GeoJSON
- client-side million-feature overload
- unbounded spatial queries
- degree-based planar distance
- mixed-CRS analysis
- raster grid misalignment
- spatial ML leakage
- temporal leakage
- provider secrets in the browser
- unrestricted WFS
- raster full-download workflows
- map reinitialization
- N+1 spatial requests

---

## Repository structure

```text
webgis-claude-skills/
├── skills/
│   ├── core/
│   ├── webgis/
│   ├── spatial/
│   ├── remote-sensing/
│   ├── geoai/
│   ├── 3d/
│   ├── desktop/
│   ├── realtime/
│   ├── infrastructure/
│   ├── quality/
│   └── scientific-integrity/
├── profiles/
├── decision-matrices/
├── contracts/
├── anti-patterns/
├── fixtures/
├── evals/
├── learning/
├── templates/
└── project-memory/
```

> The repository currently keeps proven existing paths stable while the broader target architecture is established through compatible additions rather than a risky bulk reorganization.

---

## Project profiles

The orchestrator can classify work as:

- Web GIS application
- GIS portal
- GeoAI platform
- Remote-sensing platform
- GIS dashboard
- Desktop GIS
- GIS API/service
- GIS data pipeline
- 3D GIS
- Real-time GIS
- Enterprise GIS
- Scientific/research GIS
- Commercial GIS SaaS

Hybrid projects are supported.

---

## Technology selection

The system does not hard-code a single framework.

Technology choices are requirements-driven and can evaluate, where relevant:

**Frontend:** React/Vite, Next.js, Vue/Nuxt, Angular, Svelte/SvelteKit

**Maps:** MapLibre GL JS, OpenLayers, Leaflet, Cesium

**Backend:** FastAPI/Python, Node/TypeScript, .NET, Java/Spring, Go

**Spatial database:** PostGIS, SQLite/GeoPackage

**Raster:** COG/GDAL, object storage, STAC, raster services

**Point cloud:** LAS/LAZ, COPC, PDAL, 3D Tiles

**Deployment:** VPS, containers, managed infrastructure, Kubernetes, on-premises, hybrid

The decision engine records constraints, alternatives, evidence, cost/licensing implications, and exit considerations.

---

## Free-first and licensing

The default policy is:

> **Use the best viable free/open-source option first.**

Paid services are considered when a concrete requirement justifies them, such as scale, SLA, proprietary data, production GPU throughput, or managed reliability.

This repository is licensed under **Apache License 2.0**.

Third-party components, if incorporated later, should retain their original license and attribution requirements.

---

## Using the skills

The repository is intended for coding-agent workflows that can read repository files and skills.

A typical session follows:

```text
1. Load project memory
2. Classify the project
3. Select relevant skills
4. Resolve architecture / technology gates
5. Inspect the existing implementation
6. Implement the smallest coherent change
7. Run domain + correctness + security + performance checks
8. Run relevant evaluation cases
9. Record the verified state
10. Optionally derive sanitized learning candidates
11. Commit and continue from the exact next action
```

---

## Current evaluation adapters

- CRS metadata/invariant checks
- Geometry fixture checks
- Raster metadata/alignment checks
- GeoAI experiment/leakage checks
- Web GIS scalability checks
- Spatial API/security checks
- Performance budget/regression checks

Learning safety currently has a deterministic contract case covering unvalidated automatic promotion. Runtime aggregation/telemetry is intentionally not enabled by this repository.

The harness deliberately refuses to claim numerical correctness when a real computational engine is required but not executed.

---

## Roadmap

### Foundation
- [x] Repository-backed project memory
- [x] Project orchestrator
- [x] Software engineering foundation
- [x] GIS correctness gate
- [x] Technology decision engine
- [x] Project profiles
- [x] Data contracts
- [x] Golden GIS fixtures
- [x] Evidence-driven learning boundary

### Domain engineering
- [x] Web GIS architecture/frontend/map engine/UX
- [x] PostGIS
- [x] GeoServer
- [x] Spatial APIs
- [x] Remote sensing / GEE
- [x] GeoAI
- [x] Raster / LiDAR / 3D / OGC
- [x] Desktop / real-time
- [x] DevOps / observability / performance

### Quality and research integrity
- [x] Anti-pattern remediation
- [x] Executable evaluation harness
- [x] Scientific integrity gate
- [x] Scalability evaluation
- [x] API/security evaluation
- [x] Performance regression checks
- [x] Learning safety case
- [ ] Unified evaluation command with pluggable runtime adapters
- [ ] Learning candidate validator
- [ ] Optional privacy-safe contribution protocol
- [ ] CI regression execution for deterministic cases
- [ ] Repository health dashboard
- [ ] Public skill/version manifest
- [ ] Release automation

---

## Contributing

Contributions should add durable engineering value.

When adding a skill, contract, anti-pattern, fixture, evaluation, or learning candidate:

1. define the problem and scope
2. add deterministic validation where possible
3. document assumptions and failure modes
4. preserve licensing and provenance
5. avoid secrets and private project data
6. keep learning candidates non-authoritative until validated
7. update project memory
8. verify before claiming completion

---

## License

Apache License 2.0. See [LICENSE](LICENSE).

---

<div align="center">

**Built for serious GIS engineering with coding agents.**

[Repository](https://github.com/Muhammad-Tariq/webgis-claude-skills)

</div>
