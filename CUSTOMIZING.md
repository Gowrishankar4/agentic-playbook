# Customizing Agentic Playbook

All customization is YAML. Nothing requires editing the skill itself.

| File | Scope |
|---|---|
| `~/.config/playbook/config.yml` (or `$PLAYBOOK_CONFIG`) | You, or your team via `include:` |
| `<playbook>/playbook.yml` | One playbook |
| `05-DIRECTIVES.md` | Approver's standing rules — beat everything |

Start from the annotated [`config.example.yml`](plugins/playbook/skills/playbook/config/config.example.yml). Every key and its default: [`default.yml`](plugins/playbook/skills/playbook/config/default.yml). Full reference: [`extensions.md`](plugins/playbook/skills/playbook/references/extensions.md).

Check a config any time:

```bash
python3 tools/audit.py --validate-config ~/.config/playbook/config.yml
```
or `/playbook config validate` · `/playbook config explain <key>` shows which file set a value.

## 1. Use your own skills and tools — `capabilities`

The playbook never names a tool. Each step asks for a capability; you map it to a fallback chain.

```yaml
capabilities:
  interview: [skill:prompt, builtin]                    # your own interview skill; output still saved to 00-REQUIREMENTS.md
  code-analysis:
    - { use: skill:code-graph, when: { repos: [api] } }   # code-graph only for api
    - subagent:explore
    - builtin
  verify: [command:/verify, script:"npm test && npm run lint"]
  commit: [command:/commit]
  issue-tracker: ["mcp?jira comment"]                   # discover an MCP tool for your own capability
  a11y-check: [script:"npx pa11y-ci"]                   # invent your own capability
```

Entry types: `skill:`, `command:/`, `mcp:server.tool`, `"mcp?keywords"`, `script:"…"`, `subagent:`, `instruction:"…"`, `builtin`, `none`.

## 2. Custom instructions with triggers — `rules`

```yaml
rules:
  - id: tone                          # fires every run
    trigger: always
    mode: advisory
    instruction: Plain English in log entries.

  - id: a11y-on-ui-tasks              # fires on an event, under a condition
    on_event: [task_done]
    when: { task_types: [ui] }
    mode: required
    use: a11y-check

  - id: migration-guard               # asks the user something
    on_event: [before_commit]
    when: { paths: ["**/migrations/**"] }
    mode: required
    ask: Has this migration run against a staging copy?

  - id: changelog-on-log              # fires on a command
    on: [log]
    instruction_file: ~/team/playbook/changelog-rule.md
```

**Triggers:** `trigger: always`, `on: [commands]`, `on_event: [events]`, `when: {conditions}` — combine freely.
**Events:** `before_scaffold`, `after_scaffold`, `after_interview`, `after_analysis`, `before_approval`, `after_approval`, `task_started`, `task_done`, `task_added`, `decision_recorded`, `directive_added`, `before_commit`, `before_sweep`, `after_sweep`, `audit`, `close`.
**Conditions:** `repos`, `paths`, `labels`, `task_types`, `presets`, `phases`, `request_matches`, `files_exist`, `not`.
**Actions:** exactly one of `use` (optionally with an `instruction` for it), `ask`, `instruction`, `instruction_file`.
**Mode:** `required` stops and reports if it can't run; `advisory` notes and continues.

## Tracking and issue trackers

Progress is tracked from **git** out of the box — commit, branch, pushed state, PR, tests — or `agent-tracked` when nothing is committed. Nothing to configure.

To mirror it into Jira, Linear, GitHub Issues or anything else, map your own skill to a capability and call it from rules on events:

```yaml
capabilities:
  issue-create:  [skill:jira-create]
  issue-tracker: [skill:jira-comment]
rules:
  - { id: jira-create,  on_event: [task_added],  use: issue-create,  instruction: "Ask first; append the key to Evidence." }
  - { id: jira-comment, on_event: [task_done],   use: issue-tracker, instruction: "Solution report; never change status." }
```

## 3. Your own playbook files — `custom_modules`

```yaml
custom_modules:
  - id: security-review
    file: SECURITY-REVIEW.md
    template: ~/team/playbook/security-review.md
    add_on: ask                       # offered during `new`
    reacts_to:
      task_done: Add a row for the task with reviewed / not reviewed.
```
`reacts_to` plugs the file into the ripple sweep, so it is never left stale.

## 4. Your own commands — `commands`

```yaml
commands:
  release-notes:
    description: Draft release notes from ✅ tasks since the last tag
    instruction_file: ~/team/playbook/release-notes.md
    writes: [RELEASE-NOTES.md]
```
Run `/playbook release-notes`.

## 5. Interview behaviour — `interview`

```yaml
interview:
  depth: deep                         # quick | standard | deep
  spec_format: markdown               # xml | markdown
  one_question_at_a_time: false
  extra_questions:
    - question: Which feature flag gates this?
      when: { repos: [web] }
```

## 6. Red flags, lint checks, data rules

```yaml
red_flags:
  - thought: "Staging is close enough to prod"
    reality: "Name the prod difference or test in prod-like."
audit_checks:
  - { id: no-todo, severity: warn, files: ["*PLAN*.md"], pattern: "\\bTODO\\b", message: "TODO in plan" }
  - { id: owners, severity: error, instruction: "Every phase names an owner." }
sensitive_data:
  - secrets
  - pii
  - { id: customer-ids, patterns: ["\\bCUST-\\d{6,}\\b"], placeholder: "<CUSTOMER_ID>" }
```

## 7. Presets

`preset: feature | program | regulated | ./path/to/your-preset.yml`. A preset is just a config file; ship one per team or product line.

## 8. Team config

Keep `team.yml` in a shared repo and have everyone `include:` it. Personal config adds tool mappings; team config adds rules, red flags and modules. Lists merge by `id`; `enabled: false` turns off an inherited entry.

## Examples

- [`examples/configs/solo.yml`](examples/configs/solo.yml) — one developer, git tracking, minimal
- [`examples/configs/team-jira.yml`](examples/configs/team-jira.yml) — team mirroring progress to Jira via custom skills on events, plus shared rules and a security module
