```xls
=IF(MOD(ROW()-ROW($A$2),1000)=0,"GO "&"INSERT INTO std.ZipCodes VALUES","")
	• maybe change it to every 998? 
```
