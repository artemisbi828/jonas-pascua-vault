```powershell

Get-Content resume.md | Select-Object -First 10

# go to dir, ";" → New Line, Get Content
cd C:\vsWorkspace\jpascua313\site\docs; Get-Content resume.md | Select-Object -First 10

# cat synonym method
cat C:\Users\jpasc\.ssh\id_ed25519.pub # alias: cat → get-content (ps defined)
```
