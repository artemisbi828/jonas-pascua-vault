# TL;DR

- Snowflake has **~15 core types**, not dozens
- Most SQL “types” are **aliases over NUMBER, FLOAT, VARCHAR**
- The only _unique_ primitives are:
    
    ```
    NUMBER, FLOAT, VARCHAR, BOOLEAN,
    DATE/TIME/TIMESTAMP,
    VARIANT/OBJECT/ARRAY,
    GEOGRAPHY/GEOMETRY,
    VECTOR
    ```
    

---

# 🔑 Key Observations (Deterministic Takeaways)

- **All integers collapse to `NUMBER(38,0)`**
- **All fixed decimals collapse to `NUMBER(p,s)`**
- **VARCHAR is effectively unbounded (up to 16MB)**
- **TIMESTAMP defaults to `TIMESTAMP_NTZ`**
- **VARIANT = primary primitive for semi-structured ingestion**
- **VECTOR = newer type (embeddings / AI use cases)**

> Snowflake is fairly tight—types collapse into core primitives with aliases (e.g., `NUMBER`, `DECIMAL`, `INT` → same underlying type).

---

# 🧊 Snowflake Data Types Cheat Sheet

|Category|Data Type|Aliases|Description|
|---|---|---|---|
|**Numeric (Exact)**|NUMBER(p,s)|NUMERIC, DECIMAL|Fixed-point numeric with precision `p` and scale `s`|
||INT|INTEGER, BIGINT, SMALLINT, TINYINT, BYTEINT|Integer (all map to NUMBER(38,0))|
|**Numeric (Approximate)**|FLOAT|FLOAT4, FLOAT8, DOUBLE, DOUBLE PRECISION, REAL|Floating point (approximate numeric)|

---

|Category|Data Type|Aliases|Description|
|---|---|---|---|
|**String**|VARCHAR|STRING, TEXT|Variable-length UTF-8 string|
||CHAR(n)|CHARACTER|Fixed-length string|
||BINARY|—|Binary data (byte array)|

---

|Category|Data Type|Aliases|Description|
|---|---|---|---|
|**Boolean**|BOOLEAN|BOOL|TRUE / FALSE values|

---

|Category|Data Type|Aliases|Description|
|---|---|---|---|
|**Date & Time**|DATE|—|Calendar date (no time)|
||TIME(p)|—|Time of day with fractional seconds precision|
||TIMESTAMP|TIMESTAMP_NTZ|Timestamp (no timezone)|
||TIMESTAMP_LTZ|—|Timestamp with session timezone|
||TIMESTAMP_TZ|—|Timestamp with embedded timezone|

---

|Category|Data Type|Aliases|Description|
|---|---|---|---|
|**Semi-Structured**|VARIANT|—|Stores JSON, XML, Avro, etc. (typed dynamically)|
||OBJECT|—|Key-value pairs (JSON object)|
||ARRAY|—|Ordered list (JSON array)|

---

|Category|Data Type|Aliases|Description|
|---|---|---|---|
|**Geospatial**|GEOGRAPHY|—|Earth-coordinate geospatial data|
||GEOMETRY|—|Planar (Euclidean) spatial data|

---

|Category|Data Type|Aliases|Description|
|---|---|---|---|
|**Vector (ML / AI)**|VECTOR|—|Fixed-length vector for embeddings (e.g., VECTOR(FLOAT, 768))|

---

