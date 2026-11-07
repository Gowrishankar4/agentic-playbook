# Changelog

## 1.1.0 — 2026-11-07

Fixes from an end-to-end test (headless Claude Code driving a sample feature from `new` to `close`, 7 tasks, 14 sessions).

**Audit (`scripts/audit.py`)**
- New `traceability-drift` (error): a requirement marked `✅` while one of its tasks isn't — traceability status is the worst of its tasks.
- New `stale-current-phase` (warn): plan approved but `Current phase` left empty.
- New `phase-not-started` (warn): a phase marked `🟡` with no task started, or `⬜` with tasks under way.
- Relative dates: "today" is flagged only when used as a date ("due today", "Today: …"); prose such as "behaves as today" no longer warns. Lines can opt out with `<!-- audit:ignore [check] -->`.
- PII phone-number pattern no longer matches a version followed by a date (`v1.0 2026-11-07`).
- Task IDs accept prefixes of 2–10 letters/digits (`CHKOUT-12`), matching the conventions.
- CI: broken fixture covers both new checks; new `clean-phrases-playbook` fixture must audit clean.

**Skill behaviour**
- `close` sets the plan header to `CLOSED <date>` as well as PROGRESS (was PROGRESS only, contradicting `model.md`).
- `log`: every given hash is verified before it is recorded, and a missing one is looked for on the task's branch since the last evidence before other branches; a partly done task stays `🟡` unless the user explicitly accepts it (`✅ accepted by <who>, left: <what>`).
- `work`: work that moves between tasks updates both plan rows in the same sweep.
- PROGRESS gets a `Stage` line for the lifecycle; the phase table holds delivery phases only. Plan approval is no longer written as a "Blocked by" value.
- Status cells hold the marker only (plus the model's `✅ code · ⚠️ D-NN` on task rows); qualifiers go in a `⚠️` note.
- Session instructions ("don't touch the other files") are logged as `deferred by <who>`, not turned into standing decisions.
- `one_question_at_a_time` now means one topic per message (≤ 4 related sub-questions with defaults) — matching how the interview works best in practice.
- Log: one row per sitting, not per message.
- Three new red flags (unverified hash, "just mark it done", optimistic traceability). `resume` is suggested to keep long programs cheap.

## 1.0.0 — 2026-11-03

First public release.

- One skill, 12 commands (`new`, `interview`, `work`, `log`, `decide`, `directive`, `task add`, `resume`, `audit`, `status`, `close`, `config`) plus custom commands; standard layout with optional and custom modules.
- Domain model: one owning file per fact, append-only history, derived fields, task/decision/playbook lifecycles, evidence ladder with `agent-tracked` fallback.
- Ownership-driven ripple sweep; `work` delivery loop that tracks agent implementation to done.
- Built-in requirement interview (quick / standard / deep): classify → read code → ask only what's missing → spec → approval → saved into `00-REQUIREMENTS.md` (rows, acceptance criteria, constraints, assumptions, interview record); open questions → decisions.
- Config with precedence (directives → playbook.yml → user → preset → defaults), `include:` for team config.
- Extensions: capabilities with fallback chains, rules with triggers (always / commands / events / conditions), custom modules wired into the ripple sweep, custom commands, red flags, audit checks, sensitive-data profiles.
- Progress tracked from git (commit, branch, pushed, PR) with `agent-tracked` fallback; issue trackers plug in as custom skills on events.
- Presets: feature, program, regulated. Agent adapters: Claude Code, Cursor, Codex/Gemini/Copilot/Windsurf, chat-only.
- `scripts/audit.py`: mechanical lint (IDs, evidence, agent-tracked completeness, derived-field drift, stale blockers, acceptance criteria, sensitive data, custom checks) + config validation.
- ARCHITECTURE.md: layers, data model, extension model, design decisions.
