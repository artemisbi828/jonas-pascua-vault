- Remove brackets
- Top 5 → Limit 5
- TO_DATE(TO_VARCHAR(), 'YYYYMMDD')
- ISNULL() → NVL()

# Snowflake SQL 
```sql
-- DateKey
TO_VARCHAR(TO_DATE(TO_VARCHAR(D_DATE_KEY), 'YYYYMMDD'), 'YYYY-MM-DD')

-- 
DATE_TRUNC('MONTH', TRY_TO_DATE(D_DATE_KEY::VARCHAR, 'YYYYMMDD')) AS month_star

-- # reverse for WHERE statement
TO_NUMBER(TO_CHAR(CURRENT_DATE(), 'YYYYMMDD')

-- # regrain
cast(cast(date as char(16)) as date) → DATE_TRUNC('MONTH', date as char(16)))
```

# MSSQL
```sql
set tran isolation level read uncommitted;
use EDW_PROD_SNOWFLAKE;

select top 5
       loc.LOCATION_NAME,
       cast(cast(trans.D_TRANSACTION_DATE_KEY as char(8)) as date) as transDate,
       cast(cast(trans.[D_TRANSACTION_POSTED_DATE_KEY] as char(8)) as date) as transDatePosted,
       sum(trans.TOTAL_DUE_AMOUNT) TOTAL_DUE_AMOUNT
from [EDW_PROD_SNOWFLAKE].[EDW].[F_TRANSACTION] trans
    inner join [EDW_PROD_SNOWFLAKE].[EDW].[D_TRANSACTION_TYPE] ttyp
        on ttyp.D_TRANSACTION_TYPE_KEY = trans.D_TRANSACTION_TYPE_KEY
       and ttyp.SOURCESYSTEMID = trans.SOURCE_SYSTEM_ID
    inner join [EDW_PROD_SNOWFLAKE].[EDW].[D_LOCATION] loc
        on loc.D_LOCATION_KEY = trans.D_LOCATION_ASSIGNED_KEY
where 1 = 1
  and trans.[TOTAL_DUE_AMOUNT] <> 0
  and loc.[CLOUD9_CONVERSION_DATE] >= '20240101'
  and trans.D_TRANSACTION_DATE_KEY >= '20240101'
  and trans.D_TRANSACTION_DATE_KEY <= '20250930'
  and trans.D_TRANSACTION_POSTED_DATE_KEY >= '20240101'
  and trans.D_TRANSACTION_POSTED_DATE_KEY <= '20251001'
  and cast(cast(trans.D_TRANSACTION_DATE_KEY as char(8)) as date) >= loc.[CLOUD9_CONVERSION_DATE]
  and cast(cast(trans.D_TRANSACTION_DATE_KEY as char(8)) as date) <= eomonth(loc.[CLOUD9_CONVERSION_DATE])
--and ttyp.[DESCRIPTION] not like '%[*]%' ESCAPE '\'
--and lower(ttyp.COMMENT) not like ('%balance converted%')
--and lower(ttyp.COMMENT) not like ('%converted balance%')
--and loc.FAS_IN_ORTHOFI<>'true'
--and loc.LOCATION_NAME = 'Hendersonville - Blythe'

group by loc.LOCATION_NAME,
         cast(cast(trans.D_TRANSACTION_DATE_KEY as char(8)) as date),
         cast(trans.[D_TRANSACTION_POSTED_DATE_KEY] as char(8));

```
# Snowflake
```sql

USE DATABASE EDW_PROD_SNOWFLAKE;
USE SCHEMA EDW;

SELECT
    loc.LOCATION_NAME,
    TO_DATE(TO_VARCHAR(trans.D_TRANSACTION_DATE_KEY), 'YYYYMMDD')          AS transDate,
    TO_DATE(TO_VARCHAR(trans.D_TRANSACTION_POSTED_DATE_KEY), 'YYYYMMDD')   AS transDatePosted,
    SUM(trans.TOTAL_DUE_AMOUNT) AS TOTAL_DUE_AMOUNT
FROM EDW_PROD.EDW.F_TRANSACTION trans
INNER JOIN EDW_PROD.EDW.D_TRANSACTION_TYPE ttyp
    ON ttyp.D_TRANSACTION_TYPE_KEY = trans.D_TRANSACTION_TYPE_KEY
   AND ttyp.SOURCESYSTEMID = trans.SOURCE_SYSTEM_ID
INNER JOIN EDW_PROD.EDW.D_LOCATION loc
    ON loc.D_LOCATION_KEY = trans.D_LOCATION_ASSIGNED_KEY
WHERE 1 = 1
  AND trans.TOTAL_DUE_AMOUNT <> 0
  AND loc.CLOUD9_CONVERSION_DATE >= '2024-01-01'
  AND trans.D_TRANSACTION_DATE_KEY     >= '20240101'
  AND trans.D_TRANSACTION_DATE_KEY     <= '20250930'
  AND trans.D_TRANSACTION_POSTED_DATE_KEY >= '20240101'
  AND trans.D_TRANSACTION_POSTED_DATE_KEY <= '20251001'
  AND TO_DATE(TO_VARCHAR(trans.D_TRANSACTION_DATE_KEY), 'YYYYMMDD')
        >= loc.CLOUD9_CONVERSION_DATE
  AND TO_DATE(TO_VARCHAR(trans.D_TRANSACTION_DATE_KEY), 'YYYYMMDD')
        <= LAST_DAY(loc.CLOUD9_CONVERSION_DATE)
GROUP BY
    loc.LOCATION_NAME,
    TO_DATE(TO_VARCHAR(trans.D_TRANSACTION_DATE_KEY), 'YYYYMMDD'),
    TO_DATE(TO_VARCHAR(trans.D_TRANSACTION_POSTED_DATE_KEY), 'YYYYMMDD')
LIMIT 5;
```

