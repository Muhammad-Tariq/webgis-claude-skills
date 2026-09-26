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
console.log("npm CLI smoke test passed");
