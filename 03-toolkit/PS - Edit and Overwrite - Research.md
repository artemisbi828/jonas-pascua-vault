#status/deferred/quick-paste-merge-later -- I think this is what it's doing but not 100 sure

```powershell
PS C:\vsWorkspace\jpascua313\site\docs> cd C:\vsWorkspace\jpascua313\site\docs; @"     
>> ---
>> id: resume
>> title: Jonas Pascua - Resume
>> sidebar_label: Resume
>> ---
>>
>> # JONAS PASCUA
>> **BI Developer & Data Engineer**
>> (248) 457-5312 | [jpascua@gmail.com](mailto:jpascua@gmail.com) | Asheville, NC
>> [LinkedIn](https://linkedin.com/in/jonaspascua)
>>
>> ---
>>
>> ## Core Competencies
>>
>> | Data Engineering | BI & Analytics | Databases |
>> | :--- | :--- | :--- |
>> | Azure Data Factory, Fabric | Power BI (DAX, RLS) | SQL Server (T-SQL), PostGres |
>> | PySpark, Python | Paginated Reports | Snowflake, IBM DB2 |
>> | Azure DevOps, Git | Financial Modeling | Redgate Toolbelt |
>>
>> ---
>>
>> ## Professional Experience
>>
>> ### SMILE DOCTORS | Austin, TX
>> *Business Intelligence Developer | Oct 2021 – Present*
>>
>> * **Led Power BI Deployment:** Orchestrated dashboards for 550+ locations, influencing KPI benchmarks for 5000+ employees and maximizing data quality for executive-level actionable insights.
>>
>> * **Engineered Fabric Pipelines:** Built automated API pipelines via **PySpark** for Equifax credit scoring.       
>>
>> * **AI Readiness:** Documented metadata architecture for **AI Model Context Protocol (MCP)** for Co-Pilot integration.
>>
>> * Oversight on 5 capital expenditure (CAPEX) projects via Azure Devops, including consolidation of multiple Patient Management Systems (Cloud9, OrthoFi) into a unified data lake with row level security to comply with HIPPAA audit requirements.
>>
>> * Specialized in high-availability SQL Server environments (DEV/TEST/PROD) using Redgate (SQL Compare, Test, Source Control) for seamless deployments and zero-downtime database maintenance; responsible for replication debugging, indexing, query tuning and load balancing.
>>
>> ---
>> ### LIFE CARE SERVICES | Des Moines, IA
>> *Senior Financial Manager | Mar 2021 – July 2021
>>
>> - Presented monthly FP&A analysis to leadership for a $16M annual net income portfolio (150 communities), summarizing budget vs. actual variance drivers and operational plan performance.
>>
>> - Streamlined financial reporting processes and managed SQL data pipelines from various sources (Point-Click-Care, Salesforce) to financial systems (Hyperion, Oracle, Adaptive, Power BI).
>>
>> - Led the actuarial team in financial feasibility studies, using VB and T-SQL to prepare and load data into the Adaptive platform.
>>
>> ---
>> ### THE WITTERN GROUP | Clive, IA
>> *Finance Analyst, SQL DBA | Dec 2019 – Mar 2021
>>
>> - Oversaw a full ERP cloud migration from IBM DB2 to INFOR CSI (AWS), serving as the lead SQL DBA for MS SQL Servers (2012, 2014, 2019) and migrating over 37M+ business records.
>>
>> - Automated data ingestion from raw CSV/XML sources into staging databases using SQL Server PowerShell and BCP functions, scheduling jobs and notifications via SQL Server Agent.
>>
>> - Improved operational efficiency on the machine production floor by creating real-time, parameterized DBmail notifications for operators and managers.
>>
>> - Designed and deployed dashboards using Power BI and Excel, focusing on trend analysis, identifying outliers, and correlating root-cause drivers to performance changes.
>>
>> ---
>>
>> ### TITAN INTERNATIONAL, INC | Des Moines, IA
>> *Business Analyst | Sept 2017 – Dec 2019*
>>
>> - Reduced legacy processing time by 85% for month-end close tasks (journal entries, reconciliation, accruals) by applying custom Excel MACROs.
>>
>> - Led the initiative to digitize AP workflow ($400M annual disbursements) in preparation for an ORACLE ERP transition, utilizing linear regression and Kaizen to reduce aging unvouchered receipts by 70%.
>>
>> - Reallocated 83% of AP clerk workflow by reverse engineering IBM AS400 queries to automate the 3-Point Match process for intercompany invoicing.
>>
>> - Developed real-time Power BI dashboards from a cloned ERP sister database (3NF/ODBC), bridging an information gap between Accounting, Receiving, and Purchasing; efforts led to a promotion and expanded territory oversight.
>>
>> * **Excel Macro Automation:** Reduced legacy processing time by 85% for month-end close tasks.
>>
>> ---
>>
>> ### Education
>> **UNIVERSITY OF MICHIGAN | Ross School of Business**
>> *Bachelor of Business Administration*
>> *Emphases in Finance & Corporate Strategy*
>>
>> ---
>>
>> ## Interests
>> * **Professional Violinist**
>> * **Brazilian Zouk Dance Teacher**
>> * **Martial Arts:** Muay Thai & MMA
>> "@ | Out-File -FilePath resume.md -Encoding UTF8
```