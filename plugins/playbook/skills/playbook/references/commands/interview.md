# `/playbook interview [TASK]` (aliases: `prompt`, `spec`, `requirements`)

Gather or refine requirements and save them into `00-REQUIREMENTS.md`.

- **No task** → program scope: new requirements, changed scope, a new source document. Asks only what the playbook doesn't already answer.
- **With a task ID** → make one task implementation-ready before work starts: its requirements, constraints and acceptance criteria.

Follow `../interview.md` (depth from the request, else config). On approval it writes the requirement rows, acceptance criteria, constraints, assumptions and the interview record into `00-REQUIREMENTS.md`, open questions into `03-DECISIONS.md`, then fires `after_interview` and runs the ripple sweep.

The acceptance criteria saved for a task are the evidence checklist `log` uses when the task is reported done.
