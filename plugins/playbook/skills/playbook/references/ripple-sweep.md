# The ripple sweep

Run after every change, and once (not per fact) when one message carries several facts. It works because each fact has one owner (`model.md`).

## Algorithm

1. **Owner first.** Write the change in the entity's owning file (task state → PROGRESS task row; decision → `03-DECISIONS.md`; requirement → `00-REQUIREMENTS.md` …).
2. **Find references.** Search the whole playbook for every ID touched (task, requirement, decision, directive), including custom modules.
3. **Update dependents** using the map below **plus** the `reacts_to` entries of every custom module in config. Fire `before_sweep` first.
4. **Recompute derived fields** (`model.md`): current phase, next action, phase table, traceability status. Fix them even if they were already wrong before your change.
5. **Append the log entry** — one row for the session, newest first.
6. **Report** (`after_sweep` fires here): files changed, one line each; anything left open and why. Something you can't resolve → flag it in the file (`⚠️ needs <owner>: …`) **and** in the report. Never silently skip.

## Dependents map

| Changed (in its owner) | Also update |
|---|---|
| Task started / done / reopened | traceability rows for its requirements · tasks that list it in "Blocked by" · acceptance criteria covered (traceability `Test`/`Status`) · derived fields |
| Decision answered | Open row → `✅ → DD-NN` (kept as history) + Decided row (date, answer quoted, who; `relayed by <who>` if second-hand) · every "Blocked by D-NN" cell · `<TBD → D-NN>` and "provisional (D-NN)" in requirements, analysis, contract, test cases (`Blocked: D-NN` cases → unblock or `⚠️ needs QA`) · tasks it unblocks `⏸` → previous · derived fields |
| Decision superseded | Open row → `SUPERSEDED by DD-NN`; never left `⬜` |
| Task added | plan task list + dependency graph · PROGRESS task row · requirement in `00` (new ID, `added YYYY-MM-DD, source: <who>`) if none fits · traceability row |
| Requirements changed (interview) | rows, acceptance criteria, constraints, assumptions + new interview record · traceability rows and `Test` · open questions → `03-DECISIONS.md` · plan tasks if scope changed (requirement with no task → propose `task add`) · README goal if changed |
| Directive added | Directives table (number, date, verbatim quote, who, where it lands) · plan rules/tasks it changes · ADR if architectural |
| Scope or contract change | contract changelog + version · affected requirements, acceptance criteria and tests · traceability |
| Config changed (`playbook.yml`) | README if repos changed · AGENTS.md if session rules changed |

`✅ code` + `⚠️ D-NN open: <what it may change>` when a task is done but one of its own decisions is still open — keep D-NN open.
