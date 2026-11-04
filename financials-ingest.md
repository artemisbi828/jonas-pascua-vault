---
author: agent
tags: [initiative]
---

# financials-ingest

Pipeline that loads bank extracts into the core tables in [financials](financials/). Core tables stay CSV-only; everything else lives here.

```text
financials\ingest\
├─ raw\            -- extracts as downloaded (dupes allowed)
├─ staged\         -- script output with row_hash, is_complete
├─ scripts\        -- ingest_360checking.py
└─ ingest_log.csv  -- one row per applied run
```

- [[financials-ingest-how-it-works]]
- [[financials-ingest-runbook]]
