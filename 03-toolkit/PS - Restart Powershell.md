## How to restart PowerShell

Just close the terminal window and open a new one. For VS Code specifically:

1. Click the trash icon on the terminal panel to kill the current session
2. Press `` Ctrl+` `` to open a fresh terminal

That's it — no reboot needed for this registry change, just a new terminal session.

Then in the fresh terminal:

```powershell
cd C:\Repos\data-platform
$env:Path = "C:\Users\jonas-adam.pascua\.local\bin;$env:Path"
uv run pre-commit run --all-files
```