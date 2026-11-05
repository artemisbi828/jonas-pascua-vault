Use `git checkout -b`
# TL;DR
*   **`git checkout`** = one command that does *branch switching + file restoring + detached HEAD*
*   **`git switch`** = branch switching only
*   **`git restore`** = file restoration only

So: **`switch` is clearer because it makes your intent unambiguous.**

`git switch` is dedicated to **branch switching**.

✅ Switch to a branch:

```bash
git switch UAT003
```

✅ Create and switch:

```bash
git switch -c feature/foo
```

✅ Switch to a remote-tracking branch by creating a local branch:

```bash
git switch -c UAT003 origin/UAT003
```

That’s basically it. If you see `git switch`, you immediately know: **this is about branches.**

`checkout` is a *Swiss Army knife*: useful, but it’s easy to read a command and not immediately know which “mode” it’s in—especially in scripts or when reviewing someone else’s commands.

---

## Why `git checkout` can be confusing

Historically, `git checkout` does **multiple different things** depending on how you call it:

1.  **Switch branches**

```bash
git checkout UAT003
```

2.  **Create and switch to a new branch**

```bash
git checkout -b feature/foo
```

3.  **Check out a file (or folder) from another commit/branch**

```bash
git checkout origin/PROD004 -- SMEX.Report
```

4.  **Detach HEAD (check out a commit directly)**

```bash
git checkout <commit-sha>
```

So 

***

## What `git restore` does (and only does)

Likewise, `git restore` is dedicated to **restoring file contents** (either from HEAD, from the index, or from another commit/branch).

✅ Restore from another branch:

```bash
git restore --source=origin/PROD004 -- SMEX.Report
```

✅ Discard local edits in a file (restore from HEAD):

```bash
git restore -- SMEX.Report/somefile.json
```

So `switch` + `restore` makes intent obvious:

*   **switch** = branches
*   **restore** = files

***

## Why this matters for *your* use case (PROD → UAT overwrite)

You’re doing both operations:

1.  **Move yourself onto UAT003**
2.  **Overwrite certain paths with PROD004**

Using the newer verbs makes the script self-documenting:

```bash
git switch UAT003
git restore --source=origin/PROD004 -- SMEX.Report SMEX.SemanticModel SMEX.pbip
```

Compared to `checkout`, which could mean either branch switching or file checkout depending on args.

***

## Practical benefits (beyond readability)

### 1) Fewer accidental “file checkout” vs “branch checkout” mistakes

With `checkout`, one typo can change meaning. For example, if a path matches a branch name or vice versa, you can get surprising results. `switch` removes that ambiguity.

### 2) Better mental model for teams

When someone skims a PR description or runbook:

*   `switch` reads as “branch move”
*   `restore` reads as “overwrite files”

Less “wait—what is this doing again?”

### 3) Matches Git’s modern guidance

Git has been steering users toward these commands as clearer alternatives. (You’ll see hints in Git output in many setups.)

***

## When you *still* might use `git checkout`

`checkout` isn’t “bad”—it’s just overloaded. You might still use it if:

*   you’re on an older Git version that doesn’t support `switch/restore`
*   you have muscle memory and you’re confident
*   you’re doing something quick in a local terminal and don’t care about readability

But for scripts, runbooks, team docs, and repeatable deployment steps, `switch/restore` tends to be safer and clearer.
