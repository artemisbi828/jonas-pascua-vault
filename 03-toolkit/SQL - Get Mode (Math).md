```sql
WITH ModeCTE AS (
    SELECT 
        ProductID,
        COUNT(*) AS Occurrences,
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rn
    FROM Sales
    GROUP BY ProductID
)
SELECT ProductID, Occurrences
FROM ModeCTE
WHERE rn = 1;
```
