# Contributing

## Most wanted
1. **Presets** for a stack or industry (`presets/<name>.yml`) with a line in the README on when to use it.
2. **Agent adapters and event-skill recipes** — e.g. a tested rule set that mirrors progress to Jira, Linear or GitHub Issues.
3. **Red flags and audit checks** from real projects (anonymised).
4. **Example playbooks** for different shapes (`examples/`), fully fictional.

## Read first
[ARCHITECTURE.md](ARCHITECTURE.md) — layers, data model and the checklist for changing the skill.

## Rules
- No company names, internal hosts, people or real data. Use `<PLACEHOLDER>`s.
- `SKILL.md` stays under 500 lines; detail goes in `references/`.
- Frontmatter keys start at column 0 and are only `name` and `description`.
- New config keys go in `config/default.yml`, `config/schema.json` and `references/extensions.md` together.
- Safety rails (see README) cannot be made configurable.

## Before a PR
```bash
python3 scripts/validate.py
claude plugin validate . && claude plugin validate ./plugins/playbook   # if you have Claude Code
```
Bump `version` in `plugins/playbook/.claude-plugin/plugin.json` and add a CHANGELOG entry for behaviour changes.

## Trying a change
```bash
claude --plugin-dir ./plugins/playbook
> /agentic-playbook:playbook resume checkout-redesign   # point root at ./examples in a test config
```
