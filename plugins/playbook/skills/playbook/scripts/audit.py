#!/usr/bin/env python3
"""Mechanical checks for a playbook folder (read-only), and config validation.

  audit.py <playbook-dir> [--config FILE ...] [--format md|json]
  audit.py --validate-config FILE

Exit code: 0 = no errors, 1 = errors found, 2 = usage problem.
Judgement checks (phase vs reality, wording) are left to the agent.
"""
import argparse
import fnmatch
import json
import pathlib
import re
import sys

SEVERITIES = ("error", "warn", "info")

SENSITIVE = {
    "secrets": [
        r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?token|auth[_-]?token)\s*[:=]\s*['\"]?[^\s'\"<>$]{6,}",
        r"\bAKIA[0-9A-Z]{16}\b",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"\b(gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9_-]{20,}|xox[abpr]-[A-Za-z0-9-]{10,})\b",
        r"[a-z]+://[^\s:/@<>]+:[^\s@<>]+@[^\s/]+",
    ],
    "pii": [
        r"\b[A-Za-z0-9._%+-]+@(?!example\.(com|org|net)\b)(?!placeholder\b)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        r"(?<![\w-])\+?\d[\d ()-]{9,}\d(?![\w-])",
        r"\b\d{3}-\d{2}-\d{4}\b",
    ],
    "phi": [
        r"(?i)\b(DOB|date of birth)\s*[:=]\s*\d",
        r"(?i)\bMRN\s*[:#=]?\s*\d{4,}",
        r"(?i)\b(member|insurance|policy)\s*(id|no|number)\s*[:#=]\s*[A-Z0-9]{5,}",
    ],
    "pci": [
        r"\b(?:\d[ -]?){13,19}\b",
        r"(?i)\bcvv\s*[:=]\s*\d{3,4}\b",
    ],
}
RELATIVE_DATES = re.compile(r"(?i)\b(yesterday|today|tomorrow|tonight|last week|next week|this week|next month|last month)\b")
DONE = ("✅", "[x]")
OPEN_STATES = ("⬜", "[ ]", "🟡", "[~]")


def load_structured(path):
    text = pathlib.Path(path).expanduser().read_text()
    if str(path).endswith(".json"):
        return json.loads(text)
    try:
        import yaml  # PyYAML
    except ImportError:
        raise SystemExit("PyYAML is needed to read YAML config: pip install pyyaml")
    try:
        return yaml.safe_load(text) or {}
    except yaml.YAMLError as e:
        raise SystemExit(f"YAML error in {path}: {e}\nTip: quote entries containing '?', '#' or ': ', e.g. \"mcp?jira comment\"")


def strip_code(lines):
    """Yield (lineno, line) outside fenced code blocks."""
    fence = False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            yield i, line


def tables(text):
    """Return list of (header_cells, rows[(lineno, cells)])."""
    out, cur = [], None
    lines = text.splitlines()
    for i, line in strip_code(lines):
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cur is None:
                cur = (cells, [])
            elif all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            else:
                cur[1].append((i, cells))
        else:
            if cur:
                out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return out


def col(header, *names):
    for n in names:
        for idx, h in enumerate(header):
            if h.lower().startswith(n.lower()):
                return idx
    return None


class Audit:
    def __init__(self, root, config):
        self.root = pathlib.Path(root)
        self.cfg = config or {}
        self.findings = []
        self.files = {p: p.read_text(errors="replace") for p in sorted(self.root.rglob("*.md")) if ".git" not in p.parts}

    def add(self, sev, check, path, line, msg):
        rel = path.relative_to(self.root) if path else "-"
        self.findings.append({"severity": sev, "check": check, "file": str(rel), "line": line, "message": msg})

    def find(self, pattern):
        return [p for p in self.files if fnmatch.fnmatch(p.name, pattern)]

    def run(self):
        progress = self.find("PROGRESS.md")
        if not progress:
            self.add("error", "structure", None, 0, "No PROGRESS.md — not a playbook folder")
            return self
        self.progress = progress[0]
        self.check_relative_dates()
        task_ids = self.check_tasks()
        plan_ids = self.plan_ids()
        self.compare_ids(task_ids, plan_ids)
        self.check_derived()
        decided = self.decided_ids()
        self.check_stale_blockers(decided)
        self.check_traceability()
        self.check_acceptance()
        self.check_sensitive()
        self.check_custom()
        return self

    def check_relative_dates(self):
        for p, text in self.files.items():
            if p.parent.name == "references":
                continue
            for i, line in strip_code(text.splitlines()):
                m = RELATIVE_DATES.search(line)
                if m and "`" + m.group(0) not in line:
                    self.add("warn", "relative-date", p, i, f'Relative date "{m.group(0)}" — use YYYY-MM-DD')

    def check_tasks(self):
        ids = {}
        self.states = {}
        for header, rows in tables(self.files[self.progress]):
            t, s, e = col(header, "task"), col(header, "status"), col(header, "evidence")
            if t is None or s is None:
                continue
            for ln, cells in rows:
                if len(cells) <= max(x for x in (t, s, e) if x is not None):
                    continue
                tid = cells[t].strip("`* ")
                if not tid:
                    continue
                ids[tid] = ln
                status = cells[s]
                self.states[tid] = status
                if e is not None and "agent-tracked" in cells[e] and not ("files" in cells[e] and "tests" in cells[e]):
                    self.add("warn", "agent-tracked-incomplete", self.progress, ln, f"{tid} agent-tracked evidence needs what, files and tests")
                if any(d in status for d in DONE) and e is not None and cells[e].strip() in ("", "—", "-", "None"):
                    self.add("error", "done-without-evidence", self.progress, ln, f"{tid} is done but has no evidence")
        return ids

    def plan_ids(self):
        ids = {}
        for p in self.find("*PLAN*.md"):
            for header, rows in tables(self.files[p]):
                i, title = col(header, "id"), col(header, "title")
                if i is None or title is None:
                    continue
                for ln, cells in rows:
                    if len(cells) > i and cells[i].strip("`* "):
                        ids[cells[i].strip("`* ")] = (p, ln)
        return ids

    def check_derived(self):
        """Phase table and next action must agree with task rows (model.md → Derived fields)."""
        done = lambda st: any(d in st for d in DONE)
        phases = {}
        for p in self.find("*PLAN*.md"):
            for header, rows in tables(self.files[p]):
                ph, tk = col(header, "phase"), col(header, "tasks")
                if ph is None or tk is None:
                    continue
                for _, cells in rows:
                    if len(cells) > tk:
                        phases[cells[ph].split()[0].strip("*")] = re.findall(r"\b[A-Z]{2,4}-\d+(?:\.\d+)?\b", cells[tk])
        text = self.files[self.progress]
        for header, rows in tables(text):
            ph, st = col(header, "phase"), col(header, "status")
            if ph is None or st is None or col(header, "task") is not None:
                continue
            for ln, cells in rows:
                if len(cells) <= st:
                    continue
                tasks = phases.get(cells[ph].split()[0].strip("*")) if cells[ph] else None
                known = [t for t in (tasks or []) if t in self.states]
                if not known:
                    continue
                all_done = all(done(self.states[t]) for t in known)
                if done(cells[st]) and not all_done:
                    left = ", ".join(t for t in known if not done(self.states[t]))
                    self.add("error", "phase-mismatch", self.progress, ln, f"Phase {cells[ph]} marked done but {left} not done")
                elif all_done and not done(cells[st]):
                    self.add("warn", "phase-mismatch", self.progress, ln, f"All tasks of phase {cells[ph]} are done but the phase isn't")
        for i, line in enumerate(text.splitlines(), 1):
            if line.startswith("**Next action:**"):
                for t in re.findall(r"\b[A-Z]{2,4}-\d+(?:\.\d+)?\b", line):
                    if t in self.states and done(self.states[t]):
                        self.add("warn", "stale-next-action", self.progress, i, f"Next action names {t}, which is already done")

    def compare_ids(self, task_ids, plan_ids):
        if not task_ids and not plan_ids:
            return
        for tid, ln in task_ids.items():
            if tid not in plan_ids:
                self.add("error", "id-mismatch", self.progress, ln, f"{tid} is in PROGRESS but not in the plan")
        for tid, (p, ln) in plan_ids.items():
            if tid not in task_ids:
                self.add("error", "id-mismatch", p, ln, f"{tid} is in the plan but not in PROGRESS")

    def decided_ids(self):
        decided = set()
        for p in self.find("*DECISIONS*.md"):
            for header, rows in tables(self.files[p]):
                i, s = col(header, "id"), col(header, "status")
                if i is None:
                    continue
                for ln, cells in rows:
                    if len(cells) <= i:
                        continue
                    did = cells[i].strip("`* ")
                    status = cells[s] if s is not None and len(cells) > s else ""
                    if re.fullmatch(r"D-\d+", did) and ("✅" in status or "[x]" in status or "SUPERSEDED" in status.upper()):
                        decided.add(did)
            for m in re.finditer(r"\b(D-\d+)\b[^|\n]*→\s*(DD|ADR)-\d+", self.files[p]):
                decided.add(m.group(1))
        return decided

    def check_stale_blockers(self, decided):
        if not decided:
            return
        for p, text in self.files.items():
            for i, line in strip_code(text.splitlines()):
                for did in decided:
                    if re.search(rf"(?i)provisional\s*\(\s*{did}\s*\)", line):
                        self.add("warn", "stale-provisional", p, i, f'"provisional ({did})" but {did} is decided')
            for header, rows in tables(text):
                b = col(header, "blocked by", "blocks")
                if b is None or header[b].lower() == "blocks":
                    continue
                for ln, cells in rows:
                    if len(cells) > b:
                        for did in decided:
                            if re.search(rf"\b{did}\b", cells[b]):
                                self.add("warn", "stale-blocker", p, ln, f"Blocked by {did}, which is decided")

    def check_traceability(self):
        for p in self.find("*TRACEABILITY*.md"):
            for header, rows in tables(self.files[p]):
                r, t = col(header, "req"), col(header, "task")
                if r is None or t is None:
                    continue
                for ln, cells in rows:
                    if len(cells) > t and cells[r].strip() and cells[t].strip() in ("", "—", "-"):
                        self.add("error", "requirement-without-task", p, ln, f"{cells[r]} has no task")

    def check_acceptance(self):
        for p in self.find("*REQUIREMENTS*.md"):
            for header, rows in tables(self.files[p]):
                i, a = col(header, "id"), col(header, "acceptance")
                if i is None or a is None:
                    continue
                for ln, cells in rows:
                    if len(cells) > a and cells[i].strip() and cells[a].strip() in ("", "—", "-"):
                        self.add("warn", "no-acceptance-criteria", p, ln, f"{cells[i]} has no acceptance criteria — run /playbook interview")

    def profiles(self):
        enabled = self.cfg.get("sensitive_data") or ["secrets", "pii"]
        out = {}
        for item in enabled:
            if isinstance(item, str) and item in SENSITIVE:
                out[item] = SENSITIVE[item]
            elif isinstance(item, dict):
                out[item["id"]] = item.get("patterns", [])
        out.setdefault("secrets", SENSITIVE["secrets"])
        return out

    @staticmethod
    def hit(prof, rx, line):
        for m in rx.finditer(line):
            if prof != "pci" or "cvv" in rx.pattern:
                return True
            digits = [int(c) for c in m.group(0) if c.isdigit()]
            total = sum(d if i % 2 == 0 else (d * 2 - 9 if d * 2 > 9 else d * 2) for i, d in enumerate(reversed(digits)))
            if total % 10 == 0:
                return True
        return False

    def check_sensitive(self):
        compiled = {k: [re.compile(x) for x in v] for k, v in self.profiles().items()}
        for p, text in self.files.items():
            for i, line in enumerate(text.splitlines(), 1):
                for prof, pats in compiled.items():
                    if any(self.hit(prof, rx, line) for rx in pats):
                        self.add("error", "sensitive-data", p, i, f"possible {prof} value (not shown)")
                        break

    def check_custom(self):
        for chk in self.cfg.get("audit_checks", []) or []:
            if chk.get("enabled") is False or "pattern" not in chk:
                continue
            rx = re.compile(chk["pattern"])
            globs = chk.get("files") or ["*.md"]
            for p, text in self.files.items():
                if not any(fnmatch.fnmatch(p.name, g) for g in globs):
                    continue
                for i, line in enumerate(text.splitlines(), 1):
                    if rx.search(line):
                        self.add(chk.get("severity", "warn"), chk["id"], p, i, chk.get("message", chk["id"]))
        n = sum(1 for c in self.cfg.get("audit_checks", []) or [] if "instruction" in c and c.get("enabled") is not False)
        if n:
            self.add("info", "agent-checks", None, 0, f"{n} instruction check(s) in config — the agent must run these")

    def report(self, fmt):
        order = {s: i for i, s in enumerate(SEVERITIES)}
        self.findings.sort(key=lambda f: (order[f["severity"]], f["file"], f["line"]))
        if fmt == "json":
            return json.dumps(self.findings, indent=2, ensure_ascii=False)
        if not self.findings:
            return "✅ No mechanical problems found."
        out = []
        for sev in SEVERITIES:
            group = [f for f in self.findings if f["severity"] == sev]
            if group:
                out.append(f"## {sev} ({len(group)})")
                out += [f"- `{f['file']}:{f['line']}` [{f['check']}] {f['message']}" for f in group]
        return "\n".join(out)


def merge(base, over):
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            merge(base[k], v)
        elif isinstance(v, list) and isinstance(base.get(k), list) and k in ("rules", "custom_modules", "red_flags", "audit_checks", "sensitive_data", "include"):
            ids = {x.get("id"): n for n, x in enumerate(base[k]) if isinstance(x, dict) and x.get("id")}
            for item in v:
                if isinstance(item, dict) and item.get("id") in ids:
                    base[k][ids[item["id"]]] = item
                elif item not in base[k]:
                    base[k].append(item)
        else:
            base[k] = v
    return base


def validate_config(path, file_checks=True):
    cfg = load_structured(path)
    problems = []
    schema_path = pathlib.Path(__file__).resolve().parent.parent / "config" / "schema.json"
    try:
        import jsonschema
        schema = json.loads(schema_path.read_text())
        for e in jsonschema.Draft202012Validator(schema).iter_errors(cfg):
            problems.append(f"schema: {'/'.join(map(str, e.path)) or '(root)'}: {e.message}")
    except ImportError:
        problems.append("info: jsonschema not installed — structural checks only (pip install jsonschema)")
    seen = set()
    for r in cfg.get("rules", []) or []:
        rid = r.get("id")
        if rid in seen:
            problems.append(f"rules: duplicate id '{rid}'")
        seen.add(rid)
        if r.get("enabled") is not False and not any(k in r for k in ("trigger", "on", "on_event", "when")):
            problems.append(f"rules.{rid}: no trigger (trigger/on/on_event/when)")
        actions = [k for k in ("instruction_file", "use", "ask") if k in r]
        if "instruction" in r and "use" not in r:
            actions.append("instruction")
        if r.get("enabled") is not False and len(actions) != 1:
            problems.append(f"rules.{rid}: needs exactly one of use / ask / instruction / instruction_file (use may add an instruction)")
    for m in cfg.get("custom_modules", []) or []:
        t = m.get("template")
        if file_checks and t and not pathlib.Path(t).expanduser().exists():
            problems.append(f"custom_modules.{m.get('id')}: template not found: {t}")
    for name, c in (cfg.get("commands") or {}).items():
        f = c.get("instruction_file")
        if file_checks and f and not pathlib.Path(f).expanduser().exists():
            problems.append(f"commands.{name}: instruction_file not found: {f}")
    if cfg.get("git", {}).get("push") == "always":
        problems.append("safety: git.push 'always' is not allowed — treated as 'ask'")
    if isinstance(cfg.get("sensitive_data"), list) and "secrets" not in cfg["sensitive_data"]:
        problems.append("info: 'secrets' profile is always on even though it isn't listed")
    errors = [p for p in problems if not p.startswith("info:")]
    print("\n".join(problems) if problems else "✅ Config valid.")
    return 1 if errors else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("playbook", nargs="?")
    ap.add_argument("--config", action="append", default=[], help="config file(s), lowest precedence first")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--validate-config", metavar="FILE")
    ap.add_argument("--no-file-checks", action="store_true", help="with --validate-config: skip checking that referenced files exist")
    a = ap.parse_args()
    if a.validate_config:
        sys.exit(validate_config(a.validate_config, not a.no_file_checks))
    if not a.playbook:
        ap.print_usage()
        sys.exit(2)
    cfg = {}
    files = list(a.config)
    local = pathlib.Path(a.playbook) / "playbook.yml"
    if local.exists():
        files.append(str(local))
    for f in files:
        cfg = merge(cfg, load_structured(f))
    au = Audit(a.playbook, cfg).run()
    print(au.report(a.format))
    sys.exit(1 if any(f["severity"] == "error" for f in au.findings) else 0)


if __name__ == "__main__":
    main()
