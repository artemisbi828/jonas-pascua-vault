What core.autocrlf false does
Windows and Mac/Linux end each line of text differently:

Windows uses two hidden characters, CRLF (\r\n).
Mac and Linux use one, LF (\n).
autocrlf controls whether git converts between them when saving files into history and writing them back out.

Setting	Behavior
true (default on Windows)	Converts CRLF → LF when saving to history, and LF → CRLF when writing files back out
false	Stores and restores every file exactly as it is
Why false suits this vault:

No phantom changes. Obsidian, VS Code, and notes pasted from SSMS or Sublime mix both styles. With conversion on, git can report files as "changed" when only invisible line endings differ. That would clutter the diffs you want for reviewing AI edits.
Identical copies. A copy moved to another laptop matches the original byte for byte.
No surprises with the zip. Files restored from your snapshot or from git are the same bytes.
The tradeoff: if another tool later rewrites every line ending, git will show the whole file as changed. Git offers git diff --ignore-cr-at-eol to hide those differences if it happens.