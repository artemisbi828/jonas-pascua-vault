"""Ingest *360Checking*.csv into financials\\transactions.csv. Rules: financials-ingest-how-it-works.md

Usage: python ingest_360checking.py <source.csv> [--apply]
Default is a dry run: writes the staged file, checks duplicates, appends nothing.
Exit codes: 0 ok, 2 hard-block (duplicate or unmapped account), 3 post-append verify failed, 1 other error.
"""
import csv
import getpass
import hashlib
import os
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

FINANCIALS = Path(__file__).resolve().parents[2]
INGEST = FINANCIALS / "ingest"
RAW, STAGED, LOG = INGEST / "raw", INGEST / "staged", INGEST / "ingest_log.csv"
TARGET = FINANCIALS / "transactions.csv"
ACCOUNT_MAP = {"6689": 8}  # source Account Number -> accounts.csv account_id
TARGET_COLS = ["trans_id", "account_id", "date_value", "description", "amount", "asset_notes",
               "category_id", "vendor_id", "event_id", "command_log_id", "load_datetime_utc", "load_source"]
STAGED_COLS = ["account_id", "date_value", "description", "amount", "row_hash", "is_complete"]
LOG_COLS = ["run_utc", "source_file", "staged_file", "rows", "appended", "status"]


def fail(code, msg, log=None):
    print(msg, file=sys.stderr)
    if log:
        write_log(*log, status=msg.split(";")[0][:120])
    sys.exit(code)


def row_keys(rows):
    """sha256 of account|date|amount|description|occurrence; occurrence separates same-day repeats."""
    seen, out = Counter(), []
    for acct, date_value, amount, desc in rows:
        k = f"{acct}|{date_value}|{Decimal(amount):.2f}|{desc.strip()}"
        seen[k] += 1
        out.append(hashlib.sha256(f"{k}|{seen[k]}".encode()).hexdigest())
    return out


def transform(src):
    rows = []
    with open(src, newline="", encoding="utf-8-sig") as f:
        for n, r in enumerate(csv.DictReader(f), start=2):
            acct = ACCOUNT_MAP.get(r["Account Number"].strip())
            if acct is None:
                fail(2, f"BLOCK unmapped account {r['Account Number']!r} at source line {n}")
            kind = r["Transaction Type"].strip()
            if kind not in ("Debit", "Credit"):
                fail(2, f"BLOCK unknown Transaction Type {kind!r} at source line {n}")
            amount = Decimal(r["Transaction Amount"].strip())
            if kind == "Debit":
                amount *= Decimal("-1.00")
            date_value = datetime.strptime(r["Transaction Date"].strip(), "%m/%d/%y").strftime("%Y-%m-%d")
            rows.append((acct, date_value, f"{amount:.2f}", r["Transaction Description"].strip()))
    return rows


def read_target():
    with open(TARGET, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = [h.strip() for h in next(reader)]
        if header != TARGET_COLS:
            fail(1, f"target header mismatch: {header}")
        idx = {c: i for i, c in enumerate(header)}
        data = [r for r in reader if r]
    max_id = max(int(r[idx["trans_id"]]) for r in data)
    hashes = row_keys([(r[idx["account_id"]], r[idx["date_value"]], r[idx["amount"]], r[idx["description"]])
                       for r in data])
    return set(hashes), max_id


def write_staged(path, rows, hashes, complete):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(STAGED_COLS)
        for (acct, date_value, amount, desc), h in zip(rows, hashes):
            w.writerow([acct, date_value, desc, amount, h, "TRUE" if complete else "FALSE"])


def write_log(src, staged, rows, appended, status):
    new = not LOG.exists()
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        if new:
            w.writerow(LOG_COLS)
        w.writerow([datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), src.name, staged.name,
                    rows, appended, status])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    if len(args) != 1 or "360checking" not in Path(args[0]).name.lower():
        fail(1, "usage: ingest_360checking.py <*360Checking*.csv> [--apply]")
    src = Path(args[0])
    staged = STAGED / f"{src.stem}.transformed.csv"

    rows = transform(src)
    hashes = row_keys(rows)
    STAGED.mkdir(parents=True, exist_ok=True)

    existing, max_id = read_target()
    dups = [r for r, h in zip(rows, hashes) if h in existing]
    if dups:
        for r in dups:
            print(f"DUPLICATE {r[1]} {r[2]} {r[3]}", file=sys.stderr)
        fail(2, f"BLOCK; {len(dups)} of {len(rows)} rows already in target; nothing appended. Staged file left untouched: {staged}",
             log=(src, staged, len(rows), 0) if apply else None)

    write_staged(staged, rows, hashes, complete=False)
    print(f"{len(rows)} new rows ready (staged: {staged})")
    if not apply:
        print("dry run: add --apply to append")
        return

    RAW.mkdir(parents=True, exist_ok=True)
    raw_copy = RAW / src.name
    if raw_copy.exists():
        raw_copy = RAW / f"{src.stem}.{datetime.now().strftime('%Y%m%dT%H%M%S')}{src.suffix}"
    shutil.copy2(src, raw_copy)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    who = f"{os.environ.get('USERDOMAIN', '')}\\{getpass.getuser()}"
    with open(TARGET, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        for i, (acct, date_value, amount, desc) in enumerate(rows, start=1):
            w.writerow([max_id + i, acct, date_value, desc, amount, "NULL", "NULL", "NULL", "NULL", "NULL", now, who])

    after, _ = read_target()
    missing = [h for h in hashes if h not in after]
    if missing:
        fail(3, f"VERIFY FAILED; {len(missing)} of {len(rows)} staged rows not found in target; is_complete left FALSE",
             log=(src, staged, len(rows), len(rows) - len(missing)))
    write_staged(staged, rows, hashes, complete=True)
    write_log(src, staged, len(rows), len(rows), "OK")
    print(f"appended and verified {len(rows)} rows (trans_id {max_id + 1}..{max_id + len(rows)}); staged is_complete=TRUE; raw: {raw_copy.name}")


if __name__ == "__main__":
    main()
