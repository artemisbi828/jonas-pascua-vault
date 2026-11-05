### Obsidian Cheat Sheet: M Date Conversions

Add these snippets to your vault to handle common formatting "headaches":

| **Target Format**    | **M Code Snippet**                              |
| -------------------- | ----------------------------------------------- |
| **Name to Number**   | `Date.Month(Date.FromText([MonthName] & " 1"))` |
| **Number to Name**   | `Date.MonthName(#date(2026, [MonthNum], 1))`    |
| **Leading Zero**     | `Text.PadStart(Text.From([Num]), 2, "0")`       |
| **Year from String** | `Text.Start([String], 4)`                       |