# Agentic Playbook plugin

One skill for AI-assisted delivery. `/playbook` creates and maintains a folder per feature or program — requirements, analysis, plan, decisions, progress and traceability — so any agent session continues from the same state, and runs a ripple sweep after every change so no file goes stale. Requirements come from a built-in interview that reads the code first, asks only what is missing, gets your approval and saves the result into `00-REQUIREMENTS.md`.

## Install

```
/plugin marketplace add Gowrishankar4/agentic-playbook
/plugin install playbook@agentic-playbook
```

## Use

- `/playbook:playbook new <name>` — interview, scaffold, analyse code, plan, stop for approval
- `/playbook:playbook interview [TASK]` — gather or refine requirements → `00-REQUIREMENTS.md`
- `/playbook:playbook resume` · `log` · `decide D-02` · `task add` · `work` · `audit` · `status` · `close` · `config init`

## Setup

None required. `/playbook:playbook config init` writes `~/.config/playbook/config.yml`, where you map your own skills, commands, MCP tools and scripts to each step, add rules with triggers, custom playbook files, commands and lint checks. See CUSTOMIZING.md in the repository.
