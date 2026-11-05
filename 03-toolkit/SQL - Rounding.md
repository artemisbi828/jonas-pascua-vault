ROUND DOWN
```sql
-- round down
SELECT FLOOR(19.996); -- Result: 19
SELECT ROUND(19.996, 0, 1); -- Result: 19.000
SELECT CAST(19.996 AS INT); -- Result: 19

-- round up
SELECT ROUND(19.996, 0); -- Result: 20 (up to nearest integer)
```