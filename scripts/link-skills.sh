#!/usr/bin/env bash
# Symlink every skill in this repo into the local harness skill directories,
# so a `git pull` keeps installed skills current. Re-run after adding,
# removing, or renaming a skill.
#
# Usage: scripts/link-skills.sh [target-dir ...]
# Default targets: ~/.claude/skills and ~/.agents/skills
#
# An existing real directory with a skill's name is left alone (with a warning),
# never overwritten. Remove it by hand to switch it over to the repo copy.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "$#" -gt 0 ]; then
  targets=("$@")
else
  targets=("$HOME/.claude/skills" "$HOME/.agents/skills")
fi

for target in "${targets[@]}"; do
  mkdir -p "$target"

  # Drop links that point into this repo but whose skill no longer exists.
  for link in "$target"/*; do
    if [ -L "$link" ] && [[ "$(readlink "$link")" == "$repo_root"/* ]] && [ ! -e "$link" ]; then
      rm "$link"
      echo "removed stale $link"
    fi
  done

  while IFS= read -r skill_md; do
    skill_dir="$(dirname "$skill_md")"
    name="$(basename "$skill_dir")"
    dest="$target/$name"

    if [ -L "$dest" ]; then
      ln -sfn "$skill_dir" "$dest"
    elif [ -e "$dest" ]; then
      echo "skipped $dest: a real directory exists there" >&2
      continue
    else
      ln -s "$skill_dir" "$dest"
    fi
    echo "linked $dest -> $skill_dir"
  done < <(find "$repo_root/skills" -mindepth 3 -maxdepth 3 -name SKILL.md | sort)
done
