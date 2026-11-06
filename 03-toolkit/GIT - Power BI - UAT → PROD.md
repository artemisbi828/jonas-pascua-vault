# QuickStart
```bash
# UAT --> PROD
git switch PROD004
git fetch # or pull
git status

git reset --hard 
git clean -fd  

git restore --source UAT003 -- `
    Addons.Report `
    Addons.SemanticModel `
    Addons.pbip
```
