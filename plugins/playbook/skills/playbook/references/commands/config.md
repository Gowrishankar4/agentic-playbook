# `/playbook config [init | show | explain <key> | validate]`

- **init** — runs automatically on the first `new` when no global config exists (skippable), or any time on request. Quick setup questions: agent in use, playbook root folder, preset, sensitive-data profiles, which of the user's skills/commands/tools to map to each capability (list what you can see in this session and suggest mappings). Write `~/.config/playbook/config.yml` (or a path the user names, or `playbook.yml` in the current playbook with `init --here`). Start from `config/config.example.yml`; keep its comments.
- **show** — print the merged config for the current context, with each top-level key's source file.
- **explain <key>** — the winning value, which file set it, and what it overrode.
- **validate** — check against `config/schema.json` and the rules in `../extensions.md`: unknown keys, rules with no trigger, capability entries of an unknown type, module templates that don't exist, duplicate ids, settings that would loosen a safety rail (ignored — report them). If the user has the repository's `tools/audit.py`, `python3 tools/audit.py --validate-config <file>` does the mechanical part.
