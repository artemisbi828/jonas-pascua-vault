```sql
-- # snowflake
datefromparts(year(c.DateKey), month(c.DateKey), 1) 

-- # snowflake
select top 200
    DATE_TRUNC('MONTH', "DATE") MonthKey)
```