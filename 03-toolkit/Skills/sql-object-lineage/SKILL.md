---
name: sql-object-lineage
description: Reduce a directory of SQL files to distinct physical catalog.schema.table.column references (before), resolving CTEs, subqueries and SELECT *, then map them to a target environment (after) with a schema snapshot, an environment map and a rename map. WHEN "reduce these sql files", "distinct table.column", "what objects do these queries use", "map old references to current models", "sql object inventory", "uat script references".
status: project-skill
origin: "[[2026-10-12 - Project - UAT Column State Change]]"
promote_to: C:\Repos\toolkit\ai-preferences\skills\sql-object-lineage
---

# Skill - SQL Object Lineage

Point it at a folder of `.sql` files. It returns one row for each distinct physical column the queries read, plus the matching current name in the target environment. It only reads the SQL; the files never change.

```text
sql dir (read-only)
├─ parse          -- snowflake, then tsql, then generic; comments dropped
├─ qualify        -- schema-aware; on failure, retry schema-less (renamed columns break it)
├─ reduce         -- CTE/subquery column -> physical column it reads (base column)
│  ├─ explicit projection  -> inputs already captured inside the CTE scope
│  ├─ SELECT * (1 source)  -> follow to that source
│  └─ SELECT * (2+ sources)-> follow only to the one source that owns the column (snapshot)
├─ owner pick     -- unqualified column in a join -> the one source that owns it, else flag
└─ map after      -- snapshot hit -> render target name; rename map; else `null-handling: unknown`
                          |
                          v
        <out>.csv (before, after, concept_tags) + <out>.evidence.csv (before, file, note)
```

## Inputs

| Input | Required | Shape | Speeds up |
|---|---|---|---|
| `--sql-dir` | yes | folder, recursive `*.sql` | |
| `--schema-csv` | for `after` | `schema,table,column` (base schema, no env suffix) | owner pick, star follow, `after` |
| `--env-map` | for runnable names | `gateway,sqlmesh_env,analytics_catalog,schema_suffix` | strips `__<env>` from `before`, renders `after` |
| `--target` | with `--env-map` | one `sqlmesh_env` value | |
| `--rename-map` | optional | `schema,table,old_column,new_column,status` | closes `column-missing` rows |

Schema snapshot sources, best first:
1. `sqlmesh_schema.py --models-dir <repo>\sqlmesh\models` (needs the repo on fresh `main`; record the sha).
2. A Snowflake `information_schema.columns` export, renamed to `schema,table,column`.
3. An earlier snapshot CSV, which works offline but goes stale.

## Run

```powershell
$py = "$env:LOCALAPPDATA\sql-object-lineage\.venv\Scripts\python.exe"   # python -m venv; pip install sqlglot
$s  = "C:\obsidian\Project Ascend\03 - Toolkit\Skills\sql-object-lineage\scripts"
& $py "$s\sqlmesh_schema.py" --models-dir C:\Repos\sd-edw\project-ascend\data-platform\sqlmesh\models --out .\model-columns.csv
& $py "$s\sql_object_lineage.py" --sql-dir <dir> --out .\objects.csv --schema-csv .\model-columns.csv `
      --env-map .\sqlmesh-environment.csv --target test --rename-map .\rename-map.csv
```

Expected output: one line such as `files=259 distinct_before=181 mapped=179 unknown=2 flags=413`.

## Object naming rule (sqlmesh)

`queryable = <gateway analytics_catalog>.<model schema><__env unless prod>.<model>`

The physical tables `GOLD.GOLD__<MODEL>__<fingerprint>` are versioned snapshots; never map to them. The env name comes from the `plan <env>` command, not from config, so keep `sqlmesh-environment.csv` up to date by hand.

## Evidence flags

| note | meaning | action |
|---|---|---|
| `ambiguous-owner` | unqualified column, 0 or 2+ sources own it | qualify in the SQL, or extend the snapshot |
| `query-alias` | name made in the query (`column_label`, `sort_order`) | not a model column; ignore |
| `qualify-failed` | the column is not in the snapshot (often a rename) | check the rename map |
| `column-missing-in-snapshot; near:` | the table exists but the column does not | add a rename-map row after checking the PR |
| `rename: inferred-rename` | mapped by rename map, not verified | verify, then set status `verified` |
| `table-missing-in-snapshot` | table dropped or renamed | `[gap]` |

## CD / CI loop

- **CD (continuous development):** each project run that finds a new pattern adds a rule above, and the script change ships in the same session.
- **CI (continuous improvement):** after each run, move repeated `ambiguous-owner` causes into a rule, a snapshot source or a rename map row. Track the count per run in the project log; it should go down.

## Pitfalls

- `[pitfall]` Without a snapshot, `SELECT *` from a join cannot be followed, and `before` is missing columns.
- `[pitfall]` Star expansion in `qualify` adds every column of a table, used or not. Keep `expand_stars=False`.
- `[pitfall]` Similar column names are not proof of a rename. Keep `inferred-rename` until a PR or a query confirms it.

## Promote to a global skill (gate)

- [ ] Used on 2+ projects with no code change for project-specific names.
- [ ] Scripts moved to a toolkit project (AGENTS.md rule: the toolkit is the source of truth for code). This vault copy then becomes a thin reference.
- [ ] Deployed through `ai-preferences\config.json` `skills`.
