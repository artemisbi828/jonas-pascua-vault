"""Reduce a directory of SQL files to distinct physical catalog.schema.table.column refs (before),
then map each one to a target environment (after) using a schema snapshot, an environment map and a rename map.

CTE and subquery columns resolve to the physical columns they read from. SELECT * is followed through to its source.
Comments are ignored. Every flag goes to <out>.evidence.csv with the source file.
"""
import argparse
import csv
import difflib
from collections import defaultdict
from pathlib import Path

import sqlglot
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import Scope, traverse_scope

UNKNOWN = "null-handling: unknown"
DIALECTS = ("snowflake", "tsql", None)


def read_csv(path):
    if not path:
        return []
    with Path(path).open(newline="", encoding="utf-8-sig") as fh:
        return [{k.strip().lower(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]


class Catalog:
    """Schema snapshot + environment rules. Keys are base (unsuffixed) schema.table, lowercase."""

    def __init__(self, schema_csv, env_csv, rename_csv, target):
        self.cols = defaultdict(set)
        for r in read_csv(schema_csv):
            self.cols[f"{r['schema'].lower()}.{r['table'].lower()}"].add(r["column"].lower())
        self.envs = read_csv(env_csv)
        self.suffixes = sorted({e["schema_suffix"].lower() for e in self.envs if e["schema_suffix"]},
                               key=len, reverse=True)
        self.target = None
        if target:
            hits = [e for e in self.envs if e["sqlmesh_env"].lower() == target.lower()]
            if len(hits) != 1:
                raise SystemExit(f"--target {target!r} must match exactly one sqlmesh_env row in --env-map")
            self.target = hits[0]
        self.renames = {(f"{r['schema']}.{r['table']}".lower(), r["old_column"].lower()): r
                        for r in read_csv(rename_csv)}

    def base_schema(self, schema: str) -> str:
        s = schema.lower()
        for suf in self.suffixes:
            if s.endswith(suf):
                return s[: -len(suf)]
        return s

    def key(self, t: exp.Table) -> str:
        return f"{self.base_schema(t.db)}.{t.name.lower()}"

    def has(self, key: str, col: str) -> bool:
        return col in self.cols.get(key, ())

    def qualify_schema(self):
        """Nested catalog -> schema -> table -> {col: type} for every env-map catalog and suffix."""
        out = {}
        for e in self.envs:
            cat = out.setdefault(e["analytics_catalog"].lower(), {})
            for key, cols in self.cols.items():
                if cols:
                    s, t = key.split(".")
                    cat.setdefault(s + e["schema_suffix"].lower(), {})[t] = {c: "VARCHAR" for c in cols}
        return out

    def render(self, key: str, col: str) -> str:
        if not self.target:
            return f"{key}.{col}"
        s, t = key.split(".")
        return f"{self.target['analytics_catalog'].lower()}.{s}{self.target['schema_suffix'].lower()}.{t}.{col}"

    def map_after(self, before: str):
        parts = before.split(".")
        if len(parts) < 3:
            return UNKNOWN, "unexpected-shape"
        schema, table, col = parts[-3:]
        key = f"{self.base_schema(schema)}.{table}"
        if not self.cols:
            return UNKNOWN, "no-schema-snapshot"
        if key not in self.cols:
            return UNKNOWN, "table-missing-in-snapshot"
        if col in self.cols[key]:
            return self.render(key, col), ""
        rn = self.renames.get((key, col))
        if rn and rn["new_column"].lower() in self.cols[key]:
            return self.render(key, rn["new_column"].lower()), f"rename: {rn.get('status', '')}".strip()
        near = difflib.get_close_matches(col, sorted(self.cols[key]), n=3, cutoff=0.6)
        return UNKNOWN, "column-missing-in-snapshot" + (f"; near: {' | '.join(near)}" if near else "")


def table_fqn(t: exp.Table) -> str:
    return ".".join(p for p in (t.catalog, t.db, t.name) if p).lower()


def find_source(scope: Scope, alias: str):
    s = scope
    while s is not None:
        if alias in s.sources:
            return s.sources[alias]
        s = s.parent
    return None


def owns(cat: Catalog, src, col: str, depth: int = 0) -> bool:
    """True if a physical source has col in the snapshot, or a derived source projects it (through stars)."""
    if isinstance(src, exp.Table):
        return cat.has(cat.key(src), col)
    sel = getattr(src, "expression", None)
    if not isinstance(sel, exp.Select) or depth > 10:
        return False
    for p in sel.selects:
        if p.alias_or_name.lower() == col:
            return True
        if isinstance(p, exp.Star) and any(owns(cat, s, col, depth + 1) for s in src.sources.values()):
            return True
    return False


def resolve(cat: Catalog, scope: Scope, alias: str, col: str, depth: int = 0):
    """Yield (fqn_column, note). Explicit CTE projections are skipped: their inputs are captured in the CTE scope."""
    src = find_source(scope, alias)
    if src is None:
        yield f"?{alias}.{col}", "unresolved-alias"
        return
    if isinstance(src, exp.Table):
        yield f"{table_fqn(src)}.{col}", "" if src.db else "unqualified-table"
        return
    if depth > 10:
        return
    # attribute name differs across sqlglot versions
    branches = getattr(src, "union_scopes", None) or getattr(src, "set_scopes", None) or [src]
    for b in branches:
        sel = b.expression
        if not isinstance(sel, exp.Select) or col in {p.alias_or_name.lower() for p in sel.selects}:
            continue
        for p in sel.selects:
            if isinstance(p, exp.Star):
                owners = list(b.sources) if len(b.sources) == 1 else [
                    a for a in b.sources if owns(cat, b.sources[a], col)]
                for a in owners if len(owners) == 1 else []:
                    yield from resolve(cat, b, a, col, depth + 1)
            elif isinstance(p, exp.Column) and isinstance(p.this, exp.Star):
                yield from resolve(cat, b, p.table, col, depth + 1)


def parse(sql: str):
    last = None
    for d in DIALECTS:
        try:
            return [t for t in sqlglot.parse(sql, read=d) if t is not None], d, None
        except Exception as e:  # noqa: BLE001 - try next dialect
            last = e
    return [], None, str(last).splitlines()[0][:200]


def qualify_tree(tree, dialect, schema, evidence, rel):
    opts = dict(dialect=dialect, validate_qualify_columns=False, quote_identifiers=False,
                identify=False, expand_stars=False)
    try:
        return qualify(tree, schema=schema or None, **opts)
    except Exception as e:  # noqa: BLE001
        evidence.append(("", rel, f"qualify-failed: {str(e).splitlines()[0][:200]}"))
    try:  # renamed columns break schema-aware qualify; retry schema-less
        return qualify(tree, **opts)
    except Exception:  # noqa: BLE001
        return tree


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sql-dir", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--schema-csv", help="schema,table,column[,...] snapshot (base schema names, no env suffix)")
    ap.add_argument("--env-map", help="gateway,sqlmesh_env,analytics_catalog,schema_suffix")
    ap.add_argument("--target", help="sqlmesh_env row from --env-map used to render after")
    ap.add_argument("--rename-map", help="schema,table,old_column,new_column,status")
    a = ap.parse_args()

    cat = Catalog(a.schema_csv, a.env_map, a.rename_map, a.target)
    qschema = cat.qualify_schema()
    evidence = []
    files = sorted(a.sql_dir.rglob("*.sql"))
    for f in files:
        rel = str(f.relative_to(a.sql_dir))
        trees, dialect, err = parse(f.read_text(encoding="utf-8-sig", errors="replace"))
        if err:
            evidence.append(("", rel, f"parse-failed: {err}"))
            continue
        for tree in trees:
            tree = qualify_tree(tree, dialect, qschema, evidence, rel)
            for scope in traverse_scope(tree):
                for c in scope.columns:
                    col = c.name.lower()
                    if not col or isinstance(c.this, exp.Star):
                        continue
                    alias = c.table
                    if not alias:
                        owners = list(scope.sources) if len(scope.sources) == 1 else [
                            s for s in scope.sources if owns(cat, scope.sources[s], col)]
                        if len(owners) == 1:
                            alias = owners[0]
                        elif isinstance(scope.expression, exp.Select) and col in {
                                p.alias_or_name.lower() for p in scope.expression.selects}:
                            evidence.append((f"?.{col}", rel, "query-alias"))
                            continue
                        else:
                            evidence.append((f"?.{col}", rel, "ambiguous-owner"))
                            continue
                    for fq, note in resolve(cat, scope, alias, col):
                        evidence.append((fq, rel, note))

    befores = sorted({fq for fq, _, _ in evidence if fq and not fq.startswith("?")})
    with a.out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["before", "after", "concept_tags"])
        for fq in befores:
            after, note = cat.map_after(fq)
            w.writerow([fq, after, ""])
            if note:
                evidence.append((fq, "(after)", note))
    with a.out.with_name(a.out.stem + ".evidence.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["before", "file", "note"])
        w.writerows(sorted(set(evidence)))

    unknown = sum(1 for fq in befores if cat.map_after(fq)[0] == UNKNOWN)
    print(f"files={len(files)} distinct_before={len(befores)} mapped={len(befores) - unknown} unknown={unknown} "
          f"flags={sum(1 for e in set(evidence) if e[2])}")


if __name__ == "__main__":
    main()
