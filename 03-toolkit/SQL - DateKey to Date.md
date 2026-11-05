```sql
try_cast(concat_ws('-', convert(nvarchar(32), D_DATE_KEY) / 10000,
convert(nvarchar(16), D_DATE_KEY) % 10000 / 100,
convert(nvarchar(16), D_DATE_KEY) % 100) as date) as DateKey,
```

#status/deferred/quick-paste-merge-later 
```sql
create function help.ConvertDateInt_To_Date (@dateint int)
returns date
begin 
return
-- div by 10000 converts first 4 numplaces (4 zeros = into 4 zeros then removes them)
-- modulo does opposite, instead of 4 zeros -- everything outside of first 4 numplaces becomes 00
-- nvarchar(2) truncates 1 place to the left
-- casting as date converts 2024-8-1 >> 2024-08-01
cast(concat(convert(nvarchar(4), @dateint / 10000), 
'-', 
convert(nvarchar(2), (@dateint % 10000) / 100), 
'-', 
convert(nvarchar(2), @dateint % 100)) as date)
end
go
```

```sql
declare @date int = '20250201';
 
-- get 2025
select @date / 10000;
-- get 0201
select @date % 10000;
-- get month
select @date % 10000 / 100;
-- get day
select @date % 100;
 
-- get 2025
select cast(concat(@date / 10000, '-', @date % 10000 / 100, '-', @date % 100) as date);
```

# Snowflake SQL 
```sql
-- 
DATE_TRUNC('MONTH', TRY_TO_DATE(D_DATE_KEY::VARCHAR, 'YYYYMMDD')) AS month_star

-- # reverse
TO_NUMBER(TO_CHAR(CURRENT_DATE(), 'YYYYMMDD')
```