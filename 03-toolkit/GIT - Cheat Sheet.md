# Git Cheat Sheet (personal learning notes)

Not repo content — lives in `.local-notes/`, which is gitignored (`/.local-notes/` in
`.gitignore`). Commands actually run during the AB#26823 branch/PR session, grouped by
purpose, with an ELI5 for each.

## Core concepts

- **DAG (Directed Acyclic Graph)**: git history is a graph of commits, each pointing to its
  parent(s). Most commits have 1 parent; a **merge commit** has 2+. Branches (`main`,
  `fix/...`) and `HEAD` are just movable labels pointing at a commit in that graph.
- **Merkle DAG**: each commit's hash depends on its own content plus its parent's hash, so
  tampering with any commit changes every descendant's hash — history can't be silently
  rewritten without detection.
- **Stash**: a hidden set of commits (up to 3: staged, unstaged, untracked) that the
  `refs/stash` ref points to. Same underlying mechanism as a branch, just not meant to be
  long-lived.
- **Dangling commit**: once nothing points at a commit (e.g. after `git stash drop`,
  `git branch -D`, `git reset`), the commit object doesn't vanish immediately — it stays in
  the object database until garbage collection runs. If you catch it in time, you can
  recover it directly by the hash git prints when it's dropped/removed.

## Checking state before doing anything risky

```powershell
git status --short --branch      # what's changed, and what am I tracking against
git branch -vv                   # every local branch + its remote tracking + ahead/behind
git fetch origin main --quiet    # get remote info without touching my files
git log --oneline HEAD..origin/main   # commits on remote not yet in my local branch
git log --oneline main..HEAD          # commits on my branch not yet on main
git diff origin/main <branch> --stat -- <files>   # do two branches actually differ in content?
git merge-base --is-ancestor <branch> origin/main # is branch fully merged into main? (exit 0 = yes)
```
`..` between two refs means "commits reachable from the right side, not the left side."

**Gotcha**: a squash-merged PR branch will *never* show as an ancestor of main (different
commit hash), even though its content landed. Use content diff (`git diff --stat`), not
`merge-base --is-ancestor`, to check "did this actually land," and check GitHub for the PR
state directly when in doubt.

## Isolating in-progress work / switching branches cleanly

```powershell
git stash push -u -m "message" -- <file1> <file2> ...
```
"Shelve just these files (tracked + untracked, `-u`) into a labeled box, put my working tree
back to clean." Scoping with `-- <pathspec>` avoids sweeping up unrelated untracked files
that happen to be sitting in the working tree.

```powershell
git checkout main
git pull --ff-only origin main
git checkout -b fix/26823-start-needed-5-day-window
```
Fast-forward local `main` to match GitHub exactly (`--ff-only` refuses to do anything
clever/risky like an auto-merge — if it can't be a simple fast-forward it stops and tells
you), then branch fresh off that exact point.

## Reapplying a stash — the parts that bite

```powershell
git stash show -p 'stash@{0}' -- <paths> | git apply --index
```
In PowerShell, `stash@{0}` MUST be single-quoted — the braces get mangled otherwise and the
command silently fails with "No valid patches."

```powershell
git checkout 'stash@{0}' -- <paths>
```
Pulls specific files' content out of the stash into the working tree. **Gotcha**: if even
one pathspec in the list doesn't resolve (e.g. a brand-new untracked file, which lives in a
*different* internal commit than tracked changes), the whole command aborts and restores
*nothing* — with only a small error for the one bad path, easy to miss.

```powershell
git show 'stash@{0}^3:<path>'   # ^3 = the stash's third parent = untracked-files commit
```
Untracked files stashed with `-u` live in a separate parent commit of the stash, not the
main one. This is how you pull just the untracked file back out.

**The near-miss**: don't run a destructive/cleanup command (`stash drop`, `branch -D`,
`--force` anything) in the same breath as an operation you haven't verified succeeded.
Verify (`git status`, `git diff --stat`) *then* clean up — not the other way around.

## Recovering a "lost" stash/commit

```powershell
git stash drop 'stash@{0}'
# prints: Dropped stash@{0} (e061bb27...)  <- that hash is your recovery key
git cat-file -e e061bb27...          # does the object still exist? (yes, until GC runs)
git checkout e061bb27... -- <paths>  # pull files back out by raw commit hash
```
Dropping a stash only removes the *label*; the commit object is dangling but still fully
present in the object database until garbage collection. Use the hash git printed to recover
before it's gone.

## Landing the work

```powershell
git add <exact files, never `.`>   # stage precisely what you mean to, nothing swept in
git commit -m "type(scope): message"
git push -u origin <branch>        # -u records the tracking relationship for future push/pull
```

## Cleaning up a stale/superseded branch

```powershell
git push origin --delete <branch>  # remote
git branch -D <branch>             # local, force (needed if git's ancestry check says "unmerged"
                                    # but you've confirmed via content diff / GitHub PR state
                                    # that it's actually safe to delete)
```
`git branch -d` (lowercase) refuses to delete a branch git doesn't think is merged. `-D`
(capital) forces it — only use once you've verified some other way (PR merged/closed on
GitHub, or a content diff showing nothing unique is lost).

## Fast local pre-flight (before pushing, not a replacement for CI)

```powershell
uv run sqlmesh -p sqlmesh --gateway duckdb test -k <substring>   # scoped, credential-free unit tests
$env:SKIP="checkov,terraform_fmt,terraform_validate"             # skip when no .tf changed
pre-commit run --files <exact changed files>                     # not --all-files
git diff --check                                                  # whitespace/conflict-marker sanity
```
`sqlmesh test` defaults to the `snowflake` gateway (needs live credentials) unless you pass
`--gateway duckdb` explicitly — same trick the repo's `sqlmesh-lint` pre-commit hook uses.
