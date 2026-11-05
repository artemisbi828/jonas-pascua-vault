# Idempotent
**Idempotent:** same input → same expected output

Idempotent: run the same thing, get the same thing every time 
- or different due to changes in mapping 
- **get the same expected logic outputs every time**

# Overfitting

**Overfitting:** framework over-fitted to one sample and is under-generalized (does not apply to adjacent use cases in the same cluster). (aka: *case-specific patching*)
**Config Drift:** script has hard coded behavior not fully governed by config.
**Style Inconsistency:** across query scopes

> [!Info] Solution
> refactor so it is strictly controlled by config keys to be both consistent and easier to reason (reducing cognitive load)
