This cheat sheet is designed for a SQL Server veteran. It bypasses the basics (`SELECT * FROM`) and focuses on the architectural shifts, muscle-memory breakers, and tooling replacements needed to be productive in PostgreSQL immediately.

### **I. High-Level Architecture & Philosophy**

|**Feature**|**SQL Server (The "Enterprise" Way)**|**PostgreSQL (The "Academic" Way)**|
|---|---|---|
|**Process Model**|**Thread-based.** One process, many threads. Efficient memory sharing.|**Process-based.** Each connection is a separate OS process. Higher memory overhead per connection (requires a connection pooler like `PgBouncer` for scale).|
|**Concurrency**|**Locking & Blocking.** Readers often block writers (and vice versa) unless specific isolation levels are used.|**MVCC (Multi-Version Concurrency Control).** Readers **never** block writers; writers **never** block readers.|
|**Dirty Reads**|`NOLOCK` is common to avoid blocking.|**Does not exist.** `READ UNCOMMITTED` is silently upgraded to `READ COMMITTED`. You cannot read dirty data; MVCC makes this mostly unnecessary anyway.|
|**Case Sensitivity**|Case-**insensitive** by default (`Select` = `SELECT`).|Case-**sensitive** for identifiers if quoted. Unquoted identifiers are auto-folded to **lowercase**. `Select * From TableName` looks for `tablename`.|
|**Procedural**|**T-SQL**: `CREATE PROCEDURE`. Logic often mixed with queries.|**PL/pgSQL**: `CREATE FUNCTION` (mostly). Strict block structure (`DO $$...$$`). More like Ada or Oracle PL/SQL than T-SQL.|

---

### **II. Tooling: The "Redgate" Equivalent**

You are used to **SSMS + SQL Prompt**. The bad news: `pgAdmin 4` (the default tool) will feel slow and clunky by comparison.

**The Best Replacements:**

1. **DataGrip (JetBrains):**
    
    - **Why:** It is the closest experience to "IntelliSense on steroids."
    - **Features:** Incredible auto-completion, refactoring (rename column/table safely), "go to definition," and snippets. It feels like Visual Studio + SQL Prompt combined.
    - **Cost:** Paid (subscription), but worth it for a power user.
        
2. **DBeaver (Community Edition):**
    
    - **Why:** Free, open-source, and supports every database.
    - **Features:** Decent auto-complete and visual query builder. Not as polished as DataGrip but very functional.
        
3. **Azure Data Studio (with PostgreSQL Extension):**
    
    - **Why:** If you want the "Microsoft feel."
    - **Features:** You can install the PostgreSQL extension. It supports "IntelliSense" (via the language server), snippets, and notebook support.
        

---

### **III. Syntax Cheat Sheet: Muscle Memory Fixes**

#### **1. Top Pitfalls & "Gotchas"**

- **Quotes:**
    - **Single Quotes (`'`)**: Only for string literals (`'value'`).
    - **Double Quotes (`"`)**: Only for identifiers (tables/columns) that are case-sensitive or keywords (`"UserTable"`, `"Select"`). _Avoid using double quotes if possible to keep things lowercase._
- **Brackets:** `[ColumnName]` does **not** work. Use `"ColumnName"` if you must, but better to use `column_name`.
- **Aliases:** You generally need `AS` for column aliases (optional but recommended), and you **cannot** use `ColumnName = Value` syntax for aliasing in SELECT.
    

#### **2. Function Mapping**

| **SQL Server (T-SQL)**      | **PostgreSQL Equivalent**      | **Notes**                                                                                                     |
| --------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| `TOP 10`                    | `LIMIT 10`                     | Goes at the **end** of the query.                                                                             |
| `ISNULL(Col, 0)`            | `COALESCE(Col, 0)`             | ANSI standard. `ISNULL` does not exist.                                                                       |
| `GETDATE()`                 | `NOW()` or `CURRENT_TIMESTAMP` | `NOW()` returns transaction start time (stable).                                                              |
| `DATEADD(dd, 1, GetDate())` | `NOW() + INTERVAL '1 day'`     | Use interval math: `'1 month'`, `'2 hours'`, etc.                                                             |
| `DATEDIFF(day, Start, End)` | `End - Start`                  | Subtracting dates returns an `interval` (e.g., "3 days 04:00:00"). Extract parts with `EXTRACT(DAY FROM ...)` |
| `LEN(Str)`                  | `LENGTH(Str)`                  |                                                                                                               |
| `CHARINDEX('a', Col)`       | `POSITION('a' IN Col)`         |                                                                                                               |
| `+` (String Concat)         | `\|`                           | `Select 'A'                                                                                                   |
| `IDENTITY(1,1)`             | `GENERATED ALWAYS AS IDENTITY` | Or the older `SERIAL` type (pseudo-type creating a sequence).                                                 |
| `#TempTable`                | `CREATE TEMP TABLE table_name` | Scope is **Session** by default. Use `ON COMMIT DROP` to mimic transaction scope.                             |
| `@TableVariable`            | N/A                            | No direct equivalent. Use temp tables or logic in PL/pgSQL blocks.                                            |

---

### **IV. Procedural Code: T-SQL vs. PL/pgSQL**

This is the biggest jump. PostgreSQL logic is strictly block-structured.

**Scenario:** Update a user's email and return the new updated date.

**SQL Server (T-SQL)**

SQL

```
CREATE PROCEDURE UpdateUserEmail
    @UserId INT,
    @NewEmail VARCHAR(100)
AS
BEGIN
    -- Implicit transaction or explicit BEGIN TRAN
    UPDATE Users
    SET Email = @NewEmail,
        UpdatedDate = GETDATE()
    WHERE Id = @UserId;

    -- Return the new date
    SELECT UpdatedDate FROM Users WHERE Id = @UserId;
END;
```

**PostgreSQL (PL/pgSQL)**

SQL

```
-- Often a FUNCTION, though PROCEDURES exist (Procs support transaction commits)
CREATE OR REPLACE FUNCTION update_user_email(
    p_user_id INT,           -- Parameters named to avoid collision
    p_new_email TEXT         -- TEXT is preferred over VARCHAR
) 
RETURNS TIMESTAMP AS $$      -- $$ starts the code block string
DECLARE
    v_updated_date TIMESTAMP; -- Variable declaration
BEGIN
    UPDATE users
    SET email = p_new_email,
        updated_date = NOW()
    WHERE id = p_user_id
    RETURNING updated_date INTO v_updated_date; -- "OUTPUT" clause equivalent

    RETURN v_updated_date;
END;
$$ LANGUAGE plpgsql;
```

**Key Procedural Differences:**

1. **Block Delimiters:** You wrap code in `$$` (dollar quotes) instead of just `BEGIN/END`.
2. **Variables:** Must be declared in a `DECLARE` block _before_ `BEGIN`.
3. **Assignment:** Use `:=` for assignment (`v_count := 1;`), though `=` works in some contexts, `:=` is clearer.
4. **RETURNING:** Postgres loves `RETURNING` clauses in Update/Insert/Delete statements. It saves you a second `SELECT`.
    

### **V. One Final "Pro" Tip**

In SQL Server, you often check `sysobjects` or `sys.tables`. In Postgres, get used to the **Information Schema** or the **System Catalogs**:

- `\d table_name` (in command line `psql`) is your best friend.
- Query `pg_tables`, `pg_indexes`, `pg_views` for metadata.

### Postgres vs. SQL Server: The "Under the Hood" Differences

You are asking the right questions. The architectural differences aren't just academic trivia; they change how you manage the server and when you choose one over the other.

#### 1. Process (Postgres) vs. Thread (SQL Server)

- **Postgres (Process-based):** Think of this like a **hotel**. Each user who logs in gets their own private room (a process).
    - **For Admins:** If you open "Task Manager" or `top` on a Linux server, you will see _thousands_ of `postgres` entries—one for every connected user.
    - **The "Good" Part:** **Isolation.** If one user runs a query so bad it crashes their "room," only that user is kicked out. Everyone else in the hotel is fine.
    - **The "Bad" Part:** Building a room is expensive (memory/CPU). Postgres struggles with thousands of direct connections because the server runs out of RAM. You almost _always_ need a "Connection Pooler" (like PgBouncer) to manage this.
- **SQL Server (Thread-based):** Think of this like a **huge open-plan office**. Everyone sits in one giant room (the `sqlservr.exe` process) and just grabs a different chair (thread).
    - **For Admins:** You see one massive block of memory usage in Task Manager. It is harder to see "who" is using the CPU just by looking at the OS list.
    - **The "Good" Part:** **Efficiency.** It is incredibly cheap to swap chairs. SQL Server can handle thousands of concurrent connections with much less memory overhead than Postgres because they share resources.
        

**Winner:**

- **Postgres** is better for stability and safety (one crash doesn't kill the DB).
- **SQL Server** is better for high-concurrency raw connection handling out of the box (Windows is very good at threading).
    

---

#### 2. Concurrency & Dirty Reads: Why would you want the "Bad" stuff?

You correctly noted that SQL Server defaults to "Locking" (if I am reading a row, you cannot write to it) while Postgres defaults to MVCC (Multi-Version Concurrency Control - I see an old snapshot while you write the new one).

In the modern world, MVCC (Postgres style) is generally preferred. **So, why does SQL Server still use Locking and Dirty Reads?**

The "Good Part" of Dirty Reads (NOLOCK):

Imagine you are running a report to sum up "Total Sales" for the day on Amazon. Ideally, you want the exact number. But people are buying things every millisecond.

- **In Postgres:** The DB has to work hard to keep giving you a "snapshot" of the data from the exact second you started your query. This costs CPU/Memory.
- **In SQL Server (with Dirty Reads):** You can use a command called `NOLOCK`. This tells the database: _"I don't care if the data is 100% perfect. If someone is in the middle of writing a record, just show me the half-finished version. I just need the report FAST and I don't want to slow down the shoppers."_
    

**The Benefit:** It is **blazing fast** and creates **zero blocking**.

- **Admin view:** If your boss says "Why is the checkout page slow?", in Postgres it might be because the Data Analytics team is running a huge report that is eating up I/O resources trying to maintain snapshot consistency. In SQL Server, the Analytics team uses `NOLOCK`, gets their data instantly, and the shoppers never feel a thing.
    
