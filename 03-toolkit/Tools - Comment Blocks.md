Powershell = `<# #>`
Python = `''' '''`

```table-of-contents
```

# Python Comment Block
use multi `#` or `'''` or `"""`

```
'''
this is a multi-line block
'''

"""
this 
is a 
multi-line block
"""


# this 
# is a 
# multi-line block
```



Since you’re planning to use **PowerShell** for your data cross-checking later, mastering comments is your first step toward making your scripts maintainable. PowerShell handles comments similarly to Python or Ruby, using the "hash" or "pound" symbol.

---
# Powershell Comment Block
### 1. Single-Line Comments


The `#` symbol tells PowerShell to ignore everything to its right on that specific line.

PowerShell

```
# This is a full-line comment describing the logic below
$ProjectScore = 85  # You can also add "inline" comments here
```

### 2. Multi-Line (Block) Comments

For longer explanations or "commenting out" chunks of code during testing, use the `<#` and `#>` markers.

PowerShell

```
<#
    SCRIPT: Calculate-ProjectMomentum.ps1
    AUTHOR: Gemini
    DATE: 2026-03-05
    DESCRIPTION: This block is great for header documentation 
    or explaining complex scoring logic.
#>
$TotalEffort = 120
```

---

### 3. Comment-Based Help (The "Pro" Way)

In PowerShell, if you place a block comment at the top of a script or function using specific keywords, PowerShell turns it into **official documentation**. This is how you "prep" your code for your future Android app's logic.

PowerShell

```
function Get-ProjectScore {
    <#
    .SYNOPSIS
        Calculates the completion score for a project.
    .PARAMETER ProjectPath
        The path to the Obsidian project note.
    .EXAMPLE
        Get-ProjectScore -ProjectPath "C:\Vault\ProjectA.md"
    #>
    param($ProjectPath)
    # Logic goes here...
}
```

_If you do this, you can run `Get-Help Get-ProjectScore` in your terminal and it will actually read back your comments as a manual._

---

### 4. Best Practices for your Obsidian CRM

When writing scripts to cross-check your **Obsidian logs**, use comments to define your "Data Schema":

- **Logic Breaks:** Use `# ----------------` to separate your file-parsing logic from your scoring math.
    
- **TODOs:** Use `# TODO: Implement Recency Decay` to mark features you haven't built yet.
    
- **The "Why" not the "How":** Don't comment `# Set X to 5`. Comment `# X is 5 because that is the baseline weight for Milestones.`
    

---

### 5. Quick Comparison: PowerShell vs. Other Languages

|**Type**|**PowerShell**|**JavaScript (DataviewJS)**|
|---|---|---|
|**Single Line**|`# Comment`|`// Comment`|
|**Block**|`<# ... #>`|`/* ... */`|

---

### Next Step

Since you’re looking at PowerShell for cross-checking, would you like a **starter script** that reads an Obsidian `.md` file and extracts all lines containing `CycleType:: #cycle/revert`?