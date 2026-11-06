```table-of-contents
```

Yes. You can absolutely get to **95%+ SSMS replacement** with VS Code.

For your use case (Azure SQL, Fabric SQL Analytics Endpoint, Fabric Warehouse, BI/EDW development), I'd actually recommend:

```text
VS Code
├─ MSSQL Extension
├─ SQL Database Projects Extension
├─ GitHub Copilot
├─ PowerShell
├─ Python
└─ Fabric web UI
```

Keep SSMS only as an emergency fallback for the first few weeks.

***

# 1. Install VS Code Extensions

## Required

### MSSQL

Microsoft's SQL extension.

```text
Extension ID:
ms-mssql.mssql
```

Provides:

* Connect to SQL Server
* Azure SQL
* Fabric Warehouse
* Fabric SQL Analytics Endpoints
* Query windows
* Results grids
* Execution plans
* Intellisense

***

### SQL Database Projects

```text
Extension ID:
ms-mssql.sql-database-projects-vscode
```

Equivalent to SSDT-lite.

Useful for:

* schema versioning
* DACPAC deployment
* source control

***

### GitHub Copilot

```text
GitHub Copilot
GitHub Copilot Chat
```

Huge productivity gain for SQL.

***

# 2. Connect to Azure SQL

Open command palette:

```text
Ctrl+Shift+P
```

Execute:

```text
MS SQL: Connect
```

Enter:

```text
Server:
myserver.database.windows.net

Authentication:
Microsoft Account

Database:
mydb
```

or

```text
Authentication:
Azure MFA
```

depending on environment.

***

# 3. Connect to Fabric

For Fabric Warehouse or SQL Endpoint:

```text
Ctrl+Shift+P
MS SQL: Connect
```

Server:

```text
uzqevjhdxb2ufl6rsiz4oqntva-axvquyn3ojqubl3bmqauwwbmbe.datawarehouse.fabric.microsoft.com
```

Authentication:

```text
Microsoft Account
```

or

```text
Azure Active Directory
```

depending on tenant policy.

If SSMS works but VS Code doesn't:

```text
MS SQL: Clear Connection Profiles
MS SQL: Sign Out
```

then reconnect.

***

# 4. Reset Authentication Cache

One of the biggest frustrations.

### VS Code Account

```text
Ctrl+Shift+P

Accounts: Sign Out
```

***

### MSSQL Extension

```text
MS SQL: Sign Out
```

***

### Remove Cached Tokens

Windows:

```text
Credential Manager
```

Delete:

```text
Azure
Microsoft
Fabric
Power BI
SQL
```

entries related to old identities.

Then restart VS Code.

***

# 5. Create a SQL Workspace

I would organize like this:

```text
repos
├─ data-platform
├─ sql-scratchpad
├─ fabric-admin
└─ analytics
```

Example:

```text
sql-scratchpad
├─ ad_hoc
├─ validation
├─ profiling
├─ troubleshooting
└─ archive
```

Every query becomes source-controlled.

***

# 6. Replace SSMS Features

| SSMS               | VS Code             |
| ------------------ | ------------------- |
| Query Window       | SQL File            |
| Registered Servers | Connection Profiles |
| Results Grid       | Results Grid        |
| Execution Plan     | Execution Plan      |
| Object Explorer    | MSSQL Explorer      |
| Git Plugin         | Native Git          |
| Snippets           | Native Snippets     |
| SQL Agent          | Azure Portal/Fabric |

***

# 7. Useful Settings

Enable auto save:

```json
"files.autoSave": "afterDelay"
```

Format on save:

```json
"editor.formatOnSave": true
```

SQL word wrap:

```json
"editor.wordWrap": "on"
```

Large files:

```json
"editor.largeFileOptimizations": true
```

***

# 8. Common Pitfalls

## Pitfall #1

Using multiple Microsoft accounts

Example:

```text
Company Account
Personal Account
Consulting Account
```

VS Code often silently picks the wrong token.

Symptom:

```text
Login succeeds
Database access denied
```

Fix:

```text
Accounts: Sign Out
MS SQL: Sign Out
```

then reconnect.

***

## Pitfall #2

Fabric endpoint ≠ SQL Server endpoint

People connect here:

```text
workspace.fabric.microsoft.com
```

instead of:

```text
*.datawarehouse.fabric.microsoft.com
```

Use the SQL endpoint server name.

***

## Pitfall #3

Leaving SSMS authentication cached

SSMS succeeds.

VS Code fails.

Root cause:

```text
Different token cache
Different auth provider
```

Always test with:

```text
sqlcmd
VS Code
SSMS
```

independently.

***

## Pitfall #4

Opening massive result sets

SSMS tolerates abuse.

VS Code less so.

Bad:

```sql
SELECT *
FROM giant_fact_table;
```

Better:

```sql
SELECT TOP 1000 *
FROM giant_fact_table;
```

***

## Pitfall #5

Treating ad hoc SQL as disposable

Recommendation:

```text
Every query saved.
Every query committed.
Everything in Git.
```

Future-you will thank present-you.

***

# 9. My Recommended End State

```text
VS Code
├─ MSSQL Extension
├─ GitHub Copilot
├─ Git
├─ PowerShell
├─ Python
└─ Fabric SQL Connections

SSMS
└─ Installed only as fallback
```

For a BI Developer working with Azure SQL, Snowflake/Fabric-style EDW work, and source-controlled SQL, VS Code is generally a superior daily driver because it combines SQL development, Git, Python, PowerShell, documentation, and Copilot in a single workspace instead of constantly switching between tools.
