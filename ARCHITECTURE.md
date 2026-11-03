# Architecture

How Agentic Playbook is put together, and why. Read this before changing the skill.

## The problem

AI agents forget between sessions, teammates work in different tools, and status lives in five places that drift apart. A playbook makes one folder the shared state for one piece of work, and makes keeping it consistent the agent's job, not the developer's.

## Layers

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. Core            SKILL.md — principles, lifecycle, commands,    │
│                    runtime, red flags, safety                     │
├──────────────────────────────────────────────────────────────────┤
│ 2. Model           references/model.md — entities, owning files,  │
│                    lifecycles, evidence, derived fields           │
│                    references/ripple-sweep.md — consistency algo  │
├──────────────────────────────────────────────────────────────────┤
│ 3. Procedures      references/commands/*.md, interview.md         │
│                    (read on demand, one per command)              │
├──────────────────────────────────────────────────────────────────┤
│ 4. Extension       config: capabilities · rules (triggers) ·      │
│                    custom modules · commands · red flags ·        │
│                    audit checks · presets · sensitive data        │
├──────────────────────────────────────────────────────────────────┤
│ 5. Adapters        references/adapters/agents.md, git.md          │
├──────────────────────────────────────────────────────────────────┤
│ 6. Tooling         scripts/audit.py (lint + config validation),   │
│                    templates/, presets/, config/schema.json       │
└──────────────────────────────────────────────────────────────────┘
```

Each layer depends only on the layers above it. The core never names a tool or agent, and tracks progress only from git; anything else (issue trackers, reviews, dashboards) plugs in as custom skills on events. Procedures are loaded only when their command runs, so the always-loaded part (`SKILL.md`) stays small.

## Data model

A playbook is a small database stored as markdown so that humans, any agent and git can all read it.

- **Single owner per fact.** Requirements live only in `00-REQUIREMENTS.md`, tasks in `02-PLAN.md`, task state and evidence in `PROGRESS.md`, decisions in `03-DECISIONS.md`. Everything else refers by ID.
- **Append-only history.** Interview records, decided rows, directives and log entries are never edited; corrections supersede.
- **Derived fields.** Current phase, next action, phase status and traceability status are computed from task rows on every sweep, so they cannot drift.
- **Explicit lifecycles.** Playbook, task and decision states with allowed transitions; the approval gate is the transition `DRAFT → APPROVED`.
- **Evidence ladder.** Git — commit, branch, pushed, PR — and tests when they exist; `agent-tracked` (what, files, tests) when the agent did the work and nothing else exists; `not stated` otherwise — never invented.

Full detail: `plugins/playbook/skills/playbook/references/model.md`.

## Flow

```
intent → setup (first run) → name + settings → scaffold → interview → 00-REQUIREMENTS
       → analysis → plan → APPROVAL GATE → work / log / decide / directive / task add
       → ripple sweep after every change → close
```

The interview is a capability: a team can plug in its own `/prompt`-style skill, but in a playbook its output is always saved to `00-REQUIREMENTS.md` and never executed directly.

## Consistency: the ripple sweep

1. Write the change in its owning file.
2. Search for every touched ID.
3. Update dependents (fixed map + custom modules' `reacts_to`).
4. Recompute derived fields.
5. Append one log entry; report.

`audit.py` checks the mechanical half of this (IDs, evidence, derived fields, stale blockers, sensitive data); the agent does the judgement half.

## Extension model

| Point | Lets a team | Cannot |
|---|---|---|
| `capabilities` | map any step to its own skill / command / MCP tool / script, with fallbacks and `when` | remove a step (unmapped = built-in) |
| `rules` | inject instructions or call a skill on `always`, commands, 16 events, or conditions — e.g. mirror progress to an issue tracker | loosen a safety rail |
| `custom_modules` | add files that join the ripple sweep | change core file ownership |
| `commands` | add sub-commands | bypass approval |
| `red_flags`, `audit_checks` | add judgement prompts and lint | — |
| `presets`, `include` | package and share all of the above | — |

Precedence: directives → `playbook.yml` → user config → preset → defaults. Lists merge by `id`.

## Design decisions

| # | Decision | Why | Alternative rejected |
|---|---|---|---|
| 1 | Markdown files, not a database or SaaS | Every agent and human can read and diff it; lives in git; zero install | JSON store (unreadable in review), hosted tracker (lock-in, no agent memory) |
| 2 | Playbook outside product repos | Programs span repos; no noise in product history; no write access needed | `.playbook/` per repo (fragmented across repos) |
| 3 | Capabilities, not tool names | Same skill works across agents and teams; tools change, steps don't | Hardcoded skills (broke on every machine but the author's) |
| 4 | Single owner per fact + derived fields | Turns "keep files in sync" into an algorithm; stale headers become impossible to miss | Free-form notes (drift within a week) |
| 5 | Git is the only built-in tracking source | Every developer already has it, with their own permissions; no connector, token or config. Issue trackers differ per team — they belong in custom skills on events | Built-in adapters per tracker (config sprawl, credentials, MCP vs CLI permission maze) |
| 6 | Approval gate before code | Requirements and plan are cheap to change; code isn't | Plan-as-you-go (rework) |
| 7 | `agent-tracked` evidence | Work done by an agent with no commit or ticket still needs a trail | Leave untracked (invisible work) or invent a ref (dishonest) |
| 8 | Safety rails not configurable | A shared skill must be safe by default for every team that installs it | Fully configurable (one bad config leaks data or pushes code) |

## Changing the skill

- New config key → `config/default.yml`, `config/schema.json`, `references/extensions.md`, together.
- New entity or file role → `references/model.md` first, then the ripple map, then templates.
- New command → `references/commands/<name>.md`, a row in `SKILL.md`, and the `on:` list in `extensions.md`.
- Keep `SKILL.md` under 500 lines; anything only one command needs goes in its procedure file.
- `python3 scripts/validate.py` must pass (it audits the example clean and the broken fixture for every check).
