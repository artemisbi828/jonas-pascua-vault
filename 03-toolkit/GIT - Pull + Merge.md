# Main Commands
```git
# 
git switch main
git reset --hard origin/main
git status -sb

# if switch main doesn't exist locally
git switch --track -c main origin/main
git status-sb
```



Merge `PROD004` → `UAT003` and bias to `PROD004`

```shell
git fetch origin
git checkout UAT003
git merge origin/PROD004
git push origin UAT003
git merge -X theirs origin/PROD004
```

## Setup Git; Pull Remote

```shell
# go to path
cd path/to/your/repo

# optional to remove local changes (untracked)
git clean -fd

# force merge
git pull origin main
git fetch -p #prune deleted remote branches (keeps local list clean)
```
