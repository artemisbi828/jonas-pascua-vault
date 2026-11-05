**closing vsc**: Last instance will be the first instance when open

# Restart after Path
When adding to [PATH], here are the steps, restarting tool.vsc is important

```
# adding git bash to path
Windows Search -> Edit environment variables for your account
Edit User PATH
Add:
C:\Program Files\Git\bin
C:\Program Files\Git\usr\bin
Close all terminals and VS Code
Reopen and test:
bash --version
```