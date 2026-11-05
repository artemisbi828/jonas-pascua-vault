```sql

declare @t0 datetime2 = sysdatetime();
declare @t_prev datetime2 = @t0;
print concat('T0 start: ', convert(varchar(30), @t0, 121));

-- <<insert code here >> 
print concat('Step A done. Elapsed from t0 = ', 
    datediff(second, @t0, sysdatetime()), ' sec; step = ', 
    datediff(second, @t_prev, sysdatetime()), ' sec');
set @t_prev = sysdatetime();
```