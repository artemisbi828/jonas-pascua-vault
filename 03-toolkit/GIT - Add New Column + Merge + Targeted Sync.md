1. make changes to database | view layer
2. git pull UAT
3. refresh semantic model locally
4. *optional* changes to [PBI Report Layer] 
5. git push UAT
6. test in UAT → approval
7. git UAT → PROD (add commit msg: merge)
8. PBI source control
9. refresh semantic model
10. refresh app (update app, if changes to [PBI Report Layer])

# Overwrite
***FORCE MERGE FROM UAT003.origin → UAT003.Local***
```
git fetch origin
git checkout UAT003
git reset --hard origin/UAT003
git clean -fd
```

***FORCE MERGE FROM PROD004.origin → UAT003.Local***
```
git fetch origin
git checkout UAT003
git reset --hard origin/PROD004
git push --force-with-lease origin UAT003
```

***TARGETED MERGE FROM PROD004.origin → UAT003.Local***
- Reminder: Push to UAT003.origin after

```
git switch UAT003
git fetch
git status

git reset --hard 
git clean -fd  

git restore --source PROD004 -- `
    Addons.Report `
    Addons.SemanticModel `
    Addons.pbip
```

***TARGETED MERGE FROM UAT003.origin → PROD004.Local***
- Reminder: Push to UAT003.origin after

```
git switch PROD004
git fetch
git status

git reset --hard 
git clean -fd  

git restore --source UAT003 -- `
    Discounts.Report `
    Discounts.SemanticModel `
    Discounts.pbip
```

---
# Hard Overwrite History
**NOTE: Cannot do this in AzureDEVOPS**
```
git checkout UAT003
git checkout -b UAT003 origin/U
git reset --hard origin/UAT003            # hard reset
git clean -fd                             # safety: remove untracked junk
git status

Sanity Check
git rev-parse HEAD
git rev-parse origin/UAT003
```