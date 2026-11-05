
```sql
DECLARE @SchemaName NVARCHAR(128) = 'sd';
DECLARE @TableName  NVARCHAR(128) = 'ContractKeys';
DECLARE @ColumnName NVARCHAR(128) = 'tfpguid';
DECLARE @Description NVARCHAR(2500) = 'cloud9 UUID';

-- Check if the property exists
IF EXISTS (
    SELECT NULL
    FROM sys.fn_listextendedproperty(N'MS_Description', 
        N'SCHEMA', @SchemaName, 
        N'TABLE',  @TableName, 
        N'COLUMN', @ColumnName)
)
BEGIN
    -- UPDATE existing description
    EXEC sys.sp_updateextendedproperty 
        @name = N'MS_Description', 
        @value = @Description, 
        @level0type = N'SCHEMA', @level0name = @SchemaName, 
        @level1type = N'TABLE',  @level1name = @TableName, 
        @level2type = N'COLUMN', @level2name = @ColumnName;
    PRINT 'Description Updated';
END
ELSE
BEGIN
    -- ADD new description
    EXEC sys.sp_addextendedproperty 
        @name = N'MS_Description', 
        @value = @Description, 
        @level0type = N'SCHEMA', @level0name = @SchemaName, 
        @level1type = N'TABLE',  @level1name = @TableName, 
        @level2type = N'COLUMN', @level2name = @ColumnName;
    PRINT 'Description Added';
END
```