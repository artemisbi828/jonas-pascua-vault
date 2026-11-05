## Abbreviation Reference — Project Ascend

### Azure Infrastructure

| Abbreviation | Full Name | Description |
|---|---|---|
| **ADLS** | Azure Data Lake Storage | Microsoft's cloud storage service. Gen2 (ADLS Gen2) adds Hierarchical Namespace (HNS), enabling true directory-level RBAC and structured path partitioning. |
| **ADF** | Azure Data Factory | Azure's managed ETL/ELT orchestration service. Used in this project to extract from source systems and write Parquet files to ADLS. |
| **HNS** | Hierarchical Namespace | The ADLS Gen2 feature (`is_hns_enabled = true`) that makes storage act like a real file system with directories, enabling path-level RBAC and atomic rename operations. |
| **VNet** | Virtual Network | Azure's isolated private network. ADF runs inside a Managed VNet to route all data movement through the Azure backbone, never the public internet. |
| **IR** | Integration Runtime | The compute infrastructure ADF uses to execute pipeline activities. The Managed VNet IR runs inside Azure; self-hosted IR runs on-premises or in a private network. |
| **PE** | Private Endpoint | A private IP address inside a VNet that maps to an Azure service (e.g., Azure SQL). ADF uses Managed Private Endpoints so traffic to C9 Central never leaves the Azure network. |
| **MSI / MI** | Managed Identity (System-Assigned) | An Azure AD identity automatically provisioned for an Azure resource (e.g., ADF). Eliminates the need to store credentials — ADF authenticates to Key Vault and ADLS using its MSI. |
| **SAS** | Shared Access Signature | A time-limited, permission-scoped URL token for Azure Storage access. **Not used** in this project — Managed Identity and Storage Integration replace it. |
| **RBAC** | Role-Based Access Control | The Azure (and Snowflake) permission model where access is granted via roles assigned to identities rather than directly to individuals. |
| **ACL** | Access Control List | Fine-grained file/directory permissions available on ADLS Gen2 paths. Complementary to RBAC; used for directory-scoped write grants per source. |
| **LRS** | Locally Redundant Storage | Azure storage replication that keeps three copies within a single datacenter. Used for the Dev/Test landing zone; Prod typically uses GRS. |
| **GRS** | Geo-Redundant Storage | Azure storage replication that copies data to a paired region. Higher durability than LRS at higher cost. |
| **TFC** | Terraform Cloud | HashiCorp's hosted service for storing Terraform state and running `plan`/`apply`. The project's Terraform state backend. |
| **HCL** | HashiCorp Configuration Language | The declarative language used to write Terraform resource definitions (`.tf` files). |

### Data Platform & Pipeline

| Abbreviation | Full Name | Description |
|---|---|---|
| **ELT** | Extract, Load, Transform | The platform's pipeline order: ADF extracts raw data and loads it into Snowflake (Raw), then SQLMesh transforms it in-database through Bronze → Silver → Gold. |
| **ETL** | Extract, Transform, Load | The traditional alternative where transformation happens before loading. Used loosely in the docs but ELT is the actual pattern here. |
| **CDC** | Change Data Capture | A technique that captures only changed rows from a source system by reading a database's transaction log. Listed as a "decision pending" incremental pattern in this project. |
| **SCD** | Slowly Changing Dimension | A dimension table design pattern for tracking historical attribute changes (e.g., Type 1 overwrites, Type 2 adds history rows). Relevant to Gold layer modeling. |
| **DDL** | Data Definition Language | SQL statements that define schema structure: `CREATE TABLE`, `ALTER TABLE`, `DROP`. Used when Terraform provisions Snowflake objects. |
| **DML** | Data Manipulation Language | SQL statements that modify data: `INSERT`, `UPDATE`, `MERGE`. Used in Snowpipe `COPY INTO` and SQLMesh model execution. |
| **CTE** | Common Table Expression | A named temporary result set within a SQL query, defined with `WITH`. Used extensively in SQLMesh Bronze/Silver model SQL. |
| **UDF** | User-Defined Function | A custom function stored in the database and callable from SQL. Stored in `UTIL_COMMON` for reuse across models. |
| **UUID** | Universally Unique Identifier | A 128-bit identifier guaranteed to be globally unique. The `{adf_run_id}` in the landing path is a UUID sourced from `@pipeline().RunId`. |

### Timestamps & Data Types

