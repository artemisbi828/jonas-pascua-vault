```sql
SET NOCOUNT ON;

DECLARE @sql NVARCHAR(MAX) = N'';
DECLARE @schema SYSNAME;
DECLARE @obj SYSNAME;

DECLARE cur CURSOR FAST_FORWARD FOR
SELECT C.name, A.name
FROM [sys].[all_objects] AS A
LEFT JOIN [sys].[schemas] AS C
    ON A.schema_id = C.schema_id
WHERE A.name LIKE 'vw_%'
ORDER BY C.[name], A.[type_desc], A.[modify_date] DESC;

OPEN cur;
FETCH NEXT FROM cur INTO @schema, @obj;

WHILE @@FETCH_STATUS = 0
BEGIN
    -- Build a safe statement per object. QUOTENAME prevents injection on names.
    SET @sql += N'SELECT TOP (1) * FROM ' 
                + QUOTENAME(@schema) + N'.' + QUOTENAME(@obj) + N';' 
                + CHAR(13) + CHAR(10);
    FETCH NEXT FROM cur INTO @schema, @obj;
END

CLOSE cur;
DEALLOCATE cur;

-- Optionally inspect @sql:
-- PRINT LEFT(@sql, 4000);
-- SELECT @sql AS FullScript;

-- Execute all statements at once
IF LEN(@sql) > 0
    EXEC sp_executesql @sql;

```
