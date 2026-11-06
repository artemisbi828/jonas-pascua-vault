Power Query can absolutely do a SQL‑style **ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)** — it just takes a couple of steps because M doesn’t have a built‑in window function.

The pattern is solid and works every time.

---

# ⭐ SQL Equivalent  
```sql
ROW_NUMBER() OVER (PARTITION BY Column ORDER BY Column2)
```

---

# ⭐ Power Query Equivalent (clean, reliable)

### **Step 1 — Sort the table**
You must sort first, because the row numbers will follow this order.

```m
#"Sorted Rows" =
    Table.Sort(
        #"Previous Step",
        {{"Column", Order.Ascending}, {"Column2", Order.Ascending}}
    )
```

---

### **Step 2 — Group by the partition column**
Inside each group, add an index starting at 1.

```m
#"Grouped" =
    Table.Group(
        #"Sorted Rows",
        {"Column"},   // partition key
        {
            {
                "Data",
                each Table.AddIndexColumn(_, "RowNum", 1, 1),
                type table
            }
        }
    )
```

---

### **Step 3 — Expand back out**
This returns your original rows plus the row number.

```m
#"Expanded" =
    Table.ExpandTableColumn(
        #"Grouped",
        "Data",
        Table.ColumnNames(#"Sorted Rows") & {"RowNum"}
    )
```

---

# ⭐ Final Output  
You now have a column **RowNum** that behaves exactly like SQL’s:

- Partitioned by `[Column]`
- Ordered by `[Column2]`
- Starting at 1 for each group

---

# ⭐ Full combined M code (copy/paste ready)

```m
let
    Source = #"Previous Step",

    // 1. Sort by partition + order columns
    Sorted = Table.Sort(Source,
        {{"Column", Order.Ascending}, {"Column2", Order.Ascending}}
    ),

    // 2. Group and add index inside each group
    Grouped = Table.Group(
        Sorted,
        {"Column"},
        {
            {
                "Data",
                each Table.AddIndexColumn(_, "RowNum", 1, 1),
                type table
            }
        }
    ),

    // 3. Expand back out
    Expanded = Table.ExpandTableColumn(
        Grouped,
        "Data",
        Table.ColumnNames(Sorted) & {"RowNum"}
    )
in
    Expanded
```

---

# 🎯 **Reusable Power Query Function: fnRowNumber**

```m
// fnRowNumber
(table as table, partitionCols as list, orderCols as list, optional startAt as number) as table =>
let
    Start = if startAt <> null then startAt else 1,

    // 1. Sort by the order columns
    Sorted =
        Table.Sort(
            table,
            List.Transform(orderCols, each {_, Order.Ascending})
        ),

    // 2. Group by the partition columns
    Grouped =
        Table.Group(
            Sorted,
            partitionCols,
            {
                {
                    "Data",
                    each Table.AddIndexColumn(_, "RowNum", Start, 1),
                    type table
                }
            }
        ),

    // 3. Expand back out
    Expanded =
        Table.ExpandTableColumn(
            Grouped,
            "Data",
            Table.ColumnNames(Sorted) & {"RowNum"}
        )
in
    Expanded
```

---

# 🧠 How to use it

After you paste the function into **Home → Advanced Editor**, you can call it like this:

```m
= fnRowNumber(
    #"Previous Step",
    {"Brand"},          // partition by Brand
    {"Date"},           // order by Date
    1                   // optional: starting index
)
```

Or a more complex example:

```m
= fnRowNumber(
    #"Previous Step",
    {"Manufacturer", "Brand"},   // multi-column partition
    {"CreatedAt", "Amount"},     // multi-column order
    1
)
```

---

# 🎯 Why this function is solid

- Works with **any number of partition columns**
- Works with **any number of order columns**
- Lets you choose the **starting index**
- Produces a deterministic, SQL‑style row number
- Plays nicely with your ingestion pipeline and grouping logic

---

Yes — the function I gave you **is** a Power Query **user‑defined function (UDF)**.

In Power Query terms, a UDF is simply:

- A named `let … in …` expression
- Stored in the Queries pane
- Accepting parameters
- Returning a table, list, record, or value

The function you asked for fits that definition perfectly.

---

# 🧩 Why it counts as a UDF

The moment you paste something like this:

```m
(table as table, partitionCols as list, orderCols as list, optional startAt as number) as table =>
let
    ...
in
    Expanded
```

into a **blank query**, give it a name (e.g., `fnRowNumber`), and save it — you’ve created a reusable function.

You can now call it from any other query:

```m
= fnRowNumber(#"Previous Step", {"Brand"}, {"Date"}, 1)
```

That’s exactly how Power Query UDFs are designed to work.

---

# 🧠 Quick mental model

Think of it like:

- SQL: a stored procedure or table‑valued function
- Python: a reusable function in a module
- Power Query: a named query that takes parameters

Same concept, different syntax.

---

If you want, I can help you build a **library** of reusable M functions — row numbering, ranking, deduping, text cleanup, ingestion helpers — so your pipeline becomes modular and maintainable.