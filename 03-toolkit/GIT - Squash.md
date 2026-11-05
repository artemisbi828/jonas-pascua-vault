In VS Code, "merging" multiple commits into a single one is technically called a **Squash**. There are two ways to do this: using the built-in Git interface (easiest) or using the Terminal.

### Method 1: The "Git Graph" or Built-in UI (Easiest)

If you are on a modern version of VS Code, you can do this through the **Source Control** side panel:

1. Click the **Source Control** icon (or `Ctrl + Shift + G`).
2. Look for the **"Commits"** section in the sidebar.
3. Select the multiple commits you want to combine (hold `Ctrl` and click them).
4. **Right-click** on the selected commits and select **Squash Commits**.
5. VS Code will ask you for a new commit message for the combined block. Enter it and hit **Enter**.

---

### Method 2: Interactive Rebase (Most Control)

This is the "standard" developer way to do it. It allows you to pick exactly which commits to keep and which to "squash" into the previous ones.

1. Open the **Terminal** in VS Code (`Ctrl + ` ` `).
2. Type the following command (replace `3` with the number of commits you want to merge):
`git rebase -i HEAD~3`
3. An editor window will open showing a list of your last 3 commits. Each line starts with the word `pick`.
4. Leave the **top** commit as `pick`.
5. Change the word `pick` to **`squash`** (or just **`s`**) for all the commits below it that you want to merge into the first one.
6. **Save** the file (`Ctrl + S`) and **Close** the tab (`Ctrl + W`).
7. A second window will open. Delete the old messages and type the **new** single message for your merged commit.
8. Save and close that tab too.

---

### Method 3: "Soft Reset" (The "Clean Slate" Method)

If you have 5 messy commits and just want them all to become one single new commit:

1. In the terminal, type:
`git reset --soft HEAD~5`
*(This removes the 5 commits but **keeps all your code changes** as "staged" files).*
2. Go to the **Source Control** tab.
3. Type a fresh commit message and click **Commit**.

---

### Comparison of Methods

| Method | Best For... |
| --- | --- |
| **UI Squash** | Quick fixes and beginners. |
| **Interactive Rebase** | Selecting specific commits in a long history to merge. |
| **Soft Reset** | Collapsing everything you did today into one "final" commit. |

> [!WARNING]
> **Important:** Only squash commits that you have **not yet pushed** to a shared repository (like GitHub). Squashing changes the Git history, which can cause "Conflicts" for other team members if they have already pulled the old commits.

Would you like me to show you how to **undo** a squash if you accidentally merge the wrong commits?