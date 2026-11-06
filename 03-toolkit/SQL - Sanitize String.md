```sql
declare @patid nvarchar(16) = N' GCE090489
';
set @patid = trim(replace(replace(@patID, char(13), ''), char(10), ''))
```