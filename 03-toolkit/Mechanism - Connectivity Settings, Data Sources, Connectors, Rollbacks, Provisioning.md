- Secrets Management (Key Vault)
- System-User

- Data Sources & Connectors
	- databases (CDC)
	- APIs (REST/GraphQL) → SaaS application data can be efficiently ingested 
		- REST APPI authentication
		- OAuth 2.0 API key bearer token
		- Rate limiting and throttling
		- Pagination (cursor-based and offset-based)
		- Config-driven API setting (opinionated framework, 1st class citizen)
	- files (CSV/Parquet) → S3 Azure Blob GCS → Snowpipe
	- streaming (Kafka)
	- rollbacks

- Data Integrity Engine
- CI/CD; Version-Control Strategy
	- Major-Minor-Hotfix{Patch}
	- Scheduled vs Unscheduled
	- Code Refactoring → SQL/Code Linting → SQLFluff Library
- Access Provisioning
	- Service accounts must be in the correct timezone (eg)
- Registry
- One-time obfuscation:  means you scramble something in a way that is safe _only because it is used once. If it’s reused, the protection breaks down.

```
Terraform to Standup
- ADF - IT Operational Standpoint → Snowflake → Airflow
- Keyvault
dbt → Jinja-driven incremental logic
Text Replacement (i/o "Find and Replace")
DBT against the data it's running. If it doesn't work you have to roll everything back, b/c it is a destructive-transformation (one way only)
```