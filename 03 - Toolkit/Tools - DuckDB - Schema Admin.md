# DuckDB - Schema Administration

DuckDB schemas organize tables, views, and other catalog objects inside a database. The default schema is `main`. Use schema-qualified names (`schema_name.object_name`) to make object locations explicit.

## Create a schema

```sql
CREATE SCHEMA analytics;

-- Safe to rerun; leaves an existing schema and its objects alone
CREATE SCHEMA IF NOT EXISTS analytics;
```

`CREATE OR REPLACE SCHEMA` replaces an existing schema. Avoid it for routine setup: use `IF NOT EXISTS` when you want to preserve existing contents.

## Create objects in a schema

```sql
CREATE TABLE analytics.events (
    event_id BIGINT,
    event_name VARCHAR
);

CREATE VIEW analytics.recent_events AS
SELECT *
FROM analytics.events;
```

Query with a qualified name:

```sql
SELECT *
FROM analytics.events
LIMIT 10;
```

## List schemas

```sql
SELECT schema_name
FROM information_schema.schemata
WHERE catalog_name = current_database()
ORDER BY schema_name;
```

## List tables and views in a schema

```sql
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'analytics'
ORDER BY table_type, table_name;
```

## Rename a schema

DuckDB does not provide a direct `ALTER SCHEMA ... RENAME TO ...` statement. Do not confuse renaming a table with renaming its schema.

To change a schema name, migrate its objects deliberately:

1. Create the destination schema.
2. Recreate or copy each table, view, and other required object in it.
3. Validate row counts, definitions, and dependencies.
4. Update queries/scripts that refer to the old qualified names.
5. Drop the old schema only after verifying it is no longer needed.

Example for copying a table's rows and columns (this does **not** preserve constraints, defaults, indexes, or other table metadata):

```sql
CREATE SCHEMA IF NOT EXISTS analytics_new;

CREATE TABLE analytics_new.events AS
SELECT *
FROM analytics.events;
```

Recreate views from their definitions and check any dependencies before removing the old objects.

## Move a table to another schema

DuckDB's `ALTER TABLE` supports renaming a table, but it does not provide a general schema-rename operation. For portability, recreate/copy the object into the destination schema, validate it, then remove the source object only when safe.

```sql
-- Rename the table within its current schema; this does not rename the schema
ALTER TABLE analytics.events RENAME TO event_log;
```

## Drop a schema

```sql
-- Drops an empty schema
DROP SCHEMA analytics;

-- Suppress an error if the schema does not exist
DROP SCHEMA IF EXISTS analytics;
```

`DROP SCHEMA` without `CASCADE` fails when the schema contains objects. `DROP SCHEMA ... CASCADE` also removes dependent objects; inspect and back up anything needed before using it.

## Quick reference

| Goal | DuckDB |
|---|---|
| Create schema | `CREATE SCHEMA schema_name;` |
| Create if absent | `CREATE SCHEMA IF NOT EXISTS schema_name;` |
| Replace existing schema | `CREATE OR REPLACE SCHEMA schema_name;` |
| List schemas | Query `information_schema.schemata` |
| List schema objects | Query `information_schema.tables` |
| Qualify an object | `schema_name.table_name` |
| Rename a table | `ALTER TABLE schema_name.old_name RENAME TO new_name;` |
| Rename a schema | No direct `ALTER SCHEMA ... RENAME TO`; migrate objects |
| Drop an empty schema | `DROP SCHEMA schema_name;` |
| Drop if present | `DROP SCHEMA IF EXISTS schema_name;` |

## References

- [CREATE SCHEMA](https://duckdb.org/docs/current/sql/statements/create_schema)
- [ALTER TABLE](https://duckdb.org/docs/current/sql/statements/alter_table)
- [DROP](https://duckdb.org/docs/current/sql/statements/drop)