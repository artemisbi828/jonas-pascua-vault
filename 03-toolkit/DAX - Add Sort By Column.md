```
Dynamic Slicer Selections = 
ADD COLUMNS(
	VALUES(''Table'[Type]), 
	"Order", LOOKUPVALUE('Table'[SlicerOrder], ...)
	)
```