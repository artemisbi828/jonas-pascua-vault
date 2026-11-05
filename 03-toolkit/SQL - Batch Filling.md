1. Row Count First
2. Use an Indexed Column like DateKeyCreated

|Rows|Recommendation|
|---|---|
|< 100k|One load|
|100k - 1M|Monthly|
|1M - 10M|Weekly|
|10M+|Daily|
|50M+|Hourly or key ranges|

3. For a Year, go by week
4. Dupe Sentinel 

```sql
while 1 = 1
begin

    ;with cte as
    (
        select top (50000)
            a.AppointmentKey
        from EDW.sd.Appointments a
        where a.DateKeyCreated >= '2025-01-01'
          and a.DateKeyCreated <  '2026-09-08'
          and not exists
          (
              select 1
              from gold.dim__appointment_enrichment e
              where e.AppointmentKey = a.AppointmentKey
          )
        order by a.AppointmentKey
    )

    insert ...
    from cte
    ...

    if @@rowcount = 0
        break;

end
```

## Raise Error No Wait

```sql
-- basic version
raiserror('inserted %d rows', 0, 1, @@ROWCOUNT) with nowait;
```

```sql
declare @rows int;
declare @batch int = 0;

while 1=1
begin

    set @batch += 1;

    ...

    set @rows = @@ROWCOUNT;

    raiserror(
        'Batch %d inserted %d rows',
        0,
        1,
        @batch,
        @rows
    ) with nowait;

    if @rows = 0
        break;
end

```

## Show % Complete
### Total Count
```sql
declare @total bigint;

select @total =
(
    select count(*)
    from
    (
        select
            ak.SourceSystemId,
            ak.apptGuid
        from EDW.sd.Appointments a
        join EDW.sd.AppointmentKeys ak
            on ak.AppointmentKey = a.AppointmentKey
        where a.DateKeyCreated >= '2025-01-01'
          and a.DateKeyCreated <  '2026-09-08'
        group by
            ak.SourceSystemId,
            ak.apptGuid
    ) x
);
```

### Progress
Batch 1 | Rows=50000 | Progress=8.11%
Batch 2 | Rows=50000 | Progress=16.22%
Batch 3 | Rows=50000 | Progress=24.33%

```sql
declare @loaded bigint;

select @loaded =
(
    select count(*)
    from gold.dim__appointment_enrichment
);

raiserror(
    'Batch %d | Rows=%d | Progress=%0.2f%%',
    0,
    1,
    @batch,
    @rows,
    @loaded * 100.0 / @total
) with nowait;
```
### Print
Buffered though, won't see updates until much later
```sql
declare @rows int;
declare @batch int = 0;

while 1=1
begin

    set @batch += 1;

    ...

    set @rows = @@ROWCOUNT;

    print concat(
        convert(varchar(19), getdate(), 120),
        ' Batch=', @batch,
        ' Rows=', @rows
    );

    if @rows = 0
        break;
end
```