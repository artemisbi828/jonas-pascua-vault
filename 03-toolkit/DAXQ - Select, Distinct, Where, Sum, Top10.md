```DAX
EVALUATE 'Date'

EVALUATE
SELECTCOLUMNS(
    'Date',
    "Date Key", 'Date'[DateKey],
    "Month Name", 'Date'[YearMonth]
)


EVALUATE
DISTINCT('Date'[YearMonth])

EVALUATE
FILTER(
    'Date',
    'Date'[YYYY] = 2026
)

EVALUATE
SUMMARIZECOLUMNS(
    'Date'[YearMonth],
    "TotalSales", SUM('Sales'[Amount])
)


EVALUATE
TOPN(10, 'Date', 'Date'[DateKey], DESC)
ORDER BY 'Date'[DateKey] DESC
```