`try...except`: _"Try to do this, but if something goes wrong, don't crash. Do this other thing instead."_

try this, if
- yes → print
- no → error handle

```python
try:
	if spark.catalog.tableExists(AUDIT_TABLE):
		print(f"Table {AUDIT_TABLE} already exists.")
	except Exception as e:
		print("Error checking table existence:", e)
```