**Short answer:**

For **Azure SQL** and **Fabric SQL Endpoints / Warehouses**, use:

```text
Encrypt = Mandatory (Yes)
Trust Server Certificate = No
```

That's the normal, preferred configuration.

***

## Recommended Settings

### Azure SQL

```text
Server:
myserver.database.windows.net

Authentication:
Microsoft Account / Azure AD

Encrypt:
Mandatory

Trust Server Certificate:
False / No
```

***

### Fabric Warehouse / SQL Analytics Endpoint

```text
Server:
*.datawarehouse.fabric.microsoft.com

Authentication:
Microsoft Account

Encrypt:
Mandatory

Trust Server Certificate:
False / No
```

***

## What These Settings Actually Mean (EIL5)

### Encrypt = Mandatory

```text
Laptop ─── encrypted tunnel ─── SQL Server
```

Nobody can read the traffic while it travels.

Think:

```text
HTTPS for SQL
```

Use **Mandatory**.

***

### Trust Server Certificate

This asks:

```text
Do you want me to verify
that this server is genuinely Microsoft?
```

If:

```text
Trust Server Certificate = No
```

VS Code verifies the server identity.

If:

```text
Trust Server Certificate = Yes
```

VS Code says:

```text
"I'll trust whatever certificate you give me."
```

Good for troubleshooting.

Not ideal long-term.

***

## If Connection Fails

Try:

```text
Encrypt = Mandatory
Trust Server Certificate = Yes
```

**ONLY as a diagnostic step.**

If that suddenly works, then you likely have:

* certificate validation issue
* proxy inspection
* corporate network interference
* outdated trust chain

***

## For Your Fabric Endpoint

I'd start with:

```text
Server:
uzqevjhdxb2ufl6rsiz4oqntva-axvquyn3ojqubl3bmqauwwbmbe.datawarehouse.fabric.microsoft.com

Authentication:
Microsoft Account

Encrypt:
Mandatory

Trust Server Certificate:
No
```

If authentication still fails, the next thing I'd investigate is **which Microsoft identity VS Code is actually using**. Given your earlier description ("SSMS works, VS Code doesn't"), that is statistically a more common root cause than certificate settings.

If you get the exact error message after clicking **Connect**, paste it and I can walk through the diagnosis step-by-step.
