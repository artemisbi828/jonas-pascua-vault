---
author: agent
tags: [how-it-works]
---

# financials-ingest: how it works

Part of [[financials-ingest]]. Source `[*360Checking*].csv`, target `financials\transactions.csv`.

```text
raw (copy of source)   staged\<name>.transformed.csv        financials\transactions.csv
       ^                     |  row_hash, is_complete=FALSE          ^
       |                     v                                       |
   source.csv --transform--> dedupe on row_hash --none found--> append
                                 | any found                         |
                                 v                                   v
                        BLOCK exit 2 (nothing appended)     re-read target: all row_hash present?
                                                              yes -> is_complete=TRUE + log OK
                                                              no  -> stay FALSE, exit 3
```

## Account tag

| source_account_number | account_id | account_name |
|---|---|---|
| 6689 | 8 | CAP1CHK |

## Field map

| target | from_source | rule |
|---|---|---|
| account_id | `Account Number` | lookup above; unmapped = BLOCK |
| date_value | `Transaction Date` | `MM/DD/YY` to `YYYY-MM-DD` |
| amount | `Transaction Amount` | `Debit` x -1.00; `Credit` unchanged; 2 decimals |
| description | `Transaction Description` | trimmed |

Not loaded: `Balance`. Script-added: `trans_id` (max + 1), `NULL` for asset_notes, category_id, vendor_id, event_id, command_log_id (`[gap]`: not yet decided), `load_datetime_utc` (UTC), `load_source` (`DOMAIN\user`).

## Row hash and dedupe

- `row_hash = sha256(account_id|date_value|amount|description|occurrence)`. Occurrence is 1, 2, ... for identical rows, so two same-day same-amount purchases stay distinct.
- Target hashes are computed from its existing columns; no schema change.
- Any staged hash already in the target blocks the whole file (exit 2) for review.
- Example: file has 2 identical coffees (hashes n=1, n=2). First load appends both. Re-loading the file blocks both.

## Other blocks

| condition | result |
|---|---|
| `Transaction Type` not Debit or Credit | exit 2 |
| target header differs | exit 1 |
| post-append hash missing | exit 3, `is_complete` stays FALSE |

## Known risk

`[gap]` If the bank changes a description between exports (pending to posted), the row hashes differently and loads twice.

## Decisions

- [decision:: append] [spirit:: Debit is negative, Credit unchanged, following the field map over the "if credit" prose.] [requested_by:: Jonas Pascua] [applied_by:: Copilot] [why:: existing target rows show income positive, spend negative.]
- [decision:: append] [spirit:: Pipeline folder is a sibling of financials (Q1a); staged files stay in place with is_complete flipped after verify (Q2a); occurrence number in the hash (Q3a).] [requested_by:: Jonas Pascua] [approved_by:: Jonas Pascua] [applied_by:: Copilot] [why:: keep financials as tables only and make partial appends visible.]
