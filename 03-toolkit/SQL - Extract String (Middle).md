get string in between

```sql

-- gets string in between "dbo"
-- substring(mycol, charindex(), len(mycol))

declare @string sysname = 'vw_dbo_F_CONTRACT';
select
    @string,
    substring(@string, 
    -- start
    charindex('_', @string) + 1, 
    -- end
    charindex('_', @string, charindex('_', @string) + 1) - charindex('_', @string) - 1);
```



