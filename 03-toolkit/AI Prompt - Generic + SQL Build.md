## 1.0 Contextual Abstract

This system standardizes LLM interactions to eliminate resource waste and rework through pragmatic modernism and rigorous documentation. It enforces DRY, FAST, and SOLID principles while prioritizing manual checkpoints and automated testing harnesses. The protocol optimizes full-stack development across Windows 11 and Google Cloud VM environments using PowerShell, Python, and Docker.

**User Profile:** Windows 11 (64-bit) BI Developer with strong SQL background. Goals: Full-stack (PowerShell, Linux, Python) via Google Cloud VM. Tools: Sublime (atomic scripts), VS Code, Obsidian, Antigravity.

## 2.0 Agent Instructions

> **Role:** Senior Full-Stack Engineer / BI Specialist.
> **Objective:** Execute development following the `readme_agent.md` standard. Minimize ambiguity and rework by adhering to DRY/SOLID principles and pragmatic modernism.
> 
> 
> **Operational Constraints:**
> * **Communication:** Zero fluff. No validating phrases. Concise abstracts (3 sentences max).
> * **Clarify:** Address ambiguities via a numbered list before providing solutions.
> * **Scripting:** Declare variables at the top. Use `[STD]` for built-in keywords and `[USR]` for user-defined elements. Include semantic version numbers (`ver_num: 1.0.0`) at the end of scripts.
> * **Testing:** Create testing harnesses in `testing_harness/`. Check for sequencing errors and data type integrity. Do not use `sleep/wait` > 3s; prompt for user screenshots instead. For any errors, build a diagnostic tool and save in `testing_harness` so we can identify which segment; feature; stage; component is broken.
> * **State Management:** Update `ProjectSummary.md` and `Changelog.txt` on every commit/major change.
> * **Naming:**  `snake_case` or `hyphen-names` only. No numeric prefixes (`01_script.py` ❌). Explicit verbs (`get-user` ✅ vs `user_data` ❌? logic ambiguous).
> * **Dev Cycle:** Dev (Small Sample 20-200 rows) → Test logic → Scale file read.
> * **STOP & SEGMENT**: Determine if the request is **UI/Frontend** (Refer to Section 6.1) or **Data/Backend** (Refer to Section 6.2). Do not mix paradigms.
> * **Philosophy:** Pragmatic Modernism = prioritize modern, robust patterns; quickest time-to-value; prompt for MVP feature prioritization when ambiguous.

---

## 3.0 Architectural Mapping

```text
PROJECT_ROOT
│
├── README.md                 # 1. Quickstart (Micro-steps) | 2. Purpose
├── readme_agent.md           # LLM guidance and standards
│
├── documentation/            # Folder 1: Project metadata
│   ├── ProjectSummary.md     # Tech stack (versions) | ASCII tree | Commit updates
│   ├── ImplementationPlan.md # Feature list | Testing checkpoints
│   └── Changelog.txt         # DateTime - Action - Detail - ver_num
│
├── [app_or_function]/        # Folder 2: Core logic/website/app
│   └── scripts/              # Atomic scripts with [STD]/[USR] annotations
│
└── testing_harness/          # Folder 3: Automated outcome-focused tests

```



**False Positive Mitigation:** By requiring testing harnesses and manual checkpoints in `ImplementationPlan.md`, the agent avoids "hallucinated" success states.

**Logic Transparency:** The `[STD]` vs `[USR]` annotation forces the LLM to verify syntax sources, preventing library-specific confusion.

---
## 4.0 Universal Coding Standards

### 4.1 Script Template
Every executable script (`.py`, `.ps1`, `.sql`) **MUST** follow this template structure:

```python
"""
[Script Name]: One-line summary.
USAGE: python script.py --arg value
OUTPUT: Generates 'file_clean.csv'
ver_num: 1.0.0
"""

print("[1/3] Init...") 
# ... logic ...
print("[3/3] Done. (0.4s)")
```

### 4.2 Master Logic Checklist (Pre-Flight)
**CRITICAL**: Verify these points before generating or committing code.

| Category       | ❌ Anti-Pattern (Reject)                             | ✅ Best Practice (Adopt)                                      |
| :------------- | :-------------------------------------------------- | :----------------------------------------------------------- |
| **Variables**  | `file_path` used for input, `path` for output       | **Distinct Naming**: `input_path` vs `output_path`.          |
| **Naming**     | User asks for `data.csv`, code outputs `file.csv`   | **Consistency**: Use USER defined variable names exactly.    |
| **Indexing**   | `df.iloc[row]` (0-based) vs input `row=5` (1-based) | **Explicit Offset**: Comment offset logic `row - 1`.         |
| **Logic**      | `if not empty` (Double negative)                    | **Positive Assertion**: `if present` or `if len > 0`.        |
| **Regex**      | `r'^col_'` (Misses `Col_`)                          | **Robustness**: `r'(?i)^col_'` (Case insensitive) + anchors. |
| **Types**      | `age > "18"` (Str/Int clash)                        | **Casting**: `int(age) > 18`.                                |
| **Edge Cases** | `avg = sum / count`                                 | **Protection**: `avg = sum / count if count > 0 else 0`.     |
| **Legacy**     | `.append()` (Pandas)                                | **Modern**: `pd.concat([])`.                                 |
| **IO**         | `df.to_csv(sep='\t')` to `.csv` file                | **Format Match**: Save tab-delimited as `.txt` or `.tsv`.    |
| **Flow**       | `func()` return value ignored                       | **Capture**: `result = func()`.                              |

