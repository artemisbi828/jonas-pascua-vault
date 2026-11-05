```sql
-- defines Holidays
-- defines WDE for all dates

--create TABLE dbo.Dates_Holidays_WDE ( [DateKey] date primary key, [HolidayName] varchar(22), [WDE_DayWeight] decimal(10,3) 
--)

;with DateBase
as (
   -- Assuming you have a standard Calendar table. 
   -- If not, this CTE represents your source dates.
   select
       DateKey,
       [Month],
       [DayOfWeek] as [DoW], -- 1=Sun, 2=Mon, etc. in default SQL
       [DayOfMonth]
   from dbo.Dates),
      HolidayLogic
as (  -- 
   select
       *,
       case when inr.HolidayName is not null then 1 else 0 end as IsHoliday
   from (
       select
           *,
           -- Logic for Floating Holidays
           case
                -- MLK Day: 3rd Monday of Jan (Monday is 2, Mathematically Day between 15-21)
                when [Month] = 1
                 and [DoW] = 2
                 and [DayOfMonth] between 15 and 21 then 'MLK Day'

                -- President's Day: 3rd Monday of Feb
                when [Month] = 2
                 and [DoW] = 2
                 and [DayOfMonth] between 15 and 21 then 'President''s Day'

                -- Indigenous Peoples' Day: 2nd Monday of Oct (Monday is 2, Day between 8-14); formerly Colombus' Day
                when [Month] = 10
                 and [DoW] = 2
                 and [DayOfMonth] between 8 and 14 then 'Indigenous Peoples Day'

                -- Static Fixed Holidays
                when [Month] = 1
                 and [DayOfMonth] = 1 then 'New Years Day'
                when [Month] = 7
                 and [DayOfMonth] = 4 then 'Independence Day'
                when [Month] = 11
                 and DateBase.DayOfMonth = 11 then 'Veteran''s Day'
                when [Month] = 12
                 and [DayOfMonth] = 25 then 'Christmas'
                when [Month] = 12
                 and [DayOfMonth] = 31 then 'New Years Eve'

                -- Add other holidays here (e.g., Labor Day: 1st Monday of Sept)
                when [Month] = 9
                 and [DoW] = 2
                 and [DayOfMonth] <= 7 then 'Labor Day'
                else null end as HolidayName
       from DateBase
   ) inr ),
      ProximityLogic
as (select
        *,
        -- Look ahead 1 day to see if tomorrow is a holiday
        lead(IsHoliday, 1) over (order by DateKey) as IsPreHoliday,
        -- Look back 1 day to see if yesterday was a holiday
        lag(IsHoliday, 1) over (order by DateKey) as IsPostHoliday
    from HolidayLogic)
-- ===========================================
--insert into dbo.Dates_Holidays_WDE (DateKey, HolidayName, WDE_DayWeight)
--
select
    DateKey,
    case when [IsPreHoliday] = 1 then 'PreHoliday'
         when [IsPostHoliday] = 1 then 'PostHoliday'
         else HolidayName end as HolidayName,
    cast(case
              -- specific to orthodontics
              when [HolidayName] in ('MLK Day', 'President''s Day', 'Indigenous Peoples Day', 'Veteran''s Day') then 1
              when [Month] = 12
               and [DoW] in (28, 29, 30) then 0.667
                                                              --
              when [HolidayName] = 'New Years Eve' then 0.333 -- 
              /* below is standard */
              when HolidayName is not null then 0             -- All Holidays = 0
              when [DoW] between 2 and 5 then 1.0             -- Mon (2) through Thu (5) = 1.0
              else 0.333                                      -- Fri, Sat, Sun = 0.33
         end as decimal(10, 3)) as WDE_DayWeight
from ProximityLogic
order by 1;
```