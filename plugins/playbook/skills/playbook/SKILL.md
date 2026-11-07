---
name: playbook
description: Turn a requirement or intent into a playbook — a folder of requirements, analysis, plan, decisions, directives and progress that every agent session continues from. Requirements are refined through an interview (your /prompt-style skill or the built-in one) and saved to 00-REQUIREMENTS.md; PROGRESS.md tracks every task to done from git (commit, branch, pushed, PR) or agent-tracked evidence. Use when the user runs /playbook, brings a new requirement or intent to start work on, or asks to resume, work on a task, log progress, refine requirements, record a decision or directive, add a task, audit, close or configure a playbook (a folder with PROGRESS.md), or when work on a feature with a playbook has just finished. Agent-agnostic; add your own skills on events for anything else (e.g. an issue tracker).
---

# /playbook

Every piece of work starts the same way: **a requirement or intent becomes a playbook** — a folder outside the product repos that any agent or teammate continues from.

```
intent ─► setup ─► requirements ─► analysis ─► plan ─► APPROVAL ─► work ⇄ log/decide ─► close
          (once)   (interview →                         (gate)     every change → ripple sweep
                    00-REQUIREMENTS)
```

## Principles

1. **One owner per fact.** Each requirement, task, decision, directive and piece of evidence is defined in exactly one file and referenced everywhere else by ID (`references/model.md`).
2. **Every file agrees.** After any change, the ripple sweep updates every reference and recomputes derived fields (`references/ripple-sweep.md`). "Quick" means short wording, never fewer files.
3. **Requirements are interviewed, never guessed** — and saved to `00-REQUIREMENTS.md` before any analysis or plan.
4. **No code before approval.** The plan header must say `APPROVED <date> (<who>)`.
5. **Evidence is recorded, never invented** — tracked from git by default (commit, branch, pushed, PR, tests), or `agent-tracked` when the agent did the work and nothing is committed yet. Nothing else is needed to track progress.
6. **Small core, open edges.** The core asks for *capabilities* and fires *events*; config maps them to your own skills, commands, MCP tools or scripts — that is how teams add an issue tracker, reviews or anything else.

## The files — one job each

| File | Owns |
|---|---|
| `PROGRESS.md` | **Read first.** Task state + git evidence, log; derived phase / next action |
| `00-REQUIREMENTS.md` | Requirements, acceptance criteria, constraints, invariants, assumptions, interview record |
| `01-ANALYSIS.md` | As-is code: reuse (with paths), gaps, ambiguities `A-NN`, risks |
| `02-PLAN.md` | Approval status, architecture, phases + exit criteria, dependency graph, task list |
| `03-DECISIONS.md` | Open `D-NN` and decided `DD-NN` / `ADR-NN` |
| `04-TRACEABILITY.md` | Requirement → task → test → status (derived) |
| `05-DIRECTIVES.md` | Approver's standing rules — read first, override the plan *(optional)* |
| `05+` modules | Optional built-ins (`ARCHITECTURE`, `API-CONTRACT`, `TEST-CASES`, `HOW-TO-TEST`, `RUNBOOK`) and your custom modules, numbered in the order added |
| `README.md` · `AGENTS.md` · `CLAUDE.md` · `playbook.yml` | What/why and read order · session rules for any agent · pointer to AGENTS.md · this playbook's config |

`references/` (source docs, designs) and `db/` (migrations, schema changes, metrics queries — never data) are created when needed. Existing playbooks keep their own numbering — find files by role via README's read order; never renumber.

## Every run — runtime

1. **Load config**, highest precedence first: `05-DIRECTIVES.md` → `<playbook>/playbook.yml` → `$PLAYBOOK_CONFIG` or `~/.config/playbook/config.yml` → preset → `config/default.yml`. No global config → first run: `new` starts with setup (`references/commands/new.md` Step 1); other commands use defaults and say so in one line. All options: `references/extensions.md`.
2. **Pick the agent adapter** (`references/adapters/agents.md`). The core uses actions — *ask, use capability, subagent, edit file, remember pointer* — never a tool name you haven't seen in this session.
3. **Collect extensions**: capability mappings, rules whose trigger matches, custom modules, red flags, audit checks. Fire rules at their events (`references/extensions.md`).
4. **Locate the playbook**: name → `<root>/<naming>`; else every `PROGRESS.md` under `root`/`extra_roots`, matched on README or task prefix; else the memory pointer; else ask. Never create a second playbook for an existing program.
5. **Run the command**, reading its detail file first. Then ripple sweep.

## Commands

