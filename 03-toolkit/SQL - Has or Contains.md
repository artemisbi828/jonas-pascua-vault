Max(Case When ...)
Select top 1 Where Condition

```sql
select max( case 
        when charindex(' ', left([ttyp].[ttypDescription], 7)) > 0 then -- charindex does not produce nulls, just int
               1 else 0
          end
     ) as HasSpace
```
