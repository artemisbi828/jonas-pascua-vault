---
kind: standard
status: draft
updated: 2026-09-29
---

# Standard - Process - Vault Operating Workflow

How to keep this vault clean with AI help, without losing the trail. Pairs with [[03-toolkit/README]] (map), [[AGENTS]] (rules the AI follows), [[vault-changelog]] (what changed), [[vault-decisions]] (why).

## TLDR

```
commit -> pick ONE scope -> AI writes proposal to WIP/ -> you decide -> AI applies -> log -> commit
```

- One scope per pass, e.g. "standards folder", "Add-on synonyms", "tag typos".
- Conflicts come to you as a list with options and a recommendation. Nothing changes until you pick.
- A pick that will recur becomes a rule in the matching `Standard - ...` note ("canonized").

## Two Logs, Two Jobs

| File | Answers |
|---|---|
| [[vault-changelog]] | What changed, when, which commit |
| [[vault-decisions]] | Why a rule exists, what alternatives were rejected |

## Cadence

| When | What | Who |
|---|---|---|
| During the day | Capture only. `#review/later` when tired. No organizing. | You |
| End of day | Scrub **only notes changed today** (git knows which) -> proposals -> decide -> commit | AI proposes, you decide |
| Weekly | Archive daily notes > 10 days, duplicate/merge report, `#review/later` queue, tag registry drift | AI proposes, you decide |
| Monthly | Review standards and decisions: promote, retire, merge. Empty `WIP/`. | You, with AI |

## Anti-Patterns

1. **Renaming notes outside Obsidian** breaks `[[links]]`. Rename in Obsidian, or update every link in the same commit.
2. **Vault-wide rewrite in one commit.** One rule per commit.
3. **AI merges or deletes on its own.** Always a proposal. Retired notes go to `.trash`; git still has them.
4. **Same rule in two places.** One standard owns it; everything else links.
5. **Unregistered tags.** They regrow the clutter.
6. **Deep folders.** A few top-level folders; tags and properties for the rest.
7. **Daily notes as the knowledge base.** Daily = inbox. Distill into concept notes, then archive.
8. **Editing a note while the AI edits it.** Let the pass finish first.

## Commit Message Format

`<actor>: <what> -- <why>` e.g. `ai: merge abbreviations -- single source (2b)`

## Recovery

- Undo one note: `git log -- "<note>.md"`, then `git restore --source <commit> -- "<note>.md"`
- Full baseline: `C:\obsidian\_backups\project-ascend--202609291327\` and commit `b31ae32`
