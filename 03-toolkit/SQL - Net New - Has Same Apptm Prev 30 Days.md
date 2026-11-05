STEP1 -- use lag/lead to group rows together, then:
STEP2 -- 
- use case when logic 
- use a separate windows step → RN tag the group

using another partition level allows for a tie break, plus the order by is the main tie break
order by case when 1 else 0 desc is a good tqn

```sql
-- AZP QUERY
-- trying to get a real "NET NEW" model where we dedup by patient, location, typecode.
-- we don't need garbage entries in our appointments model
-- since SCHD --> RESCH --> generates a new apptguid (diff chair, time) we want t chain them and ignore the older created datetime, we want the newest

use CentralC9; -- AZP
go

declare @testlogic bit = 0; -- or 0 to see everything
declare @patid varchar(16) = 'A2B004468';
declare @today date = getdate()at time zone 'UTC' at time zone 'Eastern Standard Time';


;
with cte1
as (select
        l.locParentCode as OfficeCode,
        p.patID,
        cast(a.apptDateTime as date) Apptm_DateKey,
        a.apptDateTime,
        at.appttypCode,
        ast.apptstCode,
        /* id */
        a.SourceSystemId,
        apptGUID
    from CentralC9.dbo.Appointment as a
        inner join CentralC9.dbo.Patient as p
            on p.SourceSystemId = a.SourceSystemId
           and p.patGUID = a.patGUID
        inner join CentralC9.dbo.AppointmentType as at
            on at.SourceSystemId = a.SourceSystemId
           and at.appttypGUID = a.appttypGUID
        inner join CentralC9.dbo.AppointmentStatus as ast
            on ast.SourceSystemId = a.SourceSystemId
           and ast.apptstGUID = a.apptstGUID
        left join Lake.C9.AppointmentGroups as ag
            on ag.ApptTypeCode = at.appttypCode
        left join CentralC9.dbo.ScheduleView as sv
            on sv.SourceSystemId = a.SourceSystemId
           and sv.schdvwGUID = a.schdvwGUID
        -- get chair
        left join CentralC9.dbo.ScheduleColumn as sc
            on sc.SourceSystemId = a.SourceSystemId
           and sc.schdcolGUID = a.schdcolGUID
        -- get location apptm
        left join CentralC9.dbo.Location as l
            on l.SourceSystemId = sv.SourceSystemId
           and l.locGUID = sv.locGUID
    where 1 = 1
      and p.patID = @patid
--and at.appttypCode = '402'
--
),
     cte2
as (select
        -- #2: by group + same30day group, prioritizing apptstCode types and most recent apptDateTime as the valid apptm
        case when row_number() over (partition by
                                         patID,
                                         OfficeCode,
                                         appttypCode,
                                         IsSame30DayGroup
                                     order by case when apptstCode in ('DISM', 'CANC', 'RESCH') then 1 else 0 end desc,
                                              apptDateTime desc
                               ) = 1 then 1
             else null end IsNetNew,
        *
    from (
        select
            -- #1: datediff w lag group
            case when datediff(day, lag(cte1.apptDateTime, 1, cte1.apptDateTime) over (partition by patID, cte1.OfficeCode, appttypCode order by cte1.apptDateTime asc), cte1.apptDateTime) < 30 then 1
                 else 0 end as IsSame30DayGroup,
            datediff(day, lag(cte1.apptDateTime, 1, cte1.apptDateTime) over (partition by patID, cte1.OfficeCode, appttypCode order by cte1.apptDateTime asc), cte1.apptDateTime) DateDiffByKey,
            *
        from cte1
    ) inr )
-- 
select * from cte2 where IsNetNew = 1 order by cte2.apptDateTime asc;
```