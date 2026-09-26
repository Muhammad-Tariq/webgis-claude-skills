# Community & Contribution

WebGIS Claude Skills is an open-source project for reusable GIS engineering knowledge and coding-agent workflows.

## Start here

- **New contributor:** read [CONTRIBUTING.md](../CONTRIBUTING.md).
- **Bug:** use the [bug report template](https://github.com/Muhammad-Tariq/webgis-claude-skills/issues/new?template=bug_report.yml).
- **Feature or new capability:** use the [feature request template](https://github.com/Muhammad-Tariq/webgis-claude-skills/issues/new?template=feature_request.yml).
- **Security issue:** follow [SECURITY.md](../SECURITY.md) instead of opening a public issue.
- **Licensing question:** check [LICENSE](../LICENSE) and the licensing section of [CONTRIBUTING.md](../CONTRIBUTING.md).

## What makes a useful contribution?

The project favors contributions that can be reused across multiple GIS projects:

- GIS engineering skills
- WebGIS architecture patterns
- CRS and spatial correctness rules
- PostGIS and GeoServer practices
- Remote-sensing and GeoAI workflows
- deterministic fixtures and evaluation cases
- security and performance checks
- project profiles and technology decision matrices
- documentation and reproducibility improvements
- privacy-safe, generalized learning candidates

A contribution should explain **why the knowledge is reusable**, not only how it solved one private project.

## Contribution quality path

```text
Idea / Problem
      ↓
Issue or focused PR
      ↓
Scope + provenance
      ↓
Implementation
      ↓
Deterministic validation
      ↓
GitHub CI
      ↓
Review / merge
      ↓
Versioned repository knowledge
```

For evidence-driven learning, the additional controlled path is:

```text
Project evidence
      ↓
Local sanitization
      ↓
Learning candidate
      ↓
Validation
      ↓
Promotion proposal
      ↓
Automated approval
      ↓
Controlled integration
      ↓
CI / regression
```

The second path must never be used to publish raw project memory, secrets, private source code, proprietary datasets, customer information, or sensitive locations.

## Contributor recognition

Contributors retain authorship of their own original contributions. The repository preserves required third-party attribution and licensing notices.

Project authorship and primary attribution:

**Tariq Azam**

See [AUTHORS.md](../AUTHORS.md) for the project attribution record.

## Forks and derivative projects

You are welcome to fork, adapt, and build on the repository under the terms of the Apache License 2.0, subject to its conditions and any applicable third-party licenses.

Derivative projects should preserve required copyright, license, patent, trademark, and attribution notices.

## Community expectations

Please keep technical discussion:

- evidence-driven
- reproducible where practical
- respectful
- focused on the engineering problem
- explicit about uncertainty and limitations

See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).

## Development environments

Contributors can work with both the **Node/npm agent distribution** and the **Python GIS runtime**.

### npm CLI

After npm publication:

```bash
npm install -g webgis-claude-skills
webgis-claude-skills install --agent all
```

Useful commands:

```bash
webgis-claude-skills verify
webgis-claude-skills doctor
webgis-claude-skills update --agent all
```

For one-off execution without a global install:

```bash
npx webgis-claude-skills install --agent all
```

Before the package is published, use the GitHub source form:

```bash
npx github:Muhammad-Tariq/webgis-claude-skills install --agent all
```

### Python GIS stack

Python is optional for agent skill installation, but is recommended when contributing to GIS processing, evaluation, remote sensing, GeoAI, or Python tooling.

Install the standard GIS contributor stack:

```bash
python -m pip install "webgis-claude-skills[gis]"
```

This provides **NumPy, Pandas, Shapely, PyProj, GeoPandas, and Rasterio**.

Optional:

```bash
python -m pip install "webgis-claude-skills[gdal]"
python -m pip install "webgis-claude-skills[remote-sensing]"
```

The first adds GDAL; the second adds the Earth Engine API.

### Which should I use?

| Work | Recommended path |
|---|---|
| Install skills into an agent project | **npm** |
| Run the installer without global installation | **npx** |
| Develop Python GIS/evaluation code | **pip + [gis]** |
| GDAL-specific work | **pip + [gdal]** |
| Earth Engine/remote sensing work | **pip + [remote-sensing]** |

The two ecosystems are deliberately separated: **npm distributes the agent skills/CLI; Python provides the GIS/scientific runtime when a contributor needs it.**
