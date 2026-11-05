Related: [[Math - Divisor, Ratio vs Proportion|Integer Quotient vs Decimal Quotient]]
- quotient + 1 


`Split + Remainder Method`: Use RN to create tie breaker row, give +1 until no remainder remains
1. zero handling pattern = 0 
2. calculate rn.seq_office per team vs total_office_qty per team
3. calculate modulo remainder (10 goal % 6 offices = 4 remainder)
4. give each office `quotient + 1` 

5. if RN <= reaminder, then give 1 (overflow)
6. 
7. divide evenly via modulo (%)
8. create RN --> line up offices and give ticket
9. calc division + remainder
10. compare RN vs remainder (ticket queue vs stock available) --> if RN <= remainder --> give 1, else 0 (out-of-stock)

```sql
-- TSQL math behavior based on datatypes
-- 5 / 3 = 1 --> division of int.numerator --> int
-- 5.0 / 3 = 1.666 --> 
-- 5 % 3 = 2 --> remainer after division (modulo operator)

;with cte1
as (select
        t.TeamName,
        o.OfficeCode,
        10 as TeamGoal,
        count(*) over (partition by o.TeamId) OfficeCount,
        o.TeamId,
        row_number() over (partition by o.TeamId order by o.OfficeCode) RN
    from Lake.sd.Offices as o
        inner join Lake.sd.Teams as t
            on t.Id = o.TeamId
    where 1 = 1
      and o.IsActive = 1
      and o.Cloud9ConversionDate is not null
      and o.TeamId in (297, 10, 78))
select
    *,
    case when RN = 1 then cte1.TeamGoal % cte1.OfficeCount end Remainder_Modulo,
    cte1.TeamGoal / cte1.OfficeCount IntQuotient,
    case when cte1.RN <= (cte1.TeamGoal % cte1.OfficeCount) then 1 else 0 end HasRemainderStock_GiveExtra,
    -- 1: orphan handling | empty parent
    case when cte1.OfficeCount = 0 then 0
         else
             -- 2: allocate TeamGoal down to Offices using "even split + remainder" method: 
             cte1.TeamGoal / cte1.OfficeCount + case when cte1.RN <= (cte1.TeamGoal % cte1.OfficeCount) then 1 else 0 end
    --
    end TotalAllocation
from cte1
order by cte1.TeamId,
         RN;
```

![Pasted image 20260225131148.png]