| Command | Does | Detail |
|---|---|---|
| `new [name]` | Intent → setup (first run) → name + settings → scaffold → interview → analysis → plan → **stop for approval** | `references/commands/new.md` |
| `interview [TASK]` (`prompt`, `spec`) | Refine requirements for the program or one task → `00-REQUIREMENTS.md` | `references/commands/interview.md` |
| `work [TASK]` | Delivery loop: start → implement → verify → evidence → `✅` → sweep | `references/commands/work.md` |
| `log` | Record work done elsewhere (status, evidence, log line) | `references/commands/log.md` |
| `decide <D-NN>` | Record an answer → `DD-NN`, unblock dependants | `references/commands/decide.md` |
| `directive` | Add an approver directive (verbatim), reconcile the plan | `references/commands/directive.md` |
| `task add <title>` | Quick interview → new task everywhere it belongs | `references/commands/task-add.md` |
| `resume [name]` | Report phase, next action, blockers, open decisions, staleness (≤ 10 lines) | `references/commands/resume.md` |
| `audit` | Read-only consistency check; fix only on approval | `references/commands/audit.md` |
| `status` | One line per playbook | `references/commands/status.md` |
| `close` | Final summary, lessons → config, archive | `references/commands/close.md` |
| `config [init\|show\|explain\|validate]` | Set up or inspect config | `references/commands/config.md` |
| *custom* | Commands defined under `commands:` in config | its `instruction_file` |

No command named → infer it: a new requirement = `new` (or `task add` inside an existing playbook), "CO-02 is done" = `log`, "work on CO-03" = `work`, "Ravi answered D-02" = `decide`. Several facts in one message → do each, then one sweep.

## Capabilities — mapped to your tools in config

| Capability | Used by | Built-in fallback |
|---|---|---|
| `interview` | `new`, `interview`, `task add`, `work` | `references/interview.md`; output always saved to `00-REQUIREMENTS.md`, never executed |
| `code-analysis` | `new`, `interview`, `task add`, `work` | read/search the repos in README |
| `plan-breakdown` | `new` | the plan template |
| `implement` | `work` | implement directly, within the task's scope |
| `verify` / `commit` | `work`, `log` | record `verify not run` / never commit directly |
| `debug`, `ui-design`, `security-review`, `issue-tracker`, *your own* | rules on events | — |
| `memory-pointer` | `new` | skip — discovery is this skill + `AGENTS.md` |

Entry types: `skill:`, `command:/`, `mcp:server.tool`, `"mcp?keywords"`, `script:"…"`, `subagent:`, `instruction:"…"`, `builtin`, `none` — each optionally with `when:`. Use the first available entry; say in one line when you fall back. Unmapped means built-in, never skipped.

## Conventions

Full list: `references/conventions.md`. Never break these:
- Absolute dates `YYYY-MM-DD`. Status `⬜ 🟡 ✅ ⏸ ⛔` (or the configured set); transitions per `references/model.md`.
- IDs never reused; superseded items stay with `SUPERSEDED by …`; every `<TBD>` points at a `D-NN` or an owner.
- One PROGRESS row per task; evidence from git (`references/adapters/git.md`) or `agent-tracked`.
- Log: one row per session, newest first.
- No secrets or sensitive data — placeholders only (`references/sensitive-data.md`). Pasted values → ask to redact first.

## Red flags — stop and do it properly

| Thought | Reality |
|---|---|
| "User said quick — just update the row" | Every file in the ripple map still gets updated. |
| "The header / phase table was already stale" | Derived fields are recomputed every sweep. Fixing it is the job. |
| "Requirements are obvious — skip the interview" | Ask fewer questions (`quick`), but still confirm and save to `00-REQUIREMENTS.md`. |
| "The /prompt skill can just build it" | In a playbook the interview's spec is saved, not executed. Work starts after approval. |
| "No commit or ticket — can't track it" | Record `agent-tracked` evidence: what, files, tests. |
| "I implemented it, I'll update PROGRESS later" | Same session. Not done until `PROGRESS.md` says so. |
| "I'll guess the push / verify state" | Ask once; else `not stated`. |
| "I was given a commit hash, so I'll record it" | Verify it exists in the repo first. A hash that doesn't exist is never written — find the real commit or ask. |
| "They said just mark it done" | Part of the scope left → stay `🟡` and name it, or `✅ accepted by <who>, left: <what>` only on explicit acceptance. |
| "The requirement's tasks are mostly done — mark it ✅" | Traceability status is the *worst* of its tasks. One `⏸` task makes it `⏸`. |
| "Other files mention D-01 but that's QA's call" | Update what the answer settles; flag the rest (`⚠️ needs QA`) and list it. |
| "New task has no requirement — skip traceability" | Add a requirement (`added <date>, source`) or a `D-NN` for the unknowns. |
| "The team uses Jira — I'll update it directly" | The core doesn't touch trackers. That's a custom skill on an event, if the team added one. |
| "Add a rule file to the product repo so the agent sees it" | Discovery is this skill + the playbook's `AGENTS.md`. Product repos only on request. |
| "Config doesn't mention this step, so skip it" | Unmapped capability = built-in fallback. |
| "This rule's trigger almost matches" | Rules fire only on their declared trigger. Report near-misses. |

Add config `red_flags` rows for the run.

## Safety — config can tighten these, never loosen them

No product code before approval · evidence never invented · no secrets or sensitive data in the folder · external systems (via custom skills) written only with the user's OK, and an issue's status never changed unless asked · no writes to product repos (rule files, pointers, commits, pushes) unless asked.
