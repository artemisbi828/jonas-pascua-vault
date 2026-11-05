#status/deferred/quick-paste-merge-later 

```sql
BULK INSERT ld.Daily
FROM N'C:\vsWorkspace\d20251014-20251120.csv'
WITH (
  FORMAT = 'CSV',
  FIRSTROW = 2,
  CODEPAGE = '65001',
  TABLOCK
);
```

Explicit Grant Access to File
```sql
# Open PowerShell as Administrator on the SQL Server host, then run:
$path = 'C:\vsWorkspace\d20251014-20251120.csv'
$acct = 'NT SERVICE\MSSQLSERVER'

$acl = Get-Acl $path
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule($acct,'Read','Allow')
$acl.AddAccessRule($rule)
Set-Acl -Path $path -AclObject $acl

# verify
Get-Acl $path | Select-Object -ExpandProperty Access
```

Test Access to Confirm Access to File
```sql
SELECT BulkColumn
FROM OPENROWSET(BULK N'C:\vsWorkspace\d20251014-20251120.csv', SINGLE_CLOB) AS x;
```

Parser
```sql
-- Create a CSV line parser that respects quoted fields and doubled quotes
CREATE OR ALTER FUNCTION dbo.ParseCsvLine(@line NVARCHAR(MAX))
RETURNS @out TABLE (pos INT, val NVARCHAR(MAX))
AS
BEGIN
    DECLARE @i INT = 1, @len INT = LEN(@line), @inQuote BIT = 0;
    DECLARE @start INT = 1, @ch NCHAR(1), @token NVARCHAR(MAX);
    DECLARE @pos INT = 1;
    WHILE @i <= @len
    BEGIN
        SET @ch = SUBSTRING(@line, @i, 1);
        IF @inQuote = 0
        BEGIN
            IF @ch = '"'
            BEGIN
                SET @inQuote = 1;
                SET @start = @i + 1;
            END
            ELSE IF @ch = ','
            BEGIN
                SET @token = LTRIM(RTRIM(SUBSTRING(@line, @start, @i - @start)));
                INSERT INTO @out VALUES(@pos, REPLACE(@token, '""', '"'));
                SET @pos += 1;
                SET @start = @i + 1;
            END
        END
        ELSE
        BEGIN
            IF @ch = '"' 
            BEGIN
                -- doubled quote => skip the escape
                IF SUBSTRING(@line, @i + 1, 1) = '"'
                    SET @i = @i + 1;
                ELSE
                BEGIN
                    -- closing quote: next char expected comma or end
                    SET @inQuote = 0;
                    IF SUBSTRING(@line, @i + 1, 1) = ','
                    BEGIN
                        SET @token = SUBSTRING(@line, @start, @i - @start);
                        INSERT INTO @out VALUES(@pos, REPLACE(@token, '""', '"'));
                        SET @pos += 1;
                        SET @i = @i + 1;
                        SET @start = @i + 1;
                    END
                    ELSE IF @i = @len
                    BEGIN
                        SET @token = SUBSTRING(@line, @start, @i - @start);
                        INSERT INTO @out VALUES(@pos, REPLACE(@token, '""', '"'));
                        SET @pos += 1;
                        SET @start = @i + 1;
                    END
                END
            END
        END
        SET @i = @i + 1;
    END
```