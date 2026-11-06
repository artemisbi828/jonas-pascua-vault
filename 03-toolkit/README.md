---
kind: readme
status: draft
updated: 2026-09-29
---

# Project Ascend Vault

Work notes for Smile Doctors EDW / Project Ascend: concepts, metrics, SQL, dashboards, standards, and daily logs.

## Quick Start

| I want to... | Go to |
|---|---|
| Log today's work | `YYYY-MM-DD.md` in the vault root (daily note) |
| Find a standard | [[Standard]] (target home: `01 - Standards/`) |
| See what changed and why | [[vault-changelog]] (what), [[vault-decisions]] (why), `git log` |
| How a cleanup pass works | [[Standard - Process - Vault Operating Workflow]] |
| Rules the AI follows | [[AGENTS]] |
| See open decisions | `WIP/` (`tmp--` files) |
| Find a concept's canonical spelling | the concept note's `aliases` / `forms` properties |
| Park something for later | add `#review/later` anywhere in the note |

## Folder Map

| Folder | Holds |
|---|---|
| `00 - Templates/` | Note templates |
| `01 - Standards/` | *(planned)* All standards; one per note |
| `02 - Logs/` | Vault changelog (human + AI changes) |
| `03 - Toolkit/` | Reusable how-tos: SQL, DAX, Git, PowerShell, mechanisms |
| `Archive/` | Daily notes older than 10 days |
| `Master Documents/` | Tag registry seed ([[_MOC - Metadata - Semantic - Domain Objects]]) and core definitions |
| `WIP/` | Drafts and decision checklists (`tmp--` prefix) awaiting approval |
| `98/99 - Attachments/` | Images and files |

## Daily Process

1. Open or create today's daily note.
2. Capture freely. Don't organize while working.
3. Too tired to finish a note? Tag it `#review/later` and move on.
4. Paste snippets under `#status/deferred/quick-paste-merge-later`; they get merged during the nightly pass.

## Nightly Process (AI-assisted)

1. `git commit` (checkpoint before AI changes).
2. The AI scrubs notes changed today:
   - apply naming and synonym standards (`auto` replaces, `flag` asks)
   - suggest missing tags from the registry
   - flag duplicates, collisions, and TLDR notes that are too long
   - convert `#review/later` into review properties
   - stamp `reviewed_ai: <date>`
3. Human approves or rejects flagged items.
4. Append the entry to [[vault-changelog]].
5. `git commit` (checkpoint after; the message states *why*).
6. Weekly: move daily notes older than 10 days to `Archive/`.

## Conventions (Quick Reference)

| Surface | Case | Example |
|---|---|---|
| Tags | kebab-case | `#add-on`, `#source/cc9` |
| SQL / Python | snake_case | `add_on__cc9` |
| Note titles, headings | Title Case | `Add-on` |
| Prose | lowercase | add-on |

- **Tags** = facets used for filtering (datasource, domain, status). Kept small and taken from the registry.
- **Properties** = facts with values (`review_status`, `reviewed_ai`, `depends_on`).
- **Links** = relationships between notes.
- **TLDR note** = short headline note: pivots, pitfalls, anti-patterns. **Doc note** = expanded "why" behind it.
- **Canonical / alias** = the one approved spelling of a concept and its known variants.

## Recovery

- Undo one change: `git log -- "<note>.md"`, then `git restore --source <commit> -- "<note>.md"`
- Full baseline: zip snapshot in `C:\obsidian\_backups\`
