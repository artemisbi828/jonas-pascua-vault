# writing an analysis query

## write base query
keep it minimalist
write base query: exclusions (eg weekends) 
transform bits/bools → tinyint
write to #t table
add a bool flag for anything you're comparing (eg is-this-month-this-week)

## write agg-calcs
ensure numerators and denominators always included 
any pct or ratio
* multiply numerator * 1.0 
* wrap denominator with nullif(0) -- prevent `#div0` error
* wrap everything with a decimal(9,4)

```sql
cast(1.0 * sum(numerator) / nullif(sum(denominator), 0) as decimal(9, 4)) 
```

## use win-fxn to create analysis



```sql
-- exclude weekends
and datename(weekday, cast(c.DateKey as date)) not in ('Saturday', 'Sunday')

-- change bool to tinyint for sums (if forgot)
alter table #t
alter column IsCaseStart tinyint

-- 7 day rolling avg comparison
-- rows between and → current day + 6 days before
-- warning! if days are not incremental, need to x-apply w full date dimension
SUM(d.CaseStartCnt) OVER (
    PARTITION BY d.OfficeCode
    ORDER BY d.DateKey
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
) AS CaseStartCnt_7BD,
SUM(d.SmileExpressCnt) OVER (
    PARTITION BY d.OfficeCode
    ORDER BY d.DateKey
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
) AS SmileExpressCnt_7BD

-- compare rolling pct to the prior week/month *as of that same weekday* (business-day lag)
-- from current row, + 5 rows up
LAG(p.SmileExpressPct_7BD,  5) OVER (PARTITION BY p.OfficeCode ORDER BY p.DateKey) AS PrevWeekPct_7BD, 
LAG(p.SmileExpressPct_7BD, 21) OVER (PARTITION BY p.OfficeCode ORDER BY p.DateKey) AS PrevMonthPct_7BD, -- 
```

Related:  [[SQL - Lag vs Lead - Rearview vs Windshield]]