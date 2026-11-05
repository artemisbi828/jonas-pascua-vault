**Decision:** keep one **source of truth** that has no client in it, with a thin adapter for each client. MCP covers the "prompt and tool" part across Copilot, Claude Desktop, Cursor, and others. Your `SKILL.md` covers agents that read skills.

# MCP MVP
`my-best.json` in my semantic-registry. Which holds: 
- weighted-criterion
- tiebreaker stances
```
refine-message\
└─ mcp\
   ├─ server.py                   -- ~40 lines Python (FastMCP, stdio); reads ..\skill\*
   └─ clients\
      ├─ vscode.mcp.json
      └─ claude_desktop_config.json  -- Mac: ~/Library/Application Support/Claude/
```

```
ai-preferences\
├─ response-style.instructions.md  -- now: "best = my-best; read my-best.json, cite the deciding key"
│                                     (old weights table deleted: one source, no drift)
└─ my-best.json                    -- conceptual axes you can edit
   ├─ criteria
   │  ├─ stack-fit        3
   │  ├─ low-friction     3  -- no extra installs, Windows + Mac (shell, platform, deps)
   │  ├─ speed            2
   │  ├─ maintainability  2
   │  ├─ blast-radius     2
   │  ├─ fails-loud       2  -- no silent false-positive parses  (new)
   │  └─ human-editable   1  -- counts, but loses ties             (new)
   └─ examples           -- past decisions, so the "why" stays with the weights
      └─ 2026-10-14 json > yaml
```
# Full MCP
```
refine-message\                        -- toolkit project (dev tier)
├─ README.md  map.md  sequence.md  SAVEPOINT.md  changelog.md  sessions\
├─ config\
│  ├─ axes.json            -- axis -> allowed values + default
│  └─ translation.csv      -- from_term, to_term, scope (1:1)
├─ skill\
│  └─ SKILL.md             -- the procedure; reads config\, never repeats it
├─ mcp\
│  ├─ server.py            -- stdio MCP server: exposes prompt + tool "refine_message"
│  └─ requirements.txt     -- only `mcp`
├─ clients\                -- install snippets only, no logic
│  ├─ vscode.mcp.json
│  └─ claude_desktop_config.json
└─ to-go\
   └─ build-package.ps1    -- zip: config + skill + mcp + clients + RUNBOOK.md
```

- **Why this layout is cross-compatible:** stdio MCP with Python works on both Mac and PC. Each client only needs a command and a path, so only the `clients\` snippets differ.
- **Promotion path:** dev tier = a category folder such as `sandbox\`. When a tool proves itself, move it to the toolkit root and update the index row. No code changes.
## Devil's advocate

- `[case-against]` An MCP server for message rewriting may be more than you need. The LLM already rewrites. A `SKILL.md` plus `axes.json` plus `translation.csv` gives 90% of the value. Only the MCP part makes it shareable to Claude Desktop for a friend. Option: build the skill first and add MCP in chunk 4.
- `[pitfall]` A `sandbox` category that never gets promoted turns into a junk drawer. Fix: put a `promote-gate::` line in each SAVEPOINT (for example "used 10 times, no edits to axes in 2 weeks").
- `[collision]` Calling the config slots "dimensions" would clash with the data-model sense in `dimension-governance.md`. That file is the handler. Use **axis**, which already appears in `cheat-sheet-requirement-ambiguity.md`.



