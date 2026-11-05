# Standard - Data Object Naming - Quick Reference

**Purpose:** Human runbook/workbook. Use this when naming a table or column quickly.

## TLDR

```text
lower_snake_case | singular table | _ = word | __ = layer/object boundary
number_first -> number_last | approved abbreviation only | unknown abbreviation -> expand + flag
int key -> _id | business/padded key -> _code | GUID/UUID -> _guid
UTC -> _utc | known local + location key -> _local | unknown timezone -> warn
int | varchar(50) | varchar(2500) | varchar(8000) | decimal(19,4)
start nullable | SCD2 load_datetime_utc NOT NULL | process_id | >5-7 columns -> review
```

## Do This

| Check         | Action                                | Example                                            |
| ------------- | ------------------------------------- | -------------------------------------------------- |
| Case          | lowercase snake case                  | `PatientStatusHistory` -> `patient_status_history` |
| Words         | split title case and compressed words | `SourceSystemId` -> `source_system_id`             |
| Number        | move leading number to end            | `123MyColumn` -> `my_column_123`                   |
| Abbreviation  | use index; otherwise expand and flag  | `appt` allowed; unknown token -> review            |
| GUID          | suffix `_guid`                        | `patGUID` -> `pat_guid`                            |
| Integer key   | suffix `_id` after uniqueness test    | `patient_id`                                       |
| Business code | suffix `_code`                        | `MCD09834` -> `member_code`                        |
| Padded code   | suffix `_code`                        | `00034` -> `location_code`                         |
| Datetime      | suffix timezone                       | `created_at_utc`, `created_at_local`               |
| Date only     | use semantic date                     | `create_date`, `date_value`, `occurrence_date`     |
| Money         | `decimal(19,4)`                       | `net_production_amount`                            |
| Sort          | `decimal(5,2)`                        | `sort_order`                                       |

## Key Decision

```text
unique single column?       yes -> evaluate id/code/guid suffix
                            no  -> recommend top 3 composite keys
```

Composite candidate notation:

```text
UPPER(value_1)|UPPER(value_2)|UPPER(value_3)
source_name|guid|id
```

Do not create the key until uniqueness passes. Document null handling.

## Required Enrichment

Taxonomy or mapping dimension:

```text
sort_order decimal(5,2)
comment varchar(2500)
```

SCD2:

```text
load_datetime_utc datetime NOT NULL
process_id int
end_datetime_utc datetime
end_comment varchar(250)
```

## Ingestion

```text
full_trunc_reload
incremental_watermark
```

Bring in all source columns. Rename, conform, and enrich downstream.

## Fast Workbook

```text
[ ] table is singular business object or explicit relationship
[ ] name is lowercase snake_case
[ ] leading number moved to end
[ ] abbreviation is approved, or expanded + flagged
[ ] key uniqueness evaluated
[ ] key suffix chosen: _id / _code / _guid
[ ] timezone known: _utc / _local / explicit zone / warning
[ ] datatype conforms
[ ] nullable by default; SCD2 load timestamp is NOT NULL
[ ] composite candidates documented if needed
[ ] >5-7 columns reviewed
```

Full standard: [[Standard - Naming - Artifacts]]
Reusable prompt: [[Standard - Process - Compact Markdown Runbook]]
