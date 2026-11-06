lookup cell 
- tgt-column1
- tgt-column2 (same array)
- null handling → 0 → ? 

```bash
=XLOOKUP(J2, $C$2:$C$35, $G$2:$G$35, "", 0)
```

2026-01-21 11:33 AM -- have to be even, Table1[@ColumnName] -- `@` is important for reference, otherwise you get the whole column in 1 cell;