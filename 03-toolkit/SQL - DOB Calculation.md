
```sql
-- 6570 is age
case when datediff(day, sds.DateOfBirth, sds.DateKey) < 6570 then 1 else 0 end as IsMinor,
```


To get an accurate **Years and Months** calculation that mirrors how humans actually count age, you should use the following logic:

### The T-SQL Solution

SQL

```
DECLARE @DOB DATE = '1995-06-15';
DECLARE @Today DATE = GETDATE();

SELECT 
    -- Calculate Years: Subtract 1 if today's date is before the birthday this year
    DATEDIFF(YEAR, @DOB, @Today) - 
        CASE 
            WHEN (MONTH(@DOB) > MONTH(@Today)) 
            OR (MONTH(@DOB) = MONTH(@Today) AND DAY(@DOB) > DAY(@Today)) 
            THEN 1 ELSE 0 
        END AS AgeYears,

    -- Calculate Months: Total months mod 12, adjusting for the day of the month
    (DATEDIFF(MONTH, @DOB, @Today) - 
        CASE 
            WHEN DAY(@DOB) > DAY(@Today) 
            THEN 1 ELSE 0 
        END) % 12 AS AgeMonths;
```

---

### How it Works

- **Years:** We start with the difference in years. If the current month and day are "behind" the birth month and day, we subtract 1.
    
- **Months:** We find the total difference in months. If the current day of the month is less than the birth day, we subtract 1 (because the full month hasn't been completed yet). We then use the modulo operator `% 12` to get the remainder after years are accounted for.
    

> **Note:** This logic handles leap years correctly by relying on SQL Server's internal date functions, which recognize Feb 29th.