# Tools - DuckDB - Macro

Cheat sheet for DuckDB macros. Used in [[2026-10-12 - Project - UAT Column State Change]] to edit the comma-delimited `concept_tags` column.

## ELI5

A macro is a **saved shortcut for a piece of SQL**.

You write a long expression once, give it a name, and from then on you type the short name. When you run a query, DuckDB **pastes the long expression back in** where the name was, then runs the query as usual.

```text
you type        add_tag(concept_tags, 'x')
                        |
                        v   DuckDB swaps in the saved text
DuckDB runs     array_to_string(list_sort(list_distinct(list_append(..., 'x'))), ',')
```

- It is **text substitution**, not a program. It stores no data and has no state.
- It is **not a stored procedure**. It cannot run `UPDATE` or `INSERT` on its own. It only returns a value (scalar macro) or rows (table macro).
- It **lives as long as the database**. In an in-memory session (`duckdb` with no file), macros disappear when you `.quit`.

## Two kinds

```text
macro
├─ scalar macro  -- returns one value per row; use it in SELECT, WHERE, SET
└─ table macro   -- returns rows; use it in FROM like a table
```

| Kind | Create | Use |
|---|---|---|
| Scalar | `CREATE MACRO f(a) AS a * 2;` | `SELECT f(price) FROM t;` |
| Table | `CREATE MACRO t_for(x) AS TABLE SELECT * FROM t WHERE k = x;` | `SELECT * FROM t_for('abc');` |

## Most common commands

| Task | Command |
|---|---|
| Create | `CREATE MACRO name(a, b) AS <expression>;` |
| Create or overwrite | `CREATE OR REPLACE MACRO name(a) AS <expression>;` |
| Session-only, even in a file database | `CREATE TEMP MACRO name(a) AS <expression>;` |
| Default parameter | `CREATE MACRO f(a, b := 5) AS a + b;` then `f(1)` = 6, `f(1, b := 2)` = 3 |
| Table macro | `CREATE MACRO name(a) AS TABLE SELECT ...;` |
| Drop scalar | `DROP MACRO name;` |
| Drop table macro | `DROP MACRO TABLE name;` |
| List your macros | `SELECT function_name, function_type, macro_definition FROM duckdb_functions() WHERE function_type IN ('macro','table_macro') AND NOT internal;` |

## The three macros from the runbook, explained

The `concept_tags` column holds text such as `appt_surrogate_key,#metric/show_up_rate`. Lists are easier to work with than text, so each macro converts text to a list, changes the list, and converts it back to text.

```text
'a,b'  --string_split-->  ['a','b']  --list work-->  ['a','b','c']  --array_to_string-->  'a,b,c'
```

### 1. `tags_of(t)`: text to list, safe on empty values

```sql
CREATE MACRO tags_of(t) AS coalesce(string_split(nullif(t, ''), ','), []::VARCHAR[]);
```

| Piece | What it does |
|---|---|
| `nullif(t, '')` | turns an empty string into `NULL` |
| `string_split(..., ',')` | `'a,b'` -> `['a','b']` (`NULL` stays `NULL`) |
| `coalesce(..., []::VARCHAR[])` | `NULL` -> empty list `[]` |

```sql
SELECT tags_of('a,b'), tags_of(''), tags_of(NULL);
-- ['a', 'b']   []   []
```

### 2. `add_tag(t, tag)`: add one tag without duplicates

```sql
CREATE MACRO add_tag(t, tag) AS
  array_to_string(list_sort(list_distinct(list_append(tags_of(t), tag))), ',');
```

Read it inside out:

```text
tags_of(t)          'b,a'        -> ['b','a']
list_append(..,tag) + 'a'        -> ['b','a','a']
list_distinct       remove dupes -> ['b','a']      (order not guaranteed)
list_sort           stable order -> ['a','b']
array_to_string ',' back to text -> 'a,b'
```

```sql
SELECT add_tag('', 'x'), add_tag('x', 'x'), add_tag('b,a', 'c');
-- 'x'    'x'    'a,b,c'
```

### 3. `drop_tag(t, tag)`: remove one tag

```sql
CREATE MACRO drop_tag(t, tag) AS
  nullif(array_to_string(list_filter(tags_of(t), x -> x <> tag), ','), '');
```

| Piece | What it does |
|---|---|
| `list_filter(list, x -> x <> tag)` | keeps every item that is not `tag` |
| `x -> x <> tag` | a **lambda**: a tiny inline function, "for each x, keep it if x is not tag" |
| `nullif(..., '')` | if nothing is left, return `NULL` instead of `''` |

```sql
SELECT drop_tag('a,b', 'a'), drop_tag('a', 'a');
-- 'b'    NULL
```

Newer DuckDB versions also accept `lambda x: x <> tag`. Both forms mean the same thing.

## Using macros with UPDATE

The macro computes the new value; `UPDATE` is what writes it.

```sql
BEGIN;
UPDATE cs SET concept_tags = add_tag(concept_tags, 'appt_surrogate_key')
WHERE split_part(before, '.', 4) = 'appointment_sk';
SELECT before, concept_tags FROM cs WHERE concept_tags LIKE '%appt_surrogate_key%';
COMMIT;      -- or ROLLBACK; to undo
```

## More small examples

```sql
-- shorter name for a repeated expression
CREATE MACRO col_of(fqn) AS split_part(fqn, '.', 4);
SELECT col_of(before) FROM cs LIMIT 5;

-- yes/no check
CREATE MACRO has_tag(t, tag) AS list_contains(tags_of(t), tag);
SELECT count(*) FROM cs WHERE has_tag(concept_tags, 'unknown');

-- table macro: all rows for one table name
CREATE MACRO rows_for(tbl_name) AS TABLE
  SELECT * FROM cs WHERE split_part(before, '.', 3) = tbl_name;
SELECT * FROM rows_for('gold_dim_location');
```

## Keep macros between sessions

| Option | How | Tradeoff |
|---|---|---|
| Paste each session | Copy the `CREATE MACRO` lines from this note | Nothing saved, nothing to manage |
| File database | `duckdb uat.duckdb` instead of `duckdb` | Macros and tables persist in the file, but it is one more file to back up |
| Startup file | Put the `CREATE OR REPLACE MACRO` lines in `%USERPROFILE%\.duckdbrc` | Loads in every CLI session, including ones that do not need them |

## Gotchas

- `[pitfall]` A missing `;` means nothing runs. The prompt changes to `‣` and waits for more input.
- `[pitfall]` `CREATE MACRO` fails if the name already exists. Use `CREATE OR REPLACE MACRO` when you edit one.
- `[pitfall]` A macro name can hide a built-in function with the same name. Use clear names (`add_tag`, not `append`).
- `[pitfall]` Macros do not check types when you create them. A wrong argument fails only when you call the macro.
- `[pitfall]` `list_distinct` does not keep order, so sort (`list_sort`) before you compare or save.
