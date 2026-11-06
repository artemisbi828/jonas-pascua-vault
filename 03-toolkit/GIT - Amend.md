*   **Just add more code to last commit:** `git commit --amend`
*   **Already pushed:** amend + `git push --force-with-lease`
*   **Fold another branch in but keep 1 commit:** `git merge --squash other-branch` then `--amend`
*   **Combine multiple commits:** `git rebase -i`

## 1) Add new changes into the **most recent commit** (same message)

```bash
git add -A
git commit --amend --no-edit
```

### If you want to also edit the commit message:

```bash
git add -A
git commit --amend
```

***

## 2) Amend only specific files (not everything)

```bash
git add path/to/file1 path/to/file2
git commit --amend --no-edit
```

***

## 3) You already pushed the commit — update remote (⚠ rewrites history)

If that last commit is already on the remote branch, amending changes the commit hash, so you must force-push.

**Safer force push:**

```bash
git push --force-with-lease
```

Full flow:

```bash
git add -A
git commit --amend --no-edit
git push --force-with-lease
```

> `--force-with-lease` is safer than `--force` because it refuses to overwrite remote changes you don’t have locally.

***

## 4) You want to “merge” another branch’s changes into the last commit (squash-merge into current state)

If you want changes from another branch but still end up with **one updated last commit**:

### Option A — bring the branch in as a squash, then amend

```bash
git checkout your-branch
git fetch
git merge --squash other-branch
git commit --amend
```

### Option B — cherry-pick specific commits, then amend

```bash
git checkout your-branch
git cherry-pick <commit1> <commit2>
git commit --amend
```

(If conflicts happen, resolve them, then:)

```bash
git add -A
git cherry-pick --continue
git commit --amend
```

***

## 5) You made changes but don’t want to stage everything (interactive add)

```bash
git add -p
git commit --amend --no-edit
```

***

## 6) You forgot to include a *new untracked file* in the last commit

```bash
git add path/to/newfile
git commit --amend --no-edit
```

***

## 7) You want to combine *several* recent commits into the last one (squash via interactive rebase)

If it’s not just “add more changes”, but “I made 3 commits and want them as 1”:

```bash
git rebase -i HEAD~3
```

In the editor:

*   keep the top one as `pick`
*   change the others to `squash` (or `s`)

Then finish, and if already pushed:

```bash
git push --force-with-lease
```
