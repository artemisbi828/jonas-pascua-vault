
# Get EOM By All Offices, Only Valid Clinics
- There are null officekeys. These should be ignored

```sql
use EDW;
drop table if exists #t;
with snapshots
as (select cast('2024-12-31 23:59:59' as datetime2) as snapshot_dt
    union all
    select
        dateadd(second, -1, cast(dateadd(day, 1, eomonth(dateadd(month, 1, snapshot_dt))) as datetime2))
    from snapshots
    where snapshot_dt < '2026-08-01')
select
    s.snapshot_dt,
    p.OfficeKey,
    count(distinct p.patGuid) as StartNeededCount
into
    #t
from snapshots s
    join bi.Persons for system_time all p
        on s.snapshot_dt >= p.StartTime
       and s.snapshot_dt < p.EndTime
where p.ptStatCode in ('STARTNEED', 'StartNeeded')
group by s.snapshot_dt,
         p.OfficeKey
option (maxrecursion 100);

-- 

select
    row_number() over (order by t.snapshot_dt, loc.office_key) rn,
    loc.location_code,
    t.*
from #t as t
    join Playground.jbi.vw_D_Locations as loc
        on loc.office_key = t.OfficeKey
where t.OfficeKey = 14;
```

# Validation - Get EOM by 1 Office
```sql
declare @officekey int = 14 -- 14: Harker Heights
declare @snapshot_start_date datetime2 = '2026-08-01'
declare @eom datetime2 = dateadd(second, -1, @snapshot_start_date)


select
    @eom snapshot_dt,
    p.OfficeKey,
    p.PersonKey,
    p.ptStatCode
into
    #t
from bi.Persons for system_time all p
where 1 = 1
  and p.ptStatCode in ('STARTNEED', 'StartNeeded')
  and @eom >= p.StartTime
  and @eom < p.EndTime
  and p.OfficeKey = @officekey;

-- 
select
    t.snapshot_dt,
    t.OfficeKey,
    t.PersonKey,
    pat.patID,
    t.ptStatCode
from #t t
    join Playground.jbi.vw_D_Patients as pat
        on pat.PersonKey = t.PersonKey;
```