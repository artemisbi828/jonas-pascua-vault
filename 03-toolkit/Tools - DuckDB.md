[[Tools - DuckDB UI]]
# Alter Tables
```sql
ALTER TABLE log
ALTER COLUMN created_at SET DEFAULT current_timestamp;

SET VARIABLE user_name = 'jpascua';
INSERT INTO log (
    comment,
    created_by
)
VALUES (
    'Testing',
    getvariable('user_name')
);

```

---

* **`Ctrl + U`**: Wipes out everything on the current line to the left of your cursor.
* **`.timer on`**: See query speed
* **`.tables`**: Shows a quick list of tables you've created.

* **`Ctrl + C`**: If you get stuck in a multi-line query (where hitting Enter just keeps giving you a `...> ` prompt because you forgot a semicolon), hitting `Ctrl + C` will cancel the current line entirely and give you a fresh, clean `D ` prompt.
* **`Ctrl + L`**: clear terminal (.clear --> didn't work)
	* Ctrl + Break
	* Ctrl + F2 / Cmd + F2

--- 
- **`.shell cls`** (and hit Enter)
* **`.help`**: Shows all available configuration options.
* **`.schema iris`**: Shows the exact SQL blueprint used to build the `iris` table.
* **`.exit`**: Safely closes DuckDB and returns you to your normal Windows prompt.


> **How it works:** The dot-command `.shell` tells DuckDB to temporarily pass a command directly to Windows. `cls` is the standard Windows command to clear the host screen.

SQL Server
├─ Server
├─ Database
└─ Connection String

DuckDB
├─ No server
├─ No listener
├─ No port
└─ Database = a local file

---
```sql
-- ============================================================================
-- SETUP
-- ============================================================================ 
PS Terminal: `winget duckdb cli` (if not already installed)
  to verify --> `Get-Command duckdb`
  
# find where it''s installed
where.exe duckdb

-- ============================================================================
-- START
-- ============================================================================ 
# to get into the database file, vs transient database
`duckdb sd_edw.duckdb` --> sd_edw D

# check database
SELECT current_database();

# see schemas
`show schemas;`

# create schemas
`create schema dim;`

# check tables
select * from information_schema.tables

# get table
select * from dim.date limit 200;

-- ============================================================================
-- BUILD THE DATE DIMENSION (CALCULATED INSTANTLY, NO LOOPS)
-- ============================================================================ 
CREATE TABLE IF NOT EXISTS dim.DATES AS 
WITH raw_dates AS (
    SELECT CAST(generate_series AS DATE) AS d
    FROM generate_series(DATE '2023-01-01', DATE '2039-12-31', INTERVAL '1 day')
)
SELECT
    d AS DateKey,
    extract('dayofyear' FROM d) AS DayOfYear,
    extract('day' FROM d) AS DayOfMonth,
    dayname(d) AS DayName,
    CAST(dayname(d) AS VARCHAR)[1:3] AS DayNameAbbrev,
    extract('dow' FROM d) AS DayOfWeek,
    extract('week' FROM d) AS WeekOfYear,
    date_trunc('month', d)::DATE AS MonthKey,
    extract('month' FROM d) AS Month,
    monthname(d) AS MonthName,
    CAST(monthname(d) AS VARCHAR)[1:3] AS MonthNameAbbrev,
    extract('year' FROM d) AS YYYY,
    strftime(d, '%Y%m') AS YYYYMM,
    strftime(d, '%Y %b') AS YearMonth,
    extract('quarter' FROM d) AS Quarter,
    last_day(d) AS EndOfMonth,
    make_date(extract('year' FROM d)::INT, 12, 31) AS EndOfYear
FROM raw_dates;
-- ============================================================================
-- RENAMES
-- ============================================================================ 
memory D ALTER TABLE dim."DATES" RENAME TO dates;
memory D ALTER TABLE dim.DATES RENAME TO date;
-- ============================================================================
-- SEARCH FOR A TABLE BY NAME
-- ============================================================================ 
SELECT table_schema, table_name 
FROM information_schema.tables 
WHERE table_name ILIKE '%dates%';
-- ============================================================================
-- INSERT HEADING HERE - NPE ADDED METRIC - SELF-CONTAINED VALIDATION QUERY
-- ============================================================================ 
substr(dayname(d), 1, 3) AS DayNameAbbrev,
-- ...
substr(monthname(d), 1, 3) AS MonthNameAbbrev,
-- vs -- 
CAST(dayname(d) AS VARCHAR)[1:3] AS DayNameAbbrev,
-- ...
CAST(monthname(d) AS VARCHAR)[1:3] AS MonthNameAbbrev,
```


---

## 2. Basic Exercises to Explore DuckDB

Now that you know how to navigate the interface, try running these 4 quick exercises to see what makes DuckDB special compared to older databases.

Make sure to run **`.timer on`** first so you can see how blindingly fast it is!

### Exercise A: Query a File Directly (No Import Needed)

DuckDB doesn't require you to "load" data into a database to look at it. If you have a CSV file on your computer, you can query it right off your hard drive.

Type this (replace the path with a real CSV file if you have one, or use this public URL to fetch data over the internet instantly!):

```sql
SELECT * FROM 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv' LIMIT 5;

```

*Yes, DuckDB just reached out to GitHub, read the CSV, parsed it, and formatted it as a table in milliseconds.*

### Exercise B: Auto-Generate a Table

Don't want to type out a full `CREATE TABLE` schema? You can create a permanent table inside DuckDB *directly from* that internet CSV file:

```sql
CREATE TABLE iris AS SELECT * FROM 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv';

```

### Exercise C: Use the `SUMMARIZE` Magic

Now that you have the `iris` table created locally, let's see how DuckDB inspects data structure. Instead of writing a dozen lines of code to get averages, minimums, and data types, just type:

```sql
SUMMARIZE iris;

```

You will get a beautifully formatted grid showing mathematical diagnostics for every single column in the dataset.

### Exercise D: Change the Output View

If a table has too many columns and wraps ugly on your screen, you can change how DuckDB prints data.

* To view data like a spreadsheet grid (Default): **`.mode box`**
* To view data like a JSON document: **`.mode json`**
* To view data as a vertical list (great for wide tables): **`.mode line`**

Try running `.mode line` and then `SELECT * FROM iris LIMIT 1;` to see the difference!

---
Coming from an MS SQL Server background, you are actually in a fantastic position to understand DuckDB, but you have to completely flip some of your mental models about how a database behaves.

Let's break down your questions and rewire that SQL Server brain for DuckDB.

## 1. Does DuckDB run on Bash?

**Yes, absolutely.** Because DuckDB is just a single executable file (`duckdb.exe` on Windows, or just `duckdb` on Linux/Mac), it can run inside **any** command-line interpreter.

- On Windows, it runs inside **Command Prompt** or **PowerShell**.
    
- On Linux, macOS, or Windows Subsystem for Linux (WSL), it runs seamlessly inside **Bash** or **Zsh**.
    

If you were on a Linux machine right now using Bash, you would just type `./duckdb` in your terminal, and you would see the exact same `D` prompt you are looking at right now on Windows. The experience is identical across all operating systems.

## 2. DuckDB vs. MS SQL Server: Shifting Your Mental Model

To expand your mental understanding, let's map what you know from MS SQL Server to how DuckDB operates. There are three massive conceptual differences:

### A. The "Server" vs. The "Library"

- **MS SQL Server:** It is a massive, always-running background Windows Service (`sqlservr.exe`). It listens on a network port (usually 1433), manages its own memory pool, and forces you to connect to it via a client like SSMS (SQL Server Management Studio).
    
- **DuckDB:** There is **no server process**. When you run `duckdb.exe`, the database engine spins up _inside_ that specific terminal window. When you close the window, the database engine completely stops. If you use DuckDB inside a Python script, the database engine lives inside the Python process itself.
    

### B. Row-Store vs. Column-Store

- **MS SQL Server:** By default, SQL Server is a **Row-Store** (OLTP). Data is stored on 8KB pages row-by-row. If you want to calculate the average of one column, SQL Server has to read all the pages containing those rows into memory. (Yes, SQL Server has _Columnstore Indexes_, but they are an add-on feature, not the default architecture).
    
- **DuckDB:** It is purely a **Column-Store** (OLAP) by default. If your table has 50 columns and 100 million rows, and you write `SELECT AVG(price) FROM sales`, DuckDB physically ignores the other 49 columns on your hard drive. It only loads the `price` column, processing it using "Vectorized Execution" (squeezing thousands of values into your CPU cache at once).
    

### C. The Concept of "Attaching" Data

- **MS SQL Server:** Data must be formally imported. If someone gives you a 10GB CSV or Parquet file, you have to use SSIS, BCP, or the Import/Export Wizard to physically ingest that data into an `.mdf` database file before you can write a single `SELECT` statement.
    
- **DuckDB:** It views files _as_ tables. DuckDB treats your local hard drive or even an AWS S3 bucket as part of its ecosystem. It streams and filters data directly out of raw files on the fly.
    

## Translation Guide for SQL Server Users

If you know how to do it in SQL Server, here is how you think about it in DuckDB:

|**Concept**|**MS SQL Server (What you know)**|**DuckDB (The Shift)**|
|---|---|---|
|**GUI Tool**|SSMS or Azure Data Studio|The CLI prompt, DBeaver, or a Jupyter Notebook|
|**System Info**|`sys.tables`, `sys.columns`|`duckdb_tables()`, `duckdb_columns()`|
|**Server Logs**|Windows Event Viewer / SQL Logs|Non-existent (it prints directly to your terminal)|
|**Isolation**|Multiple users connecting at once|Single-user (One process locks the database file)|
|**Linked Servers**|Complex setup to query external DBs|Just use the `ATTACH` command to query SQLite or Postgres files instantly|

### A Mind-Bending Example for an MS SQL User

In SQL Server, querying a remote file or a different database type requires configuring Linked Servers, OLEDB providers, or PolyBase.

In DuckDB, if you want to join a local CSV file with a Parquet file sitting on the internet, you just write it in a single query:

SQL

```
SELECT c.customer_id, p.total_spend
FROM 'C:\data\local_customers.csv' c
JOIN 'https://analytics-bucket.s3.amazonaws.com/2026/sales.parquet' p
  ON c.id = p.customer_id;
```

DuckDB acts as an execution engine that can reach out, pull exactly what columns it needs from both sources, execute a high-speed join in your RAM, and give you the answer without you ever "creating" a database.

Does this help clarify how it fits into your workflow compared to the heavyweight infrastructure of SQL Server?