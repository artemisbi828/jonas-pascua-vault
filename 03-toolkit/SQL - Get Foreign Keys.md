#status/deferred/quick-paste-merge-later 

```sql
-- only works for fkeys
declare @tablenamenoschema nvarchar(max) = N'H_Customers';
 
select
    object_name([f].[parent_object_id]) [TableName],
    col_name([fc].[parent_object_id], [fc].[parent_column_id]) [ColName]
from [sys].[foreign_keys] as [f]
    inner join [sys].[foreign_key_columns] as [fc]
        on [f].[object_id] = [fc].[constraint_object_id]
    inner join [sys].[tables] [t]
        on [t].[object_id] = [fc].[referenced_object_id]
where object_name([f].[referenced_object_id]) = @tablenamenoschema;
```

```sql
SELECT  
--obj.NAME AS FK_NAME,
    sch.NAME AS [schema_NAME],
    tab1.NAME AS [table],
    col1.NAME AS [column]
    --tab2.NAME AS [referenced_table],
    --col2.NAME AS [referenced_column]
FROM sys.foreign_key_columns fkc
INNER JOIN sys.objects obj
ON obj.object_id = fkc.constraint_object_id
INNER JOIN sys.tables tab1
ON tab1.object_id = fkc.parent_object_id
INNER JOIN sys.schemas sch
ON tab1.schema_id = sch.schema_id
INNER JOIN sys.columns col1
ON col1.column_id = parent_column_id AND col1.object_id = tab1.object_id
INNER JOIN sys.tables tab2
ON tab2.object_id = fkc.referenced_object_id
INNER JOIN sys.columns col2
ON col2.column_id = referenced_column_id AND col2.object_id = tab2.object_id
```

```sql
-- objects need to be wrapped in "()"
create table dbo.finTransactions_to_finStatements (
    TransStatementId int identity(1, 1) primary key clustered,
    transID int
        constraint [fk_finTransactions_finStatements_transID]
        foreign key ([transID]) references dbo.finTransaction ([transID]),
    StatementId int
        constraint [fk_finTransactions_finStatements_StatementID]
        foreign key ([StatementId]) references [dbo].[finStatements] (StatementId)
);
```