# Toolkit CLI - How To Use

Trial: 2026-10-07 to 2026-10-21. Project: `C:\Repos\sd-edw\toolkit\toolkit-cli`. Repo: `https://github.com/artemisbi828/toolkit-cli` (private).

## What it is

One `toolkit` command over the toolkit tools you already have. It calls the existing PowerShell scripts; it does not replace them, so the old way still works. The toolkit folder is on PATH, so `toolkit` works from any terminal.

## Daily commands

| Command | What it does |
|---|---|
| `toolkit doctor` | Checks git, py, pwsh, the rollback tag, and uncommitted changes. |
| `toolkit audit` | Runs the registry audit (docs, absolute paths, index rows). |
| `toolkit new "name" -d "purpose" [--category sublime\|autohotkey\|obsidian]` | Warns about likely duplicates (exit 2), prints the devil's-advocate questions, dry run until `--apply`. |
| `toolkit prefs` / `toolkit prefs --apply` | Previews or deploys the Copilot preference files. |
| `toolkit journal plan [--since last\|midnight\|<time>]` | Shows what happened since the save point (git commits, changed vault notes). Writes nothing. |
| `toolkit journal mark` | Moves the save point to now. Run only after the journal is written. |

## Where things live

- Tools: `C:\Repos\sd-edw\toolkit` (generic) and its `sublime\`, `autohotkey\`, `obsidian\` folders.
- Index of every tool with its folder: `C:\Repos\sd-edw\toolkit\toolkit-product-index.md`
- Copilot preferences (source of truth): `C:\Repos\sd-edw\toolkit\ai-preferences`
- Backups: `C:\Repos\sd-edw\toolkit\.dev-in-progress`
- Pre-trial full copy: `C:\Repos\sd-edw\toolkit\.dev-in-progress\20261007_111947_pre-cli-trial-backup`

## Roll back to before the trial

1. `toolkit doctor` and commit or stash any changes you want to keep.
2. `git -C C:\Repos\sd-edw\toolkit checkout pre-cli-trial`
3. To return: `git -C C:\Repos\sd-edw\toolkit checkout main`.
4. If git is unusable, copy folders back from the pre-trial backup (`toolkit`, `Startup`, `SublimeUser`).

## Keep it

After the trial, delete the backup folder and keep `main`. Nothing else to clean up.

## Push to GitHub as artemisbi828

The GitHub CLI's active account is the work account. Use:

```powershell
$env:GH_TOKEN = (gh auth token --user artemisbi828)
git -C C:\Repos\sd-edw\toolkit -c "credential.helper=!gh auth git-credential" push
Remove-Item Env:GH_TOKEN
```

Commits in this repo use the artemisbi828 noreply email (repo-local setting).

## What changed in how you work

- Tools are grouped into category folders; each README lists absolute paths.
- A new tool request is checked against the index first; duplicates are merged or extended.
- The AutoHotkey tools are unchanged. Python-backed commands may add about 100-300 ms per call.
- Not done yet: the `/journal` prompt for incremental runs. Requirements: `C:\Repos\sd-edw\toolkit\obsidian\session-journal\requirements-incremental.md`.
- Still open: the `message-notation` entry in `toolkit-admin\external-references.json` points at a note that no longer exists.

## If you get confused

Ask Copilot to read `C:\Repos\sd-edw\toolkit\toolkit-cli\README.md` and the latest `sessions\` log. They hold the retrace, rollback, and keep steps.
