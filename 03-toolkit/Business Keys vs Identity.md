**Business keys vs identity**  
Your SQL instinct is right, but split the two roles:

- Inside the tool, link on **business keys**: `entity_bk → parent_bk`. The warehouse assigns surrogate identity keys when you import.
- New parents don't have a warehouse key yet. Give each one a temporary `parent_bk` from `crypto.randomUUID()` and store the name, city, and state with it. During import, `MERGE` on the normalized name, then map the temporary key to the real one.

**Undo and traceability: use an event log, not a links table**  
Never update or delete a row; only append. The current state is the latest event for each entity. Undo appends a matching `unlink` event (or re-links to the previous parent). This is the same idea as a temporal table or SCD2.

```
links_log_<user>.csv

event_id, batch_id, action, entity_bk, parent_bk, prev_parent_bk, user_email, ts_utc

- `batch_id` groups a multi-select drag, so one undo reverses the whole drag.
- `prev_parent_bk` lets undo restore the previous parent, not just remove the new one.
- **One log file per user** avoids OneDrive write conflicts. You merge the files when you import.

Example current-state query in DuckDB:

SELECT * FROM read_csv('links_log_*.csv')

QUALIFY row_number() OVER (PARTITION BY entity_bk ORDER BY ts_utc DESC) = 1

  AND action = 'link';

The result is one row per currently linked entity, which is ready to stage and `MERGE` into the warehouse.
```



**New parent uniqueness**
Before you accept a new parent name, check it against `parents.csv` plus all new parents in the logs. Compare a normalized form: trimmed, lowercase, with spaces collapsed. Do the same later for employee emails.