>[!TIP] Performance Hack: Bits vs Booleans Power BI's VertiPaq engine compresses 1/0 (Integers) significantly better than True/False (Booleans) in large datasets. It also allows you to use SUM() in DAX instead of COUNTROWS(FILTER()), which is much faster.

