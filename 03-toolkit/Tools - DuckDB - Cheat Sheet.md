```powershell
# initialize duckdb file `C:\Repos\sd-edw\project-ascend\semantic-register\semantic_register.duckdb`
duckdb semantic_register

```


# duckdb-cheatsheet.md — SQL Server to DuckDB Reference

For developers coming from a SQL Server background, here are the most common equivalents.

---

## SELECT Statements

| Operation | SQL Server | DuckDB |
|---|---|---|
| **Basic SELECT** | `SELECT * FROM log;` | `SELECT * FROM log;` |
| **With LIMIT** | `SELECT TOP 5 * FROM log;` | `SELECT * FROM log LIMIT 5;` |
| **Order DESC** | `SELECT * FROM log ORDER BY id DESC;` | `SELECT * FROM log ORDER BY id DESC;` |
| **WHERE clause** | `SELECT * FROM log WHERE class = 'todo';` | `SELECT * FROM log WHERE class = 'todo';` |
| **COUNT aggregate** | `SELECT COUNT(*) FROM log;` | `SELECT COUNT(*) FROM log;` |
| **GROUP BY** | `SELECT class, COUNT(*) FROM log GROUP BY class;` | `SELECT class, COUNT(*) FROM log GROUP BY class;` |
| **DISTINCT** | `SELECT DISTINCT class FROM log;` | `SELECT DISTINCT class FROM log;` |
| **JOIN** | `SELECT l.* FROM log l JOIN log_class c ON l.class = c.abbrev_input;` | `SELECT l.* FROM log l JOIN log_class c ON l.class = c.abbrev_input;` |

---

## DDL: Tables & Columns

| Operation | SQL Server | DuckDB |
|---|---|---|
| **Create table** | `CREATE TABLE log (id INT PRIMARY KEY, ts DATETIME, comment VARCHAR(MAX));` | `CREATE TABLE log (id INTEGER PRIMARY KEY, ts TIMESTAMPTZ, comment VARCHAR);` |
| **Add column (nullable)** | `ALTER TABLE log ADD notes VARCHAR(255) NULL;` | `ALTER TABLE log ADD COLUMN notes VARCHAR;` |
| **Add column (NOT NULL)** | `ALTER TABLE log ADD status VARCHAR(50) NOT NULL DEFAULT 'active';` | `ALTER TABLE log ADD COLUMN status VARCHAR DEFAULT 'active';` |
| **Add identity/auto-increment** | `ALTER TABLE log ADD id INT IDENTITY(1,1) PRIMARY KEY;` | `CREATE SEQUENCE seq_log_id START 1; ALTER TABLE log ADD COLUMN id INTEGER PRIMARY KEY DEFAULT nextval('seq_log_id');` |
| **Drop column** | `ALTER TABLE log DROP COLUMN notes;` | `ALTER TABLE log DROP COLUMN notes;` |
| **Rename column** | `EXEC sp_rename 'log.old_name', 'new_name';` | `ALTER TABLE log RENAME old_name TO new_name;` |
| **Drop table** | `DROP TABLE log;` | `DROP TABLE log;` |
| **Create index** | `CREATE INDEX idx_log_class ON log(class);` | `CREATE INDEX idx_log_class ON log(class);` |

---

## Data Manipulation

| Operation | SQL Server | DuckDB |
|---|---|---|
| **INSERT single row** | `INSERT INTO log (ts, comment) VALUES (GETDATE(), 'test');` | `INSERT INTO log (ts, comment) VALUES (now(), 'test');` |
| **INSERT multiple rows** | `INSERT INTO log VALUES (1, GETDATE(), 'comment1'), (2, GETDATE(), 'comment2');` | `INSERT INTO log VALUES (1, now(), 'comment1'), (2, now(), 'comment2');` |
| **UPDATE rows** | `UPDATE log SET comment = 'updated' WHERE id = 1;` | `UPDATE log SET comment = 'updated' WHERE id = 1;` |
| **DELETE by ID** | `DELETE FROM log WHERE id = 5;` | `DELETE FROM log WHERE id = 5;` |
| **DELETE all rows** | `DELETE FROM log;` | `DELETE FROM log;` |
| **TRUNCATE table** | `TRUNCATE TABLE log;` | `DELETE FROM log;` (or `TRUNCATE TABLE log;` if supported) |

---

## Data Types

