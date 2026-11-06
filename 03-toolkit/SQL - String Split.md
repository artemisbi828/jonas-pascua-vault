---
definition:
---
table-valued function turning a string into a set of rows from 1) string 2) delimiter → explosion

Spawned from first last name partner addressing middle name issue like "Jon B Rutherford"

# Basic
```sql
SELECT value, ordinal FROM STRING_SPLIT('Amy Beth Cortinas', ' ', 1);
```

# Example
```sql
use Lake;
go

declare @input_name table (input_id int primary key identity(1, 1), input_name sysname);

insert into @input_name (input_name) values ('Cortinas'), ('Nicole B Alonzo'), ('Georgia Cole'), ('Laurel Speedy');

-- 
select * from @input_name as ina;
-- splits names that have spaces into separate row (explosion)
-- 2 standard outputs: "value, ordinal"
-- use count to get total parts --> how many words per row (part vs whole)
-- if position and total position BEQ 1 --> first name (w integrity check that it has to have 2 names at least)
-- if position EQ total position --> last name, even if there is only 1 word
-- perform implosion using max(case when)

select
    *
from @input_name as ina
    cross apply (
    -- block start 
    select
        max(case when ordinal = 1 and total_parts > 1 then inr.value end) first_name,
        max(case when ordinal = total_parts then inr.value end) last_name
    from (
    -- block end 
        select
            value,
            ordinal,
            count(*) over () as total_parts
        from string_split(trim(ina.input_name), ' ', 1)
    ) as inr
) v;

```
### 1. The "Empty" `OVER()`

When you use `COUNT(*) OVER()`, you are using a **Window Function** instead of an **Aggregate Function**.

- **Standard `COUNT(*)`:** Requires a `GROUP BY`. It collapses all rows into one.
    
- **Window `COUNT(*) OVER()`:** Does _not_ collapse rows. It calculates the count for the entire result set of that specific subquery and "appends" it to every single row.
    

In our case, the STRING_SPLIT function creates a tiny temporary table for one name at a time (because it's inside a CROSS APPLY).

If the name is "Georgia Beth Cole", STRING_SPLIT produces 3 rows. The COUNT(*) OVER() sees those 3 rows and puts the number "3" on every row.

|**Value**|**Ordinal**|**Count(*) OVER() (Total_Parts)**|
|---|---|---|
|Georgia|1|3|
|Beth|2|3|
|Cole|3|3|

Because `CROSS APPLY` executes this logic _for each row_ of `@input_name` independently, the window is naturally limited to just that name. You don't need `PARTITION BY input_id` because the subquery only "sees" the name it is currently splitting.

---

### 2. Why `MAX` works without `GROUP BY`

You correctly noted that `MAX()` usually requires a `GROUP BY`. However, in this refactor, it works because of the **Logical Processing Order** of the `CROSS APPLY`.

When we write:

SQL

```
CROSS APPLY (
    SELECT 
        MAX(CASE WHEN s.ordinal = 1 ... END) AS fname,
        MAX(CASE WHEN s.ordinal = s.total_parts ... END) AS lname
    FROM (...) AS s
) AS V
```

We are treating the `CROSS APPLY` like a **Scalar Subquery**.

1. The `FROM` clause inside the apply generates the 3 rows for "Georgia Beth Cole".
    
2. The `SELECT` with `MAX` aggregates those 3 rows down into **one single row** containing two columns (`fname`, `lname`).
    
3. Because the `SELECT` is aggregating _everything_ produced by that specific `STRING_SPLIT`, the "Group" is implicitly the entire set of words for that one name.
    

If we didn't use `MAX`, the `CROSS APPLY` would return 3 rows for Georgia (one for each word), which would cause your `@input_name` table to duplicate records. `MAX` acts as a "filter/collector" to ensure only one row comes back out of the split logic.

---

### 3. Efficiency: Why this is better than `PARTITION BY`

If we had used `PARTITION BY input_id` inside the `OVER()` clause, the SQL Optimizer would have to:

1. Split _all_ names for the whole table.
    
2. Sort the entire result set by `input_id`.
    
3. Calculate the counts.
    

By keeping the `OVER()` empty inside the `CROSS APPLY`, the Optimizer can use a **Nested Loop**. It picks up one name, splits it in memory, identifies the first/last parts, and moves to the next. This is significantly faster for smaller batches and uses much less memory "buffer" space because it never has to sort a giant list of split words.

---

### Summary Table

|**Technique**|**Role in your Query**|**Benefit**|
|---|---|---|
|**`OVER()` (Empty)**|Counts words for the _current_ name only.|No expensive sorting or partitioning required.|
|**`MAX` (No Group By)**|Collapses split words into a single `fname`/`lname` pair.|Prevents row duplication in the final update.|
|**`CROSS APPLY`**|Creates a local scope for the split functions.|Keeps string logic isolated from the main table join.|

**Would you like me to show you how to use this same `OVER()` technique to identify and remove duplicate names from your `@input_name` table before you even try to match them?**