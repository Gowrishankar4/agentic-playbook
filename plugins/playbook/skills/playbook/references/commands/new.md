# `/playbook new [name]`

Order is fixed: **setup → name and playbook settings → scaffold → requirement interview → analysis → plan → approval.** Never ask requirement questions before setup is settled, and never start analysis or planning before requirements are approved and saved.

## Step 1 — First-run setup (only if no global config exists)

No `$PLAYBOOK_CONFIG` and no `~/.config/playbook/config.yml` → this is the user's first playbook. Run `config init` (`config.md`) first — a short, skippable setup:
- where playbooks should live (`root`, default `~/playbooks`)
- preset (`feature` / `program` / `regulated`)
- sensitive-data profiles
- which of their skills / commands / tools to use for each capability — list what you can see in this session (e.g. a `prompt` or brainstorming skill for `interview`, a code-graph skill for `code-analysis`, `/verify` and `/commit`) and propose a mapping; anything unmapped uses the built-in step

Write the config, show it in one block, continue. "Skip" → use defaults, note "using defaults — run `/playbook config init` any time", continue. Chat-only agents: give the config text for the user to save.

## Step 2 — Name and playbook settings

Ask together, in one message (offer defaults; skip anything already given or set in config):
1. **Name** — if not given. Kebab-case, formatted by `naming`. Check it doesn't exist (Locating a playbook); if it does, offer `resume` instead — never create a second playbook for the same program.
2. **Preset** for this playbook, if different from the global one.
3. **Repos involved** (name + path or URL).
4. **Approver** for decisions and plan sign-off.
5. **Optional modules** — built-ins from the preset's `offer` list plus `custom_modules` with `add_on: ask`.

Anything that differs from global config goes into the playbook's `playbook.yml`.

## Step 3 — Scaffold

Fire `before_scaffold`. Create the folder under `root` and the files from `templates/` (plus custom module templates and one context file per `context_files`). README gets name, repos, approver, preset; requirement-dependent sections say `None yet — requirements pending`. Plan header: `DRAFT — requirements pending`; PROGRESS `Stage: REQUIREMENTS`, phase table empty until the plan exists. Create `references/` and `db/` only when something goes in them. Fire `after_scaffold`.

## Step 4 — Gather requirements (interview)

Use the `interview` capability: the first mapped entry that's available (e.g. `skill:prompt`), else the built-in interview in `../interview.md`. Whichever runs:
- start from the source document (path / link / paste) and its owner, the goal and success metric, and environment / rollout constraints, then the request itself
- read the repos from Step 2 before asking technical questions
- ask only what's missing; questions only someone else can answer become `D-NN`
- draft the spec, get approval, then **save into `00-REQUIREMENTS.md`** per step 7 of `../interview.md` (rows with IDs, acceptance criteria and `Default`; constraints; invariants; assumptions; the approved spec under `## Interview record`). Quote the source; don't paraphrase numbers.

A mapped skill that executes or saves elsewhere → take its spec, save it as above, and do not execute. Fire `after_interview`; update README's first paragraph and goal from `<context>` and `<task>`.

## Step 5 — Analyse the code

Per repo with `code-analysis`: what exists to reuse (with file paths), gaps, ambiguities as `A-NN` each with a proposed reading, risks. Each ambiguity needing a human → a `D-NN` with a recommendation and the tasks it blocks. Fire `after_analysis`.

## Step 6 — Plan

In `02-PLAN.md` (use `plan-breakdown` for the task breakdown only; output goes into the template): status header `DRAFT — awaiting approval` (`DRAFT (provisional — analysis pending)` if step 5 couldn't run; repo columns then say `<TBD → analysis>`), architecture, phases with exit criteria, dependency graph, task list (ID, title, repo, type). Fill `04-TRACEABILITY.md` so every requirement has ≥ 1 task and its acceptance criteria in `Test`.

## Step 7 — Show the plan and stop for approval

Fire `before_approval`. Handoff = folder path, file list, requirement count, task list, open decisions (most blocking first), questions still unanswered. No product code before the header says `APPROVED <YYYY-MM-DD> (<approver>)`. On approval fire `after_approval`.

## Step 8 — After approval

1. **Git (per `git.init`)** — `git init` + first commit of the playbook (markdown and yml only; push only if `git.push` and the user allow).
2. **Discovery (per `memory.pointer`)** — if the agent has memory: a pointer file (location, ID mapping, "read PROGRESS.md first") and an index line. Never write pointers into product repos unless asked.
3. **Hand over to delivery** — offer `/playbook work <first task>` (the derived next action). From here every change goes through `work`, `log`, `decide`, `directive`, `task add` or `interview`, each followed by the ripple sweep.
