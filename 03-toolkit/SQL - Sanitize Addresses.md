1. trim city and names
2. change null cells to ''
3. Address2 (Optional) -- concat → Address1

```sql
select nullif(isnull(trim([pat].[City]), '') + ', ' + isnull([pat].[State], '') + ' ' + isnull([pat].[PostalCode], ''), ',') as [Patient_CityStateZip],
[o].[Address1] + case when [o].[Address2] is null then '' else ', ' + [o].[Address2] end as Office_Address,

```

```sql
-- Define the sample data for demonstration
DECLARE @Addresses TABLE (
    AddressLine VARCHAR(100)
);

INSERT INTO @Addresses (AddressLine) VALUES
('4109 Overland Drive'),
('12005 High Ave'),
('2612 Lauriston Drive'),
('3020 Twin Acres Dr'),
('1526 Pine Ave'),
('14151 96Th St'),
('2 Eton Drive'),
('1120 S Drexel Ave'),
('3909 Miller Road'),
('19523 Shady Hike Lane');

-- T-SQL query to extract the two required components:
SELECT
    A.AddressLine,
    -----------------------------------------------------
    -- 1. Extract the House Number (Before the first space)
    -----------------------------------------------------
    -- Use LEFT() with a length calculated by CHARINDEX(' ') - 1
    LEFT(
        A.AddressLine, 
        CHARINDEX(' ', A.AddressLine) - 1
    ) AS HouseNumber,
    -----------------------------------------------------
    -- 2. Extract the First 5 Characters of the Street
    -----------------------------------------------------
    -- Use SUBSTRING() starting 1 character after the first space, for a length of 5
    SUBSTRING(
        A.AddressLine,
        CHARINDEX(' ', A.AddressLine) + 1, -- Start position: right after the space
        5                                  -- Length: 5 characters
    ) AS First5StreetLetters
FROM
    @Addresses AS A;
```


|           | Abbreviation |
| --------- | ------------ |
| Street    | ST           |
| Drive     | DR           |
| Highway   | HWY          |
| Avenue    | AVE          |
| Suite     | STE          |
| Parkway   | PKWY         |
| Boulevard | BLVD         |
| Circle    | n/a          |