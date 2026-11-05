related-to: [[Standards - Date - Leap Year]]

2026-APR; 2027-APR
APR-12 to NOV-13
0900 AM to 1000 AM

### Convert datetime2 --> ISO 8601
```sql
SELECT CONVERT(varchar(33), SYSUTCDATETIME(), 126);
```

### Convert String to Datetime2
```sql
DECLARE @string_date sysname = 'Thursday, May 28, 2026 12:05 PM';
DECLARE @datetime datetime2(6);

SET @datetime = TRY_PARSE(
    LTRIM(SUBSTRING(
        @string_date,
        CHARINDEX(',', @string_date) + 1,
        LEN(@string_date)
    ))
    AS datetime2
    USING 'en-US'
);

SELECT @datetime;
```


# What Is ISO-8601?

| ISO 8601 (SQL Server)             | Translated                                 |
| --------------------------------- | ------------------------------------------ |
| 2026-09-10T16:30:57.6058932-05:00 | September 10, 2026, 4:30:57.6058932 PM EST |
```
2026-09-10    = Date (September 10, 2026)
T             = Separator between date and time
16:30:57      = Time (4:30:57 PM)
.6058932      = Fractional seconds
-05:00        = UTC offset (5 hours behind UTC)
```

The -05:00 at the end already means UTC-5, which is the offset used by Eastern Standard Time (EST).


Important note

Since September is during Daylight Saving Time in the Eastern US, the actual local timezone in places like New York is typically EDT (UTC-4), not EST.

So:

Timestamp as written: 4:30:57 PM UTC-5
Equivalent Eastern local time during DST: 5:30:57 PM EDT (UTC-4)

Quick SQL Server conversion:

SELECT CONVERT(datetimeoffset, '2026-09-10T16:30:57.6058932-05:00')
       AT TIME ZONE 'Eastern Standard Time';


This would show the value adjusted to the Windows Eastern time zone rules (including DST).

# Legacy Notes
Date
ISO Week
Month

Floor: 2022-01-01
Biggest Days
1. MLK
2. President's Day

# Important Columns
`Date Value`, `Month Value`, `Quarter`, `Holiday`, `Production Day Weight`

# Canononical Timezone Recommendation 
Dates dimension for portfolio should be EST since we are US Based.
```
[@portfolio](@portfolio) -- EST  
└─ [@division](@division) -- most Eastern  
└─ [@region](@region) -- most Eastern  
└─ [@team](@team) -- most Eastern  
└─ [@location](@location) -- LTZ (Local)
```
If first of month, since data lags by 1 day:
*   subtract 1 day from getdate()
*   or whatever adjustments Minus1Month or Minus1Day → Minus2Month or Minus2Day

