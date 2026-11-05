Last Updated: 2026-02-13 08:58 AM
```sql
/* #1 -- define database + schema */
declare @schema nvarchar(64) = N'MarketingFieldReporting';
set @schema = replace(replace(@schema, '[', ''), ']', '');

--check schema
--select @schema 

select
    'select top 1 * from ' + s.name + '.' + v.name as ObjectName
from sys.all_objects as v
    left join sys.schemas as s
        on v.schema_id = s.schema_id
where 1 = 1
  -- remove system views
  and s.name not in ('sys', 'dbo', 'INFORMATION_SCHEMA', 'QualityMonitoring', 'queryinsights')
  -- remove adrien views
  and s.name not in ('SchedulingDev', 'SchedullingDirectLakeModel', 'SchedulingDirectLakeModel', 'SchedulingPhase2Dev')
  and v.type = 'V'
order by 1;
```


# Output All View Create Scripts
```sql

/*
T-SQL script to generate CREATE VIEW statements for all user-defined views.
Uses OBJECT_DEFINITION to retrieve the original SQL used to create the view.
*/
SET NOCOUNT ON;
DECLARE @SchemaName NVARCHAR(128)
DECLARE @ViewName NVARCHAR(128)
DECLARE @Definition NVARCHAR(MAX)
DECLARE view_cursor CURSOR FOR
SELECT 
    s.name AS SchemaName,
    v.name AS ViewName,
    OBJECT_DEFINITION(v.object_id) AS ViewDefinition
FROM sys.views v
INNER JOIN sys.schemas s ON v.schema_id = s.schema_id
WHERE v.is_ms_shipped = 0 -- Exclude system views
ORDER BY v.create_date ASC -- Order by creation date (oldest first)
OPEN view_cursor
FETCH NEXT FROM view_cursor INTO @SchemaName, @ViewName, @Definition
WHILE @@FETCH_STATUS = 0
BEGIN
    PRINT '----------------------------------------------------------------------------'
    PRINT '-- View: [' + @SchemaName + '].[' + @ViewName + ']'
    PRINT '----------------------------------------------------------------------------'
    
    -- Basic error handling for views that might be encrypted or inaccessible
    IF @Definition IS NULL
    BEGIN
        PRINT '-- ERROR: Could not retrieve definition for [' + @SchemaName + '].[' + @ViewName + ']'
        PRINT '-- (It might be encrypted or you lack permission)'
    END
    ELSE
    BEGIN
        -- Optional: Add an idempotent check before the CREATE VIEW
        -- PRINT 'IF OBJECT_ID(''[' + @SchemaName + '].[' + @ViewName + ']'', ''V'') IS NOT NULL'
        -- PRINT '    DROP VIEW [' + @SchemaName + '].[' + @ViewName + '];'
        -- PRINT 'GO'
        PRINT @Definition
        PRINT 'GO'
    END
    PRINT '' -- Empty line for readability
    FETCH NEXT FROM view_cursor INTO @SchemaName, @ViewName, @Definition
END
CLOSE view_cursor
DEALLOCATE view_cursor
```
