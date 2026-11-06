Where 1=1 and 1=2 allows for easy read and easy formatting although can be considered fluff as well

# Functionally The Same
Where 1=2 is just used for easy reading

```sql
-- #1 : minimalist
select * from EDW.bi.dim_AppointmentTypes as dat
where dat.IsNewPatientExam = 1
     or dat.IsRisingStar = 1
     or dat.appttypcode = '157' -- proposed by Renee 2026-03-06 12:42 PM #INC-5793

-- #2 : standard 1=1
select * from EDW.bi.dim_AppointmentTypes as dat
where 1 = 1
  and (
      dat.IsNewPatientExam = 1
     or dat.IsRisingStar = 1
     or dat.appttypcode = '157' -- proposed by Renee 2026-03-06 12:42 PM #INC-5793
  );
  
-- #3 : 1=2 (false --> so add each similar to a stack)
select * from EDW.bi.dim_AppointmentTypes as dat
where 1 = 2
	 or dat.IsNewPatientExam = 1
     or dat.IsRisingStar = 1
     or dat.appttypcode = '157' -- proposed by Renee 2026-03-06 12:42 PM #INC-5793
```