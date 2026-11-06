# Change KeyBindings
Preferences → Key Bindings → Default (Windows).sublime-keymap

```json
// changes so it's like VS Code vs ctrl+shift+(up/down)
[
	{ "keys": ["ctrl+o"], "command": "show_overlay", "args": {"overlay": "goto", "show_files": true} },
	{ "keys": ["ctrl+p"], "command": "show_overlay", "args": {"overlay": "command_palette"} },
	{ "keys": ["ctrl+shift+i"], "command": "select_lines", "args": {"forward": false} },
	{ "keys": ["ctrl+shift+m"], "command": "select_lines", "args": {"forward": true} },
	{ "keys": ["f10"], "command": "permute_lines", "args": {"operation": "unique"} }
]
```

Preferences → Package Settings → Logbook → Settings