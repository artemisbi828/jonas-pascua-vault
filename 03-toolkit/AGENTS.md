---
kind: agents
status: draft
updated: 2026-09-29
---

# Vault Agent Rules

Rules for any AI working in `C:\obsidian\Project Ascend`. Rules only; details live in the linked notes.

## Before Acting

1. Read [[03-toolkit/README]], [[Standard - Process - Vault Operating Workflow]], [[vault-decisions]], and the open checklist in `WIP/`.
2. Standards index: [[Standard]]. Follow a standard; do not restate it here.

## Operating Rules

1. One scope per pass. Commit before and after. Message: `<actor>: <what> -- <why>`.
2. Proposals go to `WIP/` as `tmp--` files. Apply only after the human decides.
3. Never merge, delete, or rename without approval. Deletions move to `.trash/`.
4. A rename updates every `[[link]]` in the same commit.
5. Log every change set in [[vault-changelog]]. Log every decision in [[vault-decisions]].
6. A decision marked canonized is written into its `Standard - ...` note; link to it, don't copy it.
7. Do not change code inside fenced blocks (SQL, DAX, PowerShell) during scrubs unless asked.
8. Stamp `reviewed_ai: YYYY-MM-DD` only on notes actually reviewed.
9. Local git only. No remotes; no copying vault content outside the machine.
10. Keep independent from `C:\Repos\sd-edw\toolkit` (it has its own `AGENTS.md`).
