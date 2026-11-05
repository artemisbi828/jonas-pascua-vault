related-to: [[Tools - Global Key Bindings]]

[Sublime - Theme - Things]
[[Sublime - Packages]]
[[Sublime - Key Bindings]]
[[Sublime - Show Console or Terminus]]

---
- [[#Tools To Clean / Refine|Tools To Clean / Refine]]
	- [[#Tools To Clean / Refine#Create Table|Create Table]]
- [[#Logs|Logs]]

---
# Tools To Clean / Refine
## Create Table

```
paste 2 tables → find diffs, get metadata
  label1: `#SET_A`
  label2: `#SET_A`

RUNTIME: 
  normalizes formatting

OUTPUTS
--------------
Recommended_Key: EmployeeCode + '|' + LocationCode
SET_A_Count: 216142
SET_B_Count: 213605

COLUMN_MAPPING:
| Set_A_Columns | Set_B_Columns | % Match |
| --- | --- | --- |
| EmployeeCode | EmployeeCode | 99.65 |
| LocationCode | LocationCode | 99.65 |

A_MISSING_IN_B:
- (none)

B_EXTRA_COLUMNS:
- (none)

MATCHING_SUMMARY:
- Matched_Pairs: 213605
- Only_SET_A: 2537
- Only_SET_B: 0
- Diff_Records: 0
- Match_Threshold: 0.6

ONLY_SET_A:
- row_seq=2  {"row_seq":"2","EmployeeCode":"111015","LocationCode":"25001"}
- row_seq=3  {"row_seq":"3","EmployeeCode":"111015","LocationCode":"25002"}
```


## SQL Group By Joins 
review superfluous joins, remove
