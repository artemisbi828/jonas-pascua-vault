```text
SQL SERVICE ACCOUNTS
Database >> Security >> Sql Server and Windows Authentication Mode == **Mixed Mode**
Restart SQL Server Service >> right click on SERVER. select **Restart**
LoginProperties >> UserMapping >> **db_datareader** or **db_owner** (full control)
```

1) basic version string
````sql
SELECT @@VERSION AS VersionString;
````

2) detailed properties
````sql
SELECT
  SERVERPROPERTY('ProductVersion') AS ProductVersion,
  SERVERPROPERTY('ProductLevel')   AS ProductLevel,
  SERVERPROPERTY('Edition')        AS Edition,
  SERVERPROPERTY('EngineEdition')  AS EngineEdition;
````

3) database compatibility level (run in the target DB)
````sql
SELECT DB_NAME() AS DatabaseName, compatibility_level
FROM sys.databases
WHERE name = DB_NAME();
````

4) check Ad Hoc Distributed Queries config (needed for OPENROWSET)
````sql
EXEC sp_configure 'show advanced options', 1; RECONFIGURE;
EXEC sp_configure 'Ad Hoc Distributed Queries';
````

5) SQL Server service account (to verify file access permissions)
````sql
SELECT servicename, service_account, status
FROM sys.dm_server_services;
````

