# Rules for any session working on <feature>

1. Read `05-DIRECTIVES.md` first if it exists, then `PROGRESS.md`. Update PROGRESS **in the same session** as any work: dates YYYY-MM-DD; evidence = commit hash, branch, pushed?, PR, test run — or, when nothing is committed, `agent-tracked <date>: what; files; tests`.
2. Every piece of work maps to a task ID in `02-PLAN.md`. No ID → add the task first.
3. Decisions go in `03-DECISIONS.md` before they're implemented. Answered → record who, when, what; unblock dependants.
4. No secrets or sensitive data in this folder (profiles: <profiles>) — placeholders and env var names only.
5. Product-repo commits follow the team's verify → commit flow with explicit approval; never push unless asked. External systems (issue trackers) only through the team's custom skills, with approval.
6. No implementation on a phase until `02-PLAN.md` says APPROVED.
7. Use `/playbook` to update this folder (`/playbook work <TASK>` to implement a task end to end); it keeps every file consistent. Config overrides for this playbook: `playbook.yml`.
