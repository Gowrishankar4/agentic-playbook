# Checkout redesign — Playbook

Single-page checkout for the web store, replacing the 4-step flow. For returning and guest shoppers on desktop and mobile. The constraint that matters most: cart totals must match the existing pricing service exactly.

- **Source:** "Checkout v2 PRD", 2026-10-20, Product (normalized in `00-REQUIREMENTS.md`)
- **Goal:** checkout completion rate from 61% to 70% within 30 days of 100% rollout
- **Approver:** Product lead
- **Preset:** feature

## Read order

| File | What it is |
|---|---|
| `PROGRESS.md` | **Start here.** Phase, next action, tasks with git evidence, log |
| `00-REQUIREMENTS.md` | Requirements, acceptance criteria, constraints, interview record |
| `01-ANALYSIS.md` | As-is code analysis, gaps, ambiguities, risks |
| `02-PLAN.md` | Approval status, architecture, phases, tasks |
| `03-DECISIONS.md` | Open and decided questions |
| `04-TRACEABILITY.md` | Requirement → task → test |

## Repos touched

| Repo | Role |
|---|---|
| `web` | Checkout page, form state |
| `api` | Totals endpoint, order creation |

## Folder layout

`references/` and `db/` are created when needed. `playbook.yml` holds this playbook's config overrides.
