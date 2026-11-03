# `/playbook audit [name]`

Read-only. Fix only after the user approves.

1. If the agent can run scripts, run `scripts/audit.py <playbook> [--config <merged config>]` for the mechanical checks. Otherwise do them by reading.
2. Do the judgement checks the script can't, plus every `audit_checks` entry with an `instruction`, plus rules with `on_event: [audit]`.

Report grouped by severity (error → warn → info):
- `✅` rows without evidence; `agent-tracked` evidence missing what / files / tests; relative dates ("yesterday", "today", "tomorrow")
- task IDs in PROGRESS but not in the plan (or vice versa); requirements with no task; commit hashes in evidence that don't exist in the repo (if git is reachable)
- "Blocked by D-xx" where D-xx is decided; "provisional (D-xx)" text after a decision
- derived fields that disagree with their sources (`../model.md`): phase status vs its tasks, next action already done, traceability status vs task states; past dates described as future
- open decisions superseded by a later decision but still ⬜; state transitions the model doesn't allow (e.g. `✅` while "Blocked by" an open decision)
- requirements with no acceptance criteria; tasks marked ✅ whose acceptance criteria have no evidence
- sensitive-data matches — `file:line (profile)` only, never the value
- custom `audit_checks` results
