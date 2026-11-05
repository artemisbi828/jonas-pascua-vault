XLS Friendly

```sql
-- ========================
-- GROUP W SUBTOTALS 
-- ========================

-- GROUP NEW ROW 1
-- #1: Union All
select
    OfficeType,
    IsPreConversion,
    sum(ProductionAmount) ProductionAmount
from #a
group by OfficeType,
         IsPreConversion
union all
select 'TOTAL', null, sum(ProductionAmount) ProductionAmount from #a;

-- ========================
-- GROUP NEW ROW 2
-- #2: `Group By Rollup` + `Grouping` → adds extra row w null for rollup-1, adds an extra row w null for roll-up2
select
    OfficeType,
    IsPreConversion,
    case when OfficeType is null then 'RollUp-1 SubTotal' -- if only 1 rollup you can use coalesce
         when IsPreConversion is null then 'Rollup-2 SubTotal' end as Section,
    sum(ProductionAmount) ProductionAmount,
    grouping(officeType) OrderingTQN --grouping_id() does same thing
from #a
group by rollup(OfficeType, IsPreConversion);

-- ========================
-- GROUPING NEW COLUMN
-- #3: `Group By` + `Windowed Function`
select
    OfficeType,
    IsPreConversion,
    sum(ProductionAmount) ProductionAmount,
    sum(sum(ProductionAmount)) over (partition by OfficeType) as ProductionAmountPerOfficeType
from #a
group by OfficeType,
         IsPreConversion;
```