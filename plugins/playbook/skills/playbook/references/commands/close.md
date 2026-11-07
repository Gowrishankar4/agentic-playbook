# `/playbook close [name]`

1. Run `audit`. Errors must be fixed or explicitly accepted by the user first.
2. List tasks not ✅ and decisions still open; ask what happens to each (moved to another playbook, dropped as `SUPERSEDED`/`won't do`, or kept open).
3. Fire `close`.
4. Add `## Closing summary` to `PROGRESS.md`: date, outcome against the goal and success metric, what shipped (tasks + evidence), what didn't, lessons (anything worth turning into a `red_flags` or `rules` entry — offer to add it to the user's config).
5. Set **both** headers to closed: PROGRESS `**Stage:** CLOSED YYYY-MM-DD` and the plan header `**Status:** CLOSED YYYY-MM-DD` (it was `APPROVED …`; `model.md` → Derived fields). Archive per `close.archive` (default `ask`: move under `<root>/archive/`, or leave in place).
