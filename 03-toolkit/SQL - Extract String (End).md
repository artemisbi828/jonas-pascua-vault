To get suffix (end) ...
1. reverse the text
2. get charindex from left → so we know charindex to use for step3
3. use right on the column + the charindex to cut from right


```sql
declare @string table (Region varchar(16));
insert into @string ([Region]) values ('Region 1'), ('Region 10'), ('Region 01');
 
-- how many characters from the end? 
select Region from @string;
select reverse(Region)from @string; -- reverse it
select charindex(' ', reverse(Region))from @string; -- charindex to find delineator position from left
select right(Region, charindex(' ', reverse(Region))) Region from @string; -- use right() to cut it from right using charindex(delineate)
```