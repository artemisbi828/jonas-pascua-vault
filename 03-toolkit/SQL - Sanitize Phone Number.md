```sql
declare @contactinfo varchar(128) 
declare @contactinforaw varchar(128) = @contactinfo;
set @contactinforaw = replace(@contactinforaw, '(', '');
set @contactinforaw = replace(@contactinforaw, ')', '');
set @contactinforaw = replace(@contactinforaw, '[', '');
set @contactinforaw = replace(@contactinforaw, ']', '');
set @contactinforaw = replace(@contactinforaw, '@', '');
set @contactinforaw = replace(@contactinforaw, '_', '');
set @contactinforaw = replace(@contactinforaw, '.', '');
set @contactinforaw = replace(@contactinforaw, ' ', '');
```

