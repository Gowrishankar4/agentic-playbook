# `/playbook work [TASK]`

The delivery loop: the agent takes a task from `⬜` to `✅` and the playbook records every step. Also applies whenever the agent implements a task without this command being named — implementing a task means tracking it.

1. **Pick the task.** Given, else the derived "Next action". Check the transition `⬜ → 🟡` is allowed (`../model.md`): plan `APPROVED`, nothing open in "Blocked by". Not allowed → say why and stop.
2. **Load context.** The task's plan row, its requirements and acceptance criteria in `00-REQUIREMENTS.md`, related decisions and directives, the analysis for its repo. Acceptance criteria missing or vague → run `interview <TASK>` (quick) first.
3. **Start.** Set the PROGRESS row to `🟡` with the date (and branch, if one is created). Fire `task_started`.
4. **Implement** with the `implement` capability (the team's product-repo workflow), else directly — exactly the task's scope. Anything that changes scope → stop, record it (`task add`, `interview`, or a new `D-NN`) before continuing. Work that moves between tasks (e.g. tests planned for a later task done now) is a scope change too: update **both** plan rows (title, and exit criteria if affected) and say so in the log, in the same sweep — the plan must describe what each task actually holds.
5. **Verify** with the `verify` capability; run what proves the acceptance criteria. Fire `before_commit` before committing; commit only through the `commit` capability and only with approval (`git.commit`); never push unless asked.
6. **Record evidence** (`../model.md` → Evidence): read from git (`../adapters/git.md`) — commit, branch, pushed, PR — plus verify result and test counts. Nothing exists → `agent-tracked YYYY-MM-DD: <what>; files: <paths>; tests: <command → result>`.
7. **Complete.** `🟡 → ✅` if evidence meets `evidence.required` (or the agent-tracked minimum) and every acceptance criterion is covered; else stay `🟡` and say what's left. Fire `task_done`. Ripple sweep.
8. **Report** in ≤ 6 lines: task, what changed, evidence, criteria met, next action.

A task is not done until `PROGRESS.md` says so — in the same session as the work.
