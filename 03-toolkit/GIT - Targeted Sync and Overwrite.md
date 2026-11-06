Syncs 3 files; Hard Overwrite

- [[#QuickStart|QuickStart]]
- [[#1. Switch into target branch|1. Switch into target branch]]
- [[#2. Discard pending commits|2. Discard pending commits]]
- [[#3. Hard Overwrite|3. Hard Overwrite]]
- [[#Supplemental|Supplemental]]
	- [[#Supplemental#Old Version|Old Version]]
- [[#Git Stash|Git Stash]]

# QuickStart
```bash
-- # UAT --> PROD
git switch UAT003
git fetch
git status

git reset --hard 
git clean -fd  

git restore --source PROD004 -- `
	MarketingFieldReporting.Report `
	MarketingFieldReporting.SemanticModel `
	MarketingFieldReporting.pbip
```

# 1. Switch into target branch
```bash
-- # UAT --> PROD
git switch PROD004
git fetch
git status
```

# 2. Discard pending commits
 .
Deletes all untracked files (local PBIP artifacts)
```bash
-- # UAT --> PROD
git reset --hard   # Deletes all uncommitted changes.
git clean -fd  # Deletes all untracked files (local PBIP artifacts
```

# 3. Hard Overwrite
```bash
git restore --source MFRV2 -- \
	MarketingFieldReporting.Report \
	MarketingFieldReporting.SemanticModel \
	MarketingFieldReporting.pbip
```

# Supplemental

## Old Version
```bash
-- # UAT --> PROD
git switch PROD004
git fetch
git status

git reset --hard
git clean -fd

git checkout origin/UAT003 -- SMEX.Report SMEX.SemanticModel SMEX.pbip

-- # PROD --> UAT
git switch UAT003
git fetch origin
git status

git reset --hard
git clean -fd

git checkout origin/PROD004 -- SMEX.Report SMEX.SemanticModel SMEX.pbip

#3: review the diffs, have those files stagged
#4: commit them
```

# Git Stash
```shell
git stash push -u -m "WIP before bringing files from MFRV2"
git diff --stat  # inspect changes
git diff # see everything different and brought in 

# same as commit and sync
git add MarketingFieldReporting.Report MarketingFieldReporting.SemanticModel MarketingFieldReporting.pbip
git commit -m "Bring PBIP artifacts from MFRV2 (selective rollback/fix)
```


---
Git interprets this as:

1. **`origin/UAT004`** → “Look at this branch/tree-ish for the source version”
2. **`--`** → “Everything after this is a path in the working tree”
3. **`RFR.Report`** → “This is the path _in my repo_, not on my filesystem”

Git then:

- Looks inside the **tree object** for `origin/UAT004`
- Finds the file or folder `RFR.Report` _in that branch’s tree_
- Copies that version into your working directory
- Stages it for commit

At no point does Git care about your Windows absolute path.
Git is path‑agnostic to your OS. It only understands the **repo’s internal directory structure**.

---

# 🧩 Why Git “knows” the remote version

Because Git stores the entire file tree of every commit and branch inside the `.git` directory.

When you say:

```
git checkout origin/UAT004 -- RFR.Report
```

Git doesn’t go to the remote server.  
It simply:

- Looks at the **tree object** for `origin/UAT004` (which you fetched earlier)
- Finds the file inside that tree
- Writes it into your working directory

Git’s object database already contains the full snapshot of that branch.