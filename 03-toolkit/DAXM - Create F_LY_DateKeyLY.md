# Date Shift
Create LY 
```PowerQuery(M)
let
    // 1. Get the Max Date from the FACT table (The Anchor)
    FactSource = Sql.Database("ARTEMIS", "NVS", [Query="SELECT MAX(DateKey) as MaxDate FROM sdrs.vw_F_OfficeDayStats"]),
    // Drill down to get the scalar date value
    FactMaxDate = Date.From(FactSource{0}[MaxDate]),

    // 2. Calculate the "Yesterday" Target and the Shift
    Yesterday = Date.From(DateTime.LocalNow()) - #duration(1, 0, 0, 0),
    RawGap = Duration.Days(Yesterday - FactMaxDate),
    // Multiples of 7 to keep Weekdays (Mon-Thu) consistent for your normalization
    WeekAlignedShift = Number.RoundDown(RawGap / 7) * 7,

    // 3. Load the CALENDAR Table
    CalendarSource = Sql.Database("ARTEMIS", "NVS", [Query="SELECT * FROM sdrs.vw_D_Dates"]),

    // 4. Transform the CALENDAR using the Shift from the FACT table
    ShiftedCalendar = Table.TransformColumns(CalendarSource, {
        {"DateKey", each Date.AddDays(_, WeekAlignedShift), type date},
        {"EndOfMonth", each Date.AddDays(_, WeekAlignedShift), type date},
        {"MonthKey", each Date.AddDays(_, WeekAlignedShift), type date}
    }),

    // 5. Update Labels (DRY Repair)
    // We update strings like "2022 Jan" so they match the new shifted DateKey year
    FinalCalendar = Table.TransformColumns(ShiftedCalendar, {
        {"YYYY", each Date.Year(Date.AddDays(#date(_,1,1), WeekAlignedShift)), Int64.Type},
        {"YearMonth", each 
            let d = Date.AddDays(Date.From(Text.Range(_, 0, 4) & "-" & Text.Range(_, 5, 3) & "-01"), WeekAlignedShift)
            in Text.From(Date.Year(d)) & " " & Date.MonthName(d, "en-us"), type text},
        {"YYYYMM_Sort", each 
            let d = Date.AddDays(Date.From(Text.Start(_, 4) & "-" & Text.End(_, 2) & "-01"), WeekAlignedShift)
            in Text.From(Date.Year(d)) & " " & Text.PadStart(Text.From(Date.Month(d)), 2, "0"), type text}
    }),
    // hard code change the data types
    #"Changed Type" = Table.TransformColumnTypes(FinalCalendar,{{"DateKey", type date}, {"MonthKey", type date}, {"EndOfMonth", type date}})
in
    #"Changed Type"
```

## SQL Version for Comprehension
- holiday dates and things need to shift so join that table after in the ERD
- 
```sql
declare @MaxDataDate date = (select max(DateKey)from sdrs.OfficeDayStats);
declare @TargetDate date = dateadd(day, -1, getdate()at time zone 'UTC' at time zone 'Central Standard Time')

-- 1. Calculate the total days between data and yesterday
DECLARE @RawDayGap INT = DATEDIFF(DAY, @MaxDataDate, @TargetDate);

-- 2. Force the gap to the nearest multiple of 7 (downward)
-- This ensures the day-of-week alignment (Mon remains Mon)
DECLARE @WeeklyAlignedShift INT = (@RawDayGap / 7) * 7;

-- 3. Select your shifted data
SELECT 
    DATEADD(DAY, @WeeklyAlignedShift, DateKey) AS ShiftedDateKey,
    -- Re-calculate columns that rely on the year/month to avoid "2025" labels
    YEAR(DATEADD(DAY, @WeeklyAlignedShift, DateKey)) AS YYYY,
    FORMAT(DATEADD(DAY, @WeeklyAlignedShift, DateKey), 'yyyy MM') AS YYYYMM_Sort,
    FORMAT(DATEADD(DAY, @WeeklyAlignedShift, DateKey), 'yyyy MMM') AS YearMonth,
    DateKey -- Pull the rest of your original columns
FROM sdrs.vw_D_Dates
WHERE DateKey <= @MaxDataDate;
```