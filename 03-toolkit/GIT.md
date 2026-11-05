---
related_to:
  - "[CI/CD]"
---
# Current Commands
[[GIT - Cheat Sheet]]

```
# most common
git checkout <br-name>
git pull
<make changes>
git add .
git commit -m "removed comments"

git status
git remote --v
git branch -r

                     
```

[[GIT - Config for SD + Artemis ]]
[[GIT - Authorship]]
# Git Setup + Basics
[[GIT - Pull + Merge]]
[[GIT - See + Delete Local Branches]]

[[GIT - High Level Overview]]
[[GIT - Ignore vs Exclude]]
[[GIT - Cancel or Undo]]
[[GIT - status]]
[[GIT - init or clone]]
[[Git - Discard Changes]]
[[GIT - checkout vs switch]]
[[GIT - commit msg - amend]]
[[GIT - Stage + Commit]]
[[GIT - Amend Commit]]



[[GIT - Origin vs Main vs Master]]
[[GIT - Get Origin URL + Branches]]

[[GIT - Oops - Reset + Merge Branch]]
[[GIT - Add New Column + Merge + Targeted Sync]]

[[GIT - Find File]]
[[Git - Check Config Globals]]
[[Git - Rename master → main]]
[[GIT - Squash]]
[[GIT - Amend]]
[[GIT - Fix Local Branch A vs Prod]]
[[GIT - Head]]
[[GIT - Targeted Sync and Overwrite]]

Look for .msi → windows 
[GPG - Commit Signing - Setup Guide]
# Error Handling
[[GIT - Error Handling - Stuck in VS Termainl]]
[[GIT - Error Handling - Remote Not Found]]
[[GIT - Error Handling - Table Compatibility Issue]]

# Advanced
[[GIT - GitHub Actions]]

# Accounts
[[GIT - Account]]


## Git UI Changes
1. setup as private
2. Settings >> Rename default branch >> main
3. Settings >> Danger Zone >> Disable Branch Protection


## Normal 

```git

git branch
git branch -a ## see all branches(local, local-current, remote) → white, green, red
git branch --show-current
git checkout -b feature/name-of-task    #switch branch

# see uncommitted
git status

# commit and stage 
git add .                                
git add filename.md
git commit -m "Add commit cmment name"

# fetch all branches and PRs from remote (soft)
git fetch origin  ## soft get
git merge

# fetch + merge all at once
git pull origin

# make sure local-main is same as remote-main
git checkout main
git pull origin main                     

# list all branches to find the pr we want
git branch -r
git checkout pr-branch-name
```

## Delete remote
```git
git push origin ## --> delete deploy/vercel
git branch -D deploy/vercel ## --> delete local
```

## Overwrite Remote
```shell

git push -u origin main --force
git push -u origin MYBRANCHNAME
git log ## history of commits

```

# Reviewing a PR
VS Code's built-in Source Control panel (Ctrl+Shift+G) to review changes visually.

```git
# fetch branch from origin
git fetch origin feature/ARed/initial-setup
git checkout feature/ARed/initial-setup

# See diffs; 
git log origin/main..HEAD
git diff origin/main

# Test the code
bash scripts/run_all.sh
```


# Navigating in Git Diff
Stuck in the terminal pager? 
```
# exit
Press: q
```

## Navigation While Viewing:

- `Space` or `Page Down` - Next page
- `b` or `Page Up` - Previous page
- `↓` or `Enter` - Next line
- `↑` - Previous line
- `g` - Go to beginning
- `G` - Go to end
- `/search-term` - Search forward
- `q` - **Quit/Exit**

## To See All Diffs at Once (No Pager):

```powershell

# Disable pager for one command
git --no-pager diff origin/main

# Or disable globally (not recommended)
git config --global core.pager cat

# Better: Use a nicer pager
git config --global core.pager "less -FRX"

```

## Pro Tip - View Diff in VS Code:

```powershell

# Much easier to review!
git difftool origin/main

```



# Supplementals
### Branch vs Fork
Branch -- for internal dev: clone within same repository, created by user w/ `write access` to repo
Fork -- for external dev: complete copy of entire repository, created by someone w/o `write access` to repo

### Main vs Head
Head -- alias usually points to main 
Main -- actual main w latest committed code


### View Log History

```bash

    git log --oneline --graph --all --decorate

```


# 🧠 **Mental Model: Git as a Database of Snapshots**

Think of Git as a **content‑addressed database** that stores:

- **Commits** → pointers to trees
- **Trees** → folder structures
- **Blobs** → file contents

Every branch is just a pointer to a commit.  
Every commit is a snapshot of your entire repo.

So Git doesn’t store “diffs” — it stores **full directory trees**.

---

# 🌳 **Visual Model: A Commit Is a Tree**

Imagine your repo like this:

```
Commit (hash)
│
└── Tree (root)
    ├── Tree: RFR.Report
    │     ├── Blob: file1.cs
    │     ├── Blob: file2.cs
    │     └── Blob: config.json
    ├── Tree: src
    ├── Tree: scripts
    └── Blob: README.md
```

Each folder is a **tree object**.  
Each file is a **blob object**.

Git stores these objects in `.git/objects/`.

---

# 🔍 **What happens when you run:**

```bash
git checkout origin/UAT004 -- RFR.Report
```

Break it down:

### 1. `origin/UAT004`

Git resolves this to a **commit hash**.

### 2. That commit hash points to a **tree** (the root directory snapshot).

### 3. Git walks that tree to find the **subtree** named `RFR.Report`.

### 4. Git copies the blobs and subtrees from that commit into your working directory.

### 5. Git stages them.

At no point does Git look at your Windows filesystem path.  
It only looks inside the **tree object** for that commit.

---

# 🧩 **Why absolute paths don’t work**

When you typed:

```
git checkout origin/UAT004 -- C:\Users\jonas-adam.pascua\Source\Repos\Pulse\RFR.Report
```

Git tried to interpret:

- `C:\Users\...` as a **repo-relative path**
- But no commit tree contains a folder named `C:\Users\...`
- So Git says “invalid reference”

Git only understands paths **inside the repo tree**, not OS paths.

---

# 🧠 **Mental Model Summary**

Here’s the model that makes everything click:

### ✔ Git stores _snapshots_, not diffs

Each branch is a pointer to a full directory tree.

### ✔ `git checkout <branch> -- <path>`

means:  
**“Take the version of `<path>` from `<branch>`’s tree and write it into my working directory.”**

### ✔ The path is always repo-relative

Git never uses OS paths to locate files in commits.

### ✔ Git already has the full snapshot locally

Because `git fetch` downloaded all the tree objects.

---

# 🎯 Why this model is powerful

Once you internalize this, you can do things like:

- Pull a single file from any commit
- Restore a folder from yesterday
- Compare trees between branches
- Cherry-pick only specific paths
- Build partial merges safely

All without ever doing a full merge.

---

If you want, I can draw the same model but showing **two branches side-by-side** so you can visualize exactly how Git copies only the subtree you request.