# 2026-10-12 - Project - UAT Column State Change

**Status:** `before` + `after` filled (179 mapped, 2 unknown); review in progress.
**Skill:** [[03 - Toolkit/Skills/sql-object-lineage/SKILL|Skill - SQL Object Lineage]] (project skill; promotion gate inside).
**Kind:** applied project (uses current tools; not a toolkit project).
**Goal:** find gaps in the semantic artifacts using the UAT SQL as the test set. Plan: list every distinct `table.column` (`before`), map it to the current sqlmesh model column (`after`), then tag it with [[SD Domain]] concepts (`concept_tags`).

## Manifest

| Role | Absolute path |
|---|---|
| Input (read-only, 259 `.sql`) | `C:\Users\jonas-adam.pascua\OneDrive - Smile Doctors, LLC\GRP _ Project Ascend _ Information Technology - Documents\05 - Governance\UAT` |
| Output | `C:\obsidian\Project Ascend\uat-script-table-column-state-change.csv` (`before, after, concept_tags`; tags are comma-delimited) |
| Evidence | `C:\obsidian\Project Ascend\uat-script-table-column-state-change.evidence.csv` (`before, file, note`) |
| Scripts (skill) | `C:\obsidian\Project Ascend\03 - Toolkit\Skills\sql-object-lineage\scripts\` (`sql_object_lineage.py`, `sqlmesh_schema.py`); venv `C:\Users\jonas-adam.pascua\AppData\Local\sql-object-lineage\.venv` |
| Schema snapshot | `C:\obsidian\Project Ascend\sqlmesh-model-columns.main.csv` (885 tables, 16,051 columns; main @ `2dd85021` v1.404.0) |
| Environment map | `C:\obsidian\Project Ascend\sqlmesh-environment.csv` (only `test` verified) |
| Rename map | `C:\obsidian\Project Ascend\uat-script-column-rename-map.csv` (4 rows, `inferred-rename`) |
| Superseded sketch | `C:\Users\jonas-adam.pascua\AppData\Local\Temp\uat-lineage\` (safe to delete) |
| Backups | `C:\Repos\sd-edw\toolkit\.dev-in-progress\<ts>_uat-script-table-column-state-change*.csv` |
| `after` source | `C:\Repos\sd-edw\project-ascend\data-platform\sqlmesh` |
| Concept source | `C:\obsidian\Project Ascend\04 - Semantic Registry\SD Domain.md` |

**Rules:** comments are ignored. CTE and subquery columns resolve to the physical model column (column-level lineage, so the base column). `null-handling: unknown` = searched and not found.

## Open loops

- [ ] Verify 4 `inferred-rename` rows against PR #1430, then set status `verified`.
- [ ] 2 unknown: `gold_dim_date.mmyyyy` (no match), `gold_fct_appointment.sourcesystemid` (`source_instance_id`? likely not the same).
- [ ] 49 distinct `?.column` ambiguous owners remain (140 files); 45 `query-alias` (labels made in the query, not model columns).
- [x] Star pass-through false positives removed (e.g. `gold_fct_appointment.patients_dismissed_within_90`). [closed:: 2026-10-12]
- [x] Fill `after` from the sqlmesh models. [closed:: 2026-10-12]
- [ ] Fill `concept_tags`. Expect mostly `unknown`, because [[SD Domain]] has 15 tags.
- [ ] Keyword intake into [[Taxonomy - Term]] (end-of-day `block` proposals).

## Log

- 2026-10-12T19:30 -- Extracted `before`: 259 files, 0 parse failures, 249 distinct physical columns, all in `analytics_test.gold__test.*`. 555 ambiguous-owner references (81 distinct columns). The example `gold_agg_total_show_rate_90.patients_dismissed_within_90` was found.
- 2026-10-12T20:15 -- Switched data-platform to `main` @ `2dd85021` (v1.404.0). Built the schema from the models on main and used it for owner resolution and the `after` fill. `before` is now 181 (the earlier 249 included star pass-through false positives). `after`: 175 mapped 1:1 (`gold.<model>.<col>`), 6 unknown. Ambiguous owners are down from 81 to 49 distinct.
- 2026-10-12T20:45 -- Snowflake check by `manual-query` showed that `after` must be the name you query, not the model key. `after` now follows `<gateway analytics_catalog>.<schema>__<env>.<model>.<col>` (sources: `sqlmesh\config.yaml` gateway `test` -> `ANALYTICS_TEST`; env `test` -> `__test` suffix). Result: 175 rows where before = after, 6 unknown.
- 2026-10-12T21:00 -- `all rec` applied. The scripts are generalized into the [[03 - Toolkit/Skills/sql-object-lineage/SKILL|sql-object-lineage]] skill, which takes a schema CSV snapshot, an env map and a rename map, so it runs without the repo. Re-run: 181 before, 179 mapped (4 by `inferred-rename`), 2 unknown, 413 flags (same as the sketch). Registered `CD` and `CI` in [[Taxonomy - Abbreviation]].
