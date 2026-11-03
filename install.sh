#!/usr/bin/env bash
# Install the playbook skill into an agent's skills folder.
#   ./install.sh --agent claude|cursor        known folders
#   ./install.sh --dir <path>                 any skills folder (Codex, Gemini CLI, Windsurf, …)
#   add --link to symlink instead of copy (stays in sync with git pull)
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/plugins/playbook/skills"
DEST=""; MODE=copy
while [ $# -gt 0 ]; do
  case "$1" in
    --agent) case "$2" in
               claude) DEST="$HOME/.claude/skills" ;;
               cursor) DEST="$HOME/.cursor/skills" ;;
               *) echo "Unknown agent '$2' — use --dir <skills folder>"; exit 1 ;;
             esac; shift 2 ;;
    --dir) DEST="$2"; shift 2 ;;
    --link) MODE=link; shift ;;
    *) echo "usage: $0 (--agent claude|cursor | --dir PATH) [--link]"; exit 1 ;;
  esac
done
[ -n "$DEST" ] || { echo "usage: $0 (--agent claude|cursor | --dir PATH) [--link]"; exit 1; }
mkdir -p "$DEST"
for s in playbook; do
  rm -rf "${DEST:?}/$s"
  if [ "$MODE" = link ]; then ln -s "$SRC/$s" "$DEST/$s"; else cp -r "$SRC/$s" "$DEST/$s"; fi
  echo "✔ $s → $DEST/$s ($MODE)"
done
mkdir -p "$HOME/.config/playbook"
if [ ! -f "$HOME/.config/playbook/config.yml" ]; then
  echo "Next: run '/playbook config init' in your agent, or copy"
  echo "      $SRC/playbook/config/config.example.yml → ~/.config/playbook/config.yml"
fi
