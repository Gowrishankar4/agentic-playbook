# `/playbook directive`

Append to `05-DIRECTIVES.md` (create it with the user's OK if missing): next number, date, the instruction **verbatim** in quotes, who gave it, "where it lands" (ADR / task IDs / files). If it conflicts with an earlier directive, the newer one wins — say which it overrides.

A directive may also change config for this playbook (e.g. "every API task needs a load test") — offer to add the matching rule to `playbook.yml`; directives still win if the two ever disagree.

Fire `directive_added`, reconcile the plan, then ripple sweep.
