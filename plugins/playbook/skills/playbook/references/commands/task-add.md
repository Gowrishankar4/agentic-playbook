# `/playbook task add <title>`

1. Next free ID in the existing scheme (scan plan + PROGRESS).
2. Run the requirement interview (`../interview.md`) at **quick** depth for the task unless the user gave everything: requirement it serves, repo, blockers, type, acceptance criteria. Use `code-analysis` to find where it lands. Never invent scope details — unknowns become a `D-NN` that blocks the task.
3. Fire `task_added`.
4. Ripple sweep: plan task list + dependency graph, PROGRESS row, requirement in `00` (new ID marked `added YYYY-MM-DD, source: <who>` if none fits), traceability, log. The interview output is saved into `00-REQUIREMENTS.md` (rows, acceptance criteria, interview record).
