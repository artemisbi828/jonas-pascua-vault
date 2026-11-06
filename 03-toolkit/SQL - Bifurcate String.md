
# Bifurcate via Tab
From C/P SSMS Table Output
- note {-1, +1}
```sql
-- bifurcate
declare @input nvarchar(max) = N'131	4244407F-8564-48FA-87FB-8F07928D4601';
declare @split int = charindex('	', @input); -- position minus 1
declare @ssid int = left(@input, @split - 1);
declare @transguid uniqueidentifier = substring(@input, @split + 1, len(@input));

```