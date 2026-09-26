from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

VERSION = "0.1.0"
REPO = "Muhammad-Tariq/webgis-claude-skills"
AGENTS = {
    "agents": [".agents/skills"],
    "claude": [".claude/skills"],
    "codex": [".agents/skills"],
    "cursor": [".cursor/skills"],
    "opencode": [".opencode/skills"],
    "all": [".agents/skills", ".claude/skills", ".cursor/skills", ".opencode/skills"],
}


def skill_frontmatter(name: str, text: str) -> str:
    if text.startswith("---\n"):
        return text
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), name)
    if "## Purpose" in text:
        purpose_lines = text.split("## Purpose", 1)[1].splitlines()
        description = " ".join(line.strip() for line in purpose_lines[1:3] if line.strip()).strip()
    else:
        description = title
    description = description or title
    description = " ".join(description.split())[:1000]
    safe_name = "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-")[:64]
    return (
        "---\n"
        f"name: {safe_name}\n"
        f"description: {description}\n"
        "license: Apache-2.0\n"
        "compatibility: agent-skills\n"
        "metadata:\n"
        "  source: webgis-claude-skills\n"
        f"  version: {VERSION}\n"
        "---\n\n"
        + text.lstrip()
    )


def source_root() -> Path:
    override = os.environ.get("WEBGIS_CLAUDE_SKILLS_SOURCE_ROOT")
    if override:
        candidate = Path(override).expanduser().resolve()
        if not (candidate / "skills").is_dir():
            raise RuntimeError("WEBGIS_CLAUDE_SKILLS_SOURCE_ROOT must contain a skills directory")
        return candidate
    local = Path(__file__).resolve().parents[1]
    if (local / "skills").is_dir():
        return local
    archive_url = f"https://github.com/{REPO}/archive/refs/tags/v{VERSION}.tar.gz"
    tmp = Path(tempfile.mkdtemp(prefix="webgis-claude-skills-"))
    archive = tmp / "repo.tar.gz"
    with urllib.request.urlopen(archive_url, timeout=30) as response:
        archive.write_bytes(response.read())
    extract = tmp / "repo"
    extract.mkdir()
    with tarfile.open(archive, "r:gz") as tf:
        root = Path(tf.getmembers()[0].name).parts[0]
        for member in tf.getmembers():
            target = Path(member.name)
            if target.is_absolute() or ".." in target.parts:
                raise RuntimeError("unsafe archive path")
        tf.extractall(extract)
    return extract / root


def install(args: argparse.Namespace) -> int:
    root = Path.home() if args.scope == "global" else Path.cwd()
    source = source_root()
    managed: set[str] = set()
    marker = root / ".webgis-claude-skills" / "INSTALL.json"
    if marker.exists():
        try:
            managed.update(json.loads(marker.read_text(encoding="utf-8")).get("managed_files", []))
        except Exception:
            pass

    for relative in AGENTS[args.agent]:
        dest = root / relative
        for skill_dir in (source / "skills").iterdir():
            if not skill_dir.is_dir():
                continue
            target = dest / skill_dir.name
            target.mkdir(parents=True, exist_ok=True)
            for src in skill_dir.rglob("*"):
                rel = src.relative_to(skill_dir)
                dst = target / rel
                if src.is_dir():
                    dst.mkdir(parents=True, exist_ok=True)
                    continue
                project_rel = str(dst.relative_to(root)).replace(os.sep, "/")
                if dst.exists() and project_rel not in managed and not args.force:
                    raise RuntimeError(f"refusing to overwrite unmanaged file: {project_rel} (use --force)")
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.name == "SKILL.md":
                    dst.write_text(skill_frontmatter(skill_dir.name, src.read_text(encoding="utf-8")), encoding="utf-8")
                else:
                    shutil.copy2(src, dst)
                managed.add(project_rel)

    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps({
        "schema_version": 1,
        "package": "webgis-claude-skills",
        "version": VERSION,
        "scope": args.scope,
        "agents": [args.agent],
        "skill_locations": AGENTS[args.agent],
        "managed_files": sorted(managed),
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Installed WebGIS Claude Skills {VERSION} ({args.agent})")
    return 0


def verify(args: argparse.Namespace) -> int:
    root = Path.home() if args.scope == "global" else Path.cwd()
    marker = root / ".webgis-claude-skills" / "INSTALL.json"
    if not marker.exists():
        raise RuntimeError("installation marker not found")
    data = json.loads(marker.read_text(encoding="utf-8"))
    count = 0
    for location in data.get("skill_locations", []):
        base = root / location
        for skill in base.iterdir():
            manifest = skill / "SKILL.md"
            if manifest.is_file():
                text = manifest.read_text(encoding="utf-8")
                if not text.startswith("---\n") or "name:" not in text or "description:" not in text:
                    raise RuntimeError(f"invalid skill manifest: {manifest}")
                count += 1
    print(f"Verified WebGIS Claude Skills {data.get('version')} ({count} manifests)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="webgis-claude-skills")
    sub = parser.add_subparsers(dest="command")
    for command in ("install", "update"):
        p = sub.add_parser(command)
        p.add_argument("--agent", choices=AGENTS, default="all")
        p.add_argument("--scope", choices=("project", "global"), default="project")
        p.add_argument("--force", action="store_true")
    p = sub.add_parser("verify")
    p.add_argument("--scope", choices=("project", "global"), default="project")
    p = sub.add_parser("version")
    args = parser.parse_args()
    if args.command in ("install", "update"):
        if args.command == "update":
            args.force = True
        return install(args)
    if args.command == "verify":
        return verify(args)
    if args.command == "version":
        print(VERSION)
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
