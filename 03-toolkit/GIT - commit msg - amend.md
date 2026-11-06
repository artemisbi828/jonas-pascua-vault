***EDIT COMMIT MSG***
```
git add -A
git commit --amend
```


```
git add infra/modules/azure_key_vault/outputs.tf
git commit --amend --no-edit
git push --force-with-lease
```

---
#status/deferred/quick-paste-merge-later 
Good question. **Yes, you can combine them.** It depends on whether you've already pushed:

---

## If you haven't pushed yet

Use `git commit --amend` to add these changes to your previous commit:

```powershell
git add infra/modules/azure_key_vault/outputs.tf
git commit --amend --no-edit
```

The `--no-edit` flag keeps the same commit message. Your previous commit now includes both the Key Vault policy changes AND the EOF/line ending fixes.

Then push normally:

```powershell
git push
```

---

## If you already pushed to the PR

You can still amend, but it requires a force-push (which rewrites history):

```powershell
git add infra/modules/azure_key_vault/outputs.tf
git commit --amend --no-edit
git push --force-with-lease
```

**`--force-with-lease` is safe** — it's the "safe force push" for PRs. It updates your PR automatically without losing anything.

---

## Best practice

**Combine them into one commit.** Why?

- They're both part of the same logical change (implementing Key Vault policy)
- Keeps the PR history clean — one commit = one change story
- Cleaner git log later

So use the `git commit --amend` approach (with or without `--force-with-lease` depending on whether you've pushed).

**Check your PR status first:**

```powershell
git log --oneline -5
```

If your previous commit is there and already pushed (you'll see it in GitHub), then use `--force-with-lease`. If you're not sure, it's safe to use anyway — it won't hurt.