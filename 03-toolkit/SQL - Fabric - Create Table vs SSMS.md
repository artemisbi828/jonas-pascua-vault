related-to: [[WH_DEV_Data_Solutions]]

# Find and Replace
```sublime
---
DROP TABLE #temptable --> 
#temptable --> edw.my_table
nvarchar --> varchar
tinyint --> int
datetime2(7) --> datetime2(6)
---
```

# Index, Taxonomy
```sql
create table dataops.process_index (
    process_id bigint not null identity,
    process_name varchar(50) not null,
    email varchar(2500) not null,
    parent varchar(50),
    sort_order decimal(5,2),
    comment varchar(2500),
    insert_datetime_utc datetime2(6)
);

create table base.contract (
	contract_id int not null,
	net_contract_amount decimal(19,4), 
	large_comment varchar(8000)
	
	)
```

[[Standard]]
> [!Note] To Create Identity Columns
> - big int
> - no seed ~~(identity (1,1))~~


---

| MSSQL type                       | Fabric Warehouse type                                          | Status                          |
| -------------------------------- | -------------------------------------------------------------- | ------------------------------- |
| `tinyint`                        | `smallint` (or `int`)                                          | ⚠️ Not listed as supported      |
| `nvarchar(n)`                    | Prefer `varchar(n)` with UTF‑8; avoid assuming nvarchar parity | ⚠️ Treat as “map”               |
| `nvarchar(max)`                  | Prefer `varchar(max)` where supported                          | ⚠️ Treat as “map”               |
| `bit`                            | `bit`                                                          | ✅ Supported                     |
| `smallint`                       | `smallint`                                                     | ✅ Supported                     |
| `int`                            | `int`                                                          | ✅ Supported                     |
| `bigint`                         | `bigint`                                                       | ✅ Supported                     |
| `decimal(p,s)` / `numeric(p,s)`  | `decimal(p,s)` / `numeric(p,s)`                                | ✅ Supported                     |
| `float`                          | `float`                                                        | ✅ Supported                     |
| `real`                           | `real`                                                         | ✅ Supported                     |
| `date`                           | `date`                                                         | ✅ Supported                     |
| `char(n)`                        | `char(n)`                                                      | ✅ Supported                     |
| `varchar(n)`                     | `varchar(n)`                                                   | ✅ Supported                     |
| `varbinary(n)`                   | `varbinary(n)`                                                 | ✅ Supported                     |
| `uniqueidentifier`               | `uniqueidentifier`                                             | ✅ Supported (interop caveat)    |
| `time(n)`                        | `time(0–6)`                                                    | ✅ Supported (precision-limited) |
| `datetime2(n)`                   | `datetime2(0–6)`                                               | ✅ Supported (precision-limited) |
| `varchar(max)`                   | `varchar(max)`                                                 | ✅ Supported (with limits)       |
| `varbinary(max)`                 | `varbinary(max)`                                               | ✅ Supported (with limits)       |
| `money` / `smallmoney`           | `decimal(19,4)` (typical)                                      | ❌ Unsupported → map             |
| `datetime` / `smalldatetime`     | `datetime2(0–6)`                                               | ❌ Unsupported → map             |
| `datetimeoffset`                 | `datetime2` (+ store offset separately if needed)              | ❌ Unsupported → map             |
| `xml`                            | `varchar(max)` (or shred upstream)                             | ❌ Unsupported → map             |
| `sql_variant`                    | Avoid; normalize to concrete types                             | ❌ Unsupported → map             |
| `geography/geometry/hierarchyid` | Store as `varchar(max)`/WKT or separate columns                | ❌ Unsupported → map             |

