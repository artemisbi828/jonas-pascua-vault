1. In SQL create value with target value
2. Put into slicer
3. Filter out Blank

```sql
case when [o].[EDW_ImportDate] < '2024-01-01' then 'Same Store Only' end as SameStoreOnlyButton,
```