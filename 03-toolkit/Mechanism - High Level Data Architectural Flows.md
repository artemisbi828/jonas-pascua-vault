related-to: [Ontology], [Ontology - Analytical Ontology]

```
## LOADS (by-source, by-object (API))
full-load
incremental: by watermark; by bkey + stamp
data-freshness-assertions

## DATA OPS
### Sanitization
### Dimension 
dimension-seed; 
dimension-tracking; (inserts vs changes)
change-tracking-traceability; governance-approval-workflow; overrides
completenes
  orphan -- lost parent
  vilomah / unbound / dangling -- lost child

### Definitions + Calcs (Logic)
stages -- population-input --> apply-framework-factor --> output
measure-calcs -- procs-or-query to create attributes + flags
  single-responsibility-principle (1:1 || attribute:process)
attribution-model
  waterfall :: remainder method
  best-fit
recognition-model
  white-list -- inclusion-factor
  black-list -- exclusion-factor
  nulls -- silent-failure
fan-in -- n:1
fan-out -- 1:n
cohort; grain-or-aggregate
predictive-model (+t)
  back-tested (-t)

### Objects
business-keys
axis (l-w-h attributes) -- rows, columns, rank

### Error Grain
red -- guardrail
yellow -- advisory

### Gates
history-gates (freeze / block late arriving data)
history-override
history-enrichment --> goal-enrichment

## ASSERTIONS
bands -- outlier-detection, constraints-factor
relative-rank: first, last, top3 / limit
date-allowance
grains + cohort
  aggregates -- numerator vs denominator

### CONSUMPTION 
  filter-layer. by page. by area.
  shields. by measure. by area.
  
### PROCESS-ADMIN
  ad-hoc-trigger: log
  batch task
  listen --> worker wakes up
  process batch + log start time
  send
  echo-receipt
  
```





Canonical Layer is everything after `Normalization` --> `Metrics & KPIs`

```
Physical Reality               # ontological
    ↓                          
System Capture                 # epistemic (logged and recorded)
    ↓                          
Raw Source Data                # raw on schedule or ad hoc
    ↓                          
Normalized Enterprise Model    # unified entities (eg patient, location, employee, person) vs events (appointment, contract, trans)
    ↓                          
Semantic Distillation          # types, codes, definitions, glossaries, lookups, maps, sequencing layers
    ↓                          
Governed Semantic Model        # tables, columns (w bool enrichments)
    ↓                          
Measures                       # math derivations (count, sum, avg, min, max) --> scalar, agg.cohort, ratio of aggs
    ↓                          
Metrics / KPIs                 # vs scope (time, cohort, benchmark)
    ↓                          
Intelligence                   # framework → reporting / presentation → desired action + outputs
    ↓                          
Action                         # strategy → playbooks → decision
    ↓                          
Success / Profit               
```

# Change
Here are prime names. Related-To [[Mechanism - High Level Change Flows]]
```
values --> hydrate; modify; clear; retain
rows --> append; modify; remove
columns --> add; modify; drop
tables --> create; modify; drop
relationships --> link; modify; unlink
```

# Anti-Patterns

| Term                                                     | Name / Term | Concept / Definition | Comments                                                                                                                          |
| -------------------------------------------------------- | :---------: | :------------------: | --------------------------------------------------------------------------------------------------------------------------------- |
| **Conceptual Collision**<br>Same Name, Different Meaning |      1      |          M           | aka "Semantic Collision"<br><br>One term<br>Multiple definitions<br>Multiple owners<br>Multiple calculation rule                  |
| **False Equivalence**<br>Different Names, Same Meaning   |      M      |          1           | aka "Snowflaking"<br><br>Different logic<br>Different grain<br>Different scope<br>Different business use<br>Same or similar label |
**Determinism Erosion**: Confidence in what a term means degrades over time
**Underspecification**: Label or name fails to specify distinctions that materially affect interpretation

### Acid Tests

```
NPE\_Added
    ├── Marketing definition
    ├── Operations definition
    └── Finance definition

The name has become overloaded
```

### Sequential Decision Tree
```
START
  ↓
Do two or more terms exist?
  ├── No
  │     ↓
  │   Does one term have multiple definitions?
  │     ├── Yes → Conceptual Collision
  │     └── No  → No naming conflict detected
  │
  └── Yes
        ↓
      Do the terms have the same calculation logic?
        ├── No
        │     ↓
        │   Are people treating them as interchangeable?
        │     ├── Yes → False Equivalence
        │     └── No  → Valid Distinct Concepts
        │
        └── Yes
              ↓
            Do they have the same grain?
              ├── No → False Equivalence / Grain Collision
              └── Yes
                    ↓
                  Do they have the same business scope?
                    ├── No → False Equivalence / Scope Collision
                    └── Yes
                          ↓
                        Do they have the same owner and decision use?
                          ├── No → Potential Business Context Split
                          └── Yes → Duplicate / Synonym

```


```
NAMING ISSUE IDENTIFIED
  ↓
Is the underlying business concept materially different?
  ├── Yes
  │     ↓
  │   SPLIT into distinct names
  │
  │   Example:
  │     NPE_Added
  │       ↓
  │     NPE_Added_Marketing
  │     NPE_Added_Operations
  │     NPE_Added_Net
  │
  └── No
        ↓
      Are there multiple names for the same concept?
        ├── Yes
        │     ↓
        │   Choose canonical name
        │   Deprecate/delete aliases
        │
        │   Example:
        │     Patient_Starts
        │     New_Patient_Starts
        │     NPE_Starts
        │       ↓
        │     Canonical: Patient_Starts
        │
        └── No
              ↓
            Keep name, but improve definition/documentation
```

### Split vs Merge vs Delete
```
Different logic
Different grain
Different owner
Different source
Different cohort
Different decision use
Different business meaning

Bad:
NPE_Added

Better:
NPE_Added_Gross
NPE_Added_Net
NPE_Added_Marketing
NPE_Added_Operations
```


**False Equivalence**
Any **no** → split

1. Are we talking about the same real-world thing?
2. Are we measuring the same business event?
3. Is the grain identical?
4. Is the population/cohort identical?
5. Is the time logic identical?
6. Is the source-system logic identical?
7. Are inclusion/exclusion rules identical?
8. Would the metric return the same result given the same input data?

**Conceptual Collision**
If mostly **yes** → **split** -or- **replace**

1. Does one name have more than one accepted definition?
2. Do different teams explain the term differently?
3. Does the name require a meeting to explain?
4. Is the metric logic different by department?
5. Has the meaning changed over time?
6. Is there no clearly accountable owner?
7. Are users asking, "Which version of this?"


```table-of-contents
```
---
# High Level Concepts
### Process Types
**Physical or Mechanical vs Technical**
  valve. mono directional 
  physical: mechanical, biological

### Ontology Summary -- 
related-to: [Ontology]
> _Ontology defines existence, predicates define truth, measures define quantity, metrics define meaning._

- **ontological** -- true reality -- *what exists?* system agnostic, defines existence
- **epistemology** / epistemic -- system data and reality -- *how do we know what we know?*
	- system ontology - tables, columns classes
- **semantic** -- metadata definition overlay to give meaning to data -- *what does this mean after putting it in context?*

# Raw Data

# Normalization Layer
Sources may have different grains (taxonomy on cl9 vs ofi different levels --> typecode (n=50) vs transactiontypeid (n=2) --> normalize as combokey --> surrogate (unified) key.

### Objects
- **events** -- appointments, financials, contracts
- **entities** -- patients, locations, employees
- **lookups** -- 
	- by-source
	- unified -- using surrogate keys
- change-tracking -- scd2 for defined entities or lookups
- *provision*
	- *promotion*
	- *demotion*



## Standard Entities
### Time Dimension
  point-in-time
  dynamic
  trendline

### Columns
- date_value
- month_value
- year_month
- year_month_w_current -- for UX dropdown

# Semantic Distillation Layer

- **Classification** (Taxonomy): 
	- **Mapping** Tables -- hierarchy: fan in and fan outs for aggregation and predicates
	- **Lookup** Tables -- definition tables
	- **Link** Tables -- M:1 or 1:M
- **Inclusion** (Eligibility)
- **Exclusion** (Suppression)
- **Enrichment**
- **Derivation** Steps (Procs): L1, L2, L3

# Semantic Model
Metadata definition overlay to give meaning to data
- **table**: system claims reality exists 
- **column**: properties of those table claims --> `table_column_name_no_abbrev` (Power BI Title Case With Space)
	- **attribute** -- column -- just a component / quality, does not answer anything
	- **predicates** -- bool flags -- (yes/no) as-of an evaluation time (*filters*)

### Data Types

| Canonical     | Standard Physical Shape |
| ------------- | ----------------------- |
| `bool`        | boolean/bit             |
| `int`         | 32-bit integer          |
| `bigint`      | 64-bit integer          |
| `sort`        | decimal(5,4)            |
| `amount`      | decimal(16,5)           |
| `string`      | varchar                 |
| `comment`     | long text               |
| `date`        | date                    |
| `datetime`    | timestamp               |
| `datetime_tz` | timestamp with timezone |
| `guid`        | UUID/GUID               |
| `json`        | semi-structured JSON    |
| `binary`      | binary/blob             |
### X Platform

| Canonical     | MSSQL            | Snowflake     | PostgreSQL    | DuckDB        |
| ------------- | ---------------- | ------------- | ------------- | ------------- |
| `bool`        | bit              | boolean       | ``            | ``            |
| `int`         | int              | integer       | ``            | ``            |
| `bigint`      | ``               | ``            | ``            | ``            |
| `sort`        | decimal(5,4)     | number(5,4)   | numeric(5,4)  | decimal(5,4)  |
| `amount`      | decimal(16,5)    | number(16,5)  | numeric(16,5) | decimal(16,5) |
| `string`      | nvarchar(n)      | varchar(n)    | varchar(n)    | varchar       |
| `comment`     | nvarchar(max)    | varchar       | text          | ``            |
| `date`        | ``               | ``            | ``            | ``            |
| `datetime`    | datetime2        | timestamp_ntz | timestamp     | ``            |
| `datetime_tz` | datetimeoffset   | timestamp_tz  | timestamptz   | ``            |
| `guid`        | uniqueidentifier | varchar(36)   | uuid          | ``            |
| `json`        | nvarchar(max)    | variant       | jsonb         | json          |

# Measures
- **measures (derived)**: math on columns-- count / sum.avg / ratio -- can use predicates
	- scalar -- by single-entity (patient or location production value)
	- aggregates -- by cohort (cluster) of entities (eg conversion rate, collection rate) -- sum, avg
	- ratio of aggregates -- defined only at evaluation scope (collection rate pct actual)
- **metrics**: meaning overlay -- requires comparison → decisions -- m.measures, vs benchmark-period


# Metrics, KPI, Consumption
- facts -- numerics
	- aggregates: location_x_day, location_x_month
- dims -- string descriptors

related-to: [[Mechanism - Governance]]
