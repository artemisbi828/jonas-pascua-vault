```sql
use SmileDoctorsEDW; -- Fabric
go

-- 
select
    o.DivisionName,
    o.RegionName,
    o.TeamName,
    o.OfficeName,
    left(vna.DateKeyCreated, 7) YearMonth,
    sum(vna.IsNPENetAdded) IsNPENetAdded
from SmileDoctorsEDW.Scheduling.vw_NPEAdded as vna
    join SmileDoctorsODS.extenders.Offices as o
        on o.locGuid = vna.locGUID COLLATE Latin1_General_100_CI_AS_KS_WS_SC_UTF8
       and o.SourceSystemId = vna.SourceSystemId
where 1 = 1
  and vna.DateKeyCreated >= '2026-01-01'
  and vna.DateKeyCreated < getdate()
group by o.DivisionName,
         o.RegionName,
         o.TeamName,
         o.OfficeName,
         left(vna.DateKeyCreated, 7);

```