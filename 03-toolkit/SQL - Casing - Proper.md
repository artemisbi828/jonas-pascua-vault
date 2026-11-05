#status/deferred/quick-paste-merge-later 
```sql
upper(left(PrStatDescription,1)) 
+ lower(substring([PrStatDescription], 2 -- 2 b/c after 1st string
	, len([PrStatDescription])
)) as GroupPatientStatus
```

```sql
select trim(upper(left([vendorName], 1)) + lower(substring([vendorName], 2, len([vendorName]))))
```