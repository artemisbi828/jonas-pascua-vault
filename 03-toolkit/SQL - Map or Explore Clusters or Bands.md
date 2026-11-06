You're not really looking for **NTILE**.

`NTILE()` is useful when you want:

```text
Bucket 1 = first 25% of employees
Bucket 2 = next 25%
Bucket 3 = next 25%
Bucket 4 = last 25%
```

But that is statistically-driven.

You are trying to discover **natural security bands**:

```text
714-717 = unrestricted
311-355 = division
160-189 = region
55-128  = team
...
```

So I'd start with gap analysis rather than NTILE.

***

## Option 1 (Recommended) - Find Natural Clusters

Use `LAG()` to look at jumps.

```sql
with cte1 as (
    select
        d.EmployeeCode,
        count(distinct d.OfficeCodeId) qty
    from Lake.rls.Details d
    group by d.EmployeeCode
),
gaps as (
    select
        qty,
        lag(qty) over(order by qty desc) prev_qty,
        lag(qty) over(order by qty desc) - qty gap_size
    from (
        select distinct qty
        from cte1
    ) x
)
select *
from gaps
order by qty desc;
```

You'll likely see:

```text
717
716  gap=1
715  gap=1
714  gap=1
713  gap=1

355  gap=358   <-- HUGE BREAK

339  gap=16
327  gap=12
311  gap=16

189  gap=122   <-- HUGE BREAK

169  gap=20
167  gap=2
166  gap=1
...
```

Which immediately suggests:

```text
714-717 = unrestricted

311-355 = division

160-189 = region

55-169 = team/local

<55 = special cases
```

***

## Option 2 - Create Discovered Bands

Once you identify breakpoints:

```sql
case
    when qty >= 700 then 'Unrestricted'
    when qty >= 300 then 'Division'
    when qty >= 150 then 'Region'
    when qty >= 50 then 'Team'
    else 'Office/Special'
end as access_band
```

Then:

```sql
select
    access_band,
    min(qty) min_qty,
    max(qty) max_qty,
    count(*) employees
from cte1
group by access_band
order by max_qty desc;
```

Output:

```text
access_band      min   max   employees
-------------    ---   ---   ---------
Unrestricted     713   717   795
Division         311   355   4
Region           151   189   20
Team              55   128   15
Office/Special     1    54   40
```

***

## Option 3 - NTILE (Less Useful Here)

If you really want quantiles:

```sql
select
    EmployeeCode,
    qty,
    ntile(5) over(order by qty desc) band
from cte1;
```

Result:

```text
Band 1 = top 20%
Band 2 = next 20%
Band 3 = next 20%
...
```

Problem:

```text
714 and 355
```

may land in the same band even though they are semantically very different security models.

***

## Option 4 - Density View (My Favorite)

This gives you the framework you're trying to discover.

```sql
select
    qty,
    count(*) employees
from cte1
group by qty
order by qty desc;
```

Then add:

```sql
sum(count(*)) over(order by qty desc) running_employees
```

Example:

```text
qty   employees
717      1
716      5
715     22
714    725
713     42
----------------
355      1
339      1
327      1
311      1
----------------
189      4
169      1
167      6
...
```

That pattern is screaming:

```text
Cluster 1
---------
713-717

Cluster 2
---------
311-355

Cluster 3
---------
151-189

Cluster 4
---------
55-128

Cluster 5
---------
Edge Cases
```

which almost certainly maps directly back to:

```text
Unrestricted
Division
Region
Team
Office
```

***

### Governance Approach

I'd actually build a classification table:

```sql
qty >= 700  --> Unrestricted
qty >= 300  --> Division
qty >= 150  --> Region
qty >= 50   --> Team
else         Office/Special
```

Then manually validate 10 users from each band against:

```sql
Lake.rls.Configs
Lake.rls.ConfigOverrides
Lake.rls.PermissionGroups
```

and adjust the thresholds until every band corresponds to a real RLS access pattern.

That gives you a deterministic framework instead of manually reviewing hundreds of employees.
