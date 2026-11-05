
```
FULL JOIN
A + B collectively determine which dates exist

A ─────┐
       ├── COALESCE(A.date, B.date)
B ─────┘


DATE SPINE: 
date timension determines which dates exist. A and B decorate those dates

           ┌── A
Date ──────┤
           └── B
```