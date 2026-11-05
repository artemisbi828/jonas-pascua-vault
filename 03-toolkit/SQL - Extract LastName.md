```sql
-- must have space
substring(FirstLastName, charindex(' ', FirstLastName, 0)+1 ,LEN(FirstLastName)) As LastName
```1