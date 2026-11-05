snake_case means a physical object: a table, column or Python name (add_on). Your naming standard already uses it there.
kebab-case means a concept or label: tags, folders, tool slugs (#add-on).
Title Case is for display: note titles and headings (Add-on).

|Surface|Form|
|---|---|
|Tag|`#add-on`|
|SQL|`add_on`|
|Note title / heading|`Add-on`|
|Prose|add-on|
|Avoid|`addon`, `add on`, `AddOn`|


Python               snake_case
column_inventory.py

SQL                   snake_case
build_contract_map.sql

Markdown/docs          kebab-case
column-inventory.md

folders/projects       kebab-case
metadata-tools/

Python classes         PascalCase
ColumnInventory




**Status:** Working standard

Use this standard for database tables and columns. It is the canonical baseline until a more specific platform or source contract overrides it.

`_extract, _records.sql
  `_counts.sql
`_output`
`_dataset
`_query

# Avoid
```
_bus.sql
_package.sql
_scratch.sql
_payload.sql
_helper.sql
_util.sql
```

## TLDR

```text
object standard (both table and column)
-- all lower_snake_case
-- keywords are separated with "_" like (id, code, guid, type, group)
-- anything titlecased originally --> separated with "_" as separate words
-- all columns should be nullable at start at a later stage we will sharpen/tighten to define
-- use a string-rename standard () -- eg, standard abbreviations
-- if not part of standard abbreviation index, de-abbreviate (call out but make a guess)
-- anything starting with a number apppend to back (eg 123MyColumn --> my_column_123)

table standard
column standard
  id -- evaluated if every row is unique
	-- if key is identified and it is int --> _id
	-- if key is identified and it is alphanumeric like MCD09834 --> _code
	-- if key is 00034 --> _code
	-- if key is GUID -- _guid

  composite key -- if evaluated that a combination will yield every row unique recommend top 3 candidates so we can create a composite key
  	1. normalize strings for all upper
  	2. separate columns with "|"
  	3. source_name|guid|id

  datetime
  	-- if can infer utc --> _utc (eg NTZ format)
  	-- if local --> time zone is dependent on location-key
  	-- if est --> est (same for cst or other time zones, let's keep it US based for now)
  	-- if cannot determine, warn for manual definition / evaluation

  datatype conformity
    -- just use int (not tinyint, smallint)
    -- small string: varchar(50)
    -- medium string (including email): varchar 2500
    -- large strig: varchar 8000
    -- money amounts --> decimal(19,4)

enrichment standard -- always added
  general taxonomy-map-dimension -- "current" related to scd2
    sort_order (decimal 5,2) 
    comment 

  scd2 -- seeded with initial taxonomy and enriched with insert only rows
    load_datetime_utc (not null)
    process_id
    end_datetime_utc
    end_comment


standard abbreviations
  appointment --> appt
  production --> pdx
  date --> should be converted and may require prompt
  	date_value
  	create_date
  	occurence_date

unstructured thoughts
-- want to use "_" and "__" (eg `sqlmesh_test.orthofi.orthofi__bronze_orthofi__contracts__1063213385`)
-- we shouldl always have a process_table (for process_id that houses the procs including any manual entry and atomic procs + )
-- prompt warning if more than 5-7 columns (too wide, rethink)
-- ingestion types are -- full-trunc-reload  or incremental-from-watermark
	-- all columns are brought in
```



## 1. Core Naming

- Use lowercase `snake_case` for every table and column.
- Separate every semantic word: `PatientStatusHistory` -> `patient_status_history`.
- Separate numeric-leading names by moving the number to the end: `123MyColumn` -> `my_column_123`.
- Remove brackets, spaces, hyphens, punctuation, and source-system casing.
- Preserve a source token only when it is meaningful for lineage or disambiguation.
- Use `_` for semantic words and `__` only for explicit object/layer boundary notation, for example:
  `orthofi__bronze_orthofi__contracts__1063213385`.

### Rename order

1. Move leading numbers to the end.
2. Expand title case, acronym boundaries, and compressed words.
3. Apply approved abbreviations from [[Data + Tech Abbreviations]].
4. De-abbreviate anything not in the approved index; make a best-effort guess and flag it for review.
5. Lowercase and join words with `_`.
6. Check for collisions with existing names and reserved SQL keywords.

Examples:

| Source name | Standard name |
|---|---|
| `SourceSystemId` | `source_system_id` |
| `patGUID` | `pat_guid` |
| `empGUIDTreatmentCoordinator` | `emp_guid_treatment_coordinator` |
| `123MyColumn` | `my_column_123` |
| `Appointment` | `appointment` |
| `ProductionAmount` | `production_amount` |

## 2. Table Standard

- Name tables after the singular business object or relationship they represent.
- Use an explicit relationship name for bridge/history objects, such as `patient_x_location_history`.
- Do not use vague suffixes such as `_bus`, `_package`, `_scratch`, `_payload`, `_helper`, or `_util` for governed objects.
- Prompt for review when a table has more than 5-7 columns. It may be too wide and should be reconsidered as multiple objects or a deliberate wide object.
- Keep layer/source boundaries explicit when the platform naming pattern requires them, using `__` consistently.

## 3. Column Standard

- All columns start nullable while the model is being discovered and stabilized.
- Tighten nullability later as part of the model contract. Exception: `scd2.load_datetime_utc` is `not null` from creation.
- Prefer semantic names over copied source names.
- Use `id` only after evaluating whether the value is unique for every row.
- Key suffix rules:
  - integer key -> `_id`
  - alphanumeric business key such as `MCD09834` -> `_code`
  - zero-padded code such as `00034` -> `_code`
  - GUID/UUID -> `_guid`
- Do not infer a key suffix from appearance alone. Confirm uniqueness, domain meaning, and stability.

### Composite keys

When no single column is unique, evaluate combinations and recommend the top three candidates. For each candidate:

1. Convert string components to uppercase.
2. Normalize null handling explicitly.
3. Join components with `|`.
4. Document the candidate columns and uniqueness test.

Example candidate:
MD5 hash

```text
|source_name|guid|id|
|CENTRALC9\|B81280B9-E92F-47B9-A97C-4DDB76B7A186\|132|
```

Do not create a composite key until the uniqueness test passes. A persisted hash key may be added later, but it does not replace documenting the natural components.

## 4. Date and Time Columns

- Use `date` for date-only values and a datetime type for instants.
- If the value is known to be UTC, use the suffix `_utc`; platform audit timestamps use an NTZ-compatible datetime representation.
- If the value is local, use `_local` only when the location/time-zone key is also defined.
- If a fixed US zone is intentionally applied, use `_est`, `_cst`, or the appropriate zone suffix. Do not use `est` as a generic synonym for local time.
- If the timezone cannot be determined, warn and require manual definition before treating the field as canonical.
- Prefer `date_value`, `create_date`, or `occurrence_date` when the semantic meaning is date-only. Correct the source typo `occurence` when renaming.

## 5. Datatype Baseline

Use the platform-supported, intentionally broad baseline:

| Meaning | Standard type |
|---|---|
| Integer | `int` |
| Small string / code | `varchar(50)` |
| Medium string, including email | `varchar(2500)` |
| Large string | `varchar(8000)` |
| Money / currency amount | `decimal(19,4)` |
| Taxonomy sort order | `decimal(5,2)` |

Do not use `tinyint` or `smallint` for new modeled objects. Preserve source fidelity in Bronze when required, then conform in Silver.

## 6. Required Enrichment

### Taxonomy and mapping dimensions

Add these standard columns where the object is a taxonomy, mapping, or manually maintained dimension:

```text
sort_order decimal(5,2)
comment varchar(2500)
```

### SCD2 objects

Seed with the initial taxonomy or source state, then enrich using insert-only history rows. Use:

```text
load_datetime_utc datetime not null
process_id int
end_datetime_utc datetime
end_comment varchar(250)
```

`process_id` must reference a process table. The process table houses orchestrated procedures, manual entries, and atomic procedures. Do not create multiple competing process identifiers such as `load_process_id` and `loaded_by_process_id` without an explicit distinction.

## 7. Ingestion Vocabulary

Use exactly one declared ingestion type per source object:

- `full_trunc_reload`
- `incremental_watermark`

All source columns are brought in during ingestion. Transformations, renames, type conformity, and enrichment occur in the appropriate downstream layer.

## 8. Approved Abbreviations

Use the approved index in [[Data + Tech Abbreviations]]. Current naming mappings:

| Concept | Standard token | Review note |
|---|---|---|
| appointment | `appt` | Existing project abbreviation; use consistently. |
| production | `pdx` | Existing project abbreviation; confirm this is still preferred over `production`. |
| date | Do not abbreviate | Use `date_value`, `create_date`, or the semantic date name. |
| GUID | `guid` | Treat as a suffix token: `patient_guid`. |
| source system | `src_sys` | Current project convention; decide later whether clarity requires `source_system_name`. |

Anything not in the abbreviation index should be de-abbreviated and flagged. Guesses must be recorded in the refinement queue or abbreviation index.

## 9. Collision Review and Refinement Queue

These existing notes need review because they overlap or conflict with this standard:

- [Standards - Database Object Naming] are linked by multiple notes but are not present as current files in `03 - Toolkit`. Create, redirect, or retire those links so there is one canonical target.
- [[Standards - Script Artifact Naming]] govern scripts and files, not database objects. Keep them separate, but cross-link this note where naming rules overlap.
- [[Data Medallion Layer - Bronze, Silver, Gold]] says objects are singular and uses `create_datetime_local`, `modify_datetime_local`, and `load_datetime_utc`. Confirm whether source watermarks retain `_local` or are converted to UTC during Silver.
- [[Data + Tech Abbreviations]] prefers `source_system_name` for clarity, while existing SQL uses `src_sys`. Choose one canonical name; this working standard keeps `src_sys` for compatibility.
- [[SQL - Data Types]] and [[SQL - Standard Architecture]] use `nvarchar` and older widths, while [[SQL - Fabric - Create Table vs SSMS]] uses `varchar(50)`, `varchar(2500)`, `varchar(8000)`, and `decimal(19,4)`. This note follows the newer Fabric-compatible baseline; confirm the target engine before applying it.
- Existing notes use both `decimal(4,2)` and `decimal(5,2)` for `sort_order`. This standard selects `decimal(5,2)`.
- Existing notes use both `loaded_by_process_id` and `process_id`. Define whether one is the process-run foreign key and whether the other is retired.
- Existing date guidance defaults portfolio dates to EST, while this standard requires UTC or an explicit location/time-zone key. Decide whether EST is a presentation/calendar convention only.
- Existing examples contain `occurrence` and the misspelling `occurence`. Canonicalize the meaning as `occurrence`.
- The requested phrase "string-rename standard ()" is incomplete. Confirm whether it means a reusable rename function, a documented mapping table, or both.
- The requested `id`, `_id`, `_code`, and `_guid` rules need a formal uniqueness test and a decision for opaque strings that are neither GUIDs nor business codes.
- "All columns nullable at start" conflicts with the required non-null `load_datetime_utc`. The SCD2 audit exception is explicit here; confirm whether any other audit columns are mandatory.

### Related standards to review

- [[Data Ingestion Vehicle Methods]] and [[Data Source Onboarding + SLA]]: ingestion type names, watermarks, CDC, and source contracts.
- [[SQL - Standard Architecture]] and [[SQL - Fabric - Create Table vs SSMS]]: layer structure, audit columns, engine-compatible types, and process metadata.
- [[SQL - Data Types]], [[SQL - Time Zones]], and [[Standards - Date]]: type widths, timestamp semantics, and calendar conventions.
- [[Standard - Attribute Logic - Null Handling]] and [[Standard - Attribute Logic - Grains]]: when discovery-stage nullability can become a contract and how grain controls key decisions.
- [[Data + Tech Abbreviations]]: canonical abbreviation index and pending `src_sys` versus `source_system_name` decision.
- [[Archive/2026-06-09]] and [[Archive/20260702 - SCD2]]: historical naming and SCD2 examples that may still be copied into new work.

## 10. Pre-merge Checks

Before accepting a new object:

- Name is lowercase `snake_case` and has no unapproved abbreviation.
- Leading numeric tokens were moved to the end.
- Table grain and singular/relationship meaning are documented.
- Key uniqueness was tested, or the top three composite-key candidates are recorded.
- Datetime timezone is known or explicitly marked unresolved.
- Datatypes follow the baseline or document the engine-specific exception.
- Required taxonomy/SCD2 enrichment is present.
- A table wider than 5-7 columns has a documented reason to remain wide.
