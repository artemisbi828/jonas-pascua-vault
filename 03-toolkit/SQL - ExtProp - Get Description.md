```sql
DECLARE @SchemaName NVARCHAR(128) = 'sd';
DECLARE @TableName  NVARCHAR(128) = 'ContractKeys';
DECLARE @ColumnName NVARCHAR(128) = 'tfpguid';

SELECT 
    s.name AS [Schema],
    t.name AS [Table],
    c.name AS [Column],
    CAST(ep.value AS NVARCHAR(MAX)) AS [Description]
FROM sys.extended_properties ep
INNER JOIN sys.tables t 
    ON ep.major_id = t.object_id
INNER JOIN sys.schemas s 
    ON t.schema_id = s.schema_id
INNER JOIN sys.columns c 
    ON ep.major_id = c.object_id 
    AND ep.minor_id = c.column_id
WHERE ep.name = 'MS_Description' -- Look specifically for the Description property
  AND s.name = @SchemaName
  AND t.name = @TableName
  AND c.name = @ColumnName;
```