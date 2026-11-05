
# Patient Status History Size Estimate

## Inputs

```text
Rows               = 23,057,407
Distinct Patients  = 6,313,962
```

Sample Grain:

```text
ssid
patGuid
ptStatCode
StartTime
EndTime
```

Example:

```text
133 | 886205F9-DEFF-40AE-8338-AD9080B9E55B | NPSch       | 2026-05-27 06:06:13 | 2026-06-13 06:07:08
133 | 886205F9-DEFF-40AE-8338-AD9080B9E55B | StartNeeded | 2026-06-13 06:07:08 | 2026-06-16 06:10:02
133 | 886205F9-DEFF-40AE-8338-AD9080B9E55B | GG          | 2026-06-16 06:10:02 | 2026-06-17 06:08:04
133 | 886205F9-DEFF-40AE-8338-AD9080B9E55B | FullBraces  | 2026-06-17 06:08:04 | NULL
```

---

## Rows per Patient

```text
23,057,407 ÷ 6,313,962
= 3.65 status rows per patient
```

Average patient appears to have approximately:

```text
3.65 status transitions
```

---

## Row Width Estimation

### ssid

```text
INT
≈ 4 bytes
```

### patGuid

```text
UNIQUEIDENTIFIER
≈ 16 bytes
```

### ptStatCode

Examples:

```text
NPSch
GG
StartNeeded
FullBraces
```

Estimate:

```text
8 bytes average text
+ 2 bytes varchar overhead

≈ 10 bytes
```

### StartTime

```text
DATETIME2(7)
≈ 8 bytes
```

### EndTime

```text
DATETIME2(7)
≈ 8 bytes
```

### SQL Server Row Overhead

```text
Row header
Null bitmap
Misc storage metadata

≈ 10 bytes
```

---

## Estimated Row Size

```text
ssid          4
patGuid      16
ptStatCode   10
StartTime     8
EndTime       8
Overhead     10
----------------
Total        56 bytes
```

Rounded:

```text
≈ 60 bytes per row
```

---

## Raw Storage Estimate

### Base Estimate

```text
23,057,407 × 60 bytes

= 1,383,444,420 bytes
≈ 1.38 GB
```

---

### Conservative Estimate

Assume:

- Longer status descriptions
- Additional row overhead

```text
75 bytes per row
```

Calculation:

```text
23,057,407 × 75 bytes

= 1,729,305,525 bytes
≈ 1.73 GB
```

---

## Compression Estimate

This dataset should compress extremely well because:

- Only 6.3M patients
- Likely small status code domain
- Repeating ssid values
- Highly repetitive timestamps
- Sequential patient histories

Typical compression:

```text
3:1 to 10:1
```

Result:

```text
Raw Size          1.4 - 1.8 GB

Compressed:
Parquet
DuckDB
Snowflake
Columnstore

≈ 150 MB - 600 MB
```

---

## Sanity Check

Per-patient footprint:

```text
3.65 rows × 60 bytes
=
219 bytes per patient
```

Multiply:

```text
219 × 6,313,962

≈ 1.38 GB
```

Matches previous estimate.

---

# Executive TLDR

| Metric | Estimate |
|----------|----------:|
| Row Count | 23.1M |
| Distinct Patients | 6.3M |
| Avg Status Rows per Patient | 3.65 |
| Estimated Row Width | 60-75 bytes |
| Raw Storage | 1.4-1.8 GB |
| Compressed Storage | 150-600 MB |

## Takeaway

**This is GB-scale, not TB-scale.**

For planning purposes:

```text
Raw Table Budget:
≈ 2 GB

Compressed Analytics Budget:
< 1 GB
```

This is small enough that most modern analytics engines (DuckDB, Snowflake, Fabric Warehouse, SQL Server Columnstore) should be able to aggregate and window over the entire dataset comfortably.