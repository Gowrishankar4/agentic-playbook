# Domain model

A playbook is a small database kept in markdown. Each kind of fact has **one owning file** — the only place it is defined. Every other file refers to it by ID. Change a fact in its owner first, then update the references (the ripple sweep). This is what keeps every file agreeing.

## Entities

| Entity | ID | Owner (defined only here) | Referenced from |
|---|---|---|---|
| Requirement | `C1`, `FR-01`, … | `00-REQUIREMENTS.md` | traceability, plan tasks, analysis, decisions |
| Acceptance criterion | column of its requirement | `00-REQUIREMENTS.md` | traceability `Test`, evidence for `✅` |
| Constraint / invariant | `I1` | `00-REQUIREMENTS.md` | plan exit criteria, analysis risks |
| Interview record | dated heading | `00-REQUIREMENTS.md` (append-only) | — |
| Ambiguity | `A-NN` | `01-ANALYSIS.md` | decisions |
| Task | `<PREFIX>-NN` | `02-PLAN.md` (task list: title, repo, type) | PROGRESS task row, traceability, other tasks' "Blocked by" |
| Phase | name | `02-PLAN.md` (tasks, exit criteria) | PROGRESS phase table (derived) |
| Open decision | `D-NN` | `03-DECISIONS.md` Open | "Blocked by", `<TBD → D-NN>`, "provisional (D-NN)" |
| Decided | `DD-NN` / `ADR-NN` | `03-DECISIONS.md` Decided (append-only) | open row `→ DD-NN`, requirements, plan |
| Directive | `DIR-NN` | `05-DIRECTIVES.md` (append-only) | plan rules, decisions |
| Task state + evidence | — | `PROGRESS.md` task row | traceability `Status` (derived) |
| Log entry | date | `PROGRESS.md` log (append-only, newest first) | — |
| External ref | e.g. an issue key added by a custom skill | `PROGRESS.md` task row (Evidence cell) | — |
| Custom module rows | module-defined | the module's file | as declared in `reacts_to` |

**Append-only** entities are never edited after the fact; a correction is a new entry that supersedes the old one.

## Derived fields — recompute, never hand-edit

| Field | Derived from |
|---|---|
| PROGRESS "Current phase" | first phase (plan order) whose tasks are not all `✅` |
| PROGRESS "Next action" | first task in that phase that is not `✅`/`⏸`/`⛔`, else the most blocking open decision |
| PROGRESS phase table status | `✅` all its tasks `✅` · `⏸`/`⛔` all remaining tasks waiting/blocked · `🟡` any started · `⬜` none started |
| Traceability `Status` | worst status among the requirement's tasks; `✅` only when every task is `✅` and its acceptance criteria have evidence |
| Plan header `Status` | `DRAFT` → `APPROVED <date> (<who>)` (set by approval only) → `CLOSED <date>` |

After any change, recompute all derived fields. A derived field that disagrees with its sources is a bug — fix it even if it was already wrong.

## Lifecycles

### Playbook

```
SETUP ─► REQUIREMENTS ─► ANALYSIS ─► DRAFT ─► APPROVED ─► IN DELIVERY ─► CLOSED
              ▲                         │
              └──── interview again ◄───┘  (scope change sends the plan back to DRAFT
                                            only if the approver says so)
```

No product code in any state before `APPROVED`.

### Task

| From → To | Allowed when | Records |
|---|---|---|
| `⬜` → `🟡` | plan `APPROVED`; no open `D-NN` or task in "Blocked by" | start date, branch if known |
| `🟡` → `✅` | evidence meets `evidence.required` (or the agent-tracked minimum) | evidence, date, acceptance criteria covered |
| any → `⏸` | an open decision blocks it | `⏸ D-NN` |
| any → `⛔` | something outside a decision blocks it | `⛔ <what>` |
| `⏸`/`⛔` → previous | the blocker is resolved | note in log |
| `✅` → `🟡` | reopened (bug, failed verify) | reason in log; evidence kept |
| any → `SUPERSEDED by <ID>` / `won't do` | scope change agreed | who, date |

`✅ code` + `⚠️ D-NN open: <impact>` is allowed when the code is done but one of the task's own decisions is still open.

### Decision

`⬜ open` → `🟡 partly answered` → `✅ → DD-NN` (or `SUPERSEDED by DD-NN`). An open row is never deleted — it is history.

## Evidence

Tracked from git by default (`adapters/git.md`). Whatever exists is recorded; nothing is invented. Config `evidence.required` sets what a `✅` needs (default: commit or PR, plus verify result); `evidence.fallback` (default `agent-tracked`) sets what happens when none of that exists.

| Kind | Form |
|---|---|
| Commit | `<repo> \`<short hash>\` (<branch>, pushed\|not pushed)` |
| PR / MR | link |
| Verify / tests | `verify PASS\|FAIL\|not run`, counts (`jest 12/12`) |
| External ref | whatever a custom skill on an event adds (issue key, comment link) |
| **Agent-tracked** | `agent-tracked YYYY-MM-DD: <what was implemented>; files: <paths>; tests: <command → result>` — used when the agent did the work and nothing is committed yet (or `evidence.fallback: agent-tracked`). Never used for work the agent did not do or see |
| Unknown | ask once; if the user won't say → `<field> not stated` |

A row with only `not stated` evidence stays `🟡` unless the user explicitly accepts it as done (`✅ accepted by <who>, evidence not stated`).
