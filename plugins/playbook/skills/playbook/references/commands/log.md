# `/playbook log [name]`

Record work done outside `work` (by the user, a teammate, another agent). For work the agent does itself, `work` records as it goes.

1. Collect per task: status and evidence (`../model.md` → Evidence) — commit hash, branch, pushed?, PR, verify result, test counts — read from git where possible (`../adapters/git.md`). **Every hash you are given is verified** (`git cat-file -e`) before it is recorded; a hash that doesn't exist is never written. Find the real one by looking **on the task's branch first**: `git -C <repo> log --format='%h %an %s' <last recorded hash>..<task branch>` (commits since the playbook's last evidence), then other branches; propose what you find (hash, author, message, branch) and ask before recording. Ask **once** for anything missing (one question listing every gap).
2. If the `verify` capability is mapped and the user wants it, run it and record the result. A commit that skipped the team's verify → commit flow is recorded plainly (`verify not run`) — never marked "verified".
3. **Scope check before `✅`.** Compare what was reported with the task's full scope (plan row + acceptance criteria). Part of it left → the task stays `🟡` and the row names what's left. It becomes `✅` only if the user explicitly accepts it as done — then `✅ accepted by <who> <date>, left: <what>`, and the leftover is either a new task (`task add`) or listed under "Not done" at close. "Quick" or "just mark it done" is not that acceptance; ask once.
4. Check the state transition is allowed (`../model.md` → Task). Fire `task_started` / `task_done` as the state changes; `before_commit` if you are about to record or make a commit.
5. Update the task's row (owner) — state, evidence, date — and note which acceptance criteria in `00-REQUIREMENTS.md` the evidence covers.
6. Ripple sweep.
