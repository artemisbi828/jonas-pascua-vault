```sql
SELECT 
    name,
    object_id,
    create_date,
    modify_date
FROM tempdb.sys.tables
WHERE name LIKE '#%'
ORDER BY name;
```
