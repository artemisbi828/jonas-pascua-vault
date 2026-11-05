2026-02-25 03:07 PM -- Cleaned up AD Group and used AI to create a cleaner to prevent this error: 

> [!error] Invalid length parameter passed to the LEFT or SUBSTRING function.


```sql
;with cte1
as ( -- 
   select
       *
   from (
       values ('Olivianna Hoey'),
              ('Marcus Cruz'),
              ('Kyree Smith'),
              ('Meredith McGlamory'),
              ('Carolyn Ross'),
              ('Cindy Reyes'),
              ('Stephen Dockter'),
              ('Paisley Whidden'),
              ('Cecelia Williams'),
              ('Griffin Adair'),
              ('Breelyn Ivey'),
              ('James Prevatt'),
              ('Savannah Eschette'),
              ('Olivia Eschette'),
              ('Elixiya Johnson'),
              ('Alice Calvert')
   ) x (patient_name) )
-- 
select
    *
from cte1
    -- trim name; get space position
    cross apply (select cleaned_name = nullif(trim(patient_name), '')) m
    cross apply (select space_pos = charindex(' ', cleaned_name)) s
    cross apply (
    select
        first_name_parsed = case when
        -- null handling --> keep null
        m.cleaned_name is null then  null
                                 -- clean none
                                 when s.space_pos = 0 then m.cleaned_name
                                 else left(m.cleaned_name, s.space_pos - 1) end
) f
    cross apply (
    select
        last_name_parsed = case when
        -- null handling --> keep null
        m.cleaned_name is null then null
                                -- clean none
                                when s.space_pos = 0 then null
                                -- +1 from space
                                else substring(m.cleaned_name, s.space_pos + 1, 8000) end
) l
```

# Older


Originally designed to break down SQL object names (e.g., `Server.Database.Schema.Table`), `PARSENAME` is often "borrowed" by developers to split strings because it is incredibly fast and concise.

- **How it works:** It looks for periods (`.`) and returns the segment at the specified index (counting from right to left, 1 to 4).
    
- **The Limitation:** It only works for up to 4 segments and requires the delimiter to be a period.
    

**Example for Names:** If you have "Amy.Middle.Cortinas", `PARSENAME` can grab them instantly. To use it with spaces, you just `REPLACE` the space with a dot.

However, it fails if the name contains an actual period (like "Jr.") or more than 3 spaces.


```sql
DECLARE @name VARCHAR(100) = 'Amy B Cortinas';
-- Reverse logic: 1 is the last part, 2 is middle, 3 is first
SELECT 
    PARSENAME(REPLACE(@name, ' ', '.'), 3) AS FirstName,
    PARSENAME(REPLACE(@name, ' ', '.'), 2) AS MiddleInitial,
    PARSENAME(REPLACE(@name, ' ', '.'), 1) AS LastName;
```