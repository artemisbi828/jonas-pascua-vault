> [!warning] Error
> `Cannot convert value '' of type Text to type Numeric`
>> For a whole number on 
>> Available NM (Force Format) = FORMAT([Available NM], "#,##0")
>>	Available NM = CALCULATE([Available], DATEADD(D_Dates[DateKey], +1, MONTH))
>>		Available = SUM(F_SF_Reserverations[TOTAL_RESERVATIONS])

# Solution

```
Available NM (Force Format) = 
VAR x = [Available NM]
RETURN
IF(ISBLANK(x), 
    BLANK(), 
    FORMAT(x, "#,##0")
)
```