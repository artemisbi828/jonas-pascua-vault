```sql
exec sp_rename 'bi.Appointments_Collections', 'bi.Appointments_Collections_obs_20231101'
exec sp_rename 'bi.Appointments_Collections2', 'Appointments_Collections'
```

> [!Warning]
> - must declare DB
> - cannot use 3 objects in rename

2026-01-21 04:46 PM -- added these 2 to the logic
- - any views using that object
- any documentation tables that need to be updated

- check if it is a fk constraint
- any procs using that column -- rename
- any procs writing to that column
- jobs referencing that proc need to be renamed

```sql
-- accidental rename? revert
exec sp_rename 'bi.[bi.d_ttypg]', 'd_ttypg'
```

```sql

-- gregg's proc
declare @proc as varchar(max) = 'sd.usp_CurrentArAging';
set @proc = replace(replace(@proc, '[', ''), ']', '');
declare @newName as varchar(max) = '_obsolete_' + convert(varchar(10), getdate(), 121) + '_' + SqlMgmt.dbo.udf_StripValueV2(@proc, '.', '', null);
declare @msg as nvarchar(max) = '`' + @proc + '` changed to `' + @newName + '`';
raiserror(@msg, 10, 1) with nowait
exec sp_rename @proc, @newName
```


# Try this TSQL
#status/deferred/quick-paste-merge-later 
```sql

DECLARE @schema      sysname = N'dbo';
DECLARE @table       sysname = N'YourTable';
DECLARE @old_column  sysname = N'OldColumnName';
DECLARE @new_column  sysname = N'NewColumnName';

DECLARE @obj_id int   = OBJECT_ID(QUOTENAME(@schema) + N'.' + QUOTENAME(@table));
IF @obj_id IS NULL
BEGIN
    RAISERROR('Table %s.%s not found.', 16, 1, @schema, @table);
    RETURN;
END;

DECLARE @col_id int = COLUMNPROPERTY(@obj_id, @old_column, 'ColumnId');
IF @col_id IS NULL
BEGIN
    RAISERROR('Column %s not found on %s.%s.', 16, 1, @old_column, @schema, @table);
    RETURN;
END;

-------------------------------------------------------------------------------
-- 1) PRINT the command to rename the column
-------------------------------------------------------------------------------
SELECT
    [What]     = 'RENAME COLUMN',
    [Command]  = N'EXEC sys.sp_rename N''' 
                 + QUOTENAME(@schema) + N'.' + QUOTENAME(@table) + N'.' + QUOTENAME(@old_column) 
                 + N''', N''' + REPLACE(@new_column,'''','''''') + N''', N''COLUMN'';'
UNION ALL
SELECT
    'OPTIONAL: refresh dependency metadata',
    N'EXEC sys.sp_refreshsqlmodule N''' + QUOTENAME(@schema) + N'.' + QUOTENAME(@table) + N''';';


-------------------------------------------------------------------------------
-- 2) PRINT ALTER VIEW scripts for views that reference THIS COLUMN
--    We detect direct column-level dependencies via sys.sql_expression_dependencies.
-------------------------------------------------------------------------------
;WITH deps AS
(
    SELECT
        v.object_id,
        v.name       AS view_name,
        sch.name     AS view_schema,
        sm.definition,
        sm.uses_ansi_nulls,
        sm.uses_quoted_identifier,
        v.is_ms_shipped,
        -- Is schemabinding present in the definition?
        has_schemabinding =
            CASE WHEN sm.definition LIKE '%WITH%SCHEMABINDING%' ESCAPE '\' THEN 1 ELSE 0 END
    FROM sys.sql_expression_dependencies d
    JOIN sys.views v
      ON v.object_id = d.referencing_id
    JOIN sys.schemas sch
      ON sch.schema_id = v.schema_id
    JOIN sys.sql_modules sm
      ON sm.object_id = v.object_id
    WHERE d.referenced_id       = @obj_id
      AND d.referenced_minor_id = @col_id          -- references THIS specific column
)
SELECT
    [What] = 'ALTER VIEW (dependent on column)',
    [Command] =
        -- Header comments
        N'/* Review before running. If the view is schema-bound, you must alter it to remove SCHEMABINDING first (or drop/recreate). */' + CHAR(13)+
        N'/* View: ' + QUOTENAME(view_schema) + N'.' + QUOTENAME(view_name) + N' */' + CHAR(13)+
        -- SET options as stored with the module
        N'SET ANSI_NULLS ' + CASE WHEN uses_ansi_nulls = 1 THEN N'ON' ELSE N'OFF' END + N';' + CHAR(13) +
        N'SET QUOTED_IDENTIFIER ' + CASE WHEN uses_quoted_identifier = 1 THEN N'ON' ELSE N'OFF' END + N';' + CHAR(13) +
        N'GO' + CHAR(13) +
        -- Definition rewritten to ALTER VIEW and with conservative column rename replacements
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        -- Swap CREATE VIEW -> ALTER VIEW
                        REPLACE(definition, N'CREATE VIEW', N'ALTER VIEW'),
                        -- Replace [Old] -> [New]
                        QUOTENAME(@old_column), QUOTENAME(@new_column)
                    ),
                    -- Replace "Old" -> "New" (quoted identifier style)
                    N'"' + @old_column + N'"', N'"' + @new_column + N'"'
                ),
                -- Common dotted reference: .Old -> .New
                N'.' + @old_column, N'.' + @new_column
            ),
            -- Common alias + space usage: ' Old ' -> ' New ' (basic, non-regex)
            N' ' + @old_column + N' ', N' ' + @new_column + N' '
        ) + CHAR(13) +
        N'GO'
FROM deps
ORDER BY view_schema, view_name;


-------------------------------------------------------------------------------
-- 3) (Optional) PRINT views that reference the TABLE (even if not this column),
--    for awareness / manual review.
-------------------------------------------------------------------------------
SELECT
    [What] = 'FYI: Views referencing table (any column)',
    [View] = QUOTENAME(s.name) + N'.' + QUOTENAME(v.name)
FROM sys.sql_expression_dependencies d
JOIN sys.views v
  ON v.object_id = d.referencing_id
JOIN sys.schemas s
  ON s.schema_id = v.schema_id
WHERE d.referenced_id = @obj_id
GROUP BY s.name, v.name
ORDER BY [View];
``

```