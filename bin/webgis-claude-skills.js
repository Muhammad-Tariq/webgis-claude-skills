#!/usr/bin/env node

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const PACKAGE_ROOT = path.resolve(__dirname, "..");
const VERSION = require(path.join(PACKAGE_ROOT, "package.json")).version;
const SKILLS_SOURCE = path.join(PACKAGE_ROOT, "skills");
const SUPPORT_DIRS = ["profiles", "contracts", "decision-matrices", "templates", "learning", "integrations"];

const AGENTS = {
  agents: { label: "Agent Skills standard", paths: [".agents/skills"] },
  claude: { label: "Claude Code", paths: [".claude/skills"] },
  codex: { label: "Codex", paths: [".agents/skills"] },
  cursor: { label: "Cursor", paths: [".cursor/skills"] },
  opencode: { label: "OpenCode", paths: [".opencode/skills"] },
  all: {
    label: "all supported native/compatible skill locations",
    paths: [".agents/skills", ".claude/skills", ".cursor/skills", ".opencode/skills"]
  }
};

function fail(message) {
  console.error("\nError: " + message);
  process.exitCode = 1;
}

function parseArgs(argv) {
  const args = { command: argv[0] || "help", agent: "all", scope: "project", full: false, memory: false, force: false };
  for (let i = 1; i < argv.length; i++) {
    const token = argv[i];
    if (token === "--agent") args.agent = argv[++i];
    else if (token === "--scope") args.scope = argv[++i];
    else if (token === "--full") args.full = true;
    else if (token === "--memory") args.memory = true;
    else if (token === "--force") args.force = true;
    else if (token === "--help" || token === "-h") args.command = "help";
    else if (token === "--version" || token === "-v") args.command = "version";
  }
  return args;
}

function safeJoin(root, relative) {
  const resolved = path.resolve(root, relative);
  const base = path.resolve(root) + path.sep;
  if (resolved !== path.resolve(root) && !resolved.startsWith(base)) {
    throw new Error("unsafe path: " + relative);
  }
  return resolved;
}

function slug(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").replace(/--+/g, "-").slice(0, 64);
}

