update statement, do not use from
```sql
update cs 
set concept_tags = 'business_key'
where concept_tags is null and ends_with(after, '_sk')
;
```