```sql
select [fv].[vendorID]
from [dbo].[finVendor] as [fv]
where 1=1 and upper([fv].[vendorName]) = [fv].[vendorGroup] COLLATE Latin1_General_CS_AS

```