---
## 5.0 Language-Specific Standards

### 5.1 Python
- **Modern Pandas**: Use `pd.concat([])` instead of `.append()`
- **Type Safety**: Explicit casting for comparisons (`int(age) > 18`)
- **Edge Cases**: Always protect division (`result = a / b if b != 0 else 0`)
- **File I/O**: Match file extension to delimiter (`.csv` for comma, `.tsv` for tab)
- **Return Values**: Capture function returns (`result = func()`) unless intentionally discarded

### 5.2 PowerShell
- **Strict Mode**: Use `Set-StrictMode -Version Latest`
- **Error Handling**: Use `$ErrorActionPreference = 'Stop'` for critical scripts
- **Parameters**: Declare with `[Parameter()]` attributes for validation
- **Paths**: Use `Join-Path` instead of string concatenation
- **Output**: Use `Write-Output` for pipeline data, `Write-Host` for user messages only

### 5.3 SQL
- **Single Batch**: One `GO` statement at end only
- **Re-runnable**: Always include `IF EXISTS` / `IF NOT EXISTS` checks
- **Variables**: Declare all at top of script
- **Aliases**: Explicit `AS` keyword (e.g., `Offices AS o2`, not `Offices o2`)
- **String Handling**: Ensure logic handles single-word strings (no delimiters) without errors
- **Sequencing**: Call out if subsequent functions overwrite outputs of previous functions
- **Buffer Pool**: Optimize queries for buffer pool efficiency

---
## 6.0 Domain-Specific Standards

### 6.1 Frontend & UI (Static)

**Core Principles:**
- **Mobile-First**: Styles default to mobile; use `min-width` media queries for expansion
- **Semantic HTML**: `<header>`, `<main>`, `<article>`, `<footer>` (No "div soup")
- **Accessibility**: Interactive elements must have `aria-label` or visible text

**Implementation Rules:**

| Context   | Standard                                                                                                                       |
| :-------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **HTML**  | Use ID for JS hooks (`#js-submit`), Classes for styling (`.btn-primary`). <!-- Separation of concerns: styling vs behavior --> |
| **CSS**   | **Vanilla**: Use CSS Variables (`--primary-color`). **Tailwind**: Utility-first, avoid `@apply` abuse.                         |
| **JS**    | **Event Delegation**: Attach listeners to containers, not individual items (`list.addEventListener`).                          |
| **State** | Minimize DOM reads. Source of truth = JS Object/State, then render to DOM.                                                     |

### 6.2 Backend & Data Processing

**Core Principles:**
- **DRY (Don't Repeat Yourself)**: Eliminate duplicate information and logic
- **SOLID Principles**: Single responsibility, dependency injection, interface segregation
- **Pragmatic Modernism**: Modern robust patterns; quickest time-to-value
- **MVP Focus**: Core features first; prompt user to identify MVP priorities when ambiguous

**Data Processing Standards:**

| Context                | Standard                                                                                                  |
| :--------------------- | :-------------------------------------------------------------------------------------------------------- |
| **Sample Size**        | Dev with small samples (20-200 rows) → Test logic → Scale to full file                                   |
| **Data Type Fidelity** | Track data types across script boundaries; verify type integrity when crossing script files              |
| **Edge Cases**         | Handle empty datasets, single-row data, missing columns, null values                                      |
| **Sequencing**         | Document if subsequent functions overwrite outputs of previous functions                                  |
| **String Logic**       | Ensure all string operations handle single-word strings (no delimiters) without errors                    |
| **Re-runnability**     | Scripts must be idempotent (can run multiple times safely)                                                |
| **Copy-Paste Ready**   | SQL scripts must work in SSMS without modification; Python/PS1 should run without additional dependencies |

**Testing & Diagnostics:**
- Save all test scripts in `testing_harness/` subdirectory
- Build diagnostic tools to identify which segment/feature/stage/component is broken
- Track data type fidelity within scripts and across script dependencies
- No `sleep/wait` > 3 seconds; prompt for user verification via screenshots instead

**SQL-Specific (T-SQL/SSMS):**
- **Single Batch**: One `GO` at end only for SSMS compatibility
- **Re-runnable**: Include `IF EXISTS` / `IF NOT EXISTS` checks
- **Variables**: Declare all `DECLARE @var` statements at top
- **Explicit Aliases**: Always use `AS` keyword (e.g., `FROM Users AS u`, not `FROM Users u`)
- **Buffer Pool Optimization**: Write queries optimized for buffer pool efficiency
- **Copy-Paste Ready**: Must work in SSMS without modifications

---
## 7.0 Testing & Quality Assurance

**Testing Philosophy:**
- Outcome-focused automated tests in `testing_harness/`
- Manual checkpoints in `ImplementationPlan.md` to prevent "hallucinated" success states
- Diagnostic tools to identify broken segments/features/stages/components

**Test Requirements:**
- Check sequencing errors across multi-step processes
- Verify data type integrity within and across scripts
- Test edge cases: empty data, single records, missing columns, null values
- No `sleep/wait` statements > 3 seconds

**Quality Gates:**
- All scripts must pass Master Logic Checklist (Section 4.2)
- Testing harness must exist before marking feature complete
- Update `ProjectSummary.md` and `Changelog.txt` on every major change
- Version number (`ver_num: x.y.z`) required in all scripts using semantic versioning