## SQL & Data Terminology Dictionary

```
DDL → shapes data
DML → moves data
DCL → protects data
TCL → protects consistency

ETL / ELT → pipelines
OLTP / OLAP → workloads
Facts / Dimensions → analytics model
```

---
ETL:: Extract, Transform, Load -- transform using staging server before loading
- better data privacy, lower storage costs
ELT:: Extract, Load, Transform -- cloud 
- faster ingestion, high scalability, supports unstructured data, retains raw data for future needs


| Term                  | Stands For                                    | Category           | What It Means (Plain English)               | Typical Examples / Usage                                                                               | Sort |
| --------------------- | --------------------------------------------- | ------------------ | ------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---- |
| **TCL**               | Transaction Control Language                  | SQL                | Manages transaction boundaries              | Commit, rollback                                                                                       | 6    |
| **DCL**               | Data Control Language                         | SQL / Security     | Controls permissions and access             | Grant, revoke                                                                                          | 5    |
| **DML**               | Data Manipulation Language                    | SQL                | Reads or changes _data rows_                | Insert, update, delete, select                                                                         | 4    |
| **DDL**               | Data Definition Language                      | SQL                | Defines or changes database _structure_     | Create tables, alter columns, drop indexes                                                             | 3    |
| **ELT**               | Extract, Load, Transform                      | Data Pipeline      | Transform data **after** loading to target  | Modern cloud warehouses; faster ingestion, high scalability, supports unstructured data, preserves raw | 2    |
| **ETL**               | Extract, Transform, Load                      | Data Pipeline      | Transform data **before** loading to target | Legacy warehouses; better data privacy, lower storage costs                                            | 1    |
| **OLTP**              | Online Transaction Processing                 | Workload Type      | High‑volume, row‑level operations           | PMS, ERP, EHR systems                                                                                  |      |
| **OLAP**              | Online Analytical Processing                  | Workload Type      | Large scans and aggregations                | BI reports, dashboards                                                                                 |      |
| **CDC**               | Change Data Capture                           | Ingestion          | Captures row‑level changes                  | Insert/update/delete feeds                                                                             |      |
| **SCD**               | Slowly Changing Dimension                     | Modeling           | Tracks dimension history over time          | Type 1 / 2 / 3 dimensions                                                                              |      |
| **RDBMS**             | Relational Database Management System         | Platform           | SQL‑based database engine                   | SQL Server, Postgres                                                                                   |      |
| **ACID**              | Atomicity, Consistency, Isolation, Durability | Transaction Theory | Guarantees reliable transactions            | Financial systems                                                                                      |      |
| **Schema**            | —                                             | Data Structure     | Logical namespace for objects               | Tables grouped by domain                                                                               |      |
| **Index**             | —                                             | Performance        | Data structure to speed lookups             | Clustered / non‑clustered                                                                              |      |
| **View**              | —                                             | Abstraction        | Stored query over tables                    | Security, reuse, simplification                                                                        |      |
| **Materialized View** | —                                             | Performance        | Precomputed query results                   | Aggregate acceleration                                                                                 |      |
| **Fact Table**        | —                                             | Data Modeling      | Stores measurable events                    | Payments, appointments                                                                                 |      |
| **Dimension Table**   | —                                             | Data Modeling      | Stores descriptive attributes               | Patient, location                                                                                      |      |
| **Grain**             | —                                             | Modeling Concept   | Level of detail per row                     | One row per visit                                                                                      |      |
| **Cardinality**       | —                                             | Data Concept       | Distinct value count                        | Low vs high cardinality                                                                                |      |
| **Predicate**         | —                                             | Query Logic        | Filtering condition                         | Where clause logic                                                                                     |      |
| **Surrogate Key**     | —                                             | Modeling           | Artificial primary key                      | Identity / sequence                                                                                    |      |
| **Natural Key**       | —                                             | Modeling           | Business‑meaningful key                     | MRN, appointment ID                                                                                    |      |
| **Idempotent**        | —                                             | Data Engineering   | Safe to run repeatedly                      | Replays without duplication                                                                            |      |
