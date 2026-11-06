
```table-of-contents
```
# Reset
```
# Reset UAT003.local to UAT003.origin 
git reset --hard origin/UAT003 

# nuclear (incoming wins)
git checkout --theirs .

# stage changes
git add -A

# commit + define message
git commit -m "Merge PROD004 into UAT003 (prefer PROD on conflicts)"

```

## Regular Merge Prefer Incoming
```
# prefer theirs
git merge origin/PROD004
```

---
### Safe Version of Reset
Reset UAT003.local to UAT003.origin  + *Precisely define source and target*

```
git fetch origin --prune
git checkout UAT003
git reset --hard origin/UAT003          # discards local changes (tracked files) 

# Removes untracked files/dirs (be careful)
git clean -fd
```

#### Safety Checks
```
# See if you're mid-merge/mid-rebase
git status

# Abort a merge if one is in progress
git merge --abort

# Abort a rebase if one is in progress
git rebase --abort

# If cherry-pick in progress
git cherry-pick --abort

# If revert in progress
git revert --abort

```

---
## Oops Commands
```shell

#discard all local changes (DANGER)
git reset --hard HEAD 

# messed up file and want to revert to last commit
git checkout -- filename.js

# undo last commit (but keep changes in file)
git reset --soft HEAD~l

```

```shell

git fetch origin
git reset --hard origin/deploy/vercel  #force sync to remote (cloned local); 
# alias → git reset --hard HEAD

git stash push -u -m "feat: add custom message"  ## -- u = untracked, m = msg

# save work temporarility to switch branches, get work back, drop it
git stash 
git stash pop
git stash drop


```