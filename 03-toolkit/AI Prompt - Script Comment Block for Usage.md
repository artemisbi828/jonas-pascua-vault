**Role:** Technical Prompt Engineer specializing in high-fidelity requirement extraction.
**Task:** Create a usage block on how to run the script with a synopsis, description, parameters, and an example for each invocation pattern / call pattern.
**Tone:** Clinical, zero-fluff; no validating phrases or conversational filler.
**Clarify:** If there are ambiguities, address via a numbered list before providing solutions so I can manually address before you generate output.

# Example:

```
<#
.SYNOPSIS
Compares two directory trees and prints relative paths that exist only in one side.

.DESCRIPTION
Builds relative-path sets from two roots, then uses Compare-Object to show deltas.
By default, only directories are compared so the output is concise and easier to review.

.PARAMETER PathA
First root path to compare.

.PARAMETER PathB
Second root path to compare.

.PARAMETER FilesOnly
If provided, compares only files and ignores directories.

.PARAMETER AllItems
If provided, compares both files and directories.

.EXAMPLE
.\ps-compare-filepath-delta.ps1 -PathA "C:\vsWorkspace_SD\4 - builds" -PathB "C:\vsWorkspace_SD\4 -builds"

.EXAMPLE
.\ps-compare-filepath-delta.ps1 -PathA "D:\FolderA" -PathB "D:\FolderB" -FilesOnly

.EXAMPLE
.\ps-compare-filepath-delta.ps1 -PathA "D:\FolderA" -PathB "D:\FolderB" -AllItems

.NOTES
Default mode is directory comparison for duplicate-check workflows.
#>
```