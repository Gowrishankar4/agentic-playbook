# `/playbook log [name]`

Record work done outside `work` (by the user, a teammate, another agent). For work the agent does itself, `work` records as it goes.

1. Collect per task: status and evidence (`../model.md` → Evidence) — commit hash, branch, pushed?, PR, verify result, test counts — read from git where possible (`../adapters/git.md`). Ask **once** for anything missing (one question listing every gap).
2. If the `verify` capability is mapped and the user wants it, run it and record the result. A commit that skipped the team's verify → commit flow is recorded plainly (`verify not run`) — never marked "verified".
3. Check the state transition is allowed (`../model.md` → Task). Fire `task_started` / `task_done` as the state changes; `before_commit` if you are about to record or make a commit.
4. Update the task's row (owner) — state, evidence, date — and note which acceptance criteria in `00-REQUIREMENTS.md` the evidence covers.
5. Ripple sweep.
