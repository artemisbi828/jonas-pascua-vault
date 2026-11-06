

## Reserved Properties (Built-in Behavior)

**`tags`** → Shows in tag pane, clickable, auto-complete, searchable  
**`aliases`** → Appears in `[[` suggestions, creates alternative file names  
**`cssclass`** → Applies CSS styling to the note  
**`publish`** → Controls Obsidian Publish visibility

## Why `tags` Behaves Differently

When you write `tags: [domain/clinical]`, Obsidian's code has `if (key === 'tags')` logic that:

- Registers tags in the tag index
- Updates tag pane UI
- Makes them clickable
- Enables `tag:#domain/clinical` search

When you write `domain: clinical` (arbitrary property):

- Just stored as metadata
- No special UI behavior
- Only queryable via DataView

## Plugin Properties

Some plugins register their own: `created`, `due`, `kanban-plugin`, etc. They only work if the plugin is active.

## Arbitrary Properties

Everything else (`database`, `object_type`, `row_count`) is custom metadata with **no built-in behavior**. You can:

- ✅ Query in DataView
- ✅ Display in Properties panel
- ✅ Search via `[property:value]`
- ❌ No auto-complete, clickable links, or UI integration

## Naming Matters ONLY for Reserved Properties

```
tags: [test]      # ✅ Works - shows in tag pane
mytags: [test]    # ❌ Doesn't work - just metadata

database: CentralC9   # ✅ Fine - arbitrary property
db: CentralC9         # ✅ Also fine - but pick ONE convention
```

**Best practice:** Use reserved properties (`tags`, `aliases`) for their native UI benefits. Use arbitrary properties for custom structured data. Don't try to reinvent `tags` as `categories` or `mytags`.