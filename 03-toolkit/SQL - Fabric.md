[[SQL - Fabric - Find and Replace (Sublime)]]
[[SQL - Fabric - Create Table vs SSMS]]
[[SQL - Get Tables#Fabric Version]]

[[SQL - Fabric - No Recursive CTE]]

[[SQL - Fabric - Mirrored DB to Lakehouse]]
[[SQL - Fabric Collation Error]]


--- 
Lakehouse -- PySpark
	SQL Endpoint -- same SQL endpoint for all data sources

Warehouse - TSQL Native -- 

Lakehouse → Materialized | Warehouse

### Join Problem on GUIDs
wrap lower(ALLCAPS-GUIODS)

Add this for **each GUID** on each side of join 
> COLLATE Latin1_General_100_CI_AS_KS_WS_SC_UTF8

[SQL - Fabric - Transformation]
[[SQL - Fabric - SmileDoctorsEDW vw_NPEAdded]]


# Structure
- TENANT -- Billing Entity
- CAPACITY -- Budget/Limit
- WORKSPACE -- Consumption of Budget (Viewer Access)
	- App
	- Dataset (Build Access)

Semantic models have **their own permission model**:

| Permission  | What it allows                             |
| ----------- | ------------------------------------------ |
| **Read**    | Consume existing reports only              |
| **Build**   | Create new reports, Analyze in Excel, XMLA |
| **Reshare** | Grant access to others                     |
| **Write**   | Modify the model                           |
| **Owner**   | Full control                               |


Fabric → DataWarehouse → SD-EDW
	Lake → SmileDoctorODS
	Snowflake.dbo.Location → Snowflake_EDW_Prod.EDW.D_Location
	jbi Objects → **NO DATABASE**
	