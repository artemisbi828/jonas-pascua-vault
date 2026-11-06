Syncs

```
# UAT --> PROD
git switch UAT003
git pull  # or pull

# wipe any possible local changes
git reset --hard 
git clean -fd  

# target sync
git restore --source PROD004 -- `
    PLATINUM DATASET 2.0.Report `
    PLATINUM DATASET 2.0.SemanticModel `
    PLATINUM DATASET 2.0.pbip
```