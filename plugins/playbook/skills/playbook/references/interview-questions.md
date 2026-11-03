# Question bank

Pick from the matching list in order; skip what's answered. `quick` = the first 3 unanswered, `standard` = up to 8, `deep` = all, then probe each spec section for gaps.

## Technical

1. What should be true when this is done — the user-visible outcome?
2. Who uses it (role, system, API consumer)?
3. Where does it live? *(confirm what the code inspection found)*
4. Inputs and outputs — shapes, formats, examples (placeholders only)?
5. Edge cases and failure behaviour — empty, invalid, timeout, duplicate, concurrent?
6. Constraints — stack, versions, performance budget, backwards compatibility?
7. Data — new fields, migrations, retention, who can see it?
8. Auth / permissions — who may do this, who must be blocked?
9. Integrations — third-party APIs, webhooks, rate limits, sandbox access?
10. How will we know it works — the tests or checks you'd accept?
11. Rollout — flag, staged, all at once; how to undo?
12. Out of scope — what should explicitly *not* change?

### Bug-specific
- Steps to reproduce, expected vs actual, since when, which environments, logs/errors (redacted), workaround in use?

## General

1. What's the deliverable — document, plan, analysis, content, decision?
2. Audience and what they should do after reading it?
3. Scope — what's in, what's out?
4. Sources to use or avoid?
5. Length, format, tone, language?
6. Deadline and review/approval path?
7. What would make it excellent vs merely acceptable?
8. Examples of something similar you liked?

## Playbook questions (`new` only)
Ask first in the interview: source document and owner · goal and success metric · environment/rollout constraints. (Name, repos, approver and modules are settled earlier, in `new` Step 2 — don't ask them again.)
