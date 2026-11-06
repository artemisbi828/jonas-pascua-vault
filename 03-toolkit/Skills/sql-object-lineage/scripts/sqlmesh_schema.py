"""Snapshot sqlmesh SQL models to a schema CSV (schema, table, column, model_file) so later runs need no repo."""
import argparse
import csv
import re
import sys
from pathlib import Path

import sqlglot
from sqlglot import exp


def split_model_block(text: str):
    """Return (model_block, rest); string-aware paren matching because descriptions contain parens."""
    m = re.search(r"\bMODEL\s*\(", text, re.I)
    if not m:
        return "", text
    i, depth, in_str = m.end(), 1, False
    while i < len(text) and depth:
        ch = text[i]
        if in_str:
            if ch == "'":
                if text[i + 1:i + 2] == "'":
                    i += 1
                else:
                    in_str = False
        elif ch == "'":
            in_str = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        i += 1
    return text[m.start():i], text[i:].lstrip().lstrip(";")


def demacro(sql: str) -> str:
    sql = re.sub(r"@\{(\w+)\}", r"\1", sql)
    sql = re.sub(r"@(\w+)\s*\(", r"MACRO_\1(", sql)
    return re.sub(r"@(\w+)", r"\1", sql)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models-dir", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--dialect", default="snowflake")
    a = ap.parse_args()

    rows, issues = [], []
    for f in sorted(a.models_dir.rglob("*.sql")):
        text = f.read_text(encoding="utf-8-sig", errors="replace")
        block, body = split_model_block(text)
        nm = re.search(r"\bname\s+([^\s,]+)", block)
        if not nm:
            issues.append((str(f), "no-model-name"))
            continue
        schema, table = demacro(nm.group(1)).lower().split(".")[-2:]
        try:
            stmts = [s for s in sqlglot.parse(demacro(body), read=a.dialect) if s is not None]
        except Exception as e:  # noqa: BLE001
            issues.append((f"{schema}.{table}", f"parse-failed: {str(e).splitlines()[0][:150]}"))
            continue
        query = next((s for s in stmts if isinstance(s, exp.Query)), None)
        if query is None:
            issues.append((f"{schema}.{table}", "no-query"))
            continue
        rel = str(f.relative_to(a.models_dir))
        for p in query.selects:
            if isinstance(p, exp.Star) or (isinstance(p, exp.Column) and isinstance(p.this, exp.Star)):
                issues.append((f"{schema}.{table}", "select-star"))
            elif p.alias_or_name and not p.alias_or_name.lower().startswith("macro_"):
                rows.append((schema, table, p.alias_or_name.lower(), rel))

    with a.out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["schema", "table", "column", "model_file"])
        w.writerows(sorted(set(rows)))
    print(f"tables={len({(r[0], r[1]) for r in rows})} columns={len(set(rows))} issues={len(issues)}")
    for i in issues:
        print("  issue:", *i, file=sys.stderr)


if __name__ == "__main__":
    main()
