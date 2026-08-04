#!/usr/bin/env bash
# Sync skills from the iCloud working copy into this repo, then commit and push.
# Run after any skill edit: ./sync.sh
set -euo pipefail

SRC="/Users/berkk/Library/Mobile Documents/com~apple~CloudDocs/AIM Articles/skills/"
cd "$(dirname "$0")"

rsync -a --delete --exclude='.DS_Store' "$SRC" skills/

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "sync: $(date '+%Y-%m-%d %H:%M')"
  git pull --rebase -q
  git push
  echo "Synced and pushed."
else
  echo "No changes."
fi
