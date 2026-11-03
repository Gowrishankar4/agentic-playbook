# Agent adapters

The core uses generic actions. Map each one to what the current agent offers. If a row's tool is not present in this session, use the next option and say so in one line.

| Action | Claude Code | Cursor | Codex CLI / Gemini CLI / Copilot / Windsurf | Chat only (Claude.ai, ChatGPT, any assistant) |
|---|---|---|---|---|
| **ask** the user | AskUserQuestion tool | ask in chat, wait | ask in chat, wait | ask in chat, wait |
| **use skill** `skill:<name>` | Skill tool | run `/<name>`, or read its `SKILL.md` from the skills folder and follow it | read the skill's `SKILL.md` and follow it | ask the user to paste it, or use the built-in fallback |
| **run command** `command:/<x>` | slash command | slash command | the agent's command/prompt mechanism, else follow the command file | tell the user to run it; record the result they report |
| **MCP** `mcp:` / `mcp?` | discover via tool search, then call | MCP tool list | the agent's MCP config | not available → fallback |
| **subagent** | Agent tool (fresh agent) | Cursor subagents | the agent's sub-task feature, else sequential | sequential |
| **script** | Bash | terminal tool | shell tool | give the user the command; record the output they paste |
| **edit file** | Edit/Write | edit | edit | return full file contents or a patch for the user to apply |
| **remember pointer** | memory folder + index line if memory is on and `memory.pointer` allows | none | none | none |

## Discovery

Agents find the playbook through this skill and the playbook's own context files (`context_files` in config — default `AGENTS.md` + `CLAUDE.md`; add `GEMINI.md`, `.github/copilot-instructions.md`, `.windsurfrules` as needed). Each extra context file contains one line: `Follow AGENTS.md in this folder.`

Never write discovery files into product repos unless the user asks — those are commits to someone else's codebase.

## Chat-only mode

When the agent cannot read or write files:
1. Ask the user to paste `PROGRESS.md` and whichever files the command needs (list them).
2. Do the work, then return each changed file in full (or a unified diff if the user prefers), clearly labelled with its path.
3. The ripple sweep still applies — list every file that must change, even if the user has to paste more of them first.
