---
kind: log
---

# Vault Decisions

Why rules exist. Append-only, oldest first. `Canonized` = written into a standard (link it).

| Date | ID | Conflict / Question | Options | Decision | Why | Canonized |
|---|---|---|---|---|---|---|
| 2026-09-29 | 1d | SQL `addon` vs `add_on` | keep legacy / split words | `add_on`; rename `edw.addon__cc9` -> `edw.add_on__cc9` | Consistency with "split every word" | [[Standard - Naming - Artifacts]] (pending) |
| 2026-09-29 | 2b | Abbreviations in 2 notes | keep both / merge | Merge into [[Data + Tech Abbreviations]]; original to `.trash` | One source | n/a |
| 2026-09-29 | 2c | Auto-replace aliases? | always / never / per alias | Per alias: `auto` or `flag` | `ctr` is ambiguous; others are safe | pending |
| 2026-09-29 | 2e | `addback` vs `add-back` | no hyphen / hyphen | `add-back` | Matches `add-on` | [[terminology-prime-names]] |
| 2026-09-29 | 5a | Backup method | local copy / git | Local git, no remote, plus folder snapshot | Per-note diffs and undo; PHI stays local | [[Standard - Process - Vault Operating Workflow]] |
