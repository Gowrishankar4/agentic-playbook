#!/usr/bin/env python3
"""Repo checks: manifests, skill frontmatter, formatting, references, configs, audit fixtures."""
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "plugins/playbook/skills"
AUDIT = SKILLS / "playbook/scripts/audit.py"
errors = []
# Optional leak check: PLAYBOOK_PRIVATE_NAMES="acme|project-x" python3 scripts/validate.py
PRIVATE = "|".join(re.escape(n) for n in os.environ.get("PLAYBOOK_PRIVATE_NAMES", "").split("|") if n)


def err(msg):
    errors.append(msg)
    print("ERROR:", msg)


market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
for entry in market["plugins"]:
    manifest = json.loads((ROOT / entry["source"] / ".claude-plugin/plugin.json").read_text())
    if manifest["name"] != entry["name"]:
        err(f"marketplace entry '{entry['name']}' != plugin name '{manifest['name']}'")
    if not re.fullmatch(r"\d+\.\d+\.\d+", manifest.get("version", "")):
        err("plugin version must be semver")

for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
    rel = skill_md.relative_to(ROOT)
    text = skill_md.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(f"{rel}: missing frontmatter")
        continue
    fm = dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", m.group(1), re.M))
    if any(l[:1].isspace() for l in m.group(1).splitlines() if l):
        err(f"{rel}: indented frontmatter line")
    if set(fm) != {"name", "description"}:
        err(f"{rel}: frontmatter keys must be exactly name, description (got {sorted(fm)})")
    if fm.get("name") != skill_md.parent.name:
        err(f"{rel}: name != folder")
    if not 0 < len(fm.get("description", "")) <= 1024:
        err(f"{rel}: description length")
    if len(text.splitlines()) > 500:
        err(f"{rel}: over 500 lines")

for md in sorted((ROOT / "plugins").rglob("*.md")):
    rel = md.relative_to(ROOT)
    text = md.read_text()
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r"^ +(\|)", line) or re.match(r"^ {1,3}```", line):
            err(f"{rel}:{i}: table row or fence has leading spaces")
    for ref in [r for r in re.findall(r"`((?:\.\./)*(?:references|templates|config|presets|scripts)/[^`\s]+?\.(?:md|yml|json|py))`", text) if "<" not in r]:
        base = md.parent
        if not (base / ref).exists() and not (SKILLS / "playbook" / ref).exists():
            err(f"{rel}: referenced file missing: {ref}")
    if PRIVATE and re.search(PRIVATE, text, re.I):
        err(f"{rel}: contains a name from PLAYBOOK_PRIVATE_NAMES")

for y in list((SKILLS / "playbook/config").glob("*.yml")) + list((SKILLS / "playbook/presets").glob("*.yml")) + list((ROOT / "examples").rglob("*.yml")):
    r = subprocess.run([sys.executable, str(AUDIT), "--validate-config", str(y), "--no-file-checks"], capture_output=True, text=True)
    if r.returncode:
        err(f"config invalid: {y.relative_to(ROOT)}\n{r.stdout}{r.stderr}")

for clean_dir in ("examples/checkout-redesign-playbook", "tests/fixtures/clean-phrases-playbook"):
    clean = subprocess.run([sys.executable, str(AUDIT), str(ROOT / clean_dir), "--format", "json"], capture_output=True, text=True)
    if clean.returncode or json.loads(clean.stdout or "[]"):
        err(f"{clean_dir} should audit clean:\n" + clean.stdout)
broken = subprocess.run([sys.executable, str(AUDIT), str(ROOT / "tests/fixtures/broken-playbook"), "--format", "json"], capture_output=True, text=True)
found = {f["check"] for f in json.loads(broken.stdout or "[]")}
expected = {"requirement-without-task", "done-without-evidence", "id-mismatch", "sensitive-data", "stale-provisional", "stale-blocker", "relative-date", "no-todo-in-plan", "no-acceptance-criteria", "phase-mismatch", "stale-next-action", "agent-tracked-incomplete", "traceability-drift", "phase-not-started", "stale-current-phase"}
if missing := expected - found:
    err(f"broken fixture: audit missed {sorted(missing)}")
relative = [f for f in json.loads(broken.stdout or "[]") if f["check"] == "relative-date"]
if not any("today" in f["message"].lower() for f in relative):
    err("broken fixture: 'due today' should still be flagged as a relative date")

print("OK" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
