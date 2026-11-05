
- case when or use these below
# 2 values only
```sql
-- # MIN
iif(a < b, a, b)

-- # MAX
iif(a > b, a, b)
```

# 2+ values
```sql
SELECT 
    (SELECT MIN(v) FROM (VALUES (ColumnA), (ColumnB)) AS value(v)) AS MinValue
FROM YourTable;
```