2026-09-14 06:00 PM
## New Procs and Objects

contracts
- txplancode from centralc9
- 

```
1. stage patients for appts touched (up to yesterday)
2a. rehydrate dim_patient
2b. load core appointment
2. hydrate creation data
3. hydrate scheduled day prior

DANGEROUS ASSUMPTIONS
-- all objects are replicated and mirror to fabric

USING DASHBOARD
VERSION 1.0
1. I want to see how well the team is doing vs LY vs 
2. I want to understand and trust the data -- loading regularly, stable.
3. see creation appointment
   - slice by person, slice by manager? 
4. see clinic vs rollup performance (dynamic top 10, 3)
   
   
Header Bar: 
-- Appointments Created This Month
-- Net New Patients This Month
-- Conversions From Appointments Created This Month

Top 10 clinics created? June vs July
See trendlines 
Net new Patient


metric <-- metric x measure (relationship) <-- measure <-- column <-- table.edw (unified -- surrogate key) 
	<-- table.appointment_cc9
	<-- table.contract_cc9 -- natural key, surrogate key, datetime local
	<-- table.contract_ofi -- datetime utc
	<-- table.edw-dimension <-- table.scd2

```
### Idemtopic Procs
1. get distinct patients from
	1. patients touched (appointment-status-history)
	2. appointments (appointment)

### Patient Dim


```sql
--create table scd2.cl9_empGUID__x__employee_code (
--    scd2_id bigint identity not null,
--    [SourceSystemId] smallint not null,
--    [empGUID] uniqueidentifier not null,
--    [EmployeeCode] int not null,
--    [SD_LastModifiedUtc] datetime2(6),
--    [persLastModified] datetime2(6),
--    [load_datetime_utc] datetime2(6)
--);

declare @now datetime2(6) = sysutcdatetime();
-- have to add process id vs manual input / correction

with cte1
as (select
        e.SourceSystemId,
        cast(e.empGUID as uniqueidentifier) empGUID,
        e2.EmployeeCode,
        max(p.SD_LastModifiedUtc) SD_LastModifiedUtc,
        max(p.persLastModified) persLastModified
    from LHS_DEV_Data_Solutions.cc9_dbo.Employee as e
        join LHS_DEV_Data_Solutions.cc9_dbo.Person as p
            on p.persGUID = e.persGUID
           and p.SourceSystemId = e.SourceSystemId
        join LHS_DEV_Data_Solutions.lake_sd.Employees as e2
            on e2.EmployeeCode = try_cast(p.persSocial as int)
    group by e.SourceSystemId,
             cast(e.empGUID as uniqueidentifier),
             e2.EmployeeCode)
insert into scd2.cl9_empGUID__x__employee_code (SourceSystemId, empGUID, EmployeeCode, SD_LastModifiedUtc, persLastModified, load_datetime_utc)
select
    s.SourceSystemId,
    s.empGUID,
    s.EmployeeCode,
    s.SD_LastModifiedUtc,
    s.persLastModified,
    @now as load_datetime_utc
from cte1 s
where not exists (
    select
        1
    from scd2.cl9_empGUID__x__employee_code as t
    where 1 = 1
      and t.empGUID = s.empGUID
      and t.SourceSystemId = s.SourceSystemId
      and t.EmployeeCode = s.EmployeeCode
);

```
# Save Point
## Fabric Query Cross Check

```sql
-- 
--select * from gold.appointment as a where a.create_date = '2026-08-04';

-- 
select
    a.created_by_employee_code, count(*) qty 
from gold.appointment as a
    join edw.appointment_type as at
        on at.appttypCode = a.appttypCode
       and at.is_npc = 1
    join edw.vw_d__employee as vde
        on vde.employee_code = a.created_by_employee_code
       and vde.job_title_category = 'NPC'
       and a.create_date = '2026-08-04'
       group by a.created_by_employee_code
       order by 2 desc
       ;

       select
    * 
from gold.appointment as a
    join edw.appointment_type as at
        on at.appttypCode = a.appttypCode
       and at.is_npc = 1
    join edw.vw_d__employee as vde
        on vde.employee_code = a.created_by_employee_code
       and vde.job_title_category = 'NPC'
       and a.create_date = '2026-08-04'
       where a.created_by_employee_code = 122114
       order by a.create_date, patid
       ;
```

## AZP Query Cross Check
```sql
---- 
--select * from gold.dim__appointment_enrichment as dae
--where dae.create_date = '2026-08-04'

select
    vfnac.created_by_employee_code, count(*) qty
from gold.vw_f__npc__appointments_created as vfnac
where 1 = 1
  and vfnac.create_date = '2026-08-04'
  group by created_by_employee_code
  order by 2 desc
  ;

  select
    * 
from gold.vw_f__npc__appointments_created as vfnac
where 1 = 1 
and vfnac.created_by_employee_code = 122114
  and vfnac.create_date = '2026-08-04'
  order by create_date, patid   
  ;


  -- 
  select top 5 * from gold.dim__appointment_enrichment as dae
  where dae.patGUID = 'A8555ADE-5863-45B6-93BD-14739B5ED259'
```
# 1. Flow
```sql

-- create or alter proc dataops.usp_orchestrate__npc_dashboard_data as

-- load staging.patient__cc9 table; specify date
exec dataops.usp_load__staging__patient_cc9__from__appointments__cc9 '2026-09-13', '2026-09-17'
go
-- 2: sync gold.patient_sd
exec dataops.usp_load__gold__patient_sd__from__staging__patient__cc9
go
-- 3: load appointment-core --> gold.appointment
exec dataops.usp_load__gold__appointment__from__staging__patient__cc9
go
-- 4: update create data
exec dataops.usp_enrich__gold_appointment_create
go
-- 5: update day_prior_scheduled
exec dataops.usp_enrich__gold_appointment__scheduled_day_prior
go
-- 6: rebuild enrichment table for is net new patient
exec dataops.usp_rebuild__gold_appointment_is_net_new_patient 
go
```



```

# 5. Trunc and Reload Enrichment Tables

```sql


/* is contract start conversion */
truncate table gold.appointment__is_contract_start_conversion;
go
insert into gold.appointment__is_contract_start_conversion
select
    vfac.SourceSystemId,
    vfac.apptGUID,
    tfp.tfpGUID,
    1 as is_contract_start_conversion,
    tfp.tfpStartDate
from npc.vw__f__appointment_created as vfac
    join LHS_DEV_Data_Solutions.cc9_dbo.TreatmentFeePlan as tfp
        on tfp.patGUID = vfac.patGUID
       and tfp.SourceSystemId = vfac.SourceSystemId
    join LHS_DEV_Data_Solutions.cc9_dbo.TransactionType as tt
        on tt.ttypGUID = tfp.ttypGUID
       and tt.SourceSystemId = tfp.SourceSystemId
    join edw.txplan as t
        on t.tx_plan_code = tt.ttypCode
where 1 = 1
  and vfac.apptstCode_current = 'DISM'
  and tfp.tfpStartDate >= vfac.occurence_date
  and t.is_contract_start = 1;
go
```