| Concept | SQL Server | DuckDB |
|---|---|---|
| **String** | `VARCHAR(MAX)`, `VARCHAR(255)`, `NVARCHAR` | `VARCHAR` (no length limit needed) |
| **Integer** | `INT`, `BIGINT`, `SMALLINT` | `INTEGER`, `BIGINT`, `SMALLINT` |
| **Decimal** | `DECIMAL(10,2)`, `NUMERIC(10,2)` | `DECIMAL(10,2)` |
| **Boolean** | `BIT` (0 or 1) | `BOOLEAN` or `TINYINT` (0 or 1) |
| **Timestamp** | `DATETIME`, `DATETIME2`, `DATETIMEOFFSET` | `TIMESTAMP`, `TIMESTAMPTZ` |
| **Date only** | `DATE` | `DATE` |
| **Null check** | `IS NULL`, `IS NOT NULL` | `IS NULL`, `IS NOT NULL` |
| **CAST** | `CAST('123' AS INT)` | `CAST('123' AS INTEGER)` or `'123'::INTEGER` |

---

## Views

| Operation | SQL Server | DuckDB |
|---|---|---|
| **Create view** | `CREATE VIEW v_todo_logs AS SELECT * FROM log WHERE class = 'todo';` | `CREATE VIEW v_todo_logs AS SELECT * FROM log WHERE class = 'todo';` |
| **Query view (with LIMIT)** | `SELECT TOP 5 * FROM v_todo_logs;` | `SELECT * FROM v_todo_logs LIMIT 5;` |
| **Alter view** | `ALTER VIEW v_todo_logs AS SELECT id, comment FROM log WHERE class = 'todo';` | `CREATE OR REPLACE VIEW v_todo_logs AS SELECT id, comment FROM log WHERE class = 'todo';` |
| **Drop view** | `DROP VIEW v_todo_logs;` | `DROP VIEW v_todo_logs;` |

---

## Sequences (Auto-Increment)

| Operation | SQL Server | DuckDB |
|---|---|---|
| **Create identity column** | `CREATE TABLE t (id INT IDENTITY(1,1) PRIMARY KEY);` | `CREATE SEQUENCE seq_t START 1; CREATE TABLE t (id INTEGER PRIMARY KEY DEFAULT nextval('seq_t'));` |
| **Get next value** | `SELECT NEXT VALUE FOR seq_name;` | `SELECT nextval('seq_name');` |
| **Reset sequence** | `DBCC CHECKIDENT ('table_name', RESEED, 0);` | `ALTER SEQUENCE seq_name RESTART WITH 1;` |

---

## Functions & Operators

| Operation | SQL Server | DuckDB |
|---|---|---|
| **Current timestamp** | `GETDATE()` | `now()` or `CURRENT_TIMESTAMP` |
| **String length** | `LEN(string)` | `LENGTH(string)` |
| **Substring** | `SUBSTRING(string, 1, 5)` | `SUBSTRING(string, 1, 5)` |
| **UPPER/LOWER** | `UPPER(string)`, `LOWER(string)` | `UPPER(string)`, `LOWER(string)` |
| **String concat** | `CONCAT('a', 'b')` or `'a' + 'b'` | `'a' \|\| 'b'` or `CONCAT('a', 'b')` |
| **COALESCE** | `COALESCE(col1, col2, 'default')` | `COALESCE(col1, col2, 'default')` |
| **CASE** | `CASE WHEN x > 0 THEN 'pos' ELSE 'neg' END` | `CASE WHEN x > 0 THEN 'pos' ELSE 'neg' END` |

---

## Quick Examples: DuckDB with logger table

```sql
-- Select last 5 entries
SELECT * FROM log LIMIT 5;

-- Count entries by class
SELECT class, COUNT(*) as count FROM log GROUP BY class;

-- Find all personal entries
SELECT id, comment FROM log WHERE is_personal = 1;

-- Delete an entry by ID
DELETE FROM log WHERE id = 3;

-- Update an entry
UPDATE log SET comment = 'new comment' WHERE id = 2;

-- Create a view for TODOs
CREATE VIEW v_todos AS SELECT id, ts, comment FROM log WHERE class = 'todo';

-- Query the view (latest 5 TODOs)
SELECT * FROM v_todos ORDER BY ts DESC LIMIT 5;

-- Cast timestamp to DATE
SELECT CAST(ts AS DATE) FROM log;

-- String operations
SELECT 
    id,
    UPPER(comment) as comment_upper,
    LENGTH(comment) as comment_length
FROM log LIMIT 3;
```

---

## Key Differences

| Aspect | SQL Server | DuckDB |
|---|---|---|
| **Top N rows** | `SELECT TOP N` | `SELECT ... LIMIT N` |
| **Identity** | Built-in `IDENTITY(seed, increment)` | Manual `SEQUENCE` + `DEFAULT nextval()` |
| **Naming** | Often uses `dbo.` prefix | No schema prefix (flat structure) |
| **Casting** | `CAST(x AS INT)` | `CAST(x AS INTEGER)` or `x::INTEGER` |
| **Pipe operator** | No | `\|\|` for string concat |
| **Datetime NOW** | `GETDATE()` | `now()` or `CURRENT_TIMESTAMP` |

