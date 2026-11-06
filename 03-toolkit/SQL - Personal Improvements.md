

# Cross Apply vs `Var + Case When`
Was looking to have an employee name parser for SD. I wrote it out w my way and then asked Gemini to refactor. Learned some things but this would be a 2nd-pass refactor; 

1. "cross-apply" can act as variables
2. "space_int" → "space_idx" -- more description
3. "substring(, len())" → just use "substring(, , 8000)" optimized for [[SQL - Buffer Pool |Buffer Pool]]

2026-01-17 12:03 PM
## Original
```sql
use Lake;

declare @input_name table (
    input_id int primary key identity(1, 1),
    employeecode int,
    input_name sysname,
    space_int int,
    first_name nvarchar(64),
    last_name nvarchar(64)
);
insert into @input_name (input_name) values ('Amy Cortinas'), ('Nicole Alonzo'), ('Georgia Cole'), ('Laurel Speedy');

-- split logic for first_name, last_name → employee_code
update @input_name set input_name = trim([input_name]);
update @input_name set space_int = charindex(' ', [input_name]) - 1;
update
    @input_name
set
    first_name = case when space_int < 0 then null else left(input_name, space_int) end,
    last_name = case when space_int < 0 then input_name
                     else substring(input_name, space_int + 2, len(input_name)) end;

-- 
update
    tgt
set
    employeecode = src.EmployeeCode
from (
    select
        ina.input_id,
        ina.input_name,
        e.*,
        row_number() over (partition by input_id order by e.EmployeeCode) RN
    from @input_name as ina
        left join Lake.sd.Employees e
            on isnull(e.CommonName, e.FirstName) = ina.first_name
           and isnull(e.PreferredLastName, e.LastName) = ina.last_name
) src
    inner join @input_name as tgt
        on tgt.input_id = src.input_id
where RN = 1;

-- 
select * from @input_name as ina;
return;
```
## Refactored
```sql
USE Lake;
GO

DECLARE @input_name TABLE (
    input_id INT PRIMARY KEY IDENTITY(1, 1),
    employeecode INT,
    input_name SYSNAME,
    first_name NVARCHAR(64),
    last_name NVARCHAR(64)
);

INSERT INTO @input_name (input_name) 
VALUES ('Amy Cortinas'), ('Nicole Alonzo'), ('Georgia Cole'), ('Laurel Speedy');

----------------------------------------------------------------                
-- Single-pass Refactor
----------------------------------------------------------------                
WITH ParsedNames AS (
    -- Calculate split positions once using CROSS APPLY
    SELECT 
        ina.input_id,
        V.fname,
        V.lname
    FROM @input_name AS ina
    CROSS APPLY (
        SELECT TRIM(ina.input_name) AS full_n
    ) AS T
    CROSS APPLY (
        SELECT CHARINDEX(' ', T.full_n) AS space_idx
    ) AS S
    CROSS APPLY (
        SELECT 
            NULLIF(LEFT(T.full_n, S.space_idx - 1), '') AS fname,
            SUBSTRING(T.full_n, S.space_idx + 1, LEN(T.full_n)) AS lname
    ) AS V
),
EmployeeLookup AS (
    -- Join against the physical table and handle duplicates
    SELECT 
        p.input_id,
        p.fname,
        p.lname,
        e.EmployeeCode,
        ROW_NUMBER() OVER (PARTITION BY p.input_id ORDER BY e.EmployeeCode) AS RN
    FROM ParsedNames p
    LEFT JOIN Lake.sd.Employees e
        ON p.fname = ISNULL(e.CommonName, e.FirstName)
       AND p.lname = ISNULL(e.PreferredLastName, e.LastName)
)
UPDATE tgt
SET 
    tgt.first_name = src.fname,
    tgt.last_name = src.lname,
    tgt.employeecode = src.EmployeeCode
FROM @input_name AS tgt
INNER JOIN EmployeeLookup AS src ON tgt.input_id = src.input_id
WHERE src.RN = 1;

-- Output Results
SELECT * FROM @input_name;
```