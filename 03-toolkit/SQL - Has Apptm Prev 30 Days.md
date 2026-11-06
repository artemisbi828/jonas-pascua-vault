function taken from Gregg to bring in another appointment within a 30 day interval
lag pulls in a prev.apptm

```sql
declare
    @PersonKeyPatient    int,
    @AppointmentDatetime datetime2,
    @AppointmentKey      int;

set @PersonKeyPatient = 580991;
set @AppointmentDatetime = '2023-08-22 16:15:00';
set @AppointmentKey = 7527201;


declare @fromDatetime as datetime2 = dateadd(day, -30, @AppointmentDatetime);

--return cast(iif(
--                exists (
--                    select top (1)
--                           1 hasPC
select 
    * -- added in for visualization
from (
    select
        apptPrev.AppointmentKey,
        --lag(apptPrev.DateKey) over (order by apptPrev.DateKeyCreated, cast(apptkey.apptGuid as varchar(64)) asc) prev
        lag(apptPrev.DateKey) over (order by apptPrev.AppointmentDatetime, cast(apptkey.apptGuid as varchar(64)) asc) prev
    from sd.Appointments apptPrev
        inner join sd.AppointmentKeys apptkey
            on apptkey.AppointmentKey = apptPrev.AppointmentKey
    where 1 = 1
      and apptPrev.IsNPE = 1
      and apptPrev.PersonKeyPatient = @PersonKeyPatient
      and apptPrev.AppointmentDatetime >= @fromDatetime
      and apptPrev.AppointmentDatetime <= @AppointmentDatetime
) tmp
where tmp.prev is not null
  and tmp.AppointmentKey = @AppointmentKey;
--),
--1,
--0) as bit);
```