from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(tempfile.mkdtemp(prefix="webgis-claude-skills-python-"))
CLI = "webgis-claude-skills"
LOCATIONS = [
    ".agents/skills",
    ".claude/skills",
    ".cursor/skills",
    ".opencode/skills",
]


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [CLI, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=check,
    )


version = subprocess.run(
    [CLI, "version"],
    text=True,
    capture_output=True,
    check=True,
).stdout.strip()
if not version:
    raise AssertionError("Python CLI returned an empty version")

run("install", "--agent", "all")
run("verify")

for location in LOCATIONS:
    base = ROOT / location
    if not base.is_dir():
        raise AssertionError(f"missing skill location: {location}")
    skills = [p for p in base.iterdir() if p.is_dir()]
    if len(skills) < 10:
        raise AssertionError(f"expected multiple skills in {location}")
    sample = skills[0] / "SKILL.md"
    text = sample.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"frontmatter missing in {sample}")
    if "name:" not in text or "description:" not in text:
        raise AssertionError(f"required frontmatter missing in {sample}")

marker_path = ROOT / ".webgis-claude-skills" / "INSTALL.json"
marker = json.loads(marker_path.read_text(encoding="utf-8"))
if marker["version"] != version:
    raise AssertionError("installation marker version mismatch")
if sorted(marker["skill_locations"]) != sorted(LOCATIONS):
    raise AssertionError("marker skill locations mismatch")
if not marker["managed_files"]:
    raise AssertionError("marker contains no managed files")

managed_sample = ROOT / marker["managed_files"][0]
managed_sample.write_text("managed mutation\n", encoding="utf-8")
result = run("install", "--agent", "all", check=False)
if result.returncode == 0:
    raise AssertionError("installer overwrote an unmanaged file without --force")

run("install", "--agent", "all", "--force")
if managed_sample.read_text(encoding="utf-8") == "managed mutation\n":
    raise AssertionError("--force did not restore the managed file")

print("Python CLI smoke test passed")
