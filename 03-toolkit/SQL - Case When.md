```sql
case tfpp.tfppFrequency
                   when 'monthly' then tfpp.tfppNumPayments
                   when 'semimonthly' then tfpp.tfppNumPayments / 2
                   when 'biweekly' then tfpp.tfppNumPayments / 26 * 12
                   when 'weekly' then tfpp.tfppNumPayments / 52 * 12
                   when 'quarterly' then tfpp.tfppNumPayments * 3
                   when 'semiannually' then tfpp.tfppNumPayments * 6
                   when 'annually' then tfpp.tfppNumPayments * 12
                   else null end
```

```sql
iif(cast([cte1].[RunDateTime] as date) = cast(getdate() as date), 1, 0) IsToday
```