function skillWithFrontmatter(name, content) {
  if (/^---\s*\n/.test(content)) return content;
  const heading = content.match(/^#\s+(.+)$/m);
  const title = heading ? heading[1].trim() : name;
  const purpose = content.match(/##\s+Purpose\s*\n\s*([^\n]+)/i);
  const description = (purpose ? purpose[1] : title).replace(/\s+/g, " ").replace(/[\r\n]/g, " ").slice(0, 1000);
  const skillName = slug(name);
  return `---
name: ${skillName}
description: ${description}
license: Apache-2.0
compatibility: agent-skills
metadata:
  source: webgis-claude-skills
  version: ${VERSION}
---

${content.replace(/^\s+/, "")}`;
}

function copyTree(source, destination, options = {}) {
  if (!fs.existsSync(source)) throw new Error("source not found: " + source);
  fs.mkdirSync(destination, { recursive: true });
  for (const entry of fs.readdirSync(source, { withFileTypes: true })) {
    const src = path.join(source, entry.name);
    const dst = path.join(destination, entry.name);
    if (entry.isDirectory()) {
      copyTree(src, dst, options);
    } else if (entry.isFile()) {
      if (!options.force && fs.existsSync(dst) && !options.managed.has(path.relative(options.projectRoot, dst))) {
        throw new Error("refusing to overwrite existing unmanaged file: " + path.relative(options.projectRoot, dst) + " (use --force)");
      }
      fs.mkdirSync(path.dirname(dst), { recursive: true });
      if (options.transformSkill && entry.name === "SKILL.md") {
        const relativeSkill = path.relative(SKILLS_SOURCE, src);
        const skillDir = relativeSkill.split(path.sep)[0];
        fs.writeFileSync(dst, skillWithFrontmatter(skillDir, fs.readFileSync(src, "utf8")), "utf8");
      } else {
        fs.copyFileSync(src, dst);
      }
      options.managed.add(path.relative(options.projectRoot, dst));
    }
  }
}

function markerPath(projectRoot) {
  return path.join(projectRoot, ".webgis-claude-skills", "INSTALL.json");
}

function loadMarker(projectRoot) {
  const p = markerPath(projectRoot);
  if (!fs.existsSync(p)) return null;
  try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; }
}

function resolveRoot(scope) {
  if (scope === "global") return os.homedir();
  return process.cwd();
}

function detect(command) {
  const names = process.platform === "win32" ? ["where", command] : ["sh", "-lc", `command -v ${command}`];
  try {
    const { execFileSync } = require("node:child_process");
    return Boolean(execFileSync(names[0], names.slice(1), { stdio: "ignore" }));
  } catch {
    return false;
  }
}

function install(args) {
  const agent = AGENTS[args.agent];
  if (!agent) throw new Error("unknown agent: " + args.agent);
  const projectRoot = resolveRoot(args.scope);
  const managed = new Set(loadMarker(projectRoot)?.managed_files || []);

  if (!fs.existsSync(SKILLS_SOURCE)) throw new Error("npm package is missing its skills directory");
  const installedPaths = [];

  for (const relative of agent.paths) {
    const destination = safeJoin(projectRoot, relative);
    copyTree(SKILLS_SOURCE, destination, {
      force: args.force,
      managed,
      projectRoot,
      transformSkill: true
    });
    installedPaths.push(relative);
  }

  if (args.full) {
    const supportRoot = safeJoin(projectRoot, ".webgis-claude-skills");
    for (const dir of SUPPORT_DIRS) {
      copyTree(path.join(PACKAGE_ROOT, dir), safeJoin(supportRoot, dir), {
        force: args.force,
        managed,
        projectRoot,
        transformSkill: false
      });
    }
  }

  const marker = {
    schema_version: 1,
    package: "webgis-claude-skills",
    version: VERSION,
    scope: args.scope,
    agents: [args.agent],
    skill_locations: installedPaths,
    full_support_bundle: args.full,
    installed_at: new Date().toISOString(),
    managed_files: [...managed].sort()
  };
  fs.mkdirSync(path.dirname(markerPath(projectRoot)), { recursive: true });
  fs.writeFileSync(markerPath(projectRoot), JSON.stringify(marker, null, 2) + "\n", "utf8");

  console.log(`
WebGIS Claude Skills ${VERSION}
✓ Installed skills
✓ Agent compatibility: ${agent.label}
✓ Skill locations: ${installedPaths.join(", ")}
${args.full ? "✓ Full support bundle: profiles, contracts, decision matrices, templates, learning" : ""}
${args.memory ? "ℹ Project memory is not initialized by default; use the project-memory templates intentionally." : ""}
${args.scope === "global" ? "✓ Global installation" : "✓ Project-local installation"}
`);
}

function verify(args) {
  const projectRoot = resolveRoot(args.scope);
  const marker = loadMarker(projectRoot);
  if (!marker) throw new Error("installation marker not found; run install first");
  let count = 0;
  const locations = marker.skill_locations || [];
  for (const location of locations) {
    const root = safeJoin(projectRoot, location);
    if (!fs.existsSync(root)) throw new Error("missing skill location: " + location);
    for (const skill of fs.readdirSync(root, { withFileTypes: true })) {
      if (!skill.isDirectory()) continue;
      const file = path.join(root, skill.name, "SKILL.md");
      if (fs.existsSync(file)) {
        const content = fs.readFileSync(file, "utf8");
        if (!/^---\s*\n/.test(content)) throw new Error("missing SKILL.md frontmatter: " + file);
        if (!/^name:\s*[a-z0-9-]+\s*$/m.test(content)) throw new Error("missing/invalid skill name: " + file);
        if (!/^description:\s*.+$/m.test(content)) throw new Error("missing skill description: " + file);
        count++;
      }
    }
  }
  console.log(`✓ WebGIS Claude Skills ${marker.version} verified (${count} skill manifests)`);
}

function doctor(args) {
  const root = resolveRoot(args.scope);
  console.log("WebGIS Claude Skills doctor");
  console.log(`✓ Node.js ${process.versions.node}`);
  console.log(`✓ Project root: ${root}`);
  for (const [name, meta] of Object.entries({ claude: "claude", codex: "codex", cursor: "cursor", opencode: "opencode" })) {
    console.log(`${detect(meta) ? "✓" : "·"} ${name}: ${detect(meta) ? "detected" : "not detected"}`);
  }
  const marker = loadMarker(root);
  console.log(marker ? `✓ Installed version: ${marker.version}` : "· No installation marker found");
  console.log("ℹ The installer does not install or modify agent CLIs themselves.");
  console.log("ℹ Python/GDAL dependencies are separate from the skill distribution.");
}

function uninstall(args) {
  const projectRoot = resolveRoot(args.scope);
  const marker = loadMarker(projectRoot);
  if (!marker) throw new Error("no managed installation found");
  for (const relative of marker.managed_files || []) {
    const target = safeJoin(projectRoot, relative);
    if (fs.existsSync(target) && fs.statSync(target).isFile()) fs.rmSync(target);
  }
  const skillLocations = marker.skill_locations || [];
  for (const location of skillLocations) {
    const root = safeJoin(projectRoot, location);
    if (fs.existsSync(root) && fs.readdirSync(root).length === 0) fs.rmSync(root);
  }
  const m = markerPath(projectRoot);
  if (fs.existsSync(m)) fs.rmSync(m);
  console.log("✓ Managed WebGIS Claude Skills files removed");
}

function help() {
  console.log(`WebGIS Claude Skills ${VERSION}

Usage:
  npx webgis-claude-skills install [--agent all|agents|claude|codex|cursor|opencode]
  npx webgis-claude-skills update [--agent ...]
  npx webgis-claude-skills verify
  npx webgis-claude-skills doctor
  npx webgis-claude-skills uninstall
  npx webgis-claude-skills version

Options:
  --scope project|global   Install into the current project or user home
  --agent ...              Select a native/compatible skill location
  --full                   Also install repository support material under .webgis-claude-skills/
  --force                  Allow overwriting existing unmanaged files

Examples:
  npx webgis-claude-skills install --agent all
  npx webgis-claude-skills install --agent claude
  npx webgis-claude-skills install --agent codex
  npx webgis-claude-skills install --agent cursor
  npx webgis-claude-skills install --agent opencode
  npx webgis-claude-skills install --full
  npx webgis-claude-skills doctor
`);
}

try {
  const args = parseArgs(process.argv.slice(2));
  if (args.command === "version") console.log(VERSION);
  else if (args.command === "install" || args.command === "update") install({ ...args, force: args.command === "update" || args.force });
  else if (args.command === "verify") verify(args);
  else if (args.command === "doctor") doctor(args);
  else if (args.command === "uninstall") uninstall(args);
  else help();
} catch (error) {
  fail(error && error.message ? error.message : String(error));
}
