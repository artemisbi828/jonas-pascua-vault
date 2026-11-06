[Dimensions]
[Stages]
[[Mechanism]]
[[Mechanism - Approach Vectors, State vs Stage, Stages vs Mechanisms]]
[[Tools - Documentation]]


- quorom
- do we have a quarry to mine? 
- not found
	- !exists - wrong place
	- !exists - right place
	- +exists but nsf permissions

SQL ENGINES: Snowflake. SQL Server, Databricks, BigQuery
SEMANTIC LAYER: Power BI / Looker / MetricFlow
TABLE-NAMING: use **snake_case**, tables are plural
- normalized tables -- customers | patients, appointments, contracts | orders
- dim_customer -- singular, 
- fact_sales - plural
- stg_
AVOID: date, user, group, order, rank, value (often reserved or confusing)
COLUMN-NAMING
- date_value | order_date
- user_id, customer_id, 
- sort_order | sequence_num, rank_num
- is_active, has_opted_in
- group_name
- sales_amount
- conversion_pct
- metric_value
- description | comment


---
1. Daily Pipelines should never break. Things that are decided to be distinct should have dedup-filter + prioritization rules. 
```
INR where RN = 1
```
	
	Validation queries are there to ensure integrity. Warnings are prioritized (P1,P2,P3)
	

3. Config tables should be `business-facing` and `business-governed`. Should have start and end dates of what dates they should affect.

# Silver Layer Medallion Normalization
Business Definitions
- Floor Date: Portfolio vs Per Location Conversion Date
String Values should be normalized on ingest (trim) - leading and trailing spaces should be removed
Money values should be decimal(18,4)

# Data Refresh Considerations
Aggregate tables for speed (by-month or by-day)
Incremental ModifiedDate for refresh

# UAT Considerations
Do as much as you can using SQL-VIEWS
Use small samples for speed for semantic-models

# UX Considerations
3-30-300 Layout
Standard Formatting
Standard Elements
- Basics
	- as-of-date 
- Header Bar
- Slicers
- Panels | Trendlines (shielded from slicers?)
Advanced Elements
- Data Dictionary 
- SSS Calc-Group
- WDE Calc-Group

# Validation Considerations
Test on locations and check if trendlines don't have any unexpected **fall-offs** or **spikes**