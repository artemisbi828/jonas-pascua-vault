
# Version 1
```sql
select
    'alter table [' + [s].[name] + '].[' + [o].[name] + '] drop constraint [' + [t].[name] + ']' as [execsql], *
from [sys].[all_objects] as [t]
    inner join [sys].[schemas] as [s]
        on [s].[schema_id] = [t].[schema_id]
    left join [sys].[all_objects] as [o]
        on [o].[object_id] = [t].[parent_object_id]
where 1 = 1
  and [s].[name] like '%sd%' -- schema
  and [o].[name] like '%OfficeGoal%' -- table
order by case when [t].[type_desc] = 'user_table' -- object type 
    then          1
              else 2 end,
         [t].[modify_date] desc;
return

```

# Ver 2.0.0
```sql
SELECT 
    tc.CONSTRAINT_NAME,
    tc.CONSTRAINT_TYPE,
    kcu.COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
    ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
    AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
    AND tc.TABLE_NAME = kcu.TABLE_NAME
WHERE tc.TABLE_SCHEMA = 'docm'
  AND tc.TABLE_NAME = 'tables'
ORDER BY tc.CONSTRAINT_TYPE, tc.CONSTRAINT_NAME;
```

# Find Constraint Referencing Table
```sql
SELECT
    fk.name AS ForeignKeyName,
    OBJECT_SCHEMA_NAME(fk.parent_object_id) AS ReferencingSchema,
    OBJECT_NAME(fk.parent_object_id) AS ReferencingTable,
    COL_NAME(fkc.parent_object_id, fkc.parent_column_id) AS ReferencingColumn
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc 
  ON fk.object_id = fkc.constraint_object_id
WHERE fk.referenced_object_id = OBJECT_ID('YourSchema.YourTable')
ORDER BY ReferencingSchema, ReferencingTable, ForeignKeyName, ReferencingColumn;
```

# Drop Column from Constraint
```sql
declare @constraint nvarchar(75) = 'UQ__objects_tables_views_columns_Key' -- N'DF__Appointme__Loade__756D6ECB';
declare @msg nvarchar(max);

select
    --ao.name as constraint_name,
    --col.name column_name,
    --s.name + '.' + object_name(ao.parent_object_id) table_name, ''
    @msg = 'alter table ' + s.name + N'.' + object_name(ao.parent_object_id) + N' drop constraint [' + isnull(ao.name,'') + N']' --
           + char(13) + char(10) + N'GO' + +char(13) + char(10) -- 
           + N'alter table ' + s.name + N'.' + object_name(ao.parent_object_id) + N' drop column [' + isnull(col.name,'') + N']'
from sys.all_objects as ao
    inner join sys.schemas as s
        on s.schema_id = ao.schema_id
    left join (
        select
            dc.object_id,
            c.name
        from sys.default_constraints dc
            join sys.columns c
                on dc.parent_object_id = c.object_id
               and dc.parent_column_id = c.column_id
    ) col
        on col.object_id = ao.object_id
where ao.name = @constraint or @constraint is null;

print @msg;
```

# Add Constraints
```sql
constraint PK__MyTableName
primary key clustered (MyColumnKeyName),

constraint FK__MyChildTableName__MyColumnName
foreign key (MyBridgeColumn)
references map.MyParentTable (MyBridgeColumn),

constraint UQ__MyTableName
unique (MyColumnName1, MyColumnName2)

alter table map.MonthlyOutcomes
add constraint UQ__map_MonthlyOutcomes__Outcome
unique(Outcome)
```