---
related_to:
  - "[[Data Framework]]"
  - "[[Tools - PMO Talk]]"
  - "[[Data Framework]]"
---
#intent/roadmap
[[Mechanism - High Level Data Architectural Flows]]
[[Mechanism - High Level Script Flows]]
[[Mechanism - Object Function Roles ]]
[[Mechanism - Data Roles]]
[[Mechanism - Lifecycle Modeling, Pathways, Smoke Testing]]
[[Mechanism - Planning w Situational Clarity, Ideation, Indexing, Scoping, Avoid Hasty Abstractions]]
[[Mechanism - Pivot Plan to Roadmap, Unexpecteds]]
[[Mechanism - Nodes, Edges]]
[Mechanism - Know By Failure, Brute Force]
[[Mechanism - Governance]]
[[Mechanism - Feature Enhancements]]



#status/open-loop/new -- m+d (merge & deprecate) [Concepts#Words]

```
I want to enrich my vocabulary set for self-talk
aplomb -- the CEO addressed the criss with great aplomb -- coolness and composure under strain; 
esoteric -- the professor's lecture was quite esoteric -- specialized niche knowledge
elan -- jonas told the story with such elan -- like panache
```

You can make this much easier to scan by tagging on 3 axes at once:
[[Mechanism - Mental Pivot for Multi-Axial, No Semantic Mixing or Soup]]


```
1. Medallion layer: #medallion/bronze #medallion/silver #medallion/gold
2. Intent: #intent/diagnose #intent/roadmap #intent/solve #intent/prove #intent/communicate
3. Domain: #domain/ingestion #domain/quality #domain/modeling #domain/ops #domain/analytics #domain/decision
```

#intent/diagnose
[[Data + Tech Abbreviations]]
[[Mechanism - Fractal vs Totalized, Shallow vs Deep]]
[[Mechanism - Reduce ambiguity, reduce technical rabbit holes, reduce friction]]
[[Mechanism - Concept, Metric Modeling]]
[[Mechanism - Impact Analysis, Saliency Point, Blast Radius, Attack Surface]]
[[Mechanism - Selection Strategy, Suppression List, Exception List]]
[[Mechanism - Policy, Implicity Deny, Explicit Grant]]
[[Mechanism - Obfuscate, Ellipsis, Epitemistological Gap]]




#domain/ingestion
[Mechanism - Config Files]
[[Mechanism - AB Testing, Split Testing, Litmus Test, Acid Test]]
[[Mechanism - Connectivity Settings, Data Sources, Connectors, Rollbacks, Provisioning]]
[[Mechanism - Setup Friction]]
[[Mechanism - Data Transfer, Rotating Schedule, Orchestration]]


#medallion-layer/bronze, #domain/ingestion 
[[Mechanism - Approach Vectors, State vs Stage, Stages vs Mechanisms]]
[[Mechanism - Entry Point, End Point, Upstream, Downstream, Waterfall]]
[[Mechanism - Pipeline Sink Path]]
[[Mechanism - Compiling, Backfilling, Generating]]
[[Mechanism - Concurrency]]
[[Mechanism - Schema Drift, Soft Failure]]
[[Mechanism - Integrity Controls (Scrubbers), Crawler, Parser]]
[Mechanism - Config → Patterns → Action, Multi-Hop]
[[Mechanism - Load Balancing, Incremental Loads]]

#domain/execution
[[Mechanism - Connection]]
[[Mechanism - Runner, Resolver]]

#medallion-layer/silver
[[Mechanism - Ingestion Monitoring - Null, Exception, Error - Null Handling]]
[[Mechanism - 1-M or M-1 or 1-1 Mutations]]
	[[Mechanism - Rollup or Bubble Up]]
	[[Mechanism - Slicing, Bifurcating, Multifurcating]]
	[[Mechanism - Clear Conceptual Boundaries, MUTEX]]

