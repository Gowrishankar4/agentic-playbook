# `/playbook audit [name]`

Read-only. Fix only after the user approves.

A line the user has confirmed is fine can carry `<!-- audit:ignore -->` (or `<!-- audit:ignore relative-date -->` for one check); `audit.py` skips it, and so do you.

1. Do the mechanical checks below by reading the playbook files — the list is complete. If the agent can run scripts and the user has a copy of `audit.py` (it lives in the repository's `tools/` folder; the Claude directory build doesn't bundle scripts), run `python3 <path>/audit.py <playbook> [--config <merged config>]` instead and add anything it reports.
2. Do the judgement checks the script can't, plus every `audit_checks` entry with an `instruction`, plus rules with `on_event: [audit]`.

Report grouped by severity (error → warn → info):
- `✅` rows without evidence; `agent-tracked` evidence missing what / files / tests; relative dates ("yesterday", "today", "tomorrow")
- task IDs in PROGRESS but not in the plan (or vice versa); requirements with no task; commit hashes in evidence that don't exist in the repo (if git is reachable)
- "Blocked by D-xx" where D-xx is decided; "provisional (D-xx)" text after a decision
- derived fields that disagree with their sources (`../model.md`): phase status vs its tasks (`phase-mismatch`, `phase-not-started`), next action already done, `Current phase` empty after approval (`stale-current-phase`), traceability status better than its worst task (`traceability-drift`); plan header not `CLOSED` after close; past dates described as future
- open decisions superseded by a later decision but still ⬜; state transitions the model doesn't allow (e.g. `✅` while "Blocked by" an open decision)
- requirements with no acceptance criteria; tasks marked ✅ whose acceptance criteria have no evidence
- sensitive-data matches — `file:line (profile)` only, never the value
- custom `audit_checks` results
