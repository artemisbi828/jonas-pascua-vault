Not VALUES()
Use the **`UNIQUE`** function:

```excel
=UNIQUE(A:A)
```

### Notes

* Returns all distinct values from column A
* Spill formula (auto-expands down)
* Keeps **first occurrence order**

***

## Variations

### 1) Sorted distinct list

```excel
=SORT(UNIQUE(A:A))
```

***

### 2) Distinct values only (remove blanks)

```excel
=UNIQUE(FILTER(A:A, A:A<>""))
```

***

### 3) Values that appear only once (true dedupe)

```excel
=UNIQUE(A:A, , TRUE)
```

* This excludes duplicates entirely
* Only values that occur **exactly once**

***

### 4) Count distinct values

```excel
=COUNTA(UNIQUE(A:A))
```

***

```excel
=SORT(UNIQUE(FILTER(A:A, A:A<>"")))
```

✔ Deduped  
✔ No blanks  
✔ Sorted  
✔ Clean for reporting / downstream joins
