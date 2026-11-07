# Config and extensions

Everything a team or developer customizes lives in YAML. Full defaults: `../config/default.yml`. Annotated example: `../config/config.example.yml`. Machine-checkable schema: `../config/schema.json`.

## Where config lives (precedence, highest first)

| Level | File | Typical use |
|---|---|---|
| 1 | `05-DIRECTIVES.md` in the playbook | Approver's standing rules — read first, win over everything |
| 2 | `<playbook>/playbook.yml` | This program's repos, extra modules, rules |
| 3 | `$PLAYBOOK_CONFIG` or `~/.config/playbook/config.yml` | A developer's or team's defaults: root folder, tools, rules |
| 4 | preset (`preset: program`) | Bundled shapes: `feature`, `program`, `regulated`, or a custom preset path |
| 5 | `config/default.yml` | Built-in defaults |

Merge rules: maps merge key by key; lists (`rules`, `custom_modules`, `red_flags`, `audit_checks`) and the `commands` map **append**, with a later entry of the same `id` replacing an earlier one. Set `enabled: false` on an `id` to switch off an inherited entry. `/playbook config explain <key>` shows the winning value and which file set it.

`include:` (list of paths) pulls in shared fragments, so a team can keep one `team-rules.yml` in a repo and every developer includes it.

## Settings

```yaml
root: ~/playbooks                # where playbooks are created
extra_roots: []                  # also searched when locating
naming: "{name}-playbook"        # {name} = kebab-case program name
preset: feature
language: en                     # language playbook prose is written in
context_files: [AGENTS.md, CLAUDE.md]   # add GEMINI.md, .github/copilot-instructions.md …
status: { style: emoji }         # emoji | ascii | custom (then status.markers)
evidence: { required: [commit_or_pr, verify], fallback: agent-tracked }
ids: { task_prefix: auto, task_style: sequential, decision: D, decided: DD }
approval: { required: true, approvers: [] }
git: { init: ask, commit: ask, push: never }
memory: { pointer: ask }         # ask | always | never
sensitive_data: [secrets, pii]   # + phi, pci, or custom profiles
modules:
  optional_default: []          # built-ins added on every `new`
  offer: []                     # built-ins offered during the interview
```

## Adding an issue tracker or other system

The core tracks progress from git only. Connect anything else with a capability + rules on events — e.g. Jira: `adapters/git.md` → "Adding a tracker".

## `capabilities` — map steps to your tools

Each capability is an ordered fallback chain. The first entry that is available **and** whose `when` matches is used.

```yaml
capabilities:
  interview: [builtin]                 # or [skill:prompt, builtin] — output is still saved to 00-REQUIREMENTS.md
  code-analysis:
    - { use: skill:code-graph, when: { repos: [api, web] } }
    - subagent:explore
    - builtin
  verify:  [command:/verify, script:"make test lint"]
  commit:  [command:/commit]
  issue-tracker:   [skill:jira-comment, "mcp?jira comment"]   # your own capability, used by a rule
  security-review: [skill:security-review, instruction:"Run the OWASP checklist in docs/security.md"]
```

| Entry | Means |
|---|---|
| `skill:<name>` | Load and follow that skill |
| `command:/<name>` | Run that slash command |
| `mcp:<server>.<tool>` | Call that exact MCP tool |
| `"mcp?<keywords>"` | Discover an MCP tool by keywords (tool search / tool list). Quote it in YAML — `?` is special |
| `script:"<shell>"` | Run the command; its output is evidence |
| `subagent:<type>` | Spawn a fresh subagent of that type |
| `instruction:"<text>"` / `instruction_file: <path>` | Do what the text says |
| `builtin` | The behaviour described in this skill |
| `none` | Deliberately skip; record "skipped by config" |

Any capability name is allowed — define your own (`perf-test`, `a11y-check`) and call it from a rule.

## `rules` — custom instructions with triggers

```yaml
rules:
  - id: perf-budget
    description: API phases carry a performance budget
    on_event: [before_approval]
    when: { paths: ["src/api/**"] }
    mode: required
    instruction: Add p95 latency and payload size to every exit criterion touching src/api.
```

| Field | Values |
|---|---|
| `id` | unique; same id later in precedence replaces it |
| `trigger` | `always` (every run) — or omit and use the fields below |
| `on` | commands: `[new, interview, work, log, decide, task add, audit, close, <custom>]` |
| `on_event` | events (table below) |
| `when` | conditions, all must match (below) |
| `do` | exactly one of `use` (a capability or skill/command/MCP/script entry — may add an `instruction` telling it what to do), `ask` (question to put to the user), `instruction`, `instruction_file` |
| `mode` | `required` — must run; if it can't, stop and report. `advisory` — run if possible; else note and continue |
| `priority` | integer, lower runs first (default 100) |
| `enabled` | `false` to switch off an inherited rule |

### Events

| Event | Fires |
|---|---|
| `before_scaffold` / `after_scaffold` | around creating the folder in `new` |
| `after_interview` | interview approved and saved to `00-REQUIREMENTS.md` |
| `after_analysis` | code analysis written |
| `before_approval` | plan about to be shown for approval |
| `after_approval` | plan header set to APPROVED |
| `task_started` | a task moves to 🟡 (`work`, `log`) |
| `task_done` | a task moves to ✅ |
| `task_added` | new task ID created |
| `decision_recorded` | a D-NN answered or superseded |
| `directive_added` | a directive appended |
| `before_commit` | before recording or making a commit |
| `before_sweep` / `after_sweep` | around every ripple sweep |
| `audit` | during `audit` (add judgement checks here) |
| `close` | during `close` |

### Conditions (`when`)

| Key | Matches |
|---|---|
| `repos` | repo names from README's repos table touched by the task |
| `paths` | globs of files the task or diff touches |
| `labels` / `task_types` | task labels or type column |
| `presets` / `phases` | active preset, current phase name |
| `request_matches` | regex or keywords in the user's message |
| `files_exist` | playbook files (globs) that must exist, e.g. `"*-API-CONTRACT.md"` |
| `not` | nested condition that must **not** match |

A rule with no `trigger`, `on`, `on_event` or `when` is invalid — `config validate` reports it.

## `custom_modules` — your own playbook files

```yaml
custom_modules:
  - id: security-review
    file: SECURITY-REVIEW.md        # numbered automatically on add: 09-SECURITY-REVIEW.md
    title: Security review
    template: ~/team/playbook/security-review.md   # or inline `template_text:`
    add_on: [new]                   # or "ask" (offered during new), or manual via task add
    read_order: after PLAN          # where it appears in README's read order
    reacts_to:
      task_done: "Add a row for the task; mark reviewed/not-reviewed with evidence"
      decision_recorded: "Re-check rows that cited the decision"
```

`reacts_to` maps an event (or a "Changed" row name from the ripple map) to the update to make. The ripple sweep includes these automatically.

## `commands` — your own sub-commands

```yaml
commands:
  release-notes:
    description: Draft release notes from ✅ tasks since the last tag
    instruction_file: ~/team/playbook/release-notes.md
    writes: [RELEASE-NOTES.md]       # files it may change; ripple sweep runs after
    read_only: false
```

Run as `/playbook release-notes`. The instruction file is followed like a command detail file; safety rails still apply.

## `red_flags` and `audit_checks`

```yaml
red_flags:
  - thought: "It's an internal endpoint, skip the security review"
    reality: "Internal endpoints get the same review."

audit_checks:
  - id: no-todo-in-plan
    severity: warn                   # error | warn | info
    files: ["02-PLAN.md"]
    pattern: "\\bTODO\\b"
    message: Plan contains TODO — turn it into a task or D-NN
  - id: rollout-owner
    severity: error
    instruction: Every phase in 08-RUNBOOK.md must name an owner.
```

Pattern checks are applied by the agent during `audit` (or mechanically by the repository's `tools/audit.py`, when the user has it); instruction checks are always done by the agent.

## `presets`

A preset is a config file with the same keys. Bundled: `feature`, `program`, `regulated` (see `../presets/`). Your own: `preset: ~/team/playbook/presets/mobile.yml`.

## Safety rails (cannot be loosened)

Config may make these stricter, never weaker. Any setting that would loosen one is ignored and reported by `config validate`:
- No product code before the plan says APPROVED (`approval.required: false` only skips the *approver name*, never the stop-and-show step).
- Evidence is never invented.
- No values from enabled sensitive-data profiles in the folder; `secrets` is always enabled.
- External systems (written only by custom skills) are written with the user's OK; an issue's status, assignee or release is never changed unless asked.
- No writes to product repos (rule files, pointers, commits) unless the user asks.
