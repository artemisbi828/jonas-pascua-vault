- **Quality Gate**
- load time thresholds = 20%
- Drill-down to error details and logs

Sanitizing Data Types
- Use for reusable conformed dimensions, facts, heavy joins, and large aggregations.
- Best for governed, high-concurrency reporting.

Staging Patterns
	- **mutating** new objects → landing zone


**Data quality dimensions** --  completeness, consistency, etc
	- reduce the barrier to entry for data quality rule
	- configuration thresholds (LEQ, GEQ, LT, GT)
	- alerts
	- which columns are the most popular (downstream count) --> prioritization
- persona: like netflix-profiles.
