# `/playbook resume [name]`

Read in order: `05-DIRECTIVES.md` (if present) → `AGENTS.md` → `playbook.yml` (if present) → `PROGRESS.md` → current phase in the plan → open decisions → requirements and acceptance criteria of any in-progress task.

Report in ≤ 10 lines:
- current phase and one-line state
- next action (with owner)
- in-progress tasks
- blockers
- open decisions blocking the next task
- active custom rules for this playbook (ids only)
- staleness noticed — derived fields that disagree with task rows (`../model.md`), e.g. phase row ⬜ while its tasks are ✅, a "next action" that's already done

Offer to fix staleness; don't fix it silently during resume.
