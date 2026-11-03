# Changelog

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
