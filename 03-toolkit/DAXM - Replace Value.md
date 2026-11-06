Best with UI
Add Column
Replace Value
```
---
= Table.ReplaceValue(#"Removed Duplicates",null,"All",Replacer.ReplaceValue,{"Brand"})
```

```
# add column is better, you can't just transform an existing one sometimes
= Table.AddColumn(
    #"ReorderColumns",
    "BrandFixed", 
        each if [Brand] = null then [Manufacturer] & " - All" else [Brand], type text
)
```