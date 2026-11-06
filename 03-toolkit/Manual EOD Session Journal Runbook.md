---
kind: runbook
status: draft
created: 2026-10-07
---

# Manual EOD Session Journal Runbook

Use this when the session-journal prompt or automation is unavailable, or when you want to inspect the underlying Copilot records yourself.

## Existing Process

- Project README: `C:\Repos\sd-edw\toolkit\session-journal\README.md`
- EOD prompt: `C:\Repos\sd-edw\toolkit\session-journal\prompts\end-of-day-log.prompt.md`
- Configuration: `C:\Repos\sd-edw\toolkit\session-journal\config.json`
- Journal output: `C:\Repos\sd-edw\toolkit\session-journal\logs\YYYY-MM-DD.md`
- Obsidian output: the `obsidian_daily_journal_directory` in `config.json` (currently `C:\obsidian\Project Ascend`)

The prompt also maintains `index\concepts.csv`, `index\transformations.csv`, and `index\learning-concepts.csv`. Check `config.json` before writing; do not assume the paths remain unchanged.

## Find Copilot Session Records

VS Code stores chat artifacts under the user profile, grouped by workspace storage ID and Copilot session ID:

```text
%APPDATA%\Code\User\workspaceStorage\<workspace-id>\GitHub.copilot-chat\transcripts\<session-id>.jsonl
%APPDATA%\Code\User\workspaceStorage\<workspace-id>\GitHub.copilot-chat\debug-logs\<session-id>\
```

Current example workspace root:

```text
C:\Users\jonas-adam.pascua\AppData\Roaming\Code\User\workspaceStorage\a2f33bdcdb574d9844df7101446eac2b\GitHub.copilot-chat\
```

List recent transcript candidates across workspace roots:

```powershell
$storage = Join-Path $env:APPDATA 'Code\User\workspaceStorage'
Get-ChildItem $storage -Filter '*.jsonl' -File -Recurse |
  Sort-Object LastWriteTime -Descending |
  Select-Object LastWriteTime, FullName
```

Treat timestamps as a discovery aid, not proof of the session's exact work date. Open candidate JSONL transcripts in VS Code and review the conversation records for user requests, assistant outcomes, tool commands/results, errors, and decisions. Debug logs are supporting evidence when a transcript is incomplete; they are not a substitute for understanding the conversation.

## Manual Close-Out

1. **Set the date.** Use the local date from `Get-Date -Format yyyy-MM-dd`. Split work by actual message timestamps if a session crosses midnight.
2. **Review sessions.** Use Chat History to locate today's sessions, then inspect their transcripts. Include completed work and useful partial work; do not omit a session just because it has no PR or commit.
3. **Cross-check evidence.** For each relevant repository, inspect `git status --short`, recent commits, and the actual changed files. Record only commands/results visible in the session or history. `Get-History` covers the current PowerShell session only; for saved PSReadLine history, check `(Get-PSReadLineOption).HistorySavePath`, and review it locally before quoting commands.
4. **Write one append-only session section** in `logs\YYYY-MM-DD.md`. Create the date file if absent. Continue the `## Session N` sequence if present; never rewrite earlier session sections.
5. **Use the established structure:** TL;DR (impact-first), Detail clusters, Commands run, Reasoning trace, and Obsidian vault changes when applicable. Capture meaningful hypothesis/check/pivot, the cause of failures, and the final validation. Avoid narrating routine tool output.
6. **Append the same session summary** to the configured Obsidian daily note. Preserve its existing content; create `# YYYY-MM-DD` only if the note does not exist.
7. **Update indexes from evidence.** Add only genuinely new concepts. Add a transformation only when the before/after pattern is reusable and not already indexed. Update existing learning concepts; never invent a learning goal.
8. **Validate.** Confirm the journal has the new section, the daily note has the appended entry, and CSV headers are intact. Re-read `config.json` and verify every write stayed within the configured journal, indexes, and daily note.

## Safety

- Transcript and terminal history can contain secrets, patient data, or other sensitive values. Do not copy credentials, tokens, or PHI into the journal; summarize the event without the sensitive value.
- Treat repository and vault content as evidence. Do not edit source files or unrelated Obsidian notes as a side effect of journaling.
- Keep prior dates and earlier same-day sessions append-only. If evidence is missing, say so instead of filling gaps by inference.
- The toolkit README/prompt remain authoritative. Update this manual guide when their destinations, write boundaries, or required section structure change.
