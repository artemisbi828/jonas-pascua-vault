TRIGGER VS CDC
  Trigger -- Trans Lock is 2x as long (dbs intrusive); can be long term; 
  CDC -- log files; less dbs intrusive; not designed for long term -- 3 days; 

```sql
select
    'disable trigger ' + tr.name + ' on ' + replace(translate(tr.name, 'bi_', 'bi.'), 'trg.', '') + ';' execsql1,
    'enable trigger ' + tr.name + ' on ' + replace(translate(tr.name, 'bi_', 'bi.'), 'trg.', '')  + ';' execsql2
from sys.triggers as tr
    inner join sys.tables as tbl
        on tbl.object_id = [tr].[parent_id]
where 1 = 1
  and tr.name like 'trg_%'
  and [tr].[is_disabled] = 0; -- 1 = disabled that needs to be activated || 0 = enabled triggers
```

