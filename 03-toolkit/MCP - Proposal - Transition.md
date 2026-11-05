**TL;DR:** Last reviewed 2026-10-17 (first written 2026-10-14). The plan is unchanged: **map, don't move**. A full restructure into the note's `toolkit-core\` layout is still about T1 ×3 (roughly 60–100 tool calls over 2–4 sessions) with high risk. The cheaper path is still: week 1 read your logs, week 2 build only the `lookup_term` slice, and only if the logs justify it (about 15–25 tool calls). **The registry tightening since 2026-10-14 changed the case, not the price:** it closed two gaps without a server (stale copies, naming drift), it shrank the token-saving benefit, and it moved the likely value of `lookup_term` from CSV rows to keyword aliases. No cost reduction has been measured; the estimates below are `[uncertified]` until S1 runs.

## What changed since 2026-10-14

```text
registry tightening (2026-10-15 .. 2026-10-17)
├─ registry-integrity       -> obsidian\registry-integrity: CHK-001 naming check, PASS/FAIL/GAP, run log, pre-commit hook   [[assert-integrity-model]]
├─ assert-freshness         -> deploy.ps1 -AssertFreshness + preferences-stamp: every chat can prove it loaded the latest   [[assert-freshness-model]]
├─ tie-out                  -> alias and duplicate scans over 103 keyword notes                                             [[tie-out-model]]
├─ models + frameworks      -> 22 models, 1 framework (was a handful of notes)                                              [[registry-integrity-framework]]
└─ taxonomy cleanup         -> taxonomy-term archived; taxonomy-abbreviation is the live note; abbreviation.csv (21 rows) stays
```

| rank | item | 2026-10-14 | 2026-10-17 | material_change |
|---|---|---|---|---|
| 1 | Stale copies (agent loads an old prompt or skill) | not covered; a server would have been one fix | covered by freshness stamp and `-AssertFreshness` (tests 10/10) | **yes** (removes a reason to build) |
| 2 | Token benefit of `lookup_term` | assumed "500+ line CSVs" | measured: `abbreviation.csv` 21, `term.csv` 21, `metric.csv` 156, `metric_alias.csv` 270 lines | **yes** (benefit is smaller; the 500+ claim was wrong) |
| 3 | Where a lookup can miss | taxonomy CSV rows | alias fields in 103 keyword notes (tie-out scan 2 found alias collisions) `[uncertified]` | **yes** (S5 scope should cover keyword aliases, not only CSVs) |
| 4 | Naming drift | not covered | CHK-001 advisory (34 findings at first run) | no (not a lookup problem) |
| 5 | S4 thin adapter cost | about 3-5 tool calls (estimate) | about 1-2: `deploy.ps1` already mirrors prompts, the CLI instructions, and the stamp; only a `CLAUDE.md` pointer remains (estimate) | small cost reduction |
| 6 | S1 baseline cost | T2 | T2, but cheaper inputs exist: `registry-integrity\logs\runs.csv`, tie-out runtime log, journal logs (estimate) | small cost reduction |
| 7 | `lookup_term` slice (S5) | about 15-25 tool calls | about 15-25 (no change) | no |
| 8 | Full restructure | T1 ×3 | T1 ×3; the publisher (D3) is still unbuilt and `C:\Repos\toolkit\semantic-registry\` does not exist | no |

**Verdict:** costs fell only at the margin (S1, S4). Benefits fell more (items 1 and 2), so the server is now closer to "mostly a miss-prevention tool for aliases" than a speed or portability win. That makes the S5 miss trigger the one that matters, and the frequency trigger weaker.

```text
MVP layer (note)              your toolkit today                                        gap
├─ canon\preferences       -> ai-preferences\ (instructions, my-best.json)              none
├─ canon\skills            -> ai-preferences\skills\*\SKILL.md                           none
├─ canon\semantic-registry -> C:\obsidian\Project Ascend\04 - Semantic Registry          [collision] rule 12; no published copy yet (D2, D3 open)
├─ integrity               -> C:\Repos\toolkit\obsidian\registry-integrity               built; reads the vault, does not publish
├─ indexes\                -> .dev-in-progress\semantic_register.2026-10-15.duckdb       backup only; not promoted (D5: CSV is source, DuckDB is a rebuilt view)
├─ adapters\               -> ai-preferences\deploy.ps1 (VS Code prompts + CLI mirror + freshness stamp)   no CLAUDE.md / mcp.json
├─ spine\server.py         -> none (toolkit-cli is a CLI facade, not MCP)                [gap]
└─ toolkit-core\ (repo)    -> C:\Repos\toolkit (git; remote undecided per index)         remote [gap]
```

```text
week 1: observe (no structural change)            dates moved: the Thu-Fri window of 2026-10-15/16 passed with no baseline
├─ S1  utilization baseline (Mon-Tue 2026-10-19/20)
│  ├─ Copilot session store  -- tool_executions, session_files: which assets get touched
│  ├─ toolkit sessions\*.md + session-journal logs  -- repeated asks and corrections
│  ├─ registry-integrity runs.csv + tie-out runtime log  -- alias and duplicate misses (new input)
│  ├─ logger DuckDB + raise-advisory tokens  -- what costs credits
│  └─ output: one table, asset x times_used x host x "would an MCP tool have helped?"
├─ S2  toolkit-cli trial verdict (2026-10-21)  -- same facade question; decide together
└─ S3  change-vector draft (Thu-Fri 2026-10-22/23): 3-5 ordered moves, each with size + evidence trigger
                    |
                    v
