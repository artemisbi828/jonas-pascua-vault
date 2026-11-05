| DataType         | Range                                                                | String Conversion |
| ---------------- | -------------------------------------------------------------------- | ----------------- |
| smallint         | -32,768 to 32,767 (2 bytes)                                          | varchar(10)       |
| uniqueidentifier |                                                                      | varchar(36)       |
| date             |                                                                      | varchar(16)       |
| tinyint          | 0 to 255 (1 byte)                                                    |                   |
| int              | -2,147,483,648 to 2,147,483,647 (4 bytes)                            |                   |
| bigint           | -9,223,372,036,854,775,808 to<br>9,223,372,036,854,775,807 (8 bytes) |                   |

---
# Concept : Data Type (Suggested)

| Concept            | Data Type      |
| ------------------ | -------------- |
| Titles             | nvarchar(64)   |
| Emails; Long Title | nvarchar(256)  |
| Money ($1,000.000) | decimal(18,4)  |
| Percentage (%)     | decimal(9,2)   |
| Sort Order (99.99) | decimal(4,2)   |
| Procedure Size     | nvarchar(4000) |
| Comment            | nvarchar(MAX)  |
| Proc Definitions   | nvarchar(MAX)  |
