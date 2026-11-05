remove `test` and `do not use`
match on -- DOB, first name, last name
2nd layer match +

create a:
- gold.patient__ofi
- scd2
	- scd2.patient__cc9
	- scd2.patient__ofi
	- scd2.xwalk__patient__oficc9


```sql

with cte1
as (select
        p.PATIENTID as ofi_patid,
        p.FIRSTNAME first_name,
        p.LASTNAME last_name,
        cast(p.DATEOFBIRTH as date) date_of_birth,
        p.ADDRESS1 address_1,
        p.ADDRESS2 address_2,
        p.ADDRESS3 address_3,
        p.CITY city,
        p.STATEABBREVIATION state_abbrev,
        p.POSTALCODE postal_code,
        row_number() over (partition by p.PATIENTID order by p.DSS_LOAD_DATE desc, p.UPDATEDON desc) rn
    from LHS_DEV_Data_Solutions.orthofi_dbo.Patients as p
    where p.PATIENTID in (select patientId from LHS_DEV_Data_Solutions.orthofi_dbo.Contracts)
--
),
     cte2
as ( -- 
   select
       p.ofi_patid,
       p.first_name,
       p.last_name,
       p.date_of_birth,
       p.address_1,
       p.address_2,
       p.address_3,
       p.city,
       p.state_abbrev,
       p.postal_code,
       cast(nativeId as uniqueidentifier) patGUID
   --p.rn
   from cte1 p
       left join LHS_DEV_Data_Solutions.orthofi_dbo.PATIENT_CROSS_REFERENCE x
           on x.orthoFiId = p.ofi_patid
   where 1 = 1
     and p.rn = 1
     and x.crossReferenceSystemName = 'Cloud9')
-- 488,359
-- 225,132
-- insert into gold.patient__ofi (ofi_patid, first_name, last_name, date_of_birth, address_1, address_2, address_3, city, state_abbrev, postal_code, patGUID)
select * from cte2;
```