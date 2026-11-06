

```sql
# check for disabled, locked, must_change_password
SHOW USERS LIKE '%zak%';
```

---
Below is a **concrete, minimal‑step Snowflake permission diagnosis playbook** you can run **top‑down**. I’ll also give you **exact prompts to paste outputs back here**, in the **smallest set of info** needed so we can pinpoint and fix the issue fast.

I will **not** make you wait or defer work—everything below is executable immediately.

***

# Snowflake User Lost Access — Fast Diagnosis & Fix Guide

## Goal

Determine **why a user lost access** and **what permission must be restored**, with the fewest checks possible.

***

## Step 0 — Capture only the essentials (paste back)

Before running anything else, collect **exactly this**:

```text
USERNAME:
WHAT FAILED (query / warehouse / database / schema / table / role / login):
ERROR MESSAGE (exact text):
WHEN IT LAST WORKED (approx):
```

That alone already narrows \~70% of cases.

***

## Step 1 — Confirm the user is not disabled or locked

Run as ACCOUNTADMIN or SECURITYADMIN:

```sql
SHOW USERS LIKE '<username>';
```

### Check:

*   `DISABLED = true` → **Root cause**
*   `LOCKED = true` → **Root cause**
*   `MUST_CHANGE_PASSWORD = true` → common login blocker

✅ **Fix**

```sql
ALTER USER <username> SET DISABLED = FALSE;
ALTER USER <username> SET LOCKED = FALSE;
```

If this fixes login, stop here.

***

## Step 2 — Check current & default roles (MOST COMMON ISSUE)

Lost access is very often a **role switch or role removal**.

```sql
SHOW GRANTS TO USER <username>;
```

### Look for:

*   Missing **expected role**
*   Role exists but is **not DEFAULT\_ROLE**
*   User is logging in with `PUBLIC` only

✅ **Immediate fix**

```sql
ALTER USER <username> SET DEFAULT_ROLE = <expected_role>;
```

or re‑grant:

```sql
GRANT ROLE <expected_role> TO USER <username>;
```

> ⚠️ If the user *can* login but objects are missing, this is almost always the issue.

***

## Step 3 — Verify the role still has permissions

If the role exists but access is gone, the role itself may have been altered.

```sql
SHOW GRANTS TO ROLE <role_name>;
```

### Look for missing:

*   `USAGE` on database
*   `USAGE` on schema
*   `SELECT / INSERT / etc.` on tables/views
*   `USAGE` on warehouse

✅ **Fix example**

```sql
GRANT USAGE ON DATABASE my_db TO ROLE my_role;
GRANT USAGE ON SCHEMA my_db.my_schema TO ROLE my_role;
GRANT SELECT ON ALL TABLES IN SCHEMA my_db.my_schema TO ROLE my_role;
```

***

## Step 4 — Warehouse access (very common silent failure)

If queries fail with warehouse errors:

```sql
SHOW GRANTS TO ROLE <role_name>;
```

### Required:

```text
USAGE on WAREHOUSE <warehouse_name>
```

✅ **Fix**

```sql
GRANT USAGE ON WAREHOUSE <warehouse_name> TO ROLE <role_name>;
```

***

## Step 5 — Role hierarchy regression (admin cleanup issue)

Sometimes permissions were indirect and a parent role was modified.

```sql
SHOW GRANTS OF ROLE <role_name>;
```

If the role **lost its parent**, inherited access disappears.

✅ **Fix**

```sql
GRANT ROLE <parent_role> TO ROLE <role_name>;
```

***

## Step 6 — Object ownership change (sneaky one)

If DDL suddenly fails:

```sql
SHOW OBJECTS LIKE '<object_name>' IN <db>.<schema>;
```

Check `OWNER`.

✅ **Fix**

```sql
GRANT OWNERSHIP ON <object> <name> TO ROLE <role_name> COPY CURRENT GRANTS;
```

***

## Step 7 — Network / policy / SSO issues (login works elsewhere?)

If login suddenly fails only from certain locations:

```sql
SHOW NETWORK POLICIES;
SHOW PARAMETERS LIKE 'NETWORK_POLICY' FOR USER <username>;
```

✅ **Fix**

```sql
ALTER USER <username> UNSET NETWORK_POLICY;
```

***

## Step 8 — Audit what changed (if this was “sudden”)

Snowflake keeps grant history:

```sql
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS
WHERE GRANTEE_NAME = '<username>'
ORDER BY CREATED_ON DESC;
```

And role changes:

```sql
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_ROLES
WHERE ROLE_NAME = '<role_name>'
ORDER BY CREATED_ON DESC;
```

This shows **exactly what was removed and when**.

***

# The 90% Fix Pattern

If you want the fastest likely fix **without overthinking**:

1.  ✅ Re‑grant the role
2.  ✅ Set it as default
3.  ✅ Ensure warehouse usage

```sql
GRANT ROLE my_role TO USER my_user;
ALTER USER my_user SET DEFAULT_ROLE = my_role;
GRANT USAGE ON WAREHOUSE my_wh TO ROLE my_role;
```

***

## Paste these back next (minimum needed)

To diagnose *precisely* with zero extra steps, paste:

1.  Output of:

```sql
SHOW USERS LIKE '<username>';
```

2.  Output of:

```sql
SHOW GRANTS TO USER <username>;
```

3.  The **exact error message** the user sees

From there, I’ll tell you **exactly which GRANT/ALTER fixes it**, no guesswork.

If this user is tied to **dbt, Power BI, Tableau, or service accounts**, say so—that changes the fastest fix slightly.
