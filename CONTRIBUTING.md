# Contributing to WebGIS Claude Skills

Thank you for helping improve **WebGIS Claude Skills**.

This repository is open source and welcomes contributions that add durable engineering value to Web GIS, GIS, GeoAI, remote sensing, spatial data, testing, security, performance, scientific integrity, and agent workflows.

## What can you contribute?

| You want to… | Add or improve | Where it belongs |
|---|---|---|
| Add a reusable agent capability | **Skill** | `skills/<domain>/<skill>/SKILL.md` |
| Support a project type | **Project profile** | `profiles/` |
| Capture a technology trade-off | **Decision matrix** | `decision-matrices/` |
| Define a spatial/data/API rule | **Contract** | `contracts/` |
| Detect and remediate a bad GIS pattern | **Anti-pattern** | `evals/cases/` and relevant docs |
| Add deterministic test knowledge | **Fixture / evaluation case** | `fixtures/`, `evals/cases/`, `evals/` |
| Improve evidence-driven learning | **Learning artifact** | `learning/` |
| Improve documentation | **Docs** | `docs/`, `README.md` |
| Fix a software/CI issue | **Code / workflow** | Existing project path |

When a change does not clearly fit one category, open an issue or discussion first.

## Before you start

For larger changes, first explain the problem, proposed scope, affected areas, and validation approach in an issue or discussion. This helps prevent duplicated work and keeps the repository coherent.

For small fixes such as typos, broken links, or isolated documentation corrections, a direct pull request is fine.

## Development workflow

1. Fork the repository.
2. Create a focused branch from `main`.
3. Make one coherent change.
4. Add or update deterministic validation where practical.
5. Run the relevant local checks.
6. Commit your changes and open a pull request against `main`.

Typical Python validation:

```bash
python -m compileall -q evals learning
python evals/runner.py --output evals/local-results.json
python evals/ci_smoke.py --check all
python evals/learning_smoke.py
python evals/contribution_smoke.py
python evals/promotion_smoke.py
python evals/promotion_proposer_smoke.py
python evals/promotion_approval_smoke.py
python evals/integration_engine_smoke.py
```

Run only the commands relevant to the area you changed when the full suite is unnecessary, but do not claim checks you did not run.


## Development environment and package distribution

The project intentionally supports **both Node/npm and Python**. They serve different purposes and should not be treated as competing installation paths.

### 1. npm — primary skill/agent distribution

Use npm when you want to install and manage the WebGIS Claude Skills CLI for coding-agent projects.

After the package is published to npm:

```bash
npm install -g webgis-claude-skills
```

Install skills for all supported agent locations:

```bash
webgis-claude-skills install --agent all
```

Install for a specific agent:

```bash
webgis-claude-skills install --agent claude
webgis-claude-skills install --agent codex
webgis-claude-skills install --agent cursor
webgis-claude-skills install --agent opencode
```

Install the complete repository support bundle:

```bash
webgis-claude-skills install --full
```

Verify and diagnose:

```bash
webgis-claude-skills verify
webgis-claude-skills doctor
```

Update:

```bash
npm update -g webgis-claude-skills
webgis-claude-skills update --agent all
```

During development, before the npm package is published, the CLI can be executed directly from the GitHub repository:

```bash
npx github:Muhammad-Tariq/webgis-claude-skills install --agent all
```

### 2. npx — zero-install / one-off execution

npx remains supported for contributors and users who do not want a permanent global npm installation.

```bash
npx webgis-claude-skills install --agent all
npx webgis-claude-skills verify
npx webgis-claude-skills doctor
```

**npm and npx are intentionally both supported.** npm is the convenient persistent CLI installation; npx is the convenient ephemeral execution path.

### 3. Python — GIS development and runtime

Python is **not required** for the skill distribution layer. It remains fully supported for contributors working on the Python evaluation harness, GIS processing, remote sensing, GeoAI, GDAL workflows, or Python-based project integrations.

Core repository development:

```bash
python -m pip install -e .
```

The optional `[gis]` extra provides the standard Python geospatial development stack:

```bash
python -m pip install "webgis-claude-skills[gis]"
```

It includes:

| Package | Primary use |
|---|---|
| **NumPy** | Numerical arrays and scientific computing |
| **Pandas** | Tabular data processing |
| **Shapely** | Vector geometry operations |
| **PyProj** | CRS, coordinate transformation, geodesic operations |
| **GeoPandas** | GeoDataFrame/vector GIS workflows |
| **Rasterio** | Raster I/O and raster processing |

Optional specialized environments:

```bash
python -m pip install "webgis-claude-skills[gdal]"
python -m pip install "webgis-claude-skills[remote-sensing]"
```

- **GDAL** — advanced raster/vector geospatial processing; native dependencies may vary by operating system.
- **Earth Engine API** — Google Earth Engine / remote-sensing workflows.

### Recommended contributor setup

For contributors working on **skills, agent distribution, documentation, and Node tooling**:

```bash
npm install
npm test
npm run pack:check
```

For contributors working on **Python GIS/evaluation functionality**:

```bash
python -m pip install -e ".[gis]"
python -m compileall -q evals learning
```

Install additional extras only when the changed functionality needs them.

### Distribution architecture

```text
                    WebGIS Claude Skills
                            |
             +--------------+--------------+
             |              |              |
            npm            npx            pip
             |              |              |
       Persistent CLI   One-off CLI    Python runtime
             |              |              |
             +--------------+--------------+
                            |
                     Shared skill repo
                            |
          Claude / Codex / Cursor / OpenCode
```

