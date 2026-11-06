related-to: [[SQL - Batch Filling]]

> [!Note]
> - @tables and outer apply is bad for anything more than 5 rows.
> - use #tmp + clustered indexes (SARGable --> Search ARGument Able)
> - keep cast <x> where cast(t.transDateTime as date) = ctr.DateKey </x>


CTEs for explanation.
#temp tables for execution boundaries.
Indexes for the next join.
Rollups for grain control.

## PREP
1. Identify the monster tables
2. Check the indexed access path first (do not bring monster-ecosystem through CTE logic)
3. persist to temp tables and create clustered index

## STEP-01
create your target then persist to #tmp

```sql
	create clustered index cx_step_01_contract_scope
	on #step_01_contract_scope
	(
	    SourceSystemId,
	    patGuid,
	    payment_start_date,
	    payment_end_date
	);
```

## STEP-02
slice the monster table --> output #tmp2
create clustered inex on that

> Why this works: SQL Server CTEs are not materialized by default. Microsoft’s guidance says CTE query results are not materialized, and each outer reference may require the CTE query to be re-executed, so repeated or expensive intermediate results are often better as temporary objects.

## STEP-03
Apply business qualifications (case-when) after physical pruning (using indexes)
BAD: filter by ttypCode before slicing by patient/date 
GOOD: filter by index first, THEN, business qualifications

TIPS: 
-- avoid outer apply on large tables
-- separate grain-changing steps
-- naming

```
#step_##_<entity>_<action_or_grain>
  #step_01_contract_scope
  #step_02_patient_transaction_slice
  #step_03_transaction_typed
  #step_04_down_payment_candidates
  #step_05_adjustment_by_credit_group
  #step_06_payment_enriched
  #step_07_payment_plan_rollup
```

Index Seek = good
Key Lookup = okay if small
Index Scan = suspicious
Table Scan = bad on huge table
Hash Match = okay sometimes, scary if unexpected
Sort spill = memory problem