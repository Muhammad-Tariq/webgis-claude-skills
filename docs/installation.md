# Installation

WebGIS Claude Skills has two distribution layers:

1. **Node/npm** for end users who want a coding-agent skill installation without Python.
2. **Python** for users who also work with Python GIS tooling such as GDAL, GeoPandas, Rasterio, Shapely, and PyProj.

The skill layer itself does not require Python.

## npm / npx

From the root of an existing project:

```bash
npx webgis-claude-skills install --agent all
```

This installs the skills into compatible project locations:

- `.agents/skills/`
- `.claude/skills/`
- `.cursor/skills/`
- `.opencode/skills/`

The installer generates compatible `SKILL.md` frontmatter when a repository skill does not already contain it.

For a single client:

```bash
npx webgis-claude-skills install --agent claude
npx webgis-claude-skills install --agent codex
npx webgis-claude-skills install --agent cursor
npx webgis-claude-skills install --agent opencode
```

For the complete repository support bundle:

```bash
npx webgis-claude-skills install --full
```

The support bundle is stored under `.webgis-claude-skills/` so it does not pollute the application source tree.

Global installation is also supported:

```bash
npx webgis-claude-skills install --scope global --agent all
```

Verify:

```bash
npx webgis-claude-skills verify
npx webgis-claude-skills doctor
```

Update:

```bash
npx webgis-claude-skills update --agent all
```

Pinned version:

```bash
npx webgis-claude-skills@0.1.0 install --agent all
```

The installer does **not** install Claude Code, Codex, Cursor, OpenCode, or other agent CLIs. It installs this repository's skills for clients that are already installed.

## Python

Python remains a first-class engineering/runtime option.

For repository development:

```bash
python -m pip install -e .
```

Optional GIS runtime dependencies:

```bash
python -m pip install -e ".[gis]"
```

GDAL bindings:

```bash
python -m pip install -e ".[gdal]"
```

The repository's existing Python evaluation harness remains available. The npm installer does not invoke it.

GDAL is a native geospatial stack and installation can depend on the platform and installed GDAL libraries. The official Python package is available through PyPI, but users should keep the Python GDAL binding compatible with their system GDAL when native libraries are involved.

## Architecture

```text
                    WebGIS Claude Skills
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
       npm / npx layer              Python layer
       skill distribution            GIS/runtime tooling
             │                           │
             ▼                           ▼
   .agents/.claude/.cursor/       GDAL / GeoPandas /
   .opencode skill discovery      Rasterio / Shapely /
                                  PyProj / scientific stack
```

The two layers are intentionally separate: users can use the skills without Python, while Python users can install the GIS runtime they actually need.
