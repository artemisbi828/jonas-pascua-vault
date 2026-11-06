
```
PRIMARY:
legacy-state       = system being retired
current-state      = authoritative production state right now
transition-state   = temporary coexistence / migration state
target-state       = intended end state

ALTERNATIVE:
as-is-state        = incumbent (becommes retired)
transition-state
to-be-state        = successor (becomes active)
```


# Transition State
```
BEFORE
Current State ──────────────────► Target State

DURING MIGRATION
Legacy State ──┐
               ├──► Transition State ──► Target State
Target State ──┘

AFTER CUTOVER
Old Current  ──► Legacy State
Old Target   ──► Current State

--- ===================================================
incumbent  →  transition  →  successor
    │                           │
    │         CUTOVER           │
    └──────────────► retired    └──► active
```