Related To: [[DAX]], [[PBI]]


[[DAXM - Date Conversions]]
[[DAXM - Create Table Variable]]
[[DAXM - String Split]]
[[DAXM - Split Cell into 2 separate Rows]]
[[DAXM - Create D_Dates_Dynamic]]
[[DAXM - Create RN like TSQL]]

# Modeling
[[DAXM - Create D_Dates]]
[[DAXM - Create F_LY_DateKeyLY]]
[[DAXM - Add Custom Case When Column From Another Column]]


# Dax Sanitization
[[DAXM - Replace Value]]
[[DAXM - Remove Repeating Words]]
[DAXM - ISNULL() Columns]
[[DAXM - Data Sanitization]]
# What?
[[DAXM - PromoteHeaders]]


---
# CHEAT SHEET
Power Query’s language (M) is a **functional language**. Unlike SQL (which is declarative) or Python (which is procedural), M is essentially one long list of instructions where each step depends on the one before it.

If you understand **Excel Formulas** or **JSON**, you are actually halfway there. Here is your cheat sheet to mastering the structure and logic of M.

---

> [!tip] Let ... in → declare variable block

### 1. The Anatomy of an M Script

Every M script is wrapped in a `let ... in` block. Think of it as: **"Let these variables exist... and then show me the last one."**



Code snippet

```
let
    StepName1 = SourceData,
    StepName2 = Table.SelectColumns(StepName1, {"Column1"}),
    StepName3 = Table.Distinct(StepName2)
in
    StepName3
```

- **The Commas:** Every line must end in a comma **except** for the very last step before the `in` keyword. This is the #1 cause of syntax errors.
    
- **The References:** Notice how `StepName2` refers to `StepName1`. This creates a chain. If you break the chain, the code fails.
    
- **Case Sensitivity:** M is strictly case-sensitive. `table.selectcolumns` will fail; it must be `Table.SelectColumns`.
    

---

### 2. Common Structural "Pitfalls"

|**Pitfall**|**Why it happens**|**The "Fix"**|
|---|---|---|
|**The "Missing Link"**|You added a step manually but forgot to update the next line to reference it.|Ensure each line's first argument is the name of the previous line.|
|**Spaces in Names**|M allows spaces in step names, but they require `#""` syntax.|Instead of `#"Added Custom"`, rename steps to `AddedCustom` to keep the code clean.|
|**Lazy Typing**|Power Query "guesses" types, often adding unnecessary `Changed Type` steps.|Delete auto-generated type steps and cast types inside your functions (like we did with `type date`).|
|**The "Trailing Comma"**|Adding a comma to the last step before `in`.|Always check the line immediately above `in`. It must be "clean."|

---

### 3. Understanding the "Each" and "_" Shortcuts

This is usually the most confusing part for beginners.

- **`each`**: This is a shorthand for "for every row in this table."
    
- **`_` (The Underscore)**: This represents "the current row/item we are looking at right now."
    

Example:

Table.TransformColumns(Source, {"Price", each _ * 1.1})

> _Translation: Take the Price column, and for **each** cell, take the **current value** and multiply by 1.1._

---

### 4. M-Query "Cheat Sheet" for Daily Use

#### Handling Tables

- **`Table.SelectColumns(Table, {"Col1", "Col2"})`** → Like `SELECT Col1, Col2` in SQL.
    
- **`Table.SelectRows(Table, each [Status] = "Active")`** → Like `WHERE Status = 'Active'` in SQL.
    
- **`Table.RenameColumns(Table, {{"Old", "New"}})`** → Like `AS` in SQL.
    

#### Handling Dates (Critical for your project)

- **`Date.From(DateTime.LocalNow())`** → Gives you "Today."
    
- **`Date.AddDays(SomeDate, 7)`** → Adds days.
    
- **`Date.StartOfMonth(SomeDate)`** → Useful for normalizing to the 1st of the month.
    

---

### 5. Pro Advice for Moving Forward

#### Tip 1: Use the "Formula Bar"

Don't always open the Advanced Editor. Turn on the Formula Bar (**View > Formula Bar**). It shows you the specific M code for the step you are currently clicked on. It’s the best way to learn the syntax incrementally.

#### Tip 2: Think in "Nested Records"

When you see `[DateKey = "2026-01-01"]`, that is a **Record**. When you see `{1, 2, 3}`, that is a **List**. M is almost entirely built on nesting Lists inside Records and vice-versa.

#### Tip 3: "DRY" with Variable References

If you have a server name used in 5 different queries, don't type it 5 times. Create a "Blank Query," name it ServerName, and just type "ARTEMIS" in the formula bar. Now, in your SQL strings, you can use:

Sql.Database(ServerName, "NVS", ...)

---

### Next Step for You

To get comfortable, try converting your manual "Change Type" steps into the integrated `type date` syntax inside `Table.TransformColumns` as we discussed. It’s the best "Level 2" exercise for an M-Query learner.

**Would you like me to take one of your existing complex M scripts and add "Comments" (using `//`) to every single line to explain exactly what the M-engine is doing?**
