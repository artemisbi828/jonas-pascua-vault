related-to: [[SQL - Fabric - Create Table vs SSMS]]

[[WH_DEV_Data_Solutions - Integrity Rules]]

[WH_DEV_Data_Solutions.edw.txplan_cc9]
[WH_DEV_Data_Solutions.edw.txplan_ofi]
[WH_DEV_Data_Solutions.edw.addon__cc9]
[WH_DEV_Data_Solutions.gold.contract_void__cc9]
[WH_DEV_Data_Solutions.edw.vw_legacy__contract]
[WH_DEV_Data_Solutions.edw.txplan__cc9]
[WH_DEV_Data_Solutions.edw.job_title]

[[WH_DEV_Data_Solutions.gold.contract__sd]] -- contract_id__edw (ContractKey)


[[PRJ - Cross Reference]]


```
insert_datetime_utc datetime2(6), 
process_id int

use conformed names not source-raw wven if easier for joins and intellisense. 
```



### taxonomy
  standard_core -- id | code | description (minimum)
  standard_enrichment -- sort_order decimal(5,2), comment
  standard_watermark (from scd2 - optional) -- update_datetime_utc

### scd2
  1. identity
  2. load_datetime_utc
  3. core fields :: audit-tracked fields in index 
	  1. including sort_order, comment
  4. **watermark-datetime** -- water_mark fields from source
    - source_created_datetime_local --> **local or utc or std**
    - source_modified_datetime_local
    - ⚠️ if none --> full staging then compare diffs
  5. loaded_by_process_id
  6. comment (helper) -- 
  7. loaded_by_email (helper) -- manual entry --> s/b NULL --> convert into process_id
  
  end_datetime_utc -- updated if removed from table

### table structuree
  1-ancestor --> nullable field in 
  M-ancestor --> 1:M table (a__x__b)
  M:M --> reduce to M-ancestor

### designing job schedules
real-time
as-of-yesterday-eod (utc standardized)
  dev: seed manual, focus only on taxonomy (no scd2 yet)
  test: scd2 + tracking -- ad hoc scheduled
  prod: daily scheduled

### example
[[PRJ - NPC Dashboard - Official]]
1. stage facts
2. stage dims
3. update dims
4. update facts

### schemas
- scd2
- gold
	- silver
	- scd2 -- for taxonomy
	- taxonomy -- types, statuses, 
	- date grain -- date, week_iso
	- base grain (unified concepts, atomic - G0) -- contract, appointment, patient, etc
	- rollup grain (aggregate - G1;G2) -- office-day, office-month (**monthyear_location_spine**)
- silver / bronze --> sanitized (trim, datatypes); raw w watermarks
- dataops -- no process id because always manual

![Pasted image 20260917120654.png]


### uat queries
- dimension gate (date)
- numerator
- denominator
- month_year_location__spine
- lifetime_retainer_attachment_rate as 