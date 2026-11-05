["entity_parents"] -- empty tags; regex starts automatically
```bash
/^entity_parents:\s*$/m

# vs_code
^entity_parents:\s*\r?\n\s*-\s*\r?\n?
```

Why this specific pattern?
VS Code is very specific about line endings. Here is what each part does:

- ^entity_parents: : Matches the start of the line and the key name.
- \s* : Catches any invisible trailing spaces after the colon.
- \r?\n : Matches the newline character (the \r? handles both Windows and Mac/Linux line endings).
- \s*-\s* : Matches the indentation, the dash, and any trailing spaces on that next line.
- \r?\n? : Captures the final newline so that you don't leave a blank empty line in your file.