#!/usr/bin/env bash
# Usage: scripts/set-owner.sh <github-user-or-org>
set -euo pipefail
[ $# -eq 1 ] || { echo "usage: $0 <github-owner>"; exit 1; }
grep -rl 'Gowrishankar4' --exclude-dir=.git . | xargs sed -i.bak "s/Gowrishankar4/$1/g"
find . -name '*.bak' -delete
echo "Replaced Gowrishankar4 with $1"
