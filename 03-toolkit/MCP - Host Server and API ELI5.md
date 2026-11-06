---
tags: []
status: draft [uncertified]
related: ["[[MCP - Mental Model and Portable Architecture]]", "[[MCP - Spine Server ELI5]]", "[[Taxonomy - Abbreviation]]"]
---
**TL;DR** The **host** is the app you open. It starts your **server**, a small program that answers requests. The **API** is the written-down contract for what you may ask; it is not a program, so it can exist with no server at all. People say "API" and "server" as if they were one thing, and that is what makes it confusing.

```table-of-contents
```

## The restaurant picture

You walk into a restaurant (the **host**, the app you opened). The kitchen counter is the **server**. The posted menu with its rules ("no substitutions, soup comes with bread") is the **API**.

- You never walk behind the counter and switch it on. The restaurant does that when it opens.
- The menu can exist on paper before any kitchen is built. That is how an API can exist with no server.
- The counter and the cook are one program. There is no separate runner.

## Who starts what

You open VS Code or Claude Desktop. That is the **host**. It reads its config file (`mcp.json`), launches `python server.py` as a **child process**, and talks to it. Closing the host ends the server.

```text
YOU opens ──► HOST (VS Code / Claude Desktop)
                ├─ LLM (in the cloud)
                ├─ MCP client (one per server, inside the host)
                └─ launches ──► SERVER process (your server.py)
```

Running `python server.py` yourself would just leave it waiting, because nothing is sending it requests. `fastmcp dev` is the exception: it starts a tiny test host.

## stdin, stdout, stderr, stdio

These are the three channels every program gets from the OS, like windows at a counter.

| abbrev | expansion | picture |
|---|---|---|
| stdin | standard input | order-slip window |
| stdout | standard output | pickup window |
| stderr | standard error | side door for complaints and logs |
| stdio | standard input/output | the two main windows together |

Normally stdin is your keyboard and stdout is your screen. For MCP, the host rewires them into pipes to the server. A stray `print()` drops junk in the pickup window and breaks the reply, so write logs to stderr.

## The request ID and "routing"

In stdio mode the server has one customer, the host that launched it, so there is nothing to route. Your friend's Mac runs its own private copy.

Each request still carries an **ID number** and the reply repeats it:

```text
host ──"id 7: call lookup_term(DA)"──► server
host ◄──"id 7: result ..."───────────  server
```

The ID matches an answer to the question that caused it, in case several are in flight. Only in HTTP mode, with many customers at once, does the framework also route replies to the right connection.

## API vs server

An API is a **contract**; a server is a **running program**. A server *implements* an API; a client *calls* it.

An API is more than documentation. It is the interface itself: names, the shape of inputs and outputs (types or classes), error behavior, and gates such as login or limits. Docs and specs describe it. It says **what** you may ask, never **how** the work is done.

```text
API
├─ library API   -- pandas.read_csv(path): runs inside your own program; no server, no waiting
├─ web API       -- the same contract carried over HTTP; a server answers
└─ protocol API  -- MCP: tools/resources/prompts as messages over stdio or HTTP
```

A wall socket's plug shape is an API. The standard exists before any power plant (server) does, and it still works with a battery pack on your desk.

## Does the minimum MCP have an API?

Yes, at two layers, and you write neither as a separate document.

```text
MCP spec (standard)          -- the protocol API; FastMCP implements it
└─ your tool API             -- tool names, parameter types, docstrings
   └─ lookup_term(term: str) -- this signature IS your API; the body is the server work
```

What you can skip in the minimum: HTTP, a hand-written spec, authentication. What you cannot skip: the tool signatures and docstrings, because the model reads them to choose what to call.
