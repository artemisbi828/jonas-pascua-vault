```
insert taxonomy, Measure (Agg: Count, Sum, Avg | Ratio), Tables, Columns, Intent, Benchmark below. validate for correctness, keep it TLDR EIL5, high fidelity  
  
at the end include learning-oriented comments or check for possible misconcepts of mental model
```


generate sharper names

too generic, doesn’t imply finality. not deterministic.

Got it - you want to **anchor your internal stack**.
anchor this to my unified conceptual stack
Your conceptual framing maps **cleanly and precisely**:
- Where your A‑Stack Fits Inside B
- Validation checklist - *Is this ontological?* 
visually and cognitively separates “rules and calculations” from:
Utility Trade-Off Framework
*concise, copy‑pasteable onboarding + SLA template*

**high-fidelity request template**; include a section with **learning-oriented comments**. 

Perfect — here is a **concise, readable, and atomic plan** focused strictly on **what to add / adjust** in `concept_register` and `metric`, in **Markdown-first form**, with **explicit decisions called out only where required**.

No prose bloat. No theory recap. Just clean structure.

**tightened, executive‑ready rewrite** 

---

Create a reusable idempotent prompt with high-fidelity reruns:
I want to see recursive traversal, hierarchal recursion
Last conceptual fork before execution and delivery of target-output

I am trying to understand these different concepts: edge vs relationship vs cardinality.

Please provide 
1. core differentiators between concepts
2. synonyms, misnomers, pitfalls. 
3. ASCII Trees especially when outlining hierarchal vs orthogonal relationships

FIRST: Explain ideas and concepts
SECOND: Create tight definitions and utilization plan. Prompt me w challenges where trade-offs matter and outline the trade-offs.

Let me know when we are at the last conceptual fork and decisions are locked before executive and delivery of target-output.


You are “Data Catalog Definition Editor,” an expert technical writer and data architect for analytics platforms.

PRIMARY GOAL
Rewrite rough, inconsistent, or narrative database/table/column descriptions into concise, high-fidelity, operational definitions that are consistent, reusable, and helpful for onboarding and governance.

OUTPUT CHARACTERISTICS (non-negotiable)
- Concise: typically 1–2 sentences per object (max 35 words unless justified).
- High fidelity: preserve all factual content; do not invent facts.
- Operational: describe role, purpose, and key caveats (not origin stories).
- Consistent voice: neutral, authoritative, present tense.
- Tool-friendly: avoid ambiguity, hedge words, and conversational asides.
- Safe assumptions: if something is unknown, label it explicitly as “unclear” and propose a targeted follow-up question.

MENTAL MODEL (apply to each item)
Answer these in order:
1) What kind of thing is this? (warehouse / landing / mirror / staging / sandbox / canonical reference / semantic layer / legacy)
2) What is its purpose / role in the ecosystem?
3) What caveat(s) matter? (cadence, ownership, legacy dependencies, scope boundaries, performance, sensitivity)

STYLE RULES
- Prefer system verbs over story verbs:
  - “managed by” > “created by”
  - “used for” / “exists to” > “used to”
  - “ingests / lands / mirrors / stages / curates” > “takes data from”
- Replace vague adjectives with precise role labels:
  - “main” → “core” or “primary curated”
  - “shared” → “shared, team-owned” (and name the team if provided)
- Keep examples optional and parenthetical, max 1 short example clause (e.g., “e.g., sd.Employees”).
- Use consistent formatting for schemas/objects (backticks).
- Do not use spaces or Title Case as identifier names; those belong to UI labels, not physical names.

INPUTS YOU MAY RECEIVE
- A table (database_name, sort_order, description) or a list of objects.
- Additional context about schemas, tool stack (Snowflake, SQL Server, dbt, Power BI), ownership, and refresh cadence.

REQUIRED OUTPUTS
Return:
A) Refined definitions: same rows, updated descriptions.
B) Rationale: bullet list of the top changes and why they improve robustness.
C) Follow-ups: a minimal set of clarifying questions only where needed.

DO NOT
- Do not add new facts.
- Do not remove critical caveats.
- Do not overstuff with examples.
- Do not change naming (database_name) unless asked.

QUALITY CHECK (run before responding)
For each refined description, verify:
- It includes role + purpose + caveat (if applicable).
- No invented facts.
- ≤ 35 words (unless an exception is justified).
- Avoids: “main,” “some,” “stuff,” “things,” “unknown” (use “unclear” + question).
``
---

---
y 
**Structure:** Use Architectural Mapping (ASCII code block) to clearly detail hierarchal and orthogonal edges. Obsidian-optimized Markdown

---
# Description / Marketing Tones
**direct, high-competence** tone. It positions Artemis not just as a "dev shop," but as a strategic partner that cares about operational efficiency.

---
**User Profile:** Windows 11 (64-bit) BI Developer with strong SQL background. Goals: Full-stack (PowerShell, Linux, Python) via Google Cloud VM. Tools: Sublime (atomic scripts), VS Code, Obsidian, Antigravity.


# Final Naming
snake_casing; lowercase, use underscores instead of spaces

# Concept Breakdown
## Bearer Tokens
> [!info] Analogy: The Valet Key
> 
> A bearer token is like a valet key. The car (Resource) doesn't care who you are; it only cares that you possess the key.

**Payload Properties:**
    - **Scope** → What are you allowed to do? (Read vs. Write)
    - **Lifetime** → TTL (Time-to-Live); prevents indefinite access if leaked.
    - **Claims** → Encoded data (UserID, Roles) to bypass DB validation hits.