[[Mechanism - Dragnet or Fallback]]
[[Mechanism - Gating, Guardrails, Sanitizing Data Types]]
[[Mechanism - Persisting to Disk]]
[[Mechanism - SUMCHK, Sanity Check]]
[[Mechanism - Fork, Tie Break, Inflexion Point]]

[[Mechanism - Outlier Detection]]
[Mechanism - Traceability]
[[Mechanism - Simplifying, Distilling]]
[[Mechanism - Parity, Same-Same, Syntactic Sugar, Alias]]
[[Mechanism - Cloning, Copying, Replication]]
[[Mechanism - Merging, Coalescing, Clusters]]
[[Mechanism - Append, Adding, Insert]]
[[Mechanism - Adding Buffer]]
[[Mechanism - Creep]]
[[Mechanism - Standardization]]


#medallion-layer/gold
[[Mechanism - pKey, cKey, sKey, fKey, HashKeys]]
[[Mechanism - Elemental, Primitive or Atomic Element]]
[Mechanism - Semantic Distillation Layer]
[[Mechanism - Improving, Corrective]]
[[Mechanism - Materiality Thresholds]]
[[Mechanism - Data Visualization Layer, BI Frameworks]]
[[Mechanism - Querying Wide Open]]
	[[Mechanism - Subtracting]]

[[Mechanism - Change, Mutating, Transforming, Staging]]
	[[Mechanism - Bridge, Tie-Back, Bijection, Decomposes, Enumerates, Normalizes, 1-1, 1-M, M-1, M-M]]
	[[Mechanism - Change + Dimension Management, Retro Disruptive, Upsert]]

[[Mechanism - High-signal, Low friction, Tight, Brevity]]
	[[Mechanism - Uptick, Downtick, Upside, Downside, Lift, Drop]]
	[[Mechanism - Flatten the Line, Flatten Curve, Curb Trend, Wrangle Data]]
	[[Mechanism- Finance Talk, Revops, Data Trust Discussions]]
	[[Mechanism - Dispersion Error, Points of Error]]
[[Mechanism - Trade-offs, Offsets, Burn Rates, Fill Rates]]


[[Mechanism - Causal Attribution Models]]
[[Mechanism - Source-Driven Deterministic Semantic Definition]]
[[Mechanism - Idempotent vs Overfitting]]

[[Mechanism - Goal Setting, Primary vs Stretch Goal]]
[Mechanism - Careful, Prudence, Measure Twice Cut Once]

[Mechanism - Consensus, Quorom, Agency]
[[Mechanism - Coaching People]]
[[Mechanism - Preference, Choosing]]
[[Mechanism - Platitudes, was about to chime up]]


Thinking
- [fractal]
- [totalized]
- narrow-lens
- multi-furcate
- auto-scrubbers --> semantic integrity controls

Actions
- redacted
- deprecated 
- demoted

Mutating Data
- anonymized data
- synthetic data
- masked data

Relationships
- clusters
- roll-ups
- drill-downs

Edges + Flows
- mono-hierarchal
- poly-hierarchal
- mono-directional
- bi-directional
- causal-attribution
- mitosis; split
- pre-cursor, predicate

Denominator Names
- capacity
- candidate

Build
- spin-up
- stand-up
- initialize
- harden
- finalize
- mature, maturation

| base         | vs                             |
| ------------ | ------------------------------ |
| redacted<br> | unredacted, exposed, published |
| deprecated   | inserted, appended, activated  |
| demoted      | promoted, elevated             |
| deconstruct  | reconstruct                    |


Measure Types
- count (rows)
- sum
- ratio
- avg

```
completed
added
removed
answered
repushed
routed
met-with
noted
recorded
budgeted
planned
would-adjust
would-refactor
would-validate-earlier
would-standardize

Planned
Queued
Deferred
Proposed
Outlined
Recommended
Standardized
Hardened
Simplified
Normalized
Generalized
Parameterized
```

[[Mechanism - Taxonomy - Employment Reasons]]