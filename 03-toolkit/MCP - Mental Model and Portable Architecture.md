---
tags: []
status: draft [uncertified]
related: ["[[MCP]]", "[[taxonomy-abbreviation|Taxonomy - Abbreviation]]", "[[MCP - Spine Server ELI5]]", "[[MCP - Host Server and API ELI5]]"]
---
**TL;DR** MCP is a standard plug: an AI app (the **host**) starts your small program (the **server**) and asks it what it can do. You keep one source of truth, write one server, and give each host a thin config file. The MCP rules are an **API** (a contract), so the minimum portable setup uses an API but you never write one by hand.

[[MCP - Proposal - Transition]]

```table-of-contents
```

## What MCP is (one paragraph)

MCP (Model Context Protocol) is a standard plug between an AI app (the **host/client**) and a program that offers capabilities (the **server**). The server says "here are my tools, resources, prompts"; any MCP-speaking host can call them. Think USB-C: write the server once, every host plugs in.

```text
HOST (the AI app)                        SERVER (your code)
├─ VS Code Copilot  ─┐                   ├─ tools      -- functions the model CALLS (query_duckdb, lookup_term)
├─ Claude Desktop   ─┼─ MCP (JSON-RPC) ─►├─ resources  -- read-only data the app ATTACHES (a registry note, a CSV)
└─ Cursor, others   ─┘   stdio or HTTP   └─ prompts    -- reusable templates the USER picks (/review-proposals)
```

## The three primitives (who controls what)

| primitive | controlled_by | use_for | your_example |
|---|---|---|---|
| tool | model decides to call | actions, lookups, computation | `lookup_term("DA")`, `run_sql(duckdb, ...)` |
| resource | app/user attaches | static or addressable context | `registry://semantic-registry`, `my-best.json` |
| prompt | user invokes | repeatable workflow entry | `/journal`, `/create-note` |

## Transport: how host talks to server

```text
stdio (local)     host launches server as a child process; talks over stdin/stdout
                  -- no network, no auth, simplest. Use for MVP.
streamable HTTP   server runs somewhere; host connects by URL
                  -- needed only to share ONE live server with others (auth required)
```

**stdio** abbreviations (registered in [[taxonomy-abbreviation|Taxonomy - Abbreviation]]):

| abbrev | expansion | plain_meaning |
|---|---|---|
| stdin | standard input | the order-slip window: what the program receives (default: keyboard) |
| stdout | standard output | the pickup window: what the program replies (default: screen) |
| stderr | standard error | the side door for log and error messages |
| stdio | standard input/output | stdin and stdout together |

Every program the OS starts gets these three channels. For MCP the host rewires them into pipes to your server. A stray `print()` lands in the pickup window and corrupts the reply, so log to stderr or a file.

## Host, client, server (who is who)

```text
YOU
 │ open VS Code / Claude Desktop
 v
HOST (the app you use)
├─ LLM connection  -- model runs in the cloud; host relays messages
├─ MCP client      -- connector inside the host, one per server
│     │ reads mcp.json, launches the server, talks over stdio
│     v
└─ SERVER process (your server.py, local, alive only while the host is open)
      └─ reads your files (canon, DuckDB)
```

| role | is | example |
|---|---|---|
| host | the app you open | VS Code Copilot, Claude Desktop |
| client | connector inside the host, one per server | invisible; the host manages it |
| server | your program offering tools, resources, prompts | `server.py` |

You do not run the server; the host does, from its config file (`.vscode\mcp.json`). Closing the host ends the server. The exception is `fastmcp dev`, which starts a test host so you can poke the server yourself.

## The server is a service counter, not a map

`server.py` the **file** is static, like a recipe card. Started, it becomes a **process**: lights on, waiting at stdin. The posted menu is built by the framework from your `@mcp.tool()` functions. When an order arrives, your function runs and its return value goes back out.

```text
host ──"id 7: call lookup_term(DA)"──► server loop ──runs──► your function
host ◄──"id 7: result ..."───────────  server loop ◄─returns─┘
```

- Counter and runner are the same program; there is no separate person.
- **Routing:** over stdio there is one customer (the host that launched it), so nothing to route. Each host gets its own private copy of the server, on your laptop and on your friend's Mac.
- Every request carries an **ID**; the reply echoes it, so answers match questions when several are in flight.
- In HTTP mode each connection is a separate customer and the framework routes replies, not your code.

## API vs server vs protocol

They are different categories, not parent and child. Everyday speech uses "API" and "server" interchangeably; that is the source of the confusion.

```text
API       = the contract: what you may ask, in what shape, what comes back   (menu + rules)
server    = a running program that does the work                             (counter + runner)
protocol  = rules of the conversation: message format, order, transport

a server IMPLEMENTS an API.  A client CALLS it.
```

**Is an API "just documentation"?** Close, but more. An API is the interface itself: names, input and output shapes (types or class definitions), error behavior, and gates (authentication, limits, validation). Documentation or a spec (for example OpenAPI) is a written description of it. An API says **what** you may ask, never **how** the server does the work.

**How can an API exist without a server?** The API is the contract, not a running thing. Three pictures:

```text
API
├─ library API     -- pandas.read_csv(path): names, inputs, outputs are defined; the code runs
│                     inside YOUR program. Nothing waits, nothing is "served".
├─ web API         -- the same idea, carried over HTTP (REST, GraphQL); a server answers.
│                     HTTP is the web protocol; a browser is only one possible client.
└─ protocol API    -- MCP: tools, resources, prompts as JSON-RPC messages,
                      carried over stdio OR HTTP
```

Analogy: a wall socket's plug shape is the API. It exists as a standard before any power plant (server) is connected. A plug and socket still work with a battery pack on your desk.

Calling your own internal server through an API is normal: any client that follows the rules works, including your own code on the same machine. What a *web* server adds is HTTP, URLs, many simultaneous customers, and authentication. Your stdio server drops all of that.

## Does the minimum portable MCP have an API?

Yes, at two layers, and you write neither as a separate document:

```text
MCP spec (fixed, standard)        -- the protocol API; FastMCP implements it for you
└─ your tool API (yours)          -- the menu: tool names, parameter types, docstrings
   └─ lookup_term(term: str)      -- this signature IS your API; the function body is the server work
```

Not required for the minimum: HTTP, a hand-written spec, authentication. Required: the tool signatures and docstrings, because the model reads them to decide what to call.

## Where everything you own sits (the layers)

Layer rule from your preferences: registry = what and why; instructions = always-on behavior; skills = on-demand procedure; MCP = the delivery mechanism, not a new source of truth.

```text
YOUR ASSETS                          MCP-NATIVE?   PORTABLE VIA
├─ Semantic Registry (vault)         no (files)    server RESOURCE + TOOL (lookup, check)
├─ my-best.json, config CSV/JSON     no (files)    server RESOURCE + TOOL (score)
├─ DuckDB indexes                    no (file)     server TOOL (read-only SQL)
├─ Skills (SKILL.md)                 NO -- host-specific (Copilot/Claude Code read them)
│                                                  server PROMPT exposes the same text to any host
├─ ai-preferences / AGENTS.md        NO -- host-specific instruction file
│                                                  thin adapter per host: CLAUDE.md, copilot-instructions.md
└─ Scripts / tools (toolkit)         no            server TOOL wrapper (calls the script)
```

Key insight: **MCP carries tools, resources, prompts. It does not carry "always-on instructions".** Those need a one-line adapter file per host that points at the same canonical text.

Update 2026-10-17: the Copilot-side adapter already exists and is self-checking (`deploy.ps1` mirrors prompts and the CLI instructions, stamps them, and `-AssertFreshness` proves no copy is stale). Only the Claude `CLAUDE.md` pointer is missing. See [[MCP - Proposal - Transition]] for what else changed.

## MVP architecture (ASCII tree)

One spine, no client inside it, thin adapters per host.

```text
toolkit-core\                               -- git repo; the portable unit (clone = install)
├─ README.md  map.md  sequence.md  SAVEPOINT.md          -- toolkit project contract
│
├─ canon\                                   -- SOURCE OF TRUTH (no client logic)
│  ├─ semantic-registry\                    -- notes, taxonomies\*.csv (synced from the vault)
│  ├─ preferences\
│  │  ├─ instructions.md                    -- merged always-on rules (the "MOC")
│  │  └─ my-best.json
│  └─ skills\<name>\SKILL.md                -- procedures; read config, never restate it
│
├─ spine\                                   -- THE MCP SERVER (~100 lines Python, FastMCP, stdio)
│  ├─ server.py
│  │  ├─ resource  registry://<note>        -- reads canon\semantic-registry
│  │  ├─ resource  prefs://my-best          -- reads canon\preferences\my-best.json
│  │  ├─ tool      lookup_term(term)        -- prime, synonyms, collision/drift flags
│  │  ├─ tool      score_options(...)       -- applies my-best weights
│  │  ├─ tool      query_index(sql)         -- DuckDB, READ-ONLY connection
│  │  └─ prompt    <skill-name>             -- serves canon\skills\*\SKILL.md text
│  ├─ config.json                           -- paths: canon root, duckdb file (operator-editable)
│  └─ requirements.txt                      -- fastmcp, duckdb (venv: .venv, pip install -r)
│
├─ indexes\                                 -- DuckDB files, REBUILT from canon (not committed)
│  └─ build-index.py                        -- canon -> registry.duckdb
│
└─ adapters\                                -- THIN: one per host, nothing else inside
   ├─ vscode\
   │  ├─ .vscode\mcp.json                   -- {"servers":{"toolkit":{"command":"python","args":[spine\server.py]}}}
   │  └─ .github\copilot-instructions.md    -- "Read canon\preferences\instructions.md"
   ├─ claude-desktop\
   │  ├─ claude_desktop_config.json         -- Mac: ~/Library/Application Support/Claude/
   │  └─ CLAUDE.md                          -- same one-line pointer
   └─ install.ps1 / install.sh              -- writes the host config with ABSOLUTE paths for that machine
```

## Venn overlap (what is shared, what is host-specific)

```text
              ┌────────────── SHARED CORE (write once) ──────────────┐
              │  canon\ (registry, prefs, skills text, my-best.json)  │
              │  spine\server.py (tools, resources, prompts)          │
              │  indexes\ (DuckDB, rebuilt per machine)               │
              └───────────────┬──────────────────────┬───────────────┘
                              │                      │
        VS CODE COPILOT (you) │                      │ CLAUDE DESKTOP (friend, Mac)
        ├─ .vscode\mcp.json   │                      │ ├─ claude_desktop_config.json
        ├─ copilot-instr.md   │                      │ ├─ CLAUDE.md
        ├─ native SKILL.md    │                      │ ├─ no native skills -> use server prompts
        └─ Windows paths      │                      │ └─ Mac paths
```

| concern | shared | host_specific |
|---|---|---|
| definitions, rules, weights | yes | |
| tool logic | yes | |
| how server is launched | | config file location and format |
| always-on instruction file name | | `copilot-instructions.md` vs `CLAUDE.md` |
| skill auto-discovery | | Copilot/Claude Code only; others get server prompts |
| path separators, shell | | install script resolves per OS |

## Flow of one request

```text
you ask: "is 'DA' registered?"
      |
      v
host model sees tool list (from server on startup)
      |
      v
model calls lookup_term("DA")  --JSON-RPC-->  spine\server.py
      |                                           reads canon\ / duckdb (read-only)
      v                                           returns prime, status, pitfalls
model answers with the registry's result (cited)
```

## Build order (smallest slice first)

| step | slice | done_when |
|---|---|---|
| S1 | server with ONE tool `lookup_term` over taxonomies CSV | tool appears in VS Code and answers |
| S2 | add resource `prefs://my-best` + prompt serving one SKILL.md | same prompt works unchanged in Claude Desktop |
| S3 | `install.ps1` / `install.sh` writes host config | friend clones, runs installer, tool visible |
| S4 | DuckDB `query_index` (read-only) | answers from a rebuilt index |
| S5 | decide HTTP vs stdio for sharing a live server | only if copying the repo is not enough |

## Devil's advocate

- `[drift]` "API" and "server" are used interchangeably in everyday speech. Suggested registry split: API = the contract, server = the running implementation. Neither is registered yet.
- `[pitfall]` The counter analogy breaks on concurrency: a simple server loop may handle one order at a time, so a slow tool blocks the line.
- `[case-against]` A server may be redundant: `lookup_term` could be a skill that greps CSVs. MCP earns its place only for structured calls (DuckDB, scoring) and cross-host reach.
- `[pitfall]` Copying the registry to a friend copies your private/work (orthodontics) content. Split `canon\` into a public/personal core and private domain registries before sharing.
- `[pitfall]` Two copies drift: vault registry vs `canon\semantic-registry`. Pick one writer (vault) and sync one way; never edit the copy.
- `[anti-pattern]` Putting host logic inside the server. Keep adapters thin.
- `[falsifier]` If the friend never calls a tool and only wants the instructions, a plain `CLAUDE.md` plus the canon folder is enough; skip the server.
- `[uncertified]` Config keys and file locations above come from general MCP practice; verify against current VS Code and Claude Desktop docs when building S1.

## Terms to register (`[gap]`)

`spine`, `canon\`, `adapter`, `MOC` (here = always-on instruction file, not Obsidian hub note), `API`, `host`, `client`, `server` are not in the Semantic Registry. Proposed: queue via `review proposals`.
