Ran terminal command: $p="$env:USERPROFILE\.agents\skills"; Get-ChildItem $p -Directory | Select -First 8 Name; Get-ChildItem "$p\journal" -Recurse | Select FullName; Get-ChildItem C:\Repos\toolkit\ai-preferences -Recurse -Depth 2 -Filter *.md | Select -First 15 FullName; Select-String -Path C:\Repos\toolkit\ai-preferences\config.json -Pattern journal -Context 2,2

Ran terminal command: Get-ChildItem "$env:USERPROFILE\.agents\skills\journal" -Recurse | % FullName; Get-ChildItem C:\Repos\toolkit\ai-preferences -Depth 2 | % FullName | select -First 30; Get-ChildItem "$env:APPDATA\Code\User\prompts" | % Name

Search for `journal\.prompt`

Ran terminal command: Get-ChildItem C:\Repos\toolkit\obsidian\session-journal | % Name; Select-String C:\Repos\toolkit\ai-preferences\config.json -Pattern 'journal' -Context 3,3 | Out-String; Get-Content "$env:APPDATA\Code\User\prompts\journal.prompt.md" -TotalCount 12

**TL;DR:** `/journal` is a custom command. It is a plain Markdown file, not a plugin. It already has a project (README, map, sequence, config) in your toolkit, so you don't need a separate manifest.

**How it works (ELI5)**

```text
Slash command = a text file the chat reads as its instructions
├─ Built-in (out of the box)   -- /help, /clear, /compact ... code inside VS Code
├─ Prompt files (yours)        -- NAME.prompt.md in %APPDATA%\Code\User\prompts
│  ├─ /journal                 -- journal.prompt.md
│  └─ /create-note             -- create-note.prompt.md
└─ Skills (also invokable)     -- NAME\SKILL.md in %USERPROFILE%\.agents\skills
   └─ keyword-enrich, simple-english, ...
```

- Typing `/journal` pastes the contents of `journal.prompt.md` into the chat as your message. The file's header (`mode: agent`, `description:`) controls how it runs.
- The file can tell the AI to read other files, run scripts, or write notes. That is how `/journal` reads `requirements-incremental.md` and `end-of-day-log.prompt.md`.
- To make a new command, create `anything.prompt.md` with that header and steps. The filename becomes `/anything`.

**Your `/journal` setup**
- Source: `C:\Repos\toolkit\obsidian\session-journal\prompts\journal.prompt.md`.
- Deployed copy: `C:\Users\jonas-adam.pascua\AppData\Roaming\Code\User\prompts\journal.prompt.md`. `ai-preferences\deploy.ps1` copies it there, listed under `extra_prompts` in `ai-preferences\config.json`.
- Its project folder already has `README.md`, `map.md`, `sequence.md`, `config.json`, `changelog.md` and `state.json`. That is your manifest. A second one would duplicate `config.json`.

**Your "certified or elevated" question**
- There is no certified or elevated tier. Prompts and skills run with the same permissions as your chat session.
- A prompt can call anything in the toolkit by absolute path, as `/journal` does. This is allowed. Your rule 12 says the toolkit must run without files outside it, so keep the prompt source in the toolkit and deploy a copy.

`[case-against]` Each new command costs a file to deploy and maintain. Make one only for something you repeat weekly. A skill is better if the AI should pick it up on its own.

**Your actions:** **Pick one repeated copy/paste task and tell me its name.** Example: "`/standup` summarizes today's session logs."
**Next steps:** I can scaffold it with `new-tool.ps1`, or add it as a prompt under `ai-preferences` so `deploy.ps1` ships it.