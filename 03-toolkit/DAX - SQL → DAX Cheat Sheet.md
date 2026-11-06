
```
NPS Score = IFERROR(DIVIDE(
	SUM(F_OfficeMonthStats[NPSscoreNumerator]), SUM(F_OfficeMonthStats[NPSscoreDenominator]))
	, BLANK()
	)
```

---

# 🧠 DAX Query Cheat Sheet (for SQL Users)

## 1. Basic "SELECT *"

In DAX, you don't select a whole table with a wildcard; you simply evaluate the table name.

| SQL | DAX Query |
| --- | --- |
| `SELECT * FROM Dates` | `EVALUATE 'Date'` |

---

## 2. SELECT Specific Columns

Use `SELECTCOLUMNS` to pick specific fields and rename them if desired.

**SQL:**

```sql
SELECT DateKey, YearMonth FROM Dates

```

**DAX:**

```dax
EVALUATE
SELECTCOLUMNS(
    'Date',
    "Date Key", 'Date'[DateKey],
    "Month Name", 'Date'[YearMonth]
)

```

---

## 3. SELECT DISTINCT

Use `DISTINCT` or `VALUES`. `VALUES` is usually preferred as it respects the data model relationships.

**SQL:**

```sql
SELECT DISTINCT YearMonth FROM Dates

```

**DAX:**

```dax
EVALUATE
DISTINCT('Date'[YearMonth])

```

---

## 4. WHERE (Filtering)

Use `FILTER` for complex logic or `CALCULATETABLE` for high performance.

**SQL:**

```sql
SELECT * FROM Dates WHERE YYYY = 2026

```

**DAX:**

```dax
EVALUATE
FILTER(
    'Date',
    'Date'[YYYY] = 2026
)

```

---

## 5. GROUP BY (Aggregation)

`SUMMARIZECOLUMNS` is the gold standard for grouping. It is essentially your `SELECT...GROUP BY` statement.

**SQL:**

```sql
SELECT YearMonth, SUM(Sales) as TotalSales 
FROM Sales 
GROUP BY YearMonth

```

**DAX:**

```dax
EVALUATE
SUMMARIZECOLUMNS(
    'Date'[YearMonth],
    "TotalSales", SUM('Sales'[Amount])
)

```

---

## 6. TOP N & ORDER BY

Use `TOPN` for the limit and `ORDER BY` at the very end of the script.

**SQL:**

```sql
SELECT TOP 10 * FROM Dates ORDER BY DateKey DESC

```

**DAX:**

```dax
EVALUATE
TOPN(10, 'Date', 'Date'[DateKey], DESC)
ORDER BY 'Date'[DateKey] DESC

```

---

## 7. JOINS

In Power BI, joins are usually handled by the **Model Relationships**, so you don't have to write them. However, if you need to force a join in a query:

| SQL Join Type | DAX Equivalent |
| --- | --- |
| **Inner Join** | `NATURALINNERJOIN(T1, T2)` |
| **Left Join** | `NATURALLEFTOUTERJOIN(T1, T2)` |
| **Cross Join** | `CROSSJOIN(T1, T2)` |

---

## 8. Variable Logic (The "WITH" Clause)

Just like a SQL CTE (Common Table Expression), you can use `VAR` to define temporary tables.

**DAX:**

```dax
DEFINE
    VAR TrailingMonthly = 
        FILTER('Date', 'Date'[IsTrailingMonthly] = 1)

EVALUATE
    SUMMARIZECOLUMNS(
        TrailingMonthly[YearMonth],
        "Standard Work Days", SUM(TrailingMonthly[WDE_DayWeight])
    )

```

---

### ⚠️ Common SQL-to-DAX Pitfalls

1. **The Trailing Comma:** Like Power Query, DAX is sensitive to commas. In `SUMMARIZECOLUMNS`, every pair of `"Name", Expression` must be separated by a comma, but the last one shouldn't have a trailing one.
2. **Evaluation Order:** `EVALUATE` always comes first, but `ORDER BY` always comes last (outside the main function).
3. **Table vs. Scalar:** SQL treats almost everything as a table. DAX distinguishes between a **Table** (multiple rows/cols) and a **Scalar** (a single number like `SUM`). You cannot `EVALUATE` a sum directly; you must wrap it in a table constructor like `{ SUM(...) }`.

**Would you like me to create a specific DAX query for you that calculates your "Normalized Sales per Office" so you can test it in the Query View right now?**