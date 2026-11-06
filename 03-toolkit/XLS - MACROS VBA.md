


> [!steps]
> 1. **Enable Developer Tab** (if not visible):
>     
>     - Right-click on any ribbon tab → `Customize the Ribbon`
>     - Check the box for `Main Tabs: Developer` on the right side
>     - Click `OK`
> 2. **Record Macro:**
>     
>     - Click `Developer` tab
>     - Click `Record Macro` button
>     - Store macro in: `Personal Macro Workbook`
>     - Click `OK`
>     - Immediately click `Stop Recording` (same button)
> 
> 3. Press `ALT + F11` (VBA Editor)
> 4. In the menu: `File` → `Import File...`
> 5. Or just go to `Insert` → `Module` in any workbook
> 6. Paste the VBA code
> 7. Press `ALT + F8` to assign CTRL+T
> 
> Now assign it to CTRL+Shift+T:
> 
> 8. Press `ALT + F8`
> 9. Select `CreateTableWithNullCleanup`
> 10. Click `Options`
> 11. Shortcut key: `t`
> 12. Click `OK`

---
# Create Table With Null Cleanup
Need macro for local key binding.

## Adapted
2026-02-05 10:00 AM
```
Sub CreateTableWithNullCleanup()

' Keyboard Shortcut: Ctrl+Shift+T

    Dim ws As Worksheet
    Dim rng As Range
    Dim cur As Range
    Dim tbl As ListObject
    
    ' Use current selection
    Set ws = ActiveSheet
    Set rng = ActiveCell
    Set cur = rng.CurrentRegion
    Set rng = Intersect(ws.UsedRange, cur)
    
    
    ' Replace "NULL" with empty strings in selection
    rng.Replace What:="NULL", Replacement:="", LookAt:=xlWhole, _
        SearchOrder:=xlByRows, MatchCase:=False, SearchFormat:=False, _
        ReplaceFormat:=False
    
    ' Create table with headers (xlYes = first row is header)
    On Error Resume Next
    Set tbl = ActiveSheet.ListObjects.Add(xlSrcRange, rng, , xlYes)
    On Error GoTo 0
    tbl.Range.Columns.AutoFit
    
    ' Optional: Apply a table style
    If Not tbl Is Nothing Then
        tbl.TableStyle = "TableStyleMedium6"
    End If
End Sub

```
## Old
```
Sub CreateTableWithNullCleanup()
    Dim rng As Range
    Dim tbl As ListObject
    
    ' Use current selection
    Set rng = Selection
    
    ' Replace "NULL" with empty strings in selection
    rng.Replace What:="NULL", Replacement:="", LookAt:=xlWhole, _
        SearchOrder:=xlByRows, MatchCase:=False, SearchFormat:=False, _
        ReplaceFormat:=False
    
    ' Create table with headers (xlYes = first row is header)
    On Error Resume Next
    Set tbl = ActiveSheet.ListObjects.Add(xlSrcRange, rng, , xlYes)
    On Error GoTo 0
    
    ' Optional: Apply a table style
    If Not tbl Is Nothing Then
        tbl.TableStyle = "TableStyleMedium2"
    End If
End Sub
```

Suggested for Copilot
```

Sub CreateTableWithNullCleanup()
' Keyboard Shortcut: Ctrl+Shift+T

    Dim ws As Worksheet
    Dim target As Range
    Dim rng As Range
    Dim tbl As ListObject
    Dim hadTable As Boolean
    
    Set ws = ActiveSheet
    Set target = ActiveCell

    
    If target Is Nothing Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    
    On Error GoTo CleanFail
    
    ' If we're already inside a table, use that table's full range.
    If Not target.ListObject Is Nothing Then
        Set rng = target.ListObject.Range
        hadTable = True
    Else
        ' Emulate Ctrl+T selection: current cell's rectangular block
        ' Use UsedRange to avoid selecting entire sheet when data is sparse
        Dim cur As Range
        Set cur = target.CurrentRegion
        Set rng = Intersect(ws.UsedRange, cur)
        
        ' Fallback if Intersect returns Nothing (rare)
        If rng Is Nothing Then Set rng = cur
    End If
    
    ' If range is empty, bail out gracefully
    If WorksheetFunction.CountA(rng) = 0 Then
        MsgBox "No data found in the current region.", vbExclamation, "Create Table"
        GoTo CleanExit
    End If
    
    ' Cleanup: replace "NULL" (case-insensitive) with empty string in the chosen range
    rng.Replace What:="NULL", Replacement:="", LookAt:=xlWhole, _
                SearchOrder:=xlByRows, MatchCase:=False, SearchFormat:=False, _
                ReplaceFormat:=False
    
    ' Create table only if we weren't already in one
    If Not hadTable Then
        ' Assume first row is header (same as Ctrl+T default when it detects headers).
        ' Change xlYes to xlNo if you know the first row is data.
        On Error Resume Next
        Set tbl = ws.ListObjects.Add(xlSrcRange:=rng, XlListObjectHasHeaders:=xlYes)
        On Error GoTo 0
    Else
        Set tbl = target.ListObject
    End If
    
    If Not tbl Is Nothing Then
        ' Optional: style + autofit
        tbl.TableStyle = "TableStyleMedium2"
        tbl.Range.Columns.AutoFit
        ' Select the table for convenience
        tbl.Range.Select
    ElseIf Not hadTable Then
        MsgBox "Could not create a table from the selected region.", vbExclamation, "Create Table"
    End If

CleanExit:
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    Exit Sub

CleanFail:
    ' Basic error handler
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    MsgBox "An error occurred: " & Err.Description, vbExclamation, "Create Table"
End Sub

```

Recorded Macro 
```
Sub create_table()
'
' create_table Macro
'
' Keyboard Shortcut: Ctrl+Shift+T
'
    ActiveSheet.ListObjects.Add(xlSrcRange, Range("$C$9:$D$17"), , xlYes).Name = _
        "Table6"
    Range("D15").Select
    ActiveCell.FormulaR1C1 = "Null"
    Range("Table6").Select
    Range("D16").Activate
    Selection.Replace What:="NULL", Replacement:="", LookAt:=xlPart, _
        SearchOrder:=xlByRows, MatchCase:=False, SearchFormat:=False, _
        ReplaceFormat:=False, FormulaVersion:=xlReplaceFormula2
End Sub

```