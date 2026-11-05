2026-01-27 02:39 PM -- having trouble with SD Pulse

```bash
#midway in merge? abort 
`git merge --abort`

#force local to match remote
git fetch
git checkout branch-A
git reset --hard origin/branch-A

#merge locally then push
git checkout branch-A
git merge origin/prod
git push

# update all my remotes
git fetch --all

# prod to win all conflicts
git merge -X theirs origin/prod
git push
```