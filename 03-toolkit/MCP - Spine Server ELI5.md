---
tags: []
status: draft [uncertified]
related: ["[[MCP - Mental Model and Portable Architecture]]", "[[MCP]]"]
---
**TL;DR** `server.py` is a small program that does nothing until an AI app asks it something. It announces what it can do (tools, resources, prompts), answers when asked, and goes back to waiting. It holds no knowledge itself; it just reads your files and hands them over.

```table-of-contents
```

## The service counter and the menu

Your registry, `my-best.json`, skills and DuckDB are the **kitchen**. Copilot or Claude Desktop is the **host** (the app you open; it starts the server for you). `server.py` is the **service counter with a menu**: the counter and the runner behind it are one running program, not two.

- The file is only the written menu and instructions. It is static, like a recipe card.
- When the host launches it, it becomes a running process: lights on, listening on **stdio** (one customer, so no routing needed).
- It hands over the **menu** (tools, resources, prompts), runs the matching function when asked, and returns the result tagged with the request ID.
- It does not cook. If it invents answers, the kitchen and the counter disagree (drift).

Same menu, any host: that is why a Mac with Claude Desktop and your Windows VS Code can share it. More in [[MCP - Host Server and API ELI5]].
## What the file contains

Three kinds of things, each a plain Python function with a label on top (a **decorator**, the `@...` line):

```text
server.py
├─ @mcp.tool()      lookup_term(term)     -- "go look this up"   (the model decides to call it)
├─ @mcp.resource()  prefs://my-best       -- "here is a document" (you or the app attach it)
├─ @mcp.prompt()    refine_message        -- "here is a saved instruction" (you pick it)
└─ mcp.run()                              -- "open the doors and wait"
```

A minimal version (about the size of the real one; verify names against current FastMCP docs):

```python
from fastmcp import FastMCP
import csv, pathlib

mcp = FastMCP("toolkit")
CANON = pathlib.Path(__file__).parent.parent / "canon"

@mcp.tool()
def lookup_term(term: str) -> str:
    """Return the registered prime for a term, or say it is not registered."""
    with open(CANON / "semantic-registry" / "taxonomies" / "abbreviation.csv") as f:
        for row in csv.DictReader(f):
            if row["abbreviation"].lower() == term.lower():
                return str(row)
    return "[gap] not registered"

@mcp.resource("prefs://my-best")
def my_best() -> str:
    return (CANON / "preferences" / "my-best.json").read_text()

if __name__ == "__main__":
    mcp.run()
```

The docstring matters: the model reads it to decide when to use the tool. The type hints (`term: str`) tell the host what to send.

## What happens when you start it

You do not run it yourself. The host does, from the one-line config in `.vscode\mcp.json` (or Claude's `claude_desktop_config.json`).

```text
1. host starts:  python spine\server.py        -- as a child process
2. host asks:    "what can you do?"            -- server replies with the menu
3. you ask:      "is DA registered?"
4. model picks:  lookup_term("DA")             -- host sends it down the pipe
5. server reads the CSV, replies
6. model answers, citing the result
```

The "pipe" is **stdio**: the server reads requests from standard input and writes replies to standard output. No network, no password. This is also why the server must never `print()` debug text; that would corrupt the reply. Log to a file or stderr instead.

## What it must not do

- **Hold knowledge.** Facts live in `canon\`; the server reads them each time, so there is one source of truth.
- **Contain host logic.** No "if Claude then...". Differences between hosts belong in `adapters\`.
- **Write to canon or DuckDB.** Open DuckDB read-only so a wrong model call cannot damage anything.
- **Grow big.** If the file passes a few hundred lines, split tools into modules; the file stays a thin menu.

## Try it by hand

Run it without any AI app to see the menu (needs the `fastmcp` package in a venv; venv must be activated):

```powershell
.\.venv\Scripts\Activate.ps1
fastmcp dev spine\server.py
```

You should see an inspector page listing `lookup_term` and `prefs://my-best`; call the tool with `DA` and it returns a row or `[gap] not registered`. `[uncertified]`: the command name comes from FastMCP docs as I recall them, so check them first.
