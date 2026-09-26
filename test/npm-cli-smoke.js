const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { execFileSync } = require("node:child_process");

const root = fs.mkdtempSync(path.join(os.tmpdir(), "webgis-claude-skills-"));
const bin = path.resolve(__dirname, "..", "bin", "webgis-claude-skills.js");

function run(...args) {
  return execFileSync(process.execPath, [bin, ...args], { cwd: root, encoding: "utf8" });
}

run("install", "--agent", "all", "--full");
run("verify");
const locations = [
  ".agents/skills",
  ".claude/skills",
  ".cursor/skills",
  ".opencode/skills"
];
for (const location of locations) {
  const files = fs.readdirSync(path.join(root, location));
  if (files.length < 10) throw new Error("expected multiple installed skills in " + location);
  const sample = path.join(root, location, files[0], "SKILL.md");
  const text = fs.readFileSync(sample, "utf8");
  if (!text.startsWith("---\n")) throw new Error("frontmatter missing in " + sample);
  if (!/^name:\s*[a-z0-9-]+$/m.test(text)) throw new Error("skill name missing in " + sample);
  if (!/^description:\s*.+$/m.test(text)) throw new Error("skill description missing in " + sample);
}
const marker = JSON.parse(fs.readFileSync(path.join(root, ".webgis-claude-skills", "INSTALL.json"), "utf8"));
if (marker.version !== require("../package.json").version) throw new Error("version marker mismatch");

const managedRuntimeDir = path.join(root, ".webgis-claude-skills", "venv");
const managedPython = path.join(managedRuntimeDir, "bin", "python");
fs.mkdirSync(path.dirname(managedPython), { recursive: true });
fs.writeFileSync(managedPython, "test-runtime", "utf8");

const managedMarkerPath = path.join(root, ".webgis-claude-skills", "INSTALL.json");
const managedMarker = {
  schema_version: 1,
  package: "webgis-claude-skills",
  version: require("../package.json").version,
  scope: "project",
  agents: ["all"],
  skill_locations: [],
  full_support_bundle: false,
  gis_runtime: { mode: "managed-venv", python: managedPython, packages: ["numpy>=1.26"] },
  managed_files: []
};
fs.writeFileSync(managedMarkerPath, JSON.stringify(managedMarker, null, 2) + "\n", "utf8");
run("uninstall");
if (fs.existsSync(managedRuntimeDir)) throw new Error("managed GIS venv was not removed by uninstall");
if (fs.existsSync(managedMarkerPath)) throw new Error("installation marker was not removed by uninstall");

const systemRoot = fs.mkdtempSync(path.join(os.tmpdir(), "webgis-claude-skills-system-"));
const systemRuntime = path.join(systemRoot, "system-python");
fs.mkdirSync(systemRuntime, { recursive: true });
const systemMarkerDir = path.join(systemRoot, ".webgis-claude-skills");
fs.mkdirSync(systemMarkerDir, { recursive: true });
const systemMarkerPath = path.join(systemMarkerDir, "INSTALL.json");
fs.writeFileSync(systemMarkerPath, JSON.stringify({
  schema_version: 1,
  package: "webgis-claude-skills",
  version: require("../package.json").version,
  scope: "project",
  agents: ["all"],
  skill_locations: [],
  full_support_bundle: false,
  gis_runtime: { mode: "system", python: path.join(systemRuntime, process.platform === "win32" ? "python.exe" : "python"), packages: ["numpy>=1.26"] },
  managed_files: []
}, null, 2) + "\n", "utf8");
execFileSync(process.execPath, [bin, "uninstall"], { cwd: systemRoot, encoding: "utf8" });
if (!fs.existsSync(systemRuntime)) throw new Error("system Python runtime directory was removed by uninstall");

console.log("npm CLI smoke test passed");