```
Authentication Flow
├── 1. Identity Verification (Who are you?)
│   └── Result: Identity Confirmed
└── 2. Token Issuance (What can you do?)
    ├── Scope → Access Level
    ├── Lifetime → Expiry
    └── Bearer Token → "The Key"
```

> [!tip] SQL Developer Pivot
> 
> Think of a Bearer Token as a Temporary View with strict WHERE clauses (Scopes) and an EXPIRE trigger. It prevents the need to run an EXISTS check on the Users table for every single API request.

## 📋 File Naming Conventions

### General Rules
- **All lowercase**: All filenames should use lowercase letters only
  - ✅ `readme.md`, `readme.txt`
  - ❌ `README.md`, `README.txt`, `ReadMe.md`
  
- **Underscores for spaces**: Use underscores instead of spaces
  - ✅ `my_script.py`, `data_processor.ps1`
  - ❌ `my script.py`, `data processor.ps1`

- **No numeric prefixes**: Remove prefixes like `00_`, `01_`, `02_`
  - ✅ `setup.py`, `config.ps1`
  - ❌ `00_setup.py`, `01_config.ps1`

---
# Business Logic Definition
Prompt
> [!info] Business Logic Documentation
> I need to deeply understand the business logic of [METRIC/CALCULATION NAME].
> 
> CONTEXT:
> - Business purpose: [What decision does this drive?]
> - Current understanding: [Your hypothesis about what it does]
> - Specific confusion: [The exact temporal/logical aspect you're unsure about]
> 
> CODE: [Paste full code including all nested functions]
> 
> REQUIREMENTS:
> 1. **Explanation Depth**: Don't just describe the code syntax. Explain:
>    - The business intent behind each condition
>    - How temporal windows work (inclusive/exclusive boundaries)
>    - Edge cases and tie-breakers
>    - What happens to related records (does past data change retroactively?)
> 
> 2. **Temporal Scenarios**: For time-based logic, provide:
>    - Concrete examples with specific dates/times
>    - Boundary condition behavior (Day 30 vs Day 31)
>    - Whether calculations are point-in-time or retroactive
> 
> 3. **Test Case Generation**: Provide:
>    - SQL queries to find real-world examples for each scenario
>    - Expected outcomes for each test case
>    - Validation queries to confirm the logic is working correctly
> 
> 4. **Edge Cases**: Identify:
>    - Tie-breaker logic (e.g., same datetime, what's the sort order?)
>    - Null handling
>    - Cascading effects (does changing one record affect others?)
> 
> SPECIFIC QUESTIONS:
> - [Your specific question, e.g., "If appointment.a is on Day 1 and appointment.b is on Day 31, are both IsNetAdded = 1?"]

# LLM Choice
```
Stick with Claude 3.7 Sonnet for this type of task. It excels at:

Multi-step logical reasoning
SQL generation with proper syntax
Business context translation
Temporal/sequential logic
Comprehensive test coverage thinking

Only switch to o1 (if available) if you need even deeper reasoning on extremely complex nested logic or mathematical proofs.

GPT-4o → more creative w SQL
```

---
# AI LLM Models
Based on the expanded list in your screenshot (which reflects a future/hypothetical model landscape circa late 2025), here is a concise dictionary of **Name: Use-When**.

### **The "Daily Drivers" (Start Here)**

- **Auto**: You don't want to choose; lets the system pick the model based on task complexity.
- **Claude Sonnet 4.5**: **The Default.** Best balance of human-like reasoning, idiomatic code, and speed. Use for 90% of tasks.
- **Claude Sonnet 4**: Budget fallback. Use only if 4.5 is hitting rate limits or costing too much.
    

### **The "Heavy Lifters" (Reasoning & Architecture)**

- **Claude Opus 4.5 (Preview)**: Deepest thinker. Use for high-level system design, complex architectural decisions, or nuanced writing where speed doesn't matter.
- **GPT-5**: Raw logical power. Use for complex algorithm implementation, math-heavy logic, or when Sonnet is being too "creative" and you need rigid adherence.
- **GPT-5.1 (Preview)**: Refined flagship. Use for edge-case debugging where GPT-5 fails; likely smarter but potentially less stable.
- **GPT-5.2 (Preview)**: Bleeding edge. Use for experimental tasks or solving problems no other model can (expect bugs).
    

### **The "Specialists" (Coding & Context)**

- **Gemini 3 Pro (Preview)**: Context King. Use when you need to feed in **massive** amounts of documentation or entire repositories (e.g., "how does this whole library work?").
- **GPT-5-Codex (Preview)**: Code specialist. Use for generating boilerplate or strict syntax in obscure languages.
- **GPT-5.1-Codex (Preview)**: Updated code specialist. Use for standard function generation.
- **GPT-5.1-Codex-Max (Preview)**: Heavyweight coder. Use for massive refactors (e.g., "Migrate this entire class from React to Vue") where precision across many lines is vital.
- **Raptor mini (Preview)**: Edit specialist. Likely fine-tuned for applying code changes (diffs). Use for "Apply to file" actions rather than chat.
    

### **The "Speedsters" (Quick Tasks)**

- **Claude Haiku 4.5**: Fast & cheap. Use for summarizing long text files, documentation lookups, or simple string manipulation.
- **Grok Code Fast 1**: Ultra-low latency. Use for quick regex, shell commands, or one-line syntax checks.
- **GPT-5 mini / GPT-5.1-Codex-Mini**: Economy class. Use for writing simple unit tests or quick scripts where "smart enough" is acceptable.
    

### **Legacy / Fallback**

- **GPT-4o / GPT-4.1 / Gemini 2.5**: Previous generation. Use only if the newer models are down or exhibiting regressions.