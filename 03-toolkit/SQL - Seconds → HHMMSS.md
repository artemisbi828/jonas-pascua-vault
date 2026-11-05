```sql
declare @startdt datetime2
declare @enddt datetime2
declare @datediff_seconds int
declare @msg sysname

set @startdt = sysutcdatetime()
-- <<do something >> -- 
set @enddt = sysutcdatetime()
set @datediff_seconds = datediff(second, @startdt, @enddt)
set @msgg = 'This step complete ' + cast(convertseconds(@datediff_seconds)) as varchar(16))
```

```sql
create function std.udf_SecondsToHHMMSS (@TotalSeconds int)
returns varchar(64)
as begin

    declare @hours int = @TotalSeconds / 3600;
    declare @minutes int = (@TotalSeconds % 3600) / 60;
    declare @seconds int = @TotalSeconds % 60;

    return (
        select
            concat(
                -- pad hours
                right('0' + cast(@hours as varchar(10)), 2),
                ':',
                -- pad minutes
                right('0' + cast(@minutes as varchar(2)), 2),
                ':',
                -- pad seconds
                right('0' + cast(@seconds as varchar(2)), 2)
            )
    );
end;
```
