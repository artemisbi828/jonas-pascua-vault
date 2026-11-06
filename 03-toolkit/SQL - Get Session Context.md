#status/deferred/quick-paste-merge-later 
```sql
 T-SQL Global Variable
 
use Snowflake
go
 
exec sp_set_session_context 'tableName', 'D_APPOINTMENT_STATUS';  
declare @tbl varchar(max) = convert(varchar(max), session_context(N'tableName')); exec dbo.CreateStageProcedure @tableName = @tbl, @run = 1;
```