Want min/max by `Location` not by `Location-ReferralSourceDescription`? 

```sql
-- # previous-cte has group by Location-ReferralSourceDescription
-- # wrap with win-fxn to shield

min(min(DateKey)) over (partition by Location)
```
![[Pasted image 20261001131357.png]]