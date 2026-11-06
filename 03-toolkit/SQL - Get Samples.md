1. create a sample popln → Apptms.IsNPE = 1 past 60 days
2. create pairs (join to itself) where current vs previous appointments 
> [!warning] remember to exclude from itself
3. want apptms greater than datekey, the same
4. use @samplesize
```sql
select top (@samplesize), 'GROUP1' as Category, ... where {Condition1}
union all 
select top (@samplesize), 'GROUP2' as Category, ... where {Condition2}
```


# Example 
2026-01-12 01:41 PM
```sql
declare @ExamplesPerCategory int = 20;

with cte1
as (select
        a.PersonKeyPatient,
        a.AppointmentKey,
        a.DateKey,
        ast.AppointmentStatusDesc,
        a.IsNetAdded
    from sd.Appointments as a
        left join sd.AppointmentStatuses as ast
            on ast.AppointmentStatusKey = a.AppointmentStatusKey
    where a.IsNPE = 1
      and a.DateKey >= dateadd(day, -60, getdate())),
     pairs
as (
   /*
      Build unique, directed pairs per patient:
      - later.DateKey > earlier.DateKey
      - OR if same day, later.AppointmentKey > earlier.AppointmentKey
    */
   select
       a.PersonKeyPatient,
       a.AppointmentKey as ApptKeyEarlier,
       b.AppointmentKey as ApptKeyLater,
       a.DateKey as DateEarlier,
       b.DateKey as DateLater,
       a.AppointmentStatusDesc as StatusEarlier,
       b.AppointmentStatusDesc as StatusLater,
       datediff(day, a.DateKey, b.DateKey) as DateDiffDays,
       b.IsNetAdded
   from cte1 a
       join cte1 b
           on b.PersonKeyPatient = a.PersonKeyPatient
           and b.AppointmentKey <> a.AppointmentKey
          and (b.DateKey > a.DateKey or (b.DateKey = a.DateKey and b.AppointmentKey > a.AppointmentKey))),
     cte_3
as (
   /*
   Return one (or more via @ExamplesPerCategory) example row(s) per category.
   */
   select top (@ExamplesPerCategory)
          'DIFF_GT_30' as Category,
          p.PersonKeyPatient,
          p.ApptKeyEarlier,
          p.DateEarlier,
          p.StatusEarlier,
          p.ApptKeyLater,
          p.DateLater,
          p.StatusLater,
          p.DateDiffDays,
          IsNetAdded
   from pairs p
   where p.DateDiffDays > 30
   union all
   select top (@ExamplesPerCategory)
          'DIFF_LT_30' as Category,
          p.PersonKeyPatient,
          p.ApptKeyEarlier,
          p.DateEarlier,
          p.StatusEarlier,
          p.ApptKeyLater,
          p.DateLater,
          p.StatusLater,
          p.DateDiffDays,
          IsNetAdded
   from pairs p
   where p.DateDiffDays > 0
     and p.DateDiffDays < 30
   union all
   /* Prefer exact =30; if none, fallback to >=30 via a priority flag */
   select top (@ExamplesPerCategory)
          'DIFF_EQ_30_OR_GTE' as Category,
          q.PersonKeyPatient,
          q.ApptKeyEarlier,
          q.DateEarlier,
          q.StatusEarlier,
          q.ApptKeyLater,
          q.DateLater,
          q.StatusLater,
          q.DateDiffDays,
          IsNetAdded
   from (
       select
           p.*,
           cast(0 as int) as pref
       from pairs p
       where p.DateDiffDays = 30
       union all
       select
           p.*,
           cast(1 as int) as pref
       from pairs p
       where p.DateDiffDays >= 30
   ) q
   union all
   select top (@ExamplesPerCategory)
          'SAME_DAY_EARLIER_CANCEL_OR_RESCH' as Category,
          p.PersonKeyPatient,
          p.ApptKeyEarlier,
          p.DateEarlier,
          p.StatusEarlier,
          p.ApptKeyLater,
          p.DateLater,
          p.StatusLater,
          p.DateDiffDays,
          IsNetAdded
   from pairs p
   where p.DateDiffDays = 0
     and p.StatusEarlier in ('CANC', 'RESCH')
   union all
   select top (@ExamplesPerCategory)
          'SAME_DAY_EARLIER_NOT_CANCEL_RESCH' as Category,
          p.PersonKeyPatient,
          p.ApptKeyEarlier,
          p.DateEarlier,
          p.StatusEarlier,
          p.ApptKeyLater,
          p.DateLater,
          p.StatusLater,
          p.DateDiffDays,
          IsNetAdded
   from pairs p
   where p.DateDiffDays = 0
     and (p.StatusEarlier is null or p.StatusEarlier not in ('CANC', 'RESCH')))
-- 
select
    Category,
    PersonKeyPatient,
    ApptKeyEarlier,
    DateEarlier,
    StatusEarlier,
    ApptKeyLater,
    DateLater,
    StatusLater,
    DateDiffDays,
    IsNetAdded
from cte3;
```