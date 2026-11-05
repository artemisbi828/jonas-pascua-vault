also works for 0.33 → 0.333

```sql
-- Snap to nearest third and keep 3-decimal precision
SELECT CAST(ROUND(ROUND(@x * 3, 0) / 3.0, 3) AS DECIMAL(9, 3)) AS thirds_value;

```
