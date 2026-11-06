# Tools - DuckDB - Transform String

Cheat sheet for DuckDB string functions, with the T-SQL (SSMS) equivalent where one exists. Related: [[Tools - DuckDB - Macro]].

**Rules to remember**

- Positions start at **1**, not 0.
- Strings use single quotes: `'abc'`. Double quotes are for identifiers (`"My Column"`).
- `||` joins strings. `+` does not.
- When any input is `NULL`, most functions return `NULL`. Use `coalesce(x, '')` to guard against it.

## Cut a piece out

| Task | DuckDB | Result | T-SQL |
|---|---|---|---|
| First n chars | `left('analytics_test', 9)` | `analytics` | `LEFT` |
| Last n chars | `right('location_sk', 2)` | `sk` | `RIGHT` |
| From position, length | `substring('location_sk', 1, 8)` | `location` | `SUBSTRING` |
| From position to end | `substring('location_sk', 10)` | `sk` | `SUBSTRING(s, 10, LEN(s))` |
| Slice syntax | `'location_sk'[1:8]` | `location` | none |
| Last n via negative | `'location_sk'[-2:]` | `sk` | none |
| Nth part by delimiter | `split_part('a.b.c.d', '.', 3)` | `c` | none (use `PARSENAME` for at most 4 parts, read right to left) |
| Last part by delimiter | `split_part('a.b.c.d', '.', -1)` | `d` | none |
| Regex capture | `regexp_extract('gold_agg_x_90', '_(\d+)$', 1)` | `90` | none |

## Find

| Task | DuckDB | Result | T-SQL |
|---|---|---|---|
| Position of substring | `strpos('location_sk', '_')` / `instr(...)` | `9` | `CHARINDEX('_', s)` |
| Contains | `contains('location_sk', 'tion')` | `true` | `CHARINDEX(...) > 0` |
| Starts / ends with | `starts_with(s, 'gold')`, `ends_with(s, '_sk')` | `true` | `LIKE 'gold%'` |
| Pattern | `s LIKE 'gold%'` | | same |
| Case-insensitive pattern | `s ILIKE 'GOLD%'` | | collation-dependent |
| Literal `_` in LIKE | `s LIKE '%\_sk' ESCAPE '\'` | | `LIKE '%[_]sk'` |
| Regex match | `regexp_matches(s, '^gold_(agg\|dim\|fct)_')` | `true` | none |
| Length (characters) | `length('abc')` | `3` | `LEN` (LEN trims trailing spaces; `length` does not) |

## Change

| Task | DuckDB | Result | T-SQL |
|---|---|---|---|
| Replace text | `replace('gold__test', '__test', '')` | `gold` | `REPLACE` |
| Replace by regex (all) | `regexp_replace('a1b22', '\d+', '#', 'g')` | `a#b#` | none |
| Character-by-character swap | `translate('a-b_c', '-_', '  ')` | `a b c` | `TRANSLATE` |
| Upper / lower | `upper(s)`, `lower(s)` | | same |
| Trim spaces | `trim(s)`, `ltrim(s)`, `rtrim(s)` | | same |
| Trim other characters | `trim('__x__', '_')` | `x` | `TRIM('_' FROM s)` |
| Pad left / right | `lpad('7', 3, '0')`, `rpad('ab', 4, '.')` | `007`, `ab..` | `RIGHT('000'+s, 3)` |
| Repeat | `repeat('-', 5)` | `-----` | `REPLICATE` |
| Reverse | `reverse('abc')` | `cba` | `REVERSE` |

## Join

| Task | DuckDB | Result | T-SQL |
|---|---|---|---|
| Join two strings | `'gold' \|\| '.' \|\| 'dim'` | `gold.dim` | `+` |
| Join, NULL-safe | `concat('a', NULL, 'b')` | `ab` | `CONCAT` |
| Join with separator | `concat_ws('.', 'gold', 'dim', 'x')` | `gold.dim.x` | `CONCAT_WS` |
| Template | `format('{}.{}', schema, tbl)` | `gold.dim` | `FORMATMESSAGE` |
| printf style | `printf('%05d', 42)` | `00042` | `FORMAT(42, '00000')` |
| Rows to one string | `string_agg(col, ',' ORDER BY col)` | `a,b,c` | `STRING_AGG ... WITHIN GROUP` |

## Split into rows or lists

```sql
SELECT string_split('a,b,c', ',');                   -- ['a', 'b', 'c']   (a list)
SELECT unnest(string_split('a,b,c', ',')) AS tag;    -- 3 rows: a / b / c
SELECT string_split_regex('a, b;c', '[,;]\s*');      -- ['a', 'b', 'c']
SELECT array_to_string(['a','b'], ',');              -- 'a,b'   (list back to text)
SELECT len(string_split('a,b,c', ','));              -- 3       (count items)
```

T-SQL equivalent: `STRING_SPLIT(s, ',')` used with `CROSS APPLY`.

## Convert

| Task | DuckDB | T-SQL |
|---|---|---|
| Cast, fails on bad data | `'42'::INTEGER` or `CAST('42' AS INTEGER)` | `CAST` |
| Cast, NULL on bad data | `TRY_CAST('x' AS INTEGER)` | `TRY_CAST` |
| Text to date | `strptime('2026-10-13', '%Y-%m-%d')` | `CONVERT(date, s)` |
| Date to text | `strftime(DATE '2026-10-13', '%Y%b')` -> `2026Oct` | `FORMAT(d, 'yyyyMMM')` |
| Month label (your prime `2026OCT`) | `upper(strftime(d, '%Y%b'))` | `UPPER(FORMAT(d, 'yyyyMMM'))` |
| Empty string to NULL | `nullif(trim(s), '')` | same |
| NULL to default | `coalesce(s, 'unknown')` | `ISNULL` / `COALESCE` |

## Compare (fuzzy)

```sql
SELECT levenshtein('isnewpatientexam', 'is_new_patient_exam');          -- 3 edits
SELECT jaro_winkler_similarity('cloud9conversiondate', 'cloud9_conversion_date');  -- about 0.96 (1 = identical)
```

Useful for rename checks, like the `near:` hints in [[2026-10-12 - Project - UAT Column State Change]].

## Patterns from this project

```sql
-- table and column out of catalog.schema.table.column
SELECT split_part(before, '.', 3) AS tbl, split_part(before, '.', -1) AS col FROM cs;

-- strip the environment suffix from the schema
SELECT regexp_replace(split_part(before, '.', 2), '__(test|stage|goldnext)$', '') AS base_schema FROM cs;

-- surrogate keys only
SELECT * FROM cs WHERE ends_with(after, '_sk');

-- count the tags in a comma-delimited column
SELECT unnest(string_split(concept_tags, ',')) AS tag, count(*) FROM cs GROUP BY ALL ORDER BY 2 DESC;
```

## Gotchas

- `[pitfall]` In `LIKE`, `_` matches any single character. To match a literal underscore, use `ends_with`, `contains`, or `ESCAPE`.
- `[pitfall]` `substring(s, 0, 3)` returns 2 characters, not 3, because position 0 comes before the first character. Start at 1.
- `[pitfall]` `regexp_replace` replaces only the **first** match unless you pass `'g'`.
- `[pitfall]` `||` with a `NULL` input returns `NULL`. `concat` skips `NULL` inputs.
- `[pitfall]` `strftime('%b')` returns `Oct`, so wrap it in `upper()` for the `2026OCT` label form.
