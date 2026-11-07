# Conventions (all playbooks)

Config can change the *style* of these (status markers, ID prefixes, evidence fields) but not the *rules*.

## Dates
Absolute `YYYY-MM-DD` only. Convert "yesterday" / "today" / "next Friday" using the current date. A past date described as future ("tomorrow", a fix version that has shipped) is an audit finding.

## Status
Default set (config `status.style: emoji`):

| Marker | Meaning |
|---|---|
| `⬜` | not started |
| `🟡` | in progress / partial — say what's left |
| `✅` | done — needs evidence |
| `⏸` | waiting on a decision — name the D-NN |
| `⛔` | blocked — say by what |

Allowed transitions between states: `model.md` → Lifecycles.

**A status cell holds the marker (and a date), nothing else.** Qualifiers go after a `·` as a `⚠️` note, never in place of the marker. The one combined form is the model's `✅ code · ⚠️ D-NN open: <impact>` on a **task** row. A traceability `Status` is the *worst* marker among its tasks (`⏸` if any task waits on a decision) — never `✅` while a task is not `✅`.

**"Blocked by" holds only task IDs, `D-NN`s or a named external blocker.** Plan approval is not a blocker: before approval, task rows stay `⬜` with `—`, and the PROGRESS `Stage` line says `DRAFT — awaiting approval`. `status.style: ascii` uses `[ ]`, `[~]`, `[x]`, `[?]`, `[!]`. A team may define its own set under `status.markers`; the five meanings stay.

## Evidence
Kinds, the `agent-tracked` fallback and what a `✅` needs: `model.md` → Evidence. Config `evidence.required` lists what a `✅` must have (default: commit or PR, plus verify result); `evidence.fallback` (default `agent-tracked`) applies when the agent did the work and none of that exists.

Unknown → ask once (one question listing every gap). If the user won't say → `push state not stated` / `verify not stated`. Never invent.

## IDs

| Kind | Default form | Config key |
|---|---|---|
| Requirements | group letter + number (`E1`, `T3`) or `FR-NN` or PRD section | `ids.requirement` |
| Tasks | `<PREFIX>-NN` (2–3 letter feature abbreviation, `WS-07`) or phase style (`BE-2.3`) | `ids.task_prefix`, `ids.task_style` |
| Open decisions | `D-NN` | `ids.decision` |
| Decided | `DD-NN` or `ADR-NN` | `ids.decided` |
| Ambiguities | `A-NN` | `ids.ambiguity` |
| Findings | `F-NN` | `ids.finding` |
| Directives | `DIR-NN` | `ids.directive` |

Task prefix never equals a requirement prefix. Never reuse an ID; superseded items stay with `SUPERSEDED by …`.

## Unknowns
`<TBD: what is missing → D-NN>` — every TBD points at an open decision (or `→ ask <owner>`). Never a bare placeholder, never a guessed value.

## Ambiguous answers
("X plus Y" = AND or OR?) Record your reading in the Decided row, add `⚠️ confirm reading with <who>`, and list it in your report.

An instruction about *this session's work* ("don't touch the other files", "skip that for now") is recorded as what happened — `deferred by <who> <date>: <what>` — never upgraded into a standing decision ("left unfrozen at the requester's instruction"). If it might be meant as standing, ask once.

## Log
A table in `PROGRESS.md`, newest first, one row per **sitting** — a conversation or work session, however many commands it ran. A later message in the same conversation extends that row (add a bold lead) rather than adding a new one; a new conversation, or a new day, starts a new row. Format (several facts → one row, bold lead per fact):
`| YYYY-MM-DD | **What (hash, repo, pushed?):** detail. verify result. ⚠️ follow-ups |`

## Task rows
One row per task ID in `PROGRESS.md`. Evidence comes from git (`adapters/git.md`) or is `agent-tracked`. Keys or links added by custom skills (e.g. an issue key) are appended to the Evidence cell.

## Sensitive data
No real values from any enabled profile (`references/sensitive-data.md`) anywhere in the folder — placeholders and env-var names only. If the user pastes any, stop and ask to redact before writing.

## External systems
The core never writes to issue trackers or other external systems. Custom skills on events may — always with the user's OK, and never changing an issue's status, assignee or release unless asked for that exact change.

## Requirement defaults
Timings, limits, rollout targets and similar defaults belong in server/app config, not code constants — note the config key in the `Default` column of `00-REQUIREMENTS.md`.
