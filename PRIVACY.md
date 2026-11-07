# Privacy

Agentic Playbook collects no data and sends nothing anywhere.

- **What it reads:** your project's files and git state (commits, branches, push and PR status), using git and, where you have it set up, the GitHub CLI with your own login. This happens on your machine, inside your Claude session.
- **What it writes:** markdown playbook files in the folder you choose (default `~/playbooks`) and an optional config file at `~/.config/playbook/config.yml`. Nothing is written into your product repositories unless you ask.
- **What it sends:** nothing. The plugin has no server, no analytics, no telemetry and no network calls of its own. Your conversation with Claude is covered by your Claude account's terms and privacy policy.
- **Sensitive data:** the skill's sensitive-data profiles (secrets, PII, PCI, PHI) keep such values out of playbook files, and the repository's `tools/audit.py` flags any that slip in.

Questions: open an issue at https://github.com/Gowrishankar4/agentic-playbook/issues.
