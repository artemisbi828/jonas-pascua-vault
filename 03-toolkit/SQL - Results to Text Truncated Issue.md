2026-01-12 05:24 PM

# Option 1: Results to Text (better for SSMS)

Press Ctrl+T (Query → Results To → Results to Text)
Tools → Options → Query Results → SQL Server → Results to Text
Set "Maximum number of characters displayed in each column" to 8192 (max allowed)
Click OK, close and reopen query window
Run query and save output

# Option 2: Export via BCP (best solution)
bcp "SELECT markdown_output FROM tempdb..#markdown_output" queryout "C:\vsWorkspace_SD\column_output.txt" -c -T -S YourServerName