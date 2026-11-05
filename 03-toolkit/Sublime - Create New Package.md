Sublime command integration
Design `golden test corpus`


Past the `.py` script
Add to JSON 
```
Context.sublime-menu
Default.sublime-commands
```

Transform the command


---
# Naming

In Sublime Text, the `"command"` string is **not** the class name. It’s the **Sublime command name** derived from the Python class name by:

- removing the trailing `Command`
- converting `CamelCase` → `snake_case`
- and (importantly) splitting acronyms like `TSql` into `t_sql`
- 
```python
class TSqlFormatterCommand(sublime_plugin.TextCommand):
```

```json
"command": "t_sql_formatter"
```

