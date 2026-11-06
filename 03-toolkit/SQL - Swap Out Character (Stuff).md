Use stuff to swap out a position + len(char) with a string

```sql

-- we want to remove that first comma "," in ",2024"
declare @sql nvarchar(max)
set @sql = ',2024-01, 2024-02'
select @sql

-- replace 1st character, 1 length, with "''"
set @sql = (select stuff(@sql, 1,1, ''))
```

---
#status/deferred/quick-paste-merge-later 

FIND AND REPLACE 
select stuff(@string, start, length, @char_to_insert into length

INSERTS string at end into string at beginning 
select stuff(@string, @startchar, @end


```sql

declare @string nvarchar(16) = N'12345';
select @string, 
/* replaces 2nd char with 3 */
stuff(@string, 2, 1, '3'), 
/* starting with 2nd char replace 4 characters with '3333'*/
stuff(@string, 2, 4, '3333'), 
/* starting with 2nd char replace 4 characters with '3' -- truncates*/
stuff(@string, 2, 4, '3');
```
