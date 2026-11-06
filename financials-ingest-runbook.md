---
author: agent
tags: [runbook]
---

# financials-ingest: runbook

Part of [[financials-ingest]]. See [[financials-ingest-how-it-works]] for the rules. No venv needed (standard library only).

1. Dry run: writes the staged file and checks duplicates, appends nothing.
2. Apply: copies the source to `raw\`, appends, verifies, flips `is_complete`, logs.

```powershell
cd "C:\Repos\jonas-pascua-vault\financials\ingest\scripts"
python .\ingest_360checking.py "C:\Users\jpasc\Downloads\2026-11-03_360Checking...6689.csv"
python .\ingest_360checking.py "C:\Users\jpasc\Downloads\2026-11-03_360Checking...6689.csv" --apply
```

Expected dry run: `108 new rows ready`. Expected apply: `appended and verified 108 rows ... is_complete=TRUE`.

Staged files still `FALSE` = not confirmed in the target; review them.
