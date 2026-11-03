# `/playbook status`

Read-only. For every `PROGRESS.md` under `root` and `extra_roots`, print one line:

`<name> · <current phase> · <done>/<total> tasks · <open decisions> open D · next: <next action> · last log <YYYY-MM-DD>`

Sort by last log date, newest first. Mark playbooks with no log entry in 14 days (`status.stale_after_days`) as `stale`. Closed playbooks (`archive/` or header `CLOSED`) are listed only with `status --all`.
