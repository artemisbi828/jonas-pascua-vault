---
related_to:
  - "[[GIT]]"
  - "[[GIT - Account]]"
---
# GIT - Error Handling - 403 Wrong Account + Fork Prompt

## Symptom
```
remote: Permission to artemisbi828/artemis-hub.git denied to jonas-pascua-sd.
fatal: unable to access 'https://github.com/artemisbi828/artemis-hub/': The requested URL returned error: 403
```
GitHub/VS Code suggests: "fork the repo and push to your fork."

## ELI5
Windows keeps one keyring holding both GitHub badges. On push, Git grabbed the **default badge** (work: `jonas-pascua-sd`) and showed it at the door of `artemisbi828/artemis-hub`. GitHub said "you're not on the list" (403).
- Nothing was wrong with the repo or the branch. Git just used the wrong account.

## Branch vs Fork
| | Branch | Fork |
|---|---|---|
| What | Separate line of work **inside one repo** | A **full copy of someone else's repo** under your own account |
| Requires | Write access to that repo | Nothing (anyone can fork a public repo) |
| Used for | Your own day-to-day work | Contributing to repos you can't write to (open-source flow: fork → push → pull request) |

GitHub thought `jonas-pascua-sd` was a stranger, so it gave the standard advice for strangers: "make your own copy." **That's the wrong fix here.** Both accounts are yours, and a fork would split the vault across two copies.

## Fix (repo-local)
Run inside the repo:
```powershell
git config --local credential.username artemisbi828   # use the personal login for this repo
git config --local user.name artemisbi828             # put the personal name on future commits here
git config --local user.email jonas.pascua@artemisbi.com
git push
```
- `--local` writes to the repo's `.git/config` only, so work repos aren't affected.
- Avoid `gh auth switch` as a fix. It's global, so you'd keep switching back and forth and eventually push under the wrong account.
- The first push opens a browser sign-in once. After that, the login is saved in Git Credential Manager.
- Mirror setup for work GitHub repos: `git config --local credential.username jonas-pascua-sd`

Undo: `git config --local --unset credential.username`

## "Choose an account" Prompt
- Shows up when 2+ GitHub logins are saved and the repo **isn't pinned** to one, so Git doesn't know which badge to use.
- Pick based on the owner in the remote URL: `SmileDoctorsIT/...` = `jonas-pascua-sd`, `artemisbi828/...` = `artemisbi828`.
- Pin it once afterward and the prompt won't come back: `git config --local credential.username <badge>`
- Pinned so far: `C:\obsidian\Artemis-Hub` → `artemisbi828`, `C:\Repos\sd-edw\project-ascend\data-platform` → `jonas-pascua-sd`

## Login vs Author Label (two different things)
| | Work | Personal |
|---|---|---|
| **GitHub login (badge)**: used for permission to push | `jonas-pascua-sd` | `artemisbi828` |
| **Commit author label** (`user.name` / `user.email`): text stamped on each commit, no permissions | `jpascua313SD` / `jonas-adam.pascua@smiledoctors.com` (global) | `artemisbi828` / `jonas.pascua@artemisbi.com` (vault-local) |

- Login = **who is allowed in**. Author label = **the name written on the package**. GitHub never checks the label for permissions.
- Local config overrides global config, so the vault uses the personal label and everything else falls back to the work label.

## Diagnostic Commands
```powershell
git remote -v                                  # where am I pushing?
git config --show-origin --get-regexp "user|credential"   # which identity/login, and from which file
git credential-manager github list             # GitHub logins saved in Windows
gh auth status                                 # gh CLI logins + which is active
git push --dry-run origin main                 # test auth without pushing
```
