```sql
	
use EDW;
set tran isolation level read uncommitted;

/* 
-- or msdb
-- exec sp_start_job  'EDW.BI - Load' -- to run job
*/


select top 200
       *
from (
    -- main table -- shows logs for the past 2 days
    select
        [jb].[name] JobName,
        [a].[step_id],
        [a].[step_name],
        case [a].[run_status]
             when 0 then '0-Failed'
             when 1 then '1-Succeeded'
             when 2 then '2-Retry'
             when 3 then '3-Canceled'
             when 4 then '4-InProgress'
             else cast([a].[run_status] as varchar(16)) end [RunStatus],
        a.run_date,
        a.run_time,
        convert(varchar(128), dateadd(second, [a].[run_duration], 0), 108) as 'Duration_hhmmss'
    from msdb.dbo.[sysjobhistory] as a
        inner join msdb.dbo.sysjobs as jb
            on [jb].[job_id] = [a].[job_id]
    where 1 = 1
    union
    -- full history maybe a Gregg thing, since 2022-10-12
    select
        [jb].[name] JobName,
        [a].[step_id],
        [a].[step_name],
        case [a].[run_status]
             when 0 then '0-Failed'
             when 1 then '1-Succeeded'
             when 2 then '2-Retry'
             when 3 then '3-Canceled'
             when 4 then '4-InProgress'
             else cast([a].[run_status] as varchar(16)) end [RunStatus],
        a.run_date,
        a.run_time,
        convert(varchar(128), dateadd(second, [a].[run_duration], 0), 108) as 'Duration_hhmmss'
    from msdb.dbo.sysjobhistoryall as a
        inner join msdb.dbo.sysjobs as jb
            on [jb].[job_id] = [a].[job_id]
    where 1 = 1
) inr;
```
