Replace column based on another column → eg clean up YYYYMM_Sort due to Current = non distinct columns
- Right-click the `YYYYMM_Sort` column.
- Select **Replace Values**.
- Type anything (e.g., `find` and `replace`) and click OK. This generates the step template.
- In the **Formula Bar**, replace the generated code with this:

```
Table.ReplaceValue(#"Previous Step Name",  qeach [YYYYMM_Sort], each if [YearMonth_Current] = "Current Month" then "2999 01" else [YYYYMM_Sort], Replacer.ReplaceValue, {"YYYYMM_Sort"})
```