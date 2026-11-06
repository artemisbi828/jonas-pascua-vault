```
DayWeight = 
VAR CurrentDate = 'Date'[Date]
VAR Mo = MONTH(CurrentDate)
VAR Yr = YEAR(CurrentDate)
VAR DoW = WEEKDAY(CurrentDate, 2) -- 1=Mon, 7=Sun
VAR DayNo = DAY(CurrentDate)

-- Calculate if it's the 2nd Monday (Indigenous) or 3rd Monday (MLK)
VAR IsMLK = (Mo = 1 && DoW = 1 && DayNo > 14 && DayNo <= 21)
VAR IsIndigenousDay = (Mo = 10 && DoW = 1 && DayNo > 7 && DayNo <= 14)

-- Static Holidays
VAR IsFixedHoliday = 
    (Mo = 1 && DayNo = 1) ||   -- New Year
    (Mo = 7 && DayNo = 4) ||   -- July 4th
    (Mo = 12 && DayNo = 25)    -- Christmas

VAR IsAnyHoliday = IsMLK || IsIndigenousDay || IsFixedHoliday

RETURN
IF(
    IsAnyHoliday, 0,
    IF(DoW <= 4, 1.0, 0.33) -- Mon-Thu = 1, Fri-Sun = 0.33
)
```

[[DAXM - Add WDE and Holiday Columns]]