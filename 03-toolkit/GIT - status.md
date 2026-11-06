

# Basic Concepts
1. Untracked Files: New from local (red)
2. Staged: Ready for snapshot --> Insert
3. Tracked: Previously committed or staged 
	- Unmodified: No Change
	- Modified: Changed | Updated

.gitignore -- untrack, ignore

## 1 Branch Ahead
Meaning: Your local is ahead vs remote (main / origin)

```
Your Local:     A -- B -- C -- D (your new commit)
GitHub Remote:  A -- B -- C
```

You need to stage commit (if haven't already) then 

```git
git push origin main
git push -u origin main               # if getting an error about upstream
```

## Sync Local to Remote
Renamed master to main
```bash
#rename from master → main
git branch -m master main

# Refresh your local list of remote branches
git fetch origin

# Link your local 'main' to the remote 'origin/main'
git branch -u origin/main main

git pull

# if you get this error from running git fetch origin
# git: 'credential-manager-core' is not a git command. See 'git --help'.
# run this
git config --global credential.helper manager
```

