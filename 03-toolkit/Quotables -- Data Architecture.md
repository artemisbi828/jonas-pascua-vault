- guardrail (red) vs advisory (yellow)

pressure test the execution point
proposed execution point
I dont want to introduce another mechanism
materialized, propagated 
default remediation response
control points 

... the idea is ...

[[Quotables - Materialized vs Propagated vs Hydrated]]
[[Mechanism - High Level Data Architectural Flows]]

## Dangling
Opposite of orphan. Unreferenced by facts.

|Term|Meaning it conveys|My take|
|---|---|---|
|**Unreferenced**|No fact FK points to it|⭐ Best technical term|
|**Unlinked**|Has no linkage into the model|⭐ Very intuitive|
|**Unused**|Exists but isn't being used|Good, plain English|
|**Dangling**|Exists without a meaningful connection|Good engineering/debug term|
|**Stale**|Was potentially useful, no longer is|Good if historically referenced|
|**Residual**|Left behind after processing/change|Good ETL-cleanup term|
|**Obsolete**|No longer valid/needed|Stronger business assertion|
|**Purge candidate**|Meets your deletion criteria|⭐ Best operational status|
|**Dead member**|Completely unused|Clear, but informal|
|**Junk**|Unwanted data|I'd avoid because **junk dimension** already has a specific dimensional-modeling meaning|

I'd separate **condition** from **action**, which fits your gove

## Validate
**assert model integrity**
validate {model, referential, linkage, relationship} integrity

```
data_integrity
├── nullability        → unexpected NULLs or required value missing
├── uniqueness         → duplicate keys
├── referential        → orphan: fact key → missing dimension (parent) | dangling: wrong parents, not parents
└── cardinality        → unexpected 1:n / n:n (relationship resolves unexpectedly >1)
```

^885909

# Airport Flight Lifecycle


```
Preflight → Clearance → Takeoff → Flight → Touchdown → Postflight
                │           │
                │           ├─ Yellow → Advisory / Diversion
                │           └─ Red    → Emergency Landing → Grounded
                │
                └─ Failed → No Clearance → Grounded
```
FLIGHT LIFECYCLE

PRE-FLIGHT
├─ Checklist       → validate prerequisites
├─ Inspection      → data-quality / integrity checks
├─ Gate            → hard pass/fail assertion
└─ Clearance       → approved to execute

TAKEOFF
├─ Departure       → process begins
└─ Liftoff         → mutations/workload starts

IN-FLIGHT
├─ Telemetry       → logging / monitoring
├─ Waypoint        → checkpoint
├─ Course Check    → intermediate validation
└─ Guardrail       → continuously evaluated safety rule

EXCEPTION STATES
├─ GREEN           → nominal / continue
├─ YELLOW          → caution
│  ├─ Advisory     → anomaly worth logging
│  ├─ Holding      → pause / don't advance
│  └─ Diversion    → take alternate processing path
│
└─ RED             → critical
   ├─ Abort         → immediately stop operation
   ├─ Emergency Landing → safely terminate processing
   └─ Grounded      → prohibit subsequent execution

LANDING
├─ Approach        → begin finalization
├─ Touchdown       → primary work completed
└─ Landing Check   → validate final state

POST-FLIGHT
├─ Taxi            → move/promote results
├─ Parking         → final resting state
├─ Shutdown        → release resources
└─ Debrief         → log / summarize outcome

MAINTENANCE
├─ Inspection      → diagnose integrity
├─ Repair          → remediate failures
├─ Cleanup         → purge residual/unreferenced data
└─ Overhaul        → rebuild / reprocess


GREEN  → CLEARANCE → continue
YELLOW → ADVISORY  → log / investigate / potentially continue
RED    → EMERGENCY LANDING → THROW