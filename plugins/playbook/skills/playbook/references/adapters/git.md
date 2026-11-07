# Git — the built-in tracking source

Progress is tracked from git by default. No config, no connector, no token: git already runs with the developer's own identity and permissions. Anything else (Jira, Linear, GitHub Issues, a dashboard) is added by the team as a custom skill on an event — see "Adding a tracker" below.

## What is recorded per task

| Field | How it's found (read-only) |
|---|---|
| Repo | the repo from the plan row (README repos table gives the path) |
| Branch | `git -C <repo> rev-parse --abbrev-ref HEAD`, or the branch the user names |
| Commit | `git -C <repo> log -1 --format=%h` after the work, or the hash the user gives — verify it exists with `git -C <repo> cat-file -e <hash>`. Not found → list `<last evidence hash>..<task branch>` on the task's branch before searching other branches |
| Pushed? | `git -C <repo> branch -r --contains <hash>` non-empty → `pushed`, else `not pushed` |
| PR / MR | link if the user gives one or it's in the commit / branch description; never guessed |
| Verify / tests | result of the `verify` capability, or the test command run (`jest 14/14`) |

Evidence cell: `<repo> \`<hash>\` (<branch>, pushed|not pushed); <PR>; verify PASS; jest 14/14`.

No commit (the agent did the work, nothing committed yet) → `agent-tracked YYYY-MM-DD: <what>; files: <paths>; tests: <command → result>` (`../model.md` → Evidence). Later commit → replace with the commit evidence and keep the date.

Can't run git (chat-only agent, repo not reachable) → ask the user for hash, branch and pushed state once; else `not stated`.

## Rules

- Git commands here are **read-only**. Commits happen only through the `commit` capability with the user's approval; pushes never, unless the user asks.
- One commit can serve several tasks; one task can list several commits (`a1b2c3d, 9f8e7d6`).
- The playbook folder itself may be a git repo (`git.init`); its commits are playbook history, not task evidence.

## Adding a tracker (custom skill on events)

The core never talks to an issue tracker. To keep one in sync, add rules that call your own skill (or command, MCP tool, script) on the events you care about. The rule's output — an issue key, a comment link — is appended to the task's Evidence cell.

```yaml
rules:
  - id: jira-create
    on_event: [task_added]
    mode: advisory
    use: skill:jira-create
    instruction: Create one issue per new task; append the key to the task's Evidence (e.g. "SHOP-212"). Ask before creating.
  - id: jira-comment
    on_event: [task_done]
    mode: advisory
    use: skill:jira-comment
    instruction: Post a solution report (requirements, what changed, commit, tests, open items). Never change the issue's status.
```

Any external write a rule makes asks the user first, and is reported with where it went.