week 2: smallest slice, gated (from 2026-10-26)
├─ S4  thin adapter only: CLAUDE.md pointer (copilot side already done by deploy.ps1)
├─ S5  IF trigger met -> spine S1: lookup_term over taxonomy CSVs + keyword aliases
│      trigger: registry lookups >= [gap: you set, e.g. 5/week] AND >= 1 miss in S1 data
└─ S6  review + SAVEPOINT in the owning project
```
## S5 trigger: sample scenario

S5 builds only the first server slice: one `lookup_term` tool over the published registry CSVs. Resources, prompts, and DuckDB each wait for their own trigger.

```text
week 1 baseline (S1) finds, over 7 days:
├─ agent read taxonomies\*.csv or registry notes   -- 9 times across 5 sessions
├─ you asked "is X registered?"                     -- 3 times
├─ naming-check read abbreviation.csv              -- 4 times
└─ 1 wrong answer: agent missed synonym "DA" -> prime  -- grep found the note, not the alias row
                  |
                  v
trigger: >= 5 lookups/week  AND  >= 1 miss  -> MET -> build lookup_term
not met: 2 lookups/week, 0 misses           -> skill + grep is enough; recheck in 2 weeks
```

A miss is the stronger signal: frequency only shows cost, a miss shows wrong answers.

## Tradeoffs of building the server

Benefits first.

| rank | benefit | criterion |
|---|---|---|
| 1 | Same answer every time: a typed tool returns the prime, aliases, and flags, or an explicit "not registered". A grep can return a wrong but plausible match | `fails-loud` |
| 2 | Fewer tokens: a 5-line row comes back instead of the agent reading a CSV or scanning 103 keyword notes. Revised 2026-10-17: the CSVs are only 21-270 lines, so the saving is real mainly for alias lookups across keyword notes | `speed`, credits |
| 3 | One code path: `naming-check` and `keyword-enrich` call one tool instead of each restating the lookup steps | `maintainability` |
| 4 | Works in any host: VS Code, Copilot CLI, and Claude Desktop on a friend's Mac | portability |
| 5 | Practice toward the full-stack goal (Python service, protocols) | `stack-fit` |

| rank | cost | criterion |
|---|---|---|
| 1 | Needs a pip package (`mcp` or `fastmcp`) on Python 3.14; compatibility not checked `[gap]` | `low-friction` |
| 2 | One more process per host (~30-60 MB, estimate `[gap]`); RAM is often under 1 GB free | `low-friction` |
| 3 | stdio failures are hard to see: one stray `print()` breaks the replies | `fails-loud` (inverted) |
| 4 | A change to the CSV columns breaks the tool. It fails loud, but you have to fix it | `maintainability` |
| 5 | More tools in the tool list means the model may pick the wrong one | `blast-radius` |

`[falsifier]` If the week-1 baseline shows zero misses, the top benefit (`fails-loud`) does not apply, and the server is mostly a speed optimization.

---
## Appendix

- [[MCP - Mental Model and Portable Architecture]] -- target architecture this transition moves toward
- [[MCP - Spine Server ELI5]], [[MCP - Host Server and API ELI5]] -- plain-language companions
- [[assert-integrity-model]], [[assert-freshness-model]], [[tie-out-model]], [[registry-integrity-framework]] -- the tightening that changed this review
- Tool: `C:\Repos\toolkit\obsidian\registry-integrity\README.md`; publisher decisions (D2, D3, D5): `C:\Repos\toolkit\ai-preferences\SAVEPOINT.md`
- Criteria source: `C:\Repos\toolkit\ai-preferences\my-best.json`