| Abbreviation | Full Name | Description |
|---|---|---|
| **UTC** | Coordinated Universal Time | The universal time standard with no timezone offset. All platform timestamps are stored in UTC. The landing path date partition (`{yyyy}/{mm}/{dd}`) uses UTC. |
| **NTZ** | No Time Zone | Snowflake's `TIMESTAMP_NTZ` type — a timestamp with no timezone offset stored, assumed UTC. The platform standard for all audit columns (`CRT_TS`, `SRC_CRT_TS`, etc.). |
| **TZ** | Time Zone | Snowflake's `TIMESTAMP_TZ` type — stores the timestamp with its original timezone offset. Used for raw source timestamp columns that may carry timezone context. |
| **ISO 8601** | International Standard 8601 | The international date/time format standard (e.g., `2026-04-07T14:32:00Z`). ADF's `pipeline().TriggerTime` returns ISO 8601 UTC. |

### Snowflake

| Abbreviation | Full Name | Description |
|---|---|---|
| **SLA** | Service Level Agreement | A formal commitment on data availability, freshness, and quality between the platform team and data consumers. Defined per source in the onboarding template. |
| **RLS** | Row-Level Security | A data governance control that restricts which rows a user can see in a query result, based on their role. Implemented in Snowflake via policies. |
| **SME** | Subject Matter Expert | The business domain expert responsible for defining business rules and validating metric definitions. Referenced in the onboarding SLA template. |

### Healthcare / Business Domain

| Abbreviation | Full Name | Description |
|---|---|---|
| **PMS** | Practice Management System | Software used by dental/healthcare practices to manage scheduling, billing, and patient records. C9 Central is the PMS in this project. |
| **ERP** | Enterprise Resource Planning | Integrated business management software for finance, HR, and operations. Workday/Dayforce are ERP sources in this project. |
| **PHI** | Protected Health Information | Any individually identifiable health information regulated under HIPAA. Drives the project's masking, RLS, and environment isolation requirements. |
| **HIPAA** | Health Insurance Portability and Accountability Act | U.S. federal law governing the privacy and security of PHI. Cited as the compliance driver for column-level masking in `GOV_COMMON` and lower-environment data refresh strategy. |
| **UCR** | Usual and Customary Rate | The gross production amount billed before any adjustments. Used in the Net Collection Rate formula in the C9 Central metrics docs. |
| **NCR** | Net Collection Rate | The ratio of net payments collected to net production. A core KPI derived from C9 Central data: $NCR = \frac{\text{Net Payments Collected}}{\text{Net Production}}$ |
| **SoR** | System of Record | The authoritative source for a given business entity or dataset. Marked on the Data Source Onboarding template to identify which system "owns" the truth for each domain. |

### DevOps & Engineering

| Abbreviation | Full Name | Description |
|---|---|---|
| **CI/CD** | Continuous Integration / Continuous Deployment | The practice of automating code testing (CI) and environment deployment (CD). GitHub Actions is the CI/CD platform for SQLMesh model promotion and ADF pipeline deployment. |
| **SFTP** | Secure File Transfer Protocol | An encrypted file transfer protocol. Used as one of the three ingestion patterns for partner-delivered file drops. |
| **REST** | Representational State Transfer | The architectural style for stateless HTTP APIs. OrthoFi and most SaaS sources expose REST APIs consumed by ADF or the `APIIngestionClient` library. |
| **API** | Application Programming Interface | A defined interface for software systems to communicate. Used broadly; in platform context refers specifically to REST APIs exposed by SaaS source systems. |
| **JSON** | JavaScript Object Notation | A lightweight text format for structured data. ADF pipeline and dataset definitions are stored as JSON; endpoint config files (`adf/config/`) are JSON arrays. |
| **YAML** | YAML Ain't Markup Language | A human-readable data serialization format. Used for SQLMesh model schema definitions and GitHub Actions workflow files. |
| **BI** | Business Intelligence | Tools and practices for analyzing and visualizing data. Power BI is the BI layer consuming Snowflake Gold/Virtual layer views in this project. |
| **KPI** | Key Performance Indicator | A measurable value used to evaluate performance against business objectives. The metric decomposition work in Sprint 2 maps KPIs to source entities. |

### General

| Abbreviation | Full Name | Description |
|---|---|---|
| **CMS** | Customer Management System | |
| **UI** | User Interface | |