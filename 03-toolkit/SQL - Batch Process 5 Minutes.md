


**Add Index to Target**
```sql
use Playground
CREATE UNIQUE INDEX UX_case_start_atomic_conversion
ON Playground.jbi.case_start_atomic_conversion (case_start_contract_key);
```

**Core Proc**
- Make sure core proc has a where not in ()

```sql
use EDW;
set nocount on;
set xact_abort on;

declare
    @WindowSeconds int         = 300, -- 5 minutes
    @ChunkSize     int         = 500, -- tune: 100..5000 depending on runtime
    @RowsInserted  int,
    @WindowStart   datetime2(3),
    @TotalInserted bigint      = 0;

while 1 = 1 begin
    set @WindowStart = sysdatetime();
    set @RowsInserted = 0;

    -- inner loop: keep taking chunks until 5 minutes elapsed OR no more rows
    while datediff(second, @WindowStart, sysdatetime()) < @WindowSeconds begin
        begin try
            begin tran;


<<INSERT CODE>>

            set @RowsInserted = @@ROWCOUNT;
            set @TotalInserted += @RowsInserted;

            commit;

            -- No more work left => exit both loops
            if @RowsInserted = 0 break;

        end try
        begin catch
            if @@TRANCOUNT > 0 rollback;
;           throw;
        end catch;
    end;

    -- If this window inserted nothing, you are done (idempotent exit)
    if @RowsInserted = 0 break;

-- optional: small pause to reduce pressure / allow log flush
-- WAITFOR DELAY '00:00:01';
end;

select @TotalInserted as total_inserted;
```