# Working in this repo

A public catalog of agent skills. Each skill follows the [Agent Skills specification](https://agentskills.io/specification).

## Layout

Skills live at `skills/<category>/<skill-name>/`. A category is a broad area of work (`content-writing`). Each category has a `README.md` that lists its skills, one line each, with the name linked to the skill's `SKILL.md`.

`.claude-plugin/marketplace.json` makes the repo a Claude Code marketplace with one plugin per category. The plugin's `skills` array lists every skill in that category, so a skill missing from it won't install as a plugin.

## Adding a skill

1. Create `skills/<category>/<skill-name>/SKILL.md`. Write it with the `skill-creator` skill when one is available.
2. Frontmatter: `name` equals the folder name (lowercase letters, digits, single hyphens, at most 64 characters); `description` says what the skill does and when to use it, in at most 1024 characters.
3. Keep `SKILL.md` under 500 lines. Put detail in `references/`, runnable code in `scripts/`, and templates or data in `assets/`, each linked from `SKILL.md` by a relative path.
4. Add the skill to its category `README.md`, to the top-level `README.md`, and to the category's `skills` array in `.claude-plugin/marketplace.json`. A new category gets its own folder, `README.md`, and plugin entry.
5. Run `claude plugin validate . --strict` from the repo root.
6. Run `scripts/link-skills.sh` to try the skill locally.

## Writing rules

- Write skill content as instructions about what should be done ("Run `refresh.py` when…"). Avoid first-person narration such as "I will refresh it".
- Scripts use only the language's standard library, or document their dependencies at the top of the file.
- Paths inside a skill are relative to the skill's own folder, so the folder works wherever it is installed.
- Run prose in this repo (READMEs, skill bodies) through `skills/content-writing/deslop` before committing.

## Automation

`.github/workflows/refresh-deslop.yml` runs weekly. When Wikipedia's Signs of AI writing gains or loses sections or watch-list phrases, it opens a pull request on the `automation/deslop-refresh` branch with the new snapshot. Before merging, update `references/signs.md` as the skill's "Keeping the catalog current" section describes.
