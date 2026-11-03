# <Feature> — Playbook

<One paragraph: what it is, who it's for, the constraint that matters most.>

- **Source:** <doc title, date, owner> (normalized in `00-REQUIREMENTS.md`)
- **Goal:** <measurable outcome>
- **Approver:** <name / role>
- **Preset:** <feature | program | regulated | custom>

## Read order

| File | What it is |
|---|---|
| `05-DIRECTIVES.md` | *(if present)* Approver directives — read first, override everything |
| `PROGRESS.md` | **Start here.** Phase, next action, tasks with git evidence, log |
| `00-REQUIREMENTS.md` | Requirements, acceptance criteria, constraints, defaults, interview record |
| `01-ANALYSIS.md` | As-is code analysis, gaps, ambiguities, risks |
| `02-PLAN.md` | Approval status, architecture, phases, tasks |
| `03-DECISIONS.md` | Open and decided questions |
| `04-TRACEABILITY.md` | Requirement → task → test |

## Repos touched

| Repo | Role |
|---|---|

## Folder layout

`references/` and `db/` are created when needed. `playbook.yml` holds this playbook's config overrides.