# Bugs

Can't parse '0' as date with format 'YYYYMMDD'

```sql
TO_DATE() → TRY_TO_DATE()
```


---
#status/deferred/quick-paste-merge-later 
Snowflake isn’t **T‑SQL** (SQL Server’s dialect), so the variable syntax is a bit different depending on **where** you’re writing code:

*   **Snowflake Scripting** (stored procedures / anonymous blocks): supports local variables with `DECLARE …` and assignment with `LET` (or `:=`).
*   **Session variables** (works in worksheets/scripts): use `SET` and reference with `$var`.
*   **SQL variables inside a single SELECT**: use CTEs/`VALUES` or `QUALIFY` patterns instead of variables.

Below are the common Snowflake patterns with examples.

***

## 1) Session variables (most common in ad-hoc SQL)

### Declare / assign

```sql
SET start_date = '2026-01-01'::DATE;
SET min_amount = 1000;
SET region = 'SOUTH';
```

### Use (reference with `$`)

```sql
SELECT *
FROM sales
WHERE sale_date >= $start_date
  AND amount >= $min_amount
  AND region = $region;
```

### Reassign

```sql
SET min_amount = 2500;
```

### Show what’s set (handy for debugging)

```sql
SHOW VARIABLES;
```

**Notes**

*   Session variables live for your **session** (connection/worksheet tab).
*   They are substituted before execution, so types can matter—cast if needed (`::DATE`, `::NUMBER`, etc.).

***

## 2) Snowflake Scripting variables (procedural code)

Use this for multi-statement logic, loops, IF/ELSE, exception handling, etc.

### Anonymous block example

```sql
BEGIN
  DECLARE v_start_date DATE DEFAULT '2026-01-01';
  DECLARE v_total NUMBER(38,2);
  DECLARE v_region STRING DEFAULT 'SOUTH';

  LET v_total := (
    SELECT COALESCE(SUM(amount), 0)
    FROM sales
    WHERE sale_date >= v_start_date
      AND region = v_region
  );

  RETURN v_total;
END;
```

### Key syntax points

*   **Declare:** `DECLARE var_name TYPE [DEFAULT expr];`
*   **Assign:** `LET var_name := expr;` (you’ll also see `var_name := expr;` in some contexts)
*   **Use:** reference by name directly inside the block (`v_start_date`), **not** with `$`.

### IF / loop example

```sql
BEGIN
  DECLARE v_i INT DEFAULT 1;
  DECLARE v_max INT DEFAULT 5;

  WHILE (v_i <= v_max) DO
    INSERT INTO log_table(msg) VALUES ('Iteration ' || v_i);
    LET v_i := v_i + 1;
  END WHILE;

  RETURN 'done';
END;
```

***

## 3) Using variables in dynamic SQL (EXECUTE IMMEDIATE)

Sometimes you need variables to build object names, optional filters, etc.

### With session variables

```sql
SET tgt_table = 'SALES_2026';

EXECUTE IMMEDIATE
  'SELECT COUNT(*) FROM ' || $tgt_table;
```

### With scripting variables (inside BEGIN…END)

```sql
BEGIN
  DECLARE v_table STRING DEFAULT 'SALES_2026';
  DECLARE v_sql   STRING;

  LET v_sql := 'SELECT COUNT(*) FROM ' || v_table;

  EXECUTE IMMEDIATE v_sql;
END;
```

> Tip: For values (not identifiers), prefer **bind variables** in `EXECUTE IMMEDIATE` when possible, to avoid quoting issues and improve safety.

***

## 4) “Variable-like” patterns inside a single query (CTE/VALUES)

If you only need a constant once and don’t want session variables:

```sql
WITH params AS (
  SELECT
    '2026-01-01'::DATE AS start_date,
    1000::NUMBER      AS min_amount
)
SELECT s.*
FROM sales s
CROSS JOIN params p
WHERE s.sale_date >= p.start_date
  AND s.amount >= p.min_amount;
```

***

## 5) Quick mapping from SQL Server T‑SQL → Snowflake

### T‑SQL

```sql
DECLARE @x INT = 5;
SELECT @x + 1;
```

### Snowflake (session variable)

```sql
SET x = 5;
SELECT $x + 1;
```

### Snowflake (scripting)

```sql
BEGIN
  DECLARE x INT DEFAULT 5;
  RETURN x + 1;
END;
```

***

## Common gotchas

*   **`$var` is for session variables only.** Inside scripting blocks, use the variable name directly.
*   **Object names** (schema/table/column) can’t be parameterized in normal SQL—use `EXECUTE IMMEDIATE` to build identifiers.
*   If you see errors like “invalid identifier `$var`”, you’re likely mixing scripting variables and session variables.

***

## What are you trying to do?

If you tell me your specific scenario (e.g., *dynamic table name*, *date range parameters*, *stored procedure*, *multi-step ETL script*), I can show the cleanest Snowflake pattern for it and help convert your existing T‑SQL snippet.
