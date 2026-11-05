# Additions, VS Code Layer
**Output:** 20260415_Summary.md
**Output-Location:** Root

```
Refine the content for executive consumption.

Goals:
- Eliminate ambiguity and semantic collisions.
- Distinguish business concepts that may appear similar but serve different purposes.
- Use precise, deterministic language.
- Avoid overloaded terminology, assumptions, and implementation-specific jargon unless necessary.
- Separate definitions, eligibility rules, status indicators, classifications, hierarchies, and metrics into distinct sections.
- Ensure terminology is consistent throughout the document.
- Highlight any concepts that could be confused with one another.
- Explicitly state what each attribute or concept represents and, equally important, what it does NOT represent.
- Surface potential historical reporting, governance, or analytical risks caused by incorrect interpretation.
- Optimize for executives, data consumers, analysts, and engineers reading the same document.
- Favor clarity over brevity when the two conflict.
- If you identify ambiguous terminology, recommend clearer alternatives.
- If business rules are implied but not stated, make them explicit.
- When appropriate, provide:
  - Executive summary
  - Business definition
  - Inclusion criteria
  - Exclusion criteria
  - Hierarchy or ownership model
  - Governance considerations
  - Common misconceptions
  - Data quality requirements

Writing Style:
- Executive-friendly
- Governance-grade
- Clinically precise
- Minimal jargon
- No marketing language
- No assumptions left implicit

Additional Instruction:
For every major concept, explicitly answer:
1. What is it?
2. Why does it exist?
3. How is it used?
4. What should it NOT be used for?
5. What are the risks if interpreted incorrectly?
```

# Supplemental

**Optional:** 
- To sharpen conceptual boundaries and delineators, feel free to use acid tests. 

> [!warning] Acid Test
> A measure has grain **X** if it is meaningful and stable when evaluated for **one instance of X without aggregation**. The value is **semantically complete, comparable, and interpretable** for **any single instance of X** at the evaluation time — _without hidden lifecycle context_.


---
**Concepts:**
```
git, azure, terraform, sql mesh, snowflake, atlan -- tooling we have for our data platform and pipeline project

highlighted areas that need to be downloaded to my mental model
- Git Monorepo vs Polyrepo
- Azure RM and how Terraform has no problem if thjat's the case
- Atlan and access precursors
	- private link vs public link to snowflake
	- azure vnet containers
	- private vs public endpoints
- infra directory on Azure
- infra vs intra vs extra
  
- **Partial pulls**: rate limits, timeouts, paging bugs, retries that stop early
- **Incremental drift**: watermark bugs, clock skew, updates arriving late
- **Duplication**: replay without idempotency, “at least once” delivery, merge key mistakes
- **Semantic mismatch**: grain confusion (line vs header), wrong join keys, missing dimensions
- **Source-side shape changes**: new enums, new fields, renamed fields, nullability changes
```

[^1]: Copied from [[AI Prompt - My User Profile - Tool Stack]]

