```
EVALUATE FILTER( SUMMARIZE( 'D_Dates', 'D_Dates'[YearMonth_Current], "DistinctSortCount", DISTINCTCOUNT('D_Dates'[YYYYMM_Sort]) ), [DistinctSortCount] > 1 )
```
