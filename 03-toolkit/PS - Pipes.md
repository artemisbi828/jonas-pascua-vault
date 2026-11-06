
PowerShell | Pipe

- The pipe passes objects (not plain text) from the left command into the right command, one at a time.
- Each object flows through the pipeline; the receiving command can act on each object as it arrives (streaming).

  
Key concepts (concise)

- Objects, not text: PowerShell commands emit .NET objects. The next command receives those objects and can access their properties/methods.
- Streaming: pipeline items are processed as they are produced (memory‑efficient, responsive).
- Automatic variable: inside ForEach-Object or Where-Object use $_ or $PSItem to refer to the current piped object.
- Parameter binding:

  - ValueFromPipeline: a command parameter can accept the entire object.
  - ValueFromPipelineByPropertyName: a parameter can bind to a property of the object when names match.


Common patterns (examples)

````powershell

# list files, filter by size, show Name and Length

Get-ChildItem -File |
  Where-Object { $_.Length -gt 1MB } |
  Select-Object Name, Length |
  Format-Table -AutoSize

# transform each item (use ForEach-Object)

Get-ChildItem -File |
  ForEach-Object { "File: $($_.Name) ($($_.Length) bytes)" }

# use property binding: Import-Csv emits objects with columns as properties

Import-Csv data.csv |
  ForEach-Object { Rename-Item -Path $_.Path -NewName ("prefix_" + $_.Name) -WhatIf }
````



Practical tips

- Use Get-Member to inspect what objects in the pipeline expose:

````powershell
Get-ChildItem | Get-Member
````

- To discard output use Out-Null:

````powershell
Some-Command | Out-Null
````

- To see text output instead of objects, pipe to Out-String:

````powershell
Get-Process | Out-String
````

- For complex per-item logic prefer ForEach-Object (in-pipeline) or collect into an array then use foreach (outside pipeline) depending on readability and need for streaming.

  

When to use pipeline vs foreach loop

- Pipeline / ForEach-Object: good for streaming, chaining small transforms/filters.
- foreach ($x in $collection): useful when you need the full collection first or easier imperative logic.

  

If you want, I can show a short demo script comparing ForEach-Object vs foreach to illustrate streaming and timing.