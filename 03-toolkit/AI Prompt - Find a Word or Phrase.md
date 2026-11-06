
> Sharpen name candidates

**Task:** 
1. Summarize in a tight fashion to confirm we are aligned
2. Generate 3-5 names or phrases candidates that minimize semantic collisions and false equivalence. Outline the tradeoffs (upside/downside) as well including any collisions or conflicts if they were used. 
3. If generating table, prioritize by high fidelity desc, then high resonance desc (highest first)

**Tone:** Executive-facing. Keep first response concise, prompt me if I want more detail.
**Context:** Robust, modern, standard practice for data architecture and semantic modeling

---
### TERM (DEV): `distillation artifact` 
### CONCEPT: 
```
The concept is similar to a map/lookup/definition table. 

Once you're passing through data and need to pivot it into meaning, it goes through a definition table with true/false flags to define dimensions in the facts (eg which are qualified type codes?)

But it's not limited to tables, sometimes it's a multi step process involving procs. But I want to encapsulate the whole idea.
1. pass through table-set-1, create transient artifact L1 (eg normalizing different datasources, matching grains)
2. pass through table-set-2, create transient artifact L2 
3. pass through logic against adjacent rows (eg reference itself, to remove dupes, noise, apply exclusions, or transformations)
```

Related: [[Mechanism]]