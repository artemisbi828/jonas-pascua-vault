2026-10-14 11:39 PM 
```
what you said                              verdict
├─ "tables are easier to read"           -> real preference (stack-fit). Keep it.
├─ "DuckDB = my formalized object"       -> bias: formality comes from the approval step, not the storage engine
├─ "more work to update = a gate"        -> bias: friction is not a gate; you skip or batch it, and nothing fails loud
└─ "SCD2 vs git"                         -> false choice: they answer different questions
   ├─ git   -- "what changed in this publish, and undo it"   (file level, rollback)
   └─ SCD2  -- "what did DA mean on 2026-10-01"              (row level, queryable)
```