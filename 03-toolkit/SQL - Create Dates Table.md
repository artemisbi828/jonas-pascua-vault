> [!warning] YYYYMM is off --> must correct 

```sql
create table dbo.Dates (
    [DateKey] date,
    [DayOfYear] int,
    [DayOfMonth] int,
    [DayName] nvarchar(30),
    [DayNameAbbrev] nvarchar(3),
    [DayOfWeek] int,
    [WeekOfYear] int,
    [MonthKey] date,
    [Month] int,
    [MonthName] nvarchar(30),
    [MonthNameAbbrev] nvarchar(3),
    [YYYY] int,
    [YYYYMM] nvarchar(10),
    [YearMonth] nvarchar(12),
    [Quarter] int,
    [EndOfMonth] date,
    [EndOfYear] date
);
go

/*
<<< IF INTO ALREADY EXISTS AND YOU HAVE DROP IT FIRST >>>  
    alter table STD.dates alter column DateKey date not null;
    alter table STD.Dates
    add
    constraint [PK__std__Dates]
    primary key clustered (DateKey);
    */

declare @StartDate date = '20230101'; -- <<< SET YOUR START YEAR
declare @CutoffDate date = '20400101'; -- <<< SET YOUR END YEAR dateadd(year, 10, getdate()); -- 10 years from today - 1
set @CutoffDate = dateadd(day, -1, @CutoffDate)


/* recursion */
;
with [seq] ([n])
as (select 0
    union all
    select [seq].[n] + 1 from [seq] where [seq].[n] < datediff(day, @StartDate, @CutoffDate)),
     [d] ([d])
as (select dateadd(day, [seq].[n], @StartDate)from [seq]),
     [src]
as (select
        [DateKey] = convert(date, [d].[d]),
        [DayOfYear] = datepart(dayofyear, [d].[d]),
        [DayOfMonth] = datepart(day, [d].[d]),
        [DayName] = datename(weekday, [d].[d]),
        [DayNameAbbrev] = left(datename(weekday, [d].[d]), 3),
        [DayOfWeek] = datepart(weekday, [d].[d]),
        [WeekOfYear] = datepart(week, [d].[d]),
        [MonthKey] = datefromparts(year([d].[d]), month([d].[d]), 1),
        [Month] = datepart(month, [d].[d]),
        [MonthName] = datename(month, [d].[d]),
        [MonthNameAbbrev] = left(datename(month, [d].[d]), 3),
        [YYYY] = datepart(year, [d].[d]),
        -- TheISOWeek      = DATEPART(ISO_WEEK,  d),

        [YYYYMM] = convert(nvarchar(8), datepart(year, [d].[d])) + right(' 0' + convert(nvarchar(8), datepart(month, [d].[d])), 2),
        [YearMonth] = convert(nvarchar(8), datepart(year, [d].[d])) + ' ' + left(datename(month, [d].[d]), 3),
        [Quarter] = datepart(quarter, [d].[d]),
        [EndOfMonth] = eomonth([d].[d]),
        [EndOfYear] = datefromparts(year([d].[d]), 12, 31)
    from [d])
insert into dbo.Dates select * from [src] order by [src].[DateKey]
option (maxrecursion 0);
```
