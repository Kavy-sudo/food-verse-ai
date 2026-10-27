#!/usr/bin/env bash
# Usage: ./push_to_github.sh <your-github-username>
# Needs the GitHub CLI (gh auth login) or an empty repo already created on github.com.
set -e
git init -q -b main
git add . && git commit -qm "Initial commit: Food Verse AI"
if command -v gh >/dev/null; then
  gh repo create food-verse-ai --public --source=. --push
else
  git remote add origin "https://github.com/$1/food-verse-ai.git"
  git push -u origin main
fi