The npm package stays lightweight and agent-focused. Python GIS dependencies are intentionally kept in Python extras rather than bundled into npm. This keeps agent installation fast while still giving GIS contributors a complete scientific/geospatial Python environment when required.

See [docs/installation.md](docs/installation.md) for the distribution architecture and [integrations/agent-support.json](integrations/agent-support.json) for the current compatibility registry.

## Adding a skill

A skill should be reusable rather than tied to one private project.

Include, where applicable:

- purpose and scope
- when it applies
- workflow
- decision rules
- inputs/outputs
- failure modes
- GIS/data correctness considerations
- security and performance implications
- validation requirements
- definition of done

Avoid embedding customer data, private project details, credentials, provider secrets, or proprietary source material.

## Adding an anti-pattern or evaluation case

Prefer the structure:

```text
Detection
→ Risk / Why it is wrong
→ Trigger
→ Correct pattern
→ Remediation
→ Validation
→ Regression protection
```

For executable cases, make the expected detection and remediation unambiguous and deterministic where possible.

GIS correctness cases should explicitly consider CRS, units, geometry validity, raster alignment, temporal assumptions, and spatial/temporal leakage where relevant.

Scientific integrity is part of the quality bar: a change must not alter an evaluation methodology merely to improve a metric.

## Evidence-driven learning contributions

Learning is deliberately separated into stages:

```text
Project evidence
→ Sanitization
→ Learning candidate
→ Validation
→ Promotion proposal
→ Automated approval
→ Controlled integration
→ CI / regression
→ Versioned knowledge
```

A contributor must never submit raw project memory as repository knowledge.

Do not include:

- raw conversations
- private source code
- proprietary datasets
- credentials, API keys, tokens, or secrets
- customer/patient/employee personal data
- unnecessary project identifiers or private URLs
- sensitive coordinates or location traces

Use the repository learning and contribution schemas. A valid learning manifest is **not** automatically accepted knowledge.

## Pull requests

Keep pull requests focused: one main concern per PR whenever practical.

Describe:

- **Problem** — what is missing or incorrect?
- **Why** — why does the repository need this change?
- **What changed** — concise implementation summary.
- **Affected surface** — skills, contracts, evaluations, CI, docs, etc.
- **Validation** — exact commands/checks you actually ran.
- **Limitations** — known gaps, blocked runtime checks, or follow-up work.

Use screenshots or examples when they materially improve understanding.

Do not include unrelated formatting churn or generated changes unless they are part of the change.

## Commit guidelines

Use clear imperative commit messages, for example:

```text
add PostGIS topology validation skill
fix raster alignment evaluation fixture
docs: clarify contribution privacy boundary
```

Avoid commits that bundle unrelated features, refactors, and dependency changes.

## Code and documentation standards

Prefer simple, explicit, testable implementations.

For Python:

- keep scripts dependency-light where possible
- fail closed when required GIS runtimes are unavailable
- return explicit states such as `PASS`, `FAIL`, `BLOCKED`, or `ESCALATE` where the surrounding contract requires them
- never hide verification failures behind successful exit codes

For GIS work:

- preserve CRS/SRID semantics
- distinguish display CRS from analysis CRS
- document units
- avoid destructive reprojection unless explicitly intended
- validate geometry/raster alignment when relevant
- prevent spatial and temporal leakage in GeoAI workflows

For documentation:

- write for maintainers and coding agents
- prefer concrete rules over vague advice
- keep examples reproducible
- preserve provenance and licensing information

## Security and privacy

Never commit secrets or confidential material.

If you discover a security vulnerability, **do not publish the details in a normal issue or pull request**. Follow [SECURITY.md](SECURITY.md).

Contributions must also respect the repository's privacy and learning boundaries.

## Licensing and attribution

This repository is licensed under the **Apache License 2.0**.

By intentionally submitting a contribution for inclusion in this repository, you agree that the contribution is provided under the same Apache-2.0 terms, unless a separate applicable license is explicitly identified and compatible with the repository's licensing requirements.

You must preserve required third-party copyright, license, patent, trademark, and attribution notices. Do not copy material from another project without checking its license and complying with its terms.

## Review and merge process

All contributors can fork the repository and submit pull requests.

Pull requests are expected to pass the repository's automated validation and CI checks relevant to the changed surface. Maintainers may request changes when correctness, reproducibility, licensing, privacy, security, or scope requirements are not satisfied.

A contribution being syntactically valid does not make it validated engineering knowledge; it must satisfy the relevant contract and evaluation gates.

## Issues and discussions

Use an issue for a concrete bug, feature request, or actionable repository problem.

Use Discussions for broader architecture questions, proposed directions, or questions that benefit from community feedback.

Please include enough technical context for another contributor to reproduce or understand the problem.

## Contributor recognition

Contributors are recognized through the normal GitHub contribution history and project records. Maintainers may also add curated acknowledgements in project documentation when appropriate.

## Project authorship and attribution

**WebGIS Claude Skills** is authored and maintained by **Tariq Azam**. See [AUTHORS.md](AUTHORS.md) for the project attribution record.

Community contributors retain authorship of their original contributions, subject to the Apache License 2.0 terms governing intentional submissions to the project. Required third-party attribution and license notices must be preserved.

## Code of Conduct

Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Participation in this project is conditional on following it.

---

**Thank you for contributing durable, reproducible GIS engineering knowledge.**
