Need to find the [[GIT - Origin vs Main vs Master|origin]]?

```
# most common
git remote -v

# helpful in debugging auth issues
git remote -v --verbose 
git remote get-url origin

# {m} remotes? get list, then ask explicit
git remote
git remote get-url <remote-name>

# get exact from git.config files
git config --get remote.origin.url
```

# Get Branches
```bash
git branch -r
```
