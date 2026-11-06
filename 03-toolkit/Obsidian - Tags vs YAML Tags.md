**YAML Tags:** **Use YAML tags for permanent classification.** 
**Inline Tags:** Temporary states (`#quick-paste-merge-later`, `#status/todo`).

---
### Inline Tags (in content)
```markdown
This is a workflow tag #status/active for tracking progress.
I use #quick-paste-merge-later when I need to digest content.
```

**Pros:** Quick to type, visible in content, searchable  
**Cons:** Mixed with narrative, not structured, harder to bulk-edit

### YAML Tags (in frontmatter)
```yaml
---
tags:
  - status/active
  - domain/clinical
  - content-type/concept
---
```

**Pros:** Structured, DataView-queryable, cleanly separated from content  
**Cons:** Requires YAML block, not visible when reading content

---
## Recommended Tag Taxonomy for Your Vault
```yaml
---
tags:
  - content-type/concept
  - domain/technical/databases
  - tool/nosql
  - learning-stage/active
---
```

Based on your workspace, here's a **3-layer hierarchy**:

```yaml
tags:
  # Layer 1: Content Type (what IS this?)
  - content-type/concept        # Explanatory notes
  - content-type/reference      # Quick lookup
  - content-type/script         # Executable code
  - content-type/moc            # Map of Content
  
  # Layer 2: Domain (what's it ABOUT?)
  - domain/clinical             # Patients, Appointments
  - domain/business             # Contracts, Financials
  - domain/technical            # Servers, Infrastructure
  - domain/methodology          # SOLID, DRY, naming
  
  # Layer 3: Tool/Technology (what USES this?)
  - tool/sql
  - tool/powershell
  - tool/git
  - tool/python
  - tool/dax
  
  # Layer 4: Status (workflow state)
  - status/active               # Currently working
  - status/todo                 # Queued
  - status/archived             # No longer relevant
```

**Note:** Your existing `#quick-paste-merge-later` is a workflow tag—keep it inline, not in YAML (temporary state).



## When NOT to Use Tags

❌ **Don't tag things already implicit in file structure**

**Bad:**
```yaml
# File: 03 - Dictionary/Patient.md
tags:
  - dictionary  # Redundant! It's already in Dictionary folder
```

**Good:**
```yaml
# File: 03 - Dictionary/Patient.md
tags:
  - domain/clinical  # Cross-cutting, not implied by location
```

❌ **Don't use tags for unique identifiers**

**Bad:**
```yaml
tags:
  - patient-id-12345  # This is data, not a category
```

**Good:**
```yaml
patient_id: 12345  # Use YAML property instead
```

❌ **Don't use tags for relationships**

**Bad:**
```yaml
tags:
  - related-to-appointments  # Use links instead
```

**Good:**
```yaml
related_concepts: [Appointments]  # Explicit link
```
