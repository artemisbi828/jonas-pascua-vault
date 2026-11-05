Below is a **practical MSSQL → Snowflake datatype conversion map** you can use for schema migration / ELT landing layers. It’s aligned to Snowflake’s supported type families and (importantly) the **real-world mappings Snowflake uses for SQL Server replication/migration tooling**. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)

---

## 1) Core conversion map (MSSQL → Snowflake)

> **Rule of thumb:**
> 
> - Prefer **Snowflake native** types (`NUMBER`, `TIMESTAMP_*`, `BOOLEAN`, `BINARY`, `VARCHAR/TEXT`). [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)
> - For “special” SQL Server types (XML, hierarchyid, sql_variant, etc.), land as **TEXT** (or VARIANT if you intentionally model semi-structured). [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)

### Numeric (exact / integer / financial)

|MSSQL datatype|Snowflake target|Notes / gotchas|
|---|---|---|
|`tinyint`|`INT`|Snowflake commonly maps SQL Server integer families to `INT` (a synonym of `NUMBER`). [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`smallint`|`INT`|Same pattern. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`int`|`INT`|Same pattern. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`bigint`|`INT`|Snowflake replication mapping often lands this as `INT` (synonym of `NUMBER`). [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`decimal(p,s)`|`NUMBER(p,s)`|If **precision > 38**, Snowflake tooling may store as `TEXT` due to Snowflake precision limit. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`numeric(p,s)`|`NUMBER(p,s)`|Same precision rule. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`money`|`NUMBER`|Consider setting scale explicitly in your DDL (SQL Server money is fixed-scale). SQL Server includes `money/smallmoney` as exact numeric types. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`smallmoney`|`NUMBER`|Same. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|

### Numeric (approx / floating)

|MSSQL datatype|Snowflake target|Notes / gotchas|
|---|---|---|
|`real`|`FLOAT`|Snowflake’s float family is approximate. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`float(n)`|`FLOAT`|Same; don’t use for currency. SQL Server categorizes float/real as approximate. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|

### Boolean / logical

|MSSQL datatype|Snowflake target|Notes / gotchas|
|---|---|---|
|`bit`|`BOOLEAN`|Direct mapping. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|

### Character / Unicode / large text

|MSSQL datatype|Snowflake target|Notes / gotchas|
|---|---|---|
|`char(n)`|`TEXT` (or `VARCHAR(n)`)|Replication tools often land char/varchar as `TEXT`. Snowflake treats `TEXT` as synonym of `VARCHAR`. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`varchar(n)`|`TEXT` (or `VARCHAR(n)`)|Same. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`varchar(max)`|`TEXT`|Snowflake `VARCHAR` default max is large; `TEXT` is common landing type. [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping)|
|`nchar(n)`|`TEXT`|Unicode in SQL Server; Snowflake `VARCHAR/TEXT` stores Unicode. Tools map to `TEXT`. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`nvarchar(n)`|`TEXT`|Same. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`nvarchar(max)`|`TEXT`|Same. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`text` _(legacy)_|`TEXT`|SQL Server legacy types exist; map to `TEXT`. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`ntext` _(legacy)_|`TEXT`|Same. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`xml`|`TEXT`|Snowflake mapping guidance/tooling commonly lands XML as `TEXT`. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|

### Binary / blobs

|MSSQL datatype|Snowflake target|Notes / gotchas|
|---|---|---|
|`binary(n)`|`BINARY`|Direct. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`varbinary(n)`|`BINARY`|Direct. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`varbinary(max)`|`BINARY`|Watch Snowflake per-row/field size constraints in your ingestion patterns; tooling notes max entry size considerations. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`image` _(legacy)_|`BINARY`|Legacy SQL Server type mapped to `BINARY`. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|

### Date & time

|MSSQL datatype|Snowflake target|Notes / gotchas|
|---|---|---|
|`date`|`DATE`|Direct. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`time`|`TIME`|Direct. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`smalldatetime`|`TIMESTAMP_NTZ`|Snowflake replication mapping lands as timestamp (no timezone). [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`datetime`|`TIMESTAMP_NTZ`|Same. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`datetime2`|`TIMESTAMP_NTZ`|Same (recommended MSSQL type) maps cleanly. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`datetimeoffset`|`TIMESTAMP_TZ`|Preserves offset/zone semantics via Snowflake TZ timestamp. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|

### Identifiers / rowversion / variants / spatial

|MSSQL datatype|Snowflake target|Notes / gotchas|
|---|---|---|
|`uniqueidentifier`|`TEXT` _(or `UUID`)_|Tooling commonly maps to `TEXT`. Snowflake also supports a `UUID` type. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17)|
|`timestamp` / `rowversion` _(SQL Server)_|`TEXT`|**Important:** SQL Server `timestamp` is **not** datetime; it’s rowversion bytes. Tooling maps to `TEXT`. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`sql_variant`|`TEXT`|Land as text. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`json` _(stored as text in MSSQL)_|`VARIANT`|Snowflake semi-structured landing type is `VARIANT` (common replication mapping). [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`geography`|`TEXT`|Tooling may insert as NULL depending on connector; treat as special case. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|
|`geometry`|`TEXT`|Same. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [learn.microsoft.com](https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver17), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)|

---

## 2) Decision rules (fast, deterministic)

### A) Integers

- If MSSQL is `tinyint/smallint/int/bigint` → use **`INT`** in Snowflake (simple, portable). [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)

### B) Decimals / currency

- If MSSQL is `decimal/numeric` → use **`NUMBER(p,s)`** (ensure `p ≤ 38`). [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping)
- If `p > 38`, plan to **downcast precision**, **store as TEXT**, or **split into two columns** (rare, but happens in dirty sources). [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)

### C) Datetime semantics

- If no timezone in MSSQL (`datetime/datetime2`) → **`TIMESTAMP_NTZ`**. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)
- If timezone-aware (`datetimeoffset`) → **`TIMESTAMP_TZ`**. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)

### D) Strings

- Default all string-ish types to **`TEXT`** (Snowflake synonym of `VARCHAR`). [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping)

---

## 3) Practical “landing layer” recommendation (what I’d do)

If your goal is a robust bronze/landing schema:

- Use **`TEXT`** for most strings (including `uniqueidentifier` initially). [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types), [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping)
- Use **`NUMBER(p,s)`** only when you trust the source precision/scale; else land as TEXT then cast in silver/gold. (Because precision overflow turns into TEXT anyway in some tooling.) [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)
- Use `TIMESTAMP_NTZ` for “server timestamps” and `TIMESTAMP_TZ` only where you truly have offsets. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)
- Land JSON payloads as `VARIANT` when you intend to query them as JSON; else keep as TEXT. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)

---

## 4) Quick clarifier (so I can tailor the map)

Are you doing:

1. **DDL conversion** (manual / dbt / Liquibase), or
2. **Replication/CDC tooling** (Fivetran / DMS / Snowflake Openflow / etc.)?

Reason: replication tools often force choices like “map char/varchar to TEXT” and handle overflow rules (e.g., decimal precision > 38 → TEXT) automatically. [docs.snowflake.cn](https://docs.snowflake.cn/en/user-guide/data-integration/openflow/connectors/sql-server/data-mapping), [docs.snowflake.com](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)