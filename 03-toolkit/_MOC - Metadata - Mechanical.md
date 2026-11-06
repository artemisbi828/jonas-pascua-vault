
#fxn/assert-convention -- spacing, word replacements

### Stage
avoid `layer` -- too ambiguous

#stage/raw -- bronze -- raw + `stamp-enriched`
#stage/sanitized -- silver -- dedupe
#stage/enriched -- capture, append, persist --> semantic definitions + rules
#stage/unification -- 
#stage/harmonize -- gold. 
#stage/assert-atomic -- 

#stage/aggregate -- trimmed for loads
#stage/assert-semantic -- cohort, period, bands (thresholds)

**Enforce: Apply**
#fxn/enforce-prime/attribute -- mutex attribute (first, last; avg; lag-lead | x time-scope)
  #fxn/allocate-ordinal -- first, last (alphabetical, numerical) | min/max | avg | lag/lead
  #fxn/allocate-remainder -- 
  #fxn/allocate-adjacent -- lag-lead
  #fxn/allocate-timescope-band -- allocation within 5 days of contract-date
  
#fxn/enforce-prime/row -- partition by, order by priority, nulls (first;last)
#fxn/enforce-null-handling -- unknown, null, '', redirect (to other existing class/bucket)
#fxn/enforce-mask -- phi

**Unit Test**
#fxn/assert-non-null 
#fxn/assert-datatype 
	#fxn/assert-true-false -- [[True vs False vs Other]]

**Agg Test**
#fxn/assert-parity
#fxn/assert-rowcount
#fxn/assert-sumchk -- related to `assert-semantic`
#fxn/assert-cardinality -- 1:1 distinct vs 1:n
	#fxn/assert-no-orphan
	#fxn/assert-no-vilomah

#fxn/write-log
#fxn/read-progress 

**Infra Test**
#fxn/assert-penetration -- penetration test to assert connection
#fxn/assert-resilience -- pressure-test/quantity -- try to break container 
[[Integrity]]
[[Resilience]]
[[Scalability]]
[[Capacity]]
[[Load - Stress]]
[[Constraint Enforcement]]

### Constraints

#limit/loop-count -- not cost $30K
#limit/cost-compute -- compute or currency
#limit/row-count -- quantity, first, last

### Deploy: Enact

#deploy/assert-integrity -- use `fxn/assert`
#deploy/snapshot -- always lowest grain, as much as possible (within limit) 
- vs capture, vs persist
#deploy/seed-manifest
#deploy/change-manifest

#### Deploy Data Pipeline Pull

**Watermark**
#deploy/pipeline-pull/seed -- same as full, but no data initially exists
#deploy/pipeline-pull/incremental/watermark -- watermark column exists

**No Watermark**
#deploy/pipeline-pull/full
#deploy/pipeline-pull/incremental/business-keys -- capture change

**Datasource Type**
#datasource/server
#datasource/api

#### Deploy Full
#deploy/orchestrator/main -- sequencer
	#deploy/orchestrator/sub -- sequence-required; partitioned in sequence for faster deploy
		- trigger + trigger-constraint
	#deploy/orchestrator/async -- sequence-agnostic

#deploy/batching -- chunking into smaller groups [[Batching]]
#deploy/trigger/ad-hoc -- kick off (manual)
#deploy/trigger/scheduled -- nightly (daily), weekly, monthly; hourly, 30 min, 5 min
#deploy/trigger/change -- update triggers
#deploy/override -- bypass, skip orchestrator

#deploy/roll-back 
#deploy/roll-forward -- from back, pushing forward
#deploy/backfill -- from select-point, fill back (widen time range)
#deploy/forwardfill -- projected times
#deploy/sync-forward -- from forward, pull forward the back

#deploy/clone -- zero copy, promote through stages


