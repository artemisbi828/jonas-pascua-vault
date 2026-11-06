- singular: ~~contracts~~ --> contract
- ~~datetime~~ --> `datetime_local` or `datetime_utc`
- 


```examples
  _type
  _family
  _rule
  
  job_title
  job_title_family_access: specific, out of 3-5 columns, what they are
    #formalized --> decomposed (semantically distinct, more.tables)
    job_title_family_access_scope: machine/engine optimized (stacked, less.tables)
  
  _access_scope --> what the scopes are
  _access_policy --> relationship; better than _policy b/c it's specific
  _access_grant, _access_entitlement --> common in security, common in IAM/RBAC
  _access_assignment --> assume 1 default relationship
  _family, _domain --> parent category but shouldn't use category b/c overloaded
  _map, _group, _bucket --> kind of generic
  
  do-not-use: 
  _category, subcategory, category_group --> overloaded. everything becomes this
  _classification, _class --> although --> collides w OO programming, classification models, taxonomies
```

Due to cognitive load + fixed (vs extensible)

> 3-5 max.(soft-hard) columns --> #modeling/friendly

Formal, stable, ready to normalize/machine-optimize?

# Friendly Modeling
- m.columns: easy to read (max 5 for modal cognitive limit)
- 1.column, m.rows (dup bkeys): config, automation, extensibility

### Sample
```
rls__job_title_
rls__job_title_family_access_scope
```

**job_title_type**: different job titles
**job_title_family_access_scope**: relationship / link / bridge
- optimized for human readability. max 5 columns (fixed vs extensible)
# Optimized Modeling
job_title_type
**job_title_family** --> job titles that rollup to a cluster / group
**job_title_scope** --> unrestricted, team, clinic
**job_title_access_scope** --> rows


# Operator Rule 
```
Stable, named, business concepts | ≤5 stable concepts | audience-human
    → Columns

Open-ended, growing, configurable concepts | unknown future count | audience-engines
    → Rows
```