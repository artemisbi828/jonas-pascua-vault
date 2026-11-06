Updated todo list

For the file you’re viewing, open a terminal in `data-platform` and run:

```powershell
git blame -- sqlmesh/models/gold/facts/contract_fields/_contract_field__acv_denominator_contract_starts.sql
```

That shows the commit author and commit for each line’s latest change. To check the file’s commit history:

```powershell
git log --follow --format="%h %an <%ae> %ad %s" --date=short -- sqlmesh/models/gold/facts/contract_fields/_contract_field__acv_denominator_contract_starts.sql
```

In VS Code, right-click the file in Explorer and choose **Open Timeline**. Select a commit to inspect its details and changes. The built-in Timeline is good for file history; `git blame` is better for seeing who last changed particular lines.