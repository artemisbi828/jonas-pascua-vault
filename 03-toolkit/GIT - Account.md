```
jonas.pascua@artemisbi.com
artemisbi828
```

new: https://github.com/artemisbi828/artemis-hub
old:https://github.com/artemisBI/artemis-hub

```
git remote set-url origin https://github.com/artemisbi828/artemis-hub
gh auth login
  follow prompts
  login using https UI
  save code --> use the code given in CLI (vscode)
  (may need to validate via email first)
  enter into browser to confirm it's the right device
git push -u origin main



# old notes
On sd, open your repo host settings.
Create a new Personal Access Token (or equivalent) with minimal scopes needed for repo read/write.
On psnl, clone/pull using HTTPS and use that token as password.
Save credentials in Git Credential Manager on psnl.
Revoke old/unused tokens.
  

```
