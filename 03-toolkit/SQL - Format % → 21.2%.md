1. multiply by 100.0
2. round(,1)
3. cast as decimal(5,1)
4. concat(, %)

```sql

SELECT
    CONCAT(CAST(ROUND(Value * 100.0, 1) AS decimal(5,1)), '%') AS PercentValue
```