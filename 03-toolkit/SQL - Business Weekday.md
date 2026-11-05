Default Settings on Servers/Computers
- 1 = Sunday
- 2 = Monday



```sql
format([dt], 'dddd') DayOfWeek
```


```sql
select
    d.DateKey,
    d.HolidayText,
    dateadd(day,
            -- add -14 day if Monday, otherwise convert to nearest Monday based on 
            case datepart(weekday, dateadd(day, -14, d.DateKey))
                 when 1 then -13 -- Sunday: -14 + 1 = -13 total
                 when 2 then -14 -- Monday: -14 + 0 = -14 total  
                 when 3 then -15 -- Tuesday: -14 - 1 = -15 total
                 when 4 then -16 -- Wednesday: -14 - 2 = -16 total
                 when 5 then -11 -- Thursday: -14 + 3 = -11 total
                 when 6 then -12 -- Friday: -14 + 2 = -12 total
                 when 7 then -13 -- Saturday: -14 + 1 = -13 total
            end,
            d.DateKey
    ) as Minus14DaysRoundToMonday
from jbi.vw_D_Dates as d
where d.HolidayText = 'President''s day'
  and d.Year >= 2025
  and d.DateKey < getdate();
```