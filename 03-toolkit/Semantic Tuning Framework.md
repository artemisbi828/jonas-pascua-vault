SANDBOX
[[Tuple vs Concept vs Objects]]
- [[Acid Test - Object or Definition]]
- [Standards - Database Object Naming]
	- [[Standards - Taxonomy - Access Levels]]
[[AI Prompt - Short Operator Rules]]

DEV 
[[Concepts - Finance + Business]]
[[Prime Names]]
[[Obsidian Normalization Framework]]
[[Mechanism - High Level Data Architectural Flows]]


#attribute 
#tuple 
- #bkey: business key
- #nkey: natural key
#artifact: dev-modeling formalization
#concept: formalization
#object
- #object_type/elemental
- #object_type/cohort
- #object_type/composite
#stage





**Modeling**
#modeling/friendly: more columns (3-5 max), less rows per bkey 
> eg job_title_family_access_policy

#modeling/extensible or #modeling/machine-optimized: more rows, less columns 
> job_title_family, job_title_access_scope, job_title_policy)



Distil this and merge with [[Mechanism - High Level Data Architectural Flows]]

```
object 
  audience (1:M): clusters and attributes
  utility / feature: why it matters x ea. audience

object-type
  elemental: dim. lowest grain
    nkey: system assigned (incremental or random (guid))
  cohort: group / cluster of elementals
  composite: event (container of elementals + attributes)
    bkeys (business-keys): defines a unit (dedupable)
object-hierarchy: strateg / layer / rollup (grain)
object-taxonomy: 1:1 or M:1 (rollup)
  industry; company | portfolio; sub-grains

attribute: 
  elemental: flag (T/F) --> qualifier-flags (is_)
  composite: has_
    suppression-flags (not_is): bottom up approach (vs top-down) --> only in sandbox: should be refined into suppression_flags (but all permutations have to be decomposed into atomics then validated (in sample, then review in population))
  time-scope: max seconds, min

state: object at a point/version/time
  state_claim: current/proposed/prior/certified state of an object
pathway: composite
pathway-step / process: input/change-artifact/output
environment: dev/sandbox/beta/uat/certified
architecture_layer = capture/storage/normalized/semantic

stage: same object, different period in time-scope


measure: pure math of either count or math-transformation of attribute
  count-rows: nulls = 1?
  sum
  diff
  delta (x stage or time-scope)
  ratio
  stats: avg, std-dev, z-score (sigs)

metric: x comparison-points
  period:  cp x pp: current period x previous period (LY, PY)
    LY: last year
    LYx2: 2 years ago
    Others: LM, LW (last month, last week)
  budget: pre-declared
  industry: against other competitors 

ENVIRONMENTS + DEVELOPMENT STAGES
  dev: internal
  sandbox: isolated business partners to co-dev
  beta: soft release -- expanded set
  uat: expanded testing
  certified: all audiences, hierarchies


PATHWAYS: builds.
  inputs --> change artifact --> output
    input-objects: 
    input-attributes: can be parametized
    static-framework: static-points that can be templatized

  NOTE: each one of this is a stage. if it's more than one path and more than 3 steps, need to decompose. then assign a cluster
  single (no fork) --> decompose forks into single paths
  trigger: (ad-hoc, scheduled (daily, weekly, monthly, quarterly, annually))

STAGING
  ontological
  epistemic (system): capture
  storage: sometimes 
  normalized
  semantic
    dims
    events: detail
    facts: x-grain --> aggs
      measure --> comparison-points | metrics --> action --> success/profit


SOLUTION APPROACH VECTORS
current-state vs proposed-state 
  impact analysis: 1
    1) clone: stage0 (all input-objects + output-objects)
    2) create change artifact (elemental flags for each attribute --> composite flag)
    3) output --> compare stage0.output vs stage1.output
  method comparison: M
    same as above for each 1
    create a scoring-model
    evaluate each method and rank methods (define: (no-tie, tie-allowed))

NOTES 
* register your elementals: if id'd in a composite and not registered, make sure you register
  hard requirement
  soft requirement: non-deterministic (refining)

EXAMPLES
elementals: 
  employee
  cost-center: clinic vs ssc
  patient
  product
  service

composites / events:
  appointment: patient x type
  contract: composite of patient x type
  transactions: ↑ invoice
  work assignment: composite of employee x cost-center x job-title
```

