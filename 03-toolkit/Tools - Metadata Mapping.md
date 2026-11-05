- column name, data type, nullability, pk/fk, business description
- identify change detection columns
- identify soft delete flags
- anonymized sample data in section 5

# Prepare SQL Update Stamp
1. use xls, put key at right-tail 
2. prefix column with "update `my_table` Set `my_column` = '"
3. wrap any text fields with `''`
	- wrap the key section (if necessary)
	- pre-wrap `'`; post-wrap with `"` → don't forget the post

![Pasted image 20260415111743.png]