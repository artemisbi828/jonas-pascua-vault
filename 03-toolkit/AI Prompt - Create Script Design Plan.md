related-to: [[Mechanism - Idempotent vs Overfitting]]

**Role:** Senior analytics systems architect with deep experience in healthcare PMS/ERP platforms, semantic modeling, and executive-facing data governance. Specialized in SQL and python automation.


#status/deferred/quick-paste-merge-later 
```
Feasibility summary:
- Sublime command integration: High feasibility.
- JSON-driven style application: Medium-high feasibility for many rules, medium for advanced alignment/collapse behavior.
- sqlglot dialect normalization (mssql <-> snowflake): Medium feasibility, with potential lossy rewrites and parser edge cases on mixed-dialect input.

Golden test corpus:
- At least 10-20 input/output SQL snapshots
Include long CASE, joins, CTEs, DDL, variables, comments

```


# Walk Through
1. Define **intent** | vision
	- inputs --> outputs
2. CONTEXT 
3. EXTEND CASES
4. best practice + why
5. distinction

INTENT → CONTEXT → EXTEND → REUSABLE TOOL

1. what I want (intent for specific use case)
2. what I'm missing? scope boundaries beyond isolated happy path? 
3. scope expansion -- make this a reusable tool
	1. how extensible? consider other environments?


**Compact Version**
```
    Break this code into strict execution steps in ELI5 language.
    Honor true order of operations.
    Explain boundary logic and anchor constants.
    Output a paste‑ready comment block.
```

**Sequential ELI5 Code Decomposition**

```
Act as a senior systems engineer and teacher.

Take the following code and explain it in strict sequential execution order,
respecting actual order of operations (not conceptual intent).

Requirements:
- Explain ONLY what the code does, step by step
- Use ELI5 language, but remain technically precise
- Number each step
- Explicitly explain:
  - Anchor values (e.g., date 0, magic constants)
  - Why offsets are applied (e.g., +1 day, -1 week)
  - Inclusive vs exclusive boundary logic
- Do NOT summarize or skip steps
- Do NOT use metaphors
- Assume the reader understands SQL syntax but not evaluation mechanics

Then, produce a cleaned comment block that could be pasted directly above the code.
```


**Pivot Used**
*   **Declarative interpretation** (what SQL *means*)
    to:
*   **Evaluative interpretation** (how SQL is *resolved*)

Most explanations fail because they mix the two.

This prompt **forces**:

*   Temporal sequencing
*   Mechanical thinking
*   Boundary correctness (which is where most bugs live)

***

## 5️⃣ One‑sentence mental model (to remember)

> Good technical comments explain *how the computer walks the code*, not what the author **hoped it meant**.

---


I confirmed a difference exists, but it appears to be whitespace-level; I’ll run a byte/line hash check so we can state exactly how they differ before coding.

```
Feasibility summary:
- Sublime command integration: High feasibility.
- JSON-driven style application: Medium-high feasibility for many rules, medium for advanced alignment/collapse behavior.
- sqlglot dialect normalization (mssql <-> snowflake): Medium feasibility, with potential lossy rewrites and parser edge cases on mixed-dialect input.

Golden test corpus:
- At least 10-20 input/output SQL snapshots
- Include long CASE, joins, CTEs, DDL, variables, comments
```

---


## Requirements
1. SINGLE BATCH (one GO at end only)
2. Re-runnable (IF EXISTS checks)
3. Copy-paste ready for SSMS
4. All variables declared at top
5. Ensure that any string logic handles single-word string (no delimiters) without throwing an error. 
6. Call out if sequencing of subsequent functions overwrite over any outputs of prevous functions
7. Ensure all aliases have an "as" (egg SmileDoctorsODS.sd.Offices o2 → SmileDoctorsODS.sd.Offices as o2)

## Optimizations
Optimize for buffer pool.

## Testing-Artifcats
save scripts for diagnostic and testing all in a root.subdir == "testing-artifacts"
- any files contains text "test" move to subdir
- build a diagnostic tool so that for any error -- we can easily identify which segment; feature; stage; component is broken
- be especially mindful of data type fidelity within the script file and as it crosses (used as dependency) script files

---


# Create Design Plan 
- make it atomic and in segments (easier to debug, less overhead when atomic) -- don't wait for large chunks! break it up when designing process sequence. (eg expensa: loads and creates objects then processes images and fills in fields)

**Task:** 
- nightly automated tool (function/procedure/job) that **enforces semantic guardrails and performs corrective normalization on operational records** where **human non‑compliance introduces false negative or distorted measures** in analytical outputs.

**Problem Context:** 
- Attached reference filedir or files

```
wait: 
  write PMO write up → "As a, I want, so that"
  define mvp + current state → target state → validation (acceptance criteria)
  define deadline (segmented milestones)
  chunk-out mvp;   bonus-points register 
  design approach vector
     define objects
     define test harness: 
     input --> output; 
     define sample micro; sample L2; sample L3
     define expected input --> output
     define limits: loops or recursions (3)
     define modality | solution framework
     define config vars
     define validation framework (pass, fail) - sumchk
     define pitfalls
tests (n): 
   log results: record time
   refinement: define changes
      error correction
      approach divergence
```

**Requirements:** 
- Signal **semantic correction, governance, or reconciliation** (not “cleanup” or “scrub”).
- Be **system‑agnostic** to reduce cross‑platform or vendor collision.
- Be credible at the **executive, finance, and analytics governance** layer.
- Sound appropriate for:
    - a scheduled job
    - a database procedure
    - or a data platform control plane capability
- Avoid casual, legacy, or manually connoted terms (e.g., _fix_, _repair_, _cleanup_).
- Prefer terms aligned with **analytics integrity, financial correctness, and semantic enforcement**.

[Learning - AI Prompt - Script Design]

---
### Standardize Project Folder
1. generate standard files and folders
	- `<root>\ingredients.txt`
	- `<root>\changelog.txt`
	- `<root>\test-scripts`
	- `<root>\inputs
	- `<root>\outputs
	- `<root>\documentation
2. if not exists, create readme.txt that outlines:
	- quickstart: how to use or call the script (including init of venv if necessary, skip if basic py script)
	- expected mutation from input → output
	- ingredients ascii tree for learning
3. if not exists, generate changelog.txt to outline:
	- changes we implemented in this session
	- separate and log test-scripts into the test-scripts sub-dir
4. run the script and create an output in the standard fileformat so I can verify the output
```
out-filepath-name:
- format: YYYYMMDD_iteration_NN.tsv
- YYYYMMDD = execution date (local system date at script start)
- NN = zero-padded, monotonically increasing run index for that date,
       auto-incremented based on existing files in the output directory
```


2026-03-23 09:26 PM
```
I found the workspace is minimal, so I’m going to make one structural improvement first: add a reusable pure-Python entry point in the formatter so it can be executed outside Sublime, then scaffold the standard folders/files around it.

I’m implementing schema inference exactly as you described: infer each column datatype from the best representative row (first row with zero nulls, else row with fewest nulls), then format every row using that inferred type map with null fill/padding.

I’ll make two concrete updates now: switch schema inference to start from row 2 (when present) so headers don’t drive type/width inference, and update the test output filename logic to the new from_input pattern; then I’ll run both back-tests and log everything in changelog.
```

--- 

6. put high level instructions and prompt for tech stack, description and tradeoffs
7. generate standard files and folders
	- `<root>\ingredients.txt`
	- `<root>\changelog.txt`
	- `<root>\test-scripts`
	- `<root>\outputs
	- `<root>\documentation
8. dev-iteratively
	- small sample from population
	- edge cases noted
9. pause project and wait for next use-case
	- decide if next use-case uses same script or new script (usually new script)


```
As a:: Data Architect and Python Automation Expert
	I want:: to build a `pdf extract-table tool`
	so that:: I can efficiently extract table objects out of pdf files.

new-script: 
- filename: pdf_table_scraper
- filetype: undetermined

input-parameters: 
- in-filepath: `C:\vsWorkspace_SD\4 - builds\extract_pdf\20260312_Metric list DRAFT 151.pdf`
- out-filetype: `csv`
- out-filepath: `<root>\outputs`

out-filepath-name:
- format: YYYYMMDD_iteration_NN.tsv
- YYYYMMDD = execution date (local system date at script start)
- NN = zero-padded, monotonically increasing run index for that date,
       auto-incremented based on existing files in the output directory

expected-output (validation target - script must fail if unmet):

---
**GENERATE STANDARD OUTPUTS:** 
- `<root>\ingredients.txt`: ascii tree of tools w versions and concise description of what the tools is doing w strict fail-fast validation
- `<root>\ingredients.toml`: actual ingredients list for project use.
- `<root>\changelog.txt`
- `<root>\outputs
  
**SCRIPT GENERATION PHILOSOPHY:** 
- abide by SOLID/DRY, FAST (don't repeat yourself, eliminate duplicate info)
- abide by Pragmatic Modernism, Modern Robustness, Sustainable Design; High-Integrity Architecture
- go for core features and quickest time-to-value; 
- if there is any ambiguity -- prompt user (eg to identify which is core for MVP (minimum-viable-product))
- use venv whenever possible.
- add concise comment block at the top of the script as a quickstart w simple concrete steps on `how-to-use` and including initialization of venv from vsCode.

**SCRIPT REFINEMENT STANDARDS**
For every iteration and error 
- → log to `changelog.txt` :: timestamp | error | current-value
- after resolving error → log to log to `changelog.txt` :: timestamp | fix (technique applied) | `before-value` → `after-value` | `code-before` → `code-after` (include line numbers)
  
---
**INSTRUCTIONS:**
1. **Clarify:** Address conflicts and/or ambiguities via a numbered list before providing solutions. 
2. generate standard outputs
3. generate script w standards
4. run a small sample as a fast test-iteration 
	   → generate output 
	   → generate changelog.txt entries as errors occur and are fixed. 
5. refine and prompt me for feedback or any clarification
```

# Table Extraction
Refined
```
### Refined VS Code Prompt (Vision-to-Reasoning Hybrid)

As a:: Data Architect and Python Automation Expert
	I want:: to build a `pdf extract-table tool`
	so that:: I can efficiently extract table objects out of pdf files.

new-script: 
- filename: pdf_table_scraper
- filetype: undetermined

input-parameters: 
- in-filepath: `C:\vsWorkspace_SD\4 - builds\extract_pdf\20260312_Metric list DRAFT 151.pdf`
- out-filetype: `csv`
- out-filepath: `<root>\outputs`

out-filepath-name:
- format: YYYYMMDD_iteration_NN.tsv
- YYYYMMDD = execution date (local system date at script start)
- NN = zero-padded, monotonically increasing run index for that date,
       auto-incremented based on existing files in the output directory

expected-output (validation target - script must fail if unmet):
- normalize columns to exact schema (order enforced)
- convert column headers to lower_snake_case `Metric/measure → metric_measure`, 'BCG refined → bcg_refined'
  
id | metric_measure | bcg_refined_definition | refined_calculation | owner | bcg_sorting |
| --- | ---| ---| --- | --- | ---| --- |
| 1 | 1 | NPE added | New patient exam appointment created for the first time | Unique NPE added for a unique patient within a time period | Jon (CMSO) | 1: Senior Leadership |
| 24 | 24 | Cost to collect | Cost associated with billing, payment processing, financial counseling, follow-up, and dispute resolution | Collections Operations Cost ÷ Cash Collected | David (COO) | 1: Senior Leadership |
| 150 |  | Initial investment amount |  |  |  |  |
| 151 |  | Non-PIF down payment percentage | Percentage of the non-PIF (Paid in Full) contract  values at the time of contract signing  | Non-PIF down payments/non-PIF contract payments  | David (COO)  | : Delivery |
| 152 |  | Initial investment amount  | Total investment amount can additionally be defined as total dollars collected at the start for all contract starts  | Total initial investment amount (Down payment) including those who have paid in full for all contract starts  | David (COO) | 2: Management |

additional-validation-guidance
- expected-row-count: 152 (exclude header)
- extraction-start-page: 3
- extraction-end-page: 17
  
sanitization: 
	- normalize punctuation
	- split into lines
	- trim leading/trailing spaces on each line
	- remove blank lines (lines that become empty after trim)
	- join remaining lines with a single space or newline? use single space to keep single-line cells
	- final trim

 failure handling: if read/parse throws → skip row
	- if notes is empty after sanitization → skip row

```



```
**The Strategy: Hybrid "Spine & Muscle" Extraction**
1. **The Spine:** Use `PyMuPDF` (fitz) to identify "ID" markers (1 through 150+) to act as row anchors.
2. **The Muscle:** Use `Docling` or `Marker` to convert the PDF to Markdown, then use a regex-based "Chunker" to group all text between ID markers into single records.
3. **The Brain:** Implement a cleaning pipeline that joins multi-line strings with a single space to maintain valid TSV formatting.

**Technical Specifications:**
* **Runtime:** Python 3.11+
* **Core Libraries:** `docling` (for high-fidelity MD conversion), `pandas` (for schema enforcement), `pathlib`, `re`.
* **Inputs:** `C:\vsWorkspace_SD\4 - builds\extract_pdf\20260312_Metric list DRAFT 151.pdf`
* **Outputs:** `<root>\outputs\YYYYMMDD_iteration_NN.tsv`
* **Schema (Lower Snake Case):** `id`, `metric_measure`, `bcg_refined_definition`, `refined_calculation`, `owner`, `bcg_sorting`.

**Instructions:**
1.  Structure the code into a `PDFProcessor` class.
2.  Use `pathlib` for all file operations.
3.  Implement a `check_schema()` method that enforces column order and naming.
```



---
**CRITICAL**: Verify these points before generating or committing code.
Every executable script (`.py`, `.ps1`) **MUST** generally strictly follow this template structure:

```python
"""
[Script Name]: One-line summary.
USAGE: python script.py --arg value
OUTPUT: Generates 'file_clean.csv'
"""

print("[1/3] Init...") 
# ... logic ...
print("[3/3] Done. (0.4s)")
```

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



# Previous Iterations

```
As a:: Data Architect and Full Stack Developer
	I want:: to build a power shell script
	so that:: I can efficiently extract obsidian keyword-definition sets out of markdown filename-content files.

output-script: extract_obsidian_definitions.ps1

input-parameters: 
- in-filepath: `C:\obsidian\Artemis-Hub`
- out-filepath: `C:\vsWorkspace_SD\2 - ps_dir_accelerators\ps-scripts\outputs`
- output-filetype: `tsv`


file-loop-selection:
- select-only-files: matching `*.md`
- filepath-or-file\recurse: `undefined → no → only top-level folder`
- filepath-or-file\hidden: `undefined → no → skip hidden files and filepaths`


standard-script-guidance:
- add comment block at top of script: quickstart on `how-to-use`
- sanitization: split into lines; trim leading/trailing spaces on each line; remove blank lines (lines that become empty after trim); join remaining lines with a single space or newline? use single space to keep single-line cells; final trim;
- failure handling: if read/parse throws → skip row; if notes is empty after sanitization → skip row;


---
# TEST CASE 1
input-test-case: 
- in-filepath: `C:\obsidian\Artemis-Hub`
- out-filepath: `C:\vsWorkspace_SD\2 - ps_dir_accelerators\ps-scripts\outputs`

output-expected:
- `file_name`::  `Entra ID (OIDC) via MSAL`
- `notes`::  `Microsoft Entra ID provides OpenID Connect authentication. MSAL handles sign‑in, tokens, refresh, SSO, and calling Microsoft APIs securely from your app.`

additional-validation-rules:
- exceptions: remove yaml blocks defined as: 
	- start delimiter line: 
	- end delimiter line: 
	- remove all such blocks (not just front matter), where delimiters must be on their own line
```

---

# Example 2

**Task:** Build a PowerShell `.ps1` script to extract a 2-column TSV (`file_name`, `notes`) from Markdown files in a specified folder.

### Inputs

*   `-RootPath` (mandatory): full folder path (example: `C:\obsidian\Artemis-Hub`)
*   `-Recurse` (optional switch): subfolders = `do not include`
*   `-OutFile` (optional): TSV output path; default to `<RootPath>\extracted_notes.tsv`

### File selection

*   Process only files matching `*.md`
*   If `-Recurse` is set, scan recursively; otherwise only the top-level folder
*   Skip hidden/system directories (optional but recommended)

### Parsing / transformations per file

1.  Read entire file as text.
2.  Remove YAML blocks defined as:
    *   Start delimiter line: `^\s*---\s*$`
    *   End delimiter line: `^\s*---\s*$`
    *   Remove **all** such blocks (not just front matter), where delimiters must be on their own line.
3.  Convert remaining content to **plain text**:
    *   Remove/convert Markdown syntax to readable text:
        *   Strip emphasis markers (`*`, `_`), inline code backticks
        *   Convert links `url` → `text`
        *   Drop images `url` → `alt` (or empty if no alt)
        *   Remove heading markers (`#`), blockquotes (`>`), list markers (`-`, `*`, `1.`) while keeping text
        *   Remove horizontal rules that are delimiter lines already handled
4.  Sanitize notes:
    *   Split into lines
    *   Trim leading/trailing spaces on each line
    *   Remove blank lines (lines that become empty after trim)
    *   Join remaining lines with a single space **or** newline? **Use single space** to keep TSV single-line cells.
    *   Final trim
5.  Set:
    *   `file_name` = file name without extension
    *   `notes` = sanitized plain text
6.  Failure rules:
    *   If read/parse throws, skip row
    *   If `notes` is empty after sanitization, skip row

### Output (TSV)

*   Write header row: `file_name<TAB>notes`
*   Each subsequent row is tab-delimited
*   Escape tabs/newlines in fields by replacing:
    *   `\t` → single space
    *   `\r\n`, `\n`, `\r` → single space (after line-join this should already be satisfied)
*   Use UTF-8 encoding

### Validation case (must pass)

Folder: `C:\obsidian\Artemis-Hub`  
File: `Entra ID (OIDC) via MSAL.md`  
Expected TSV row:

*   `file_name`: `Entra ID (OIDC) via MSAL`
*   `notes`: `Microsoft Entra ID provides OpenID Connect authentication. MSAL handles sign‑in, tokens, refresh, SSO, and calling Microsoft APIs securely from your app.`


---

SAVEPOINT
- update prompt so that we include change log + when new imports detected, update the project map
- DAX = minimal footprint



# Testing-Artifcats
save scripts for diagnostic and testing all in a root.subdir == "testing-artifacts"
- build a diagnostic tool so that for any error -- we can easily identify which segment; feature; stage; component is broken
- be especially mindful of data type fidelity within the script file and as it crosses (used as dependency) script files
- 
---
## 📝 Script Documentation Standards

Every script (`.py`, `.ps1`, etc.) **must include**:

### 1. Invoke Instructions (Header Block)
Include clear usage examples at the top of each script in a comment block.

**Example for Python:**
```python
"""
SQL Query Join Cleaner
Analyzes SQL queries to identify and remove unused tables from FROM/JOIN clauses.

USAGE:
    # Analyze only (preview in terminal)
    python reduce_sql.py query.sql --analyze-only
    
    # Clean and generate output files
    python reduce_sql.py query.sql
    
    Creates:
        query_trimmed.sql  - Cleaned query with unused joins removed
        query_map.csv      - Table mapping (schema.table, alias, usage_type)
"""
```

**Example for PowerShell:
**
```powershell
<#
.SYNOPSIS
    Brief description of what the script does

.USAGE
    # Example 1
    .\script_name.ps1
    
    # Example 2
    .\script_name.ps1 -Parameter "value"

.OUTPUTS
    Description of what the script produces
#>
```


### 2. Terminal Diagnostics
Create a change log prompt
**Log Output Example:**
```
2025-12-06 14:23:45 | INFO | Starting validation for csv_mapper_cleaner.py
2025-12-06 14:23:45 | DEBUG | Python: C:\vsWorkspace\shared-utils\.venv\Scripts\python.exe
2025-12-06 14:23:45 | DEBUG | Mode: development
2025-12-06 14:23:45 | INFO | ✅ venv check passed
2025-12-06 14:23:45 | DEBUG | Checking packages: pandas, openpyxl
2025-12-06 14:23:45 | INFO | ✅ All packages found
2025-12-06 14:23:45 | INFO | Validation complete in 45.2ms
```

#status/deferred/quick-paste-merge-later 
### 📊 Validation Mode Comparison Table

| Feature | Development | CI/CD | Production | Disabled |
|---------|-------------|-------|------------|----------|
| **venv Check** | ✅ Full | ✅ Full | ✅ Quick | ❌ Skip |
| **Package Scan** | ✅ Detailed | ✅ Detailed | ⚠️ Critical only | ❌ Skip |
| **Version Check** | ⚠️ Warn | ❌ Fail | ⚠️ Log only | ❌ Skip |
| **Missing Packages** | 🤝 Interactive install | ❌ Fail | ❌ Fail | ❌ Skip |
| **Auto-Update Map** | ✅ Yes | ✅ Yes (commit) | ❌ No | ❌ No |
| **Logging** | 🖥️ Console + File | 📄 File only | 📄 File only | ❌ None |
| **Performance** | ~50-100ms | ~50-100ms | ~1-5ms | ~0ms |
| **Interactive Prompts** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Fail on Warning** | ❌ No | ✅ Yes | ❌ No | ❌ No |

---

### 🚀 Summary: Why This Architecture Works

#### Problems Solved

1. **"Works on my machine"** → venv validation ensures consistent environment
2. **Mid-execution failures** → Pre-flight checks before expensive operations
3. **Dependency drift** → Auto-update project_map.json tracks changes
4. **Cryptic errors** → Suggests exact pip install commands
5. **Debugging nightmares** → Detailed logs with timestamps
6. **Production overhead** → Fast validation mode for deployed apps
7. **Agent confusion** → Single source of truth (project_map.json)

#### Key Principles

- **Development**: Helpful, interactive, verbose - optimize for developer experience
- **Production**: Fast, silent, resilient - optimize for uptime and performance  
- **CI/CD**: Strict, fail-fast - optimize for catching issues before deployment
- **All Modes**: Log everything for post-mortem analysis

#### Next Steps

1. Implement `shared_utils/validators.py` with mode detection
2. Create `tools/verify_env.py` with --sync and --install flags
3. Generate initial `project_map.json` from workspace scan
4. Add validator one-liners to existing scripts by class
5. Test in development mode, validate auto-update works
6. Set up CI/CD with strict mode validation
---

Scripts must print progress indicators at different stages (minimum 2: beginning and end).
**Format:** Use `[step/total]` notation with descriptive messages

**Example Output:**
```
[1/4] Reading SQL file: stg_f_transactions.sql
      File size: 4,338 characters

[2/4] Parsing query structure...
[3/4] Analyzing table usage...
      Extracting table aliases... found 12 tables
      Extracting query clauses... done
      Scanning SELECT clause... 8 tables referenced
      Scanning WHERE clause... 2 tables referenced
      Scanning JOIN conditions... 12 bridge tables found
[4/4] Analysis complete!

[Analysis only mode - no files modified]

Completed in 0.01 seconds
```

**Implementation Examples:**

**Python:**
```python
import time
start_time = time.time()

print("[1/3] Loading data...")
# ... code ...

print("[2/3] Processing records...")
# ... code ...

print("[3/3] Saving results...")
# ... code ...

elapsed = time.time() - start_time
print(f"\nCompleted in {elapsed:.2f} seconds")
```

**PowerShell:**
```powershell
$startTime = Get-Date

Write-Host "[1/3] Loading data..." -ForegroundColor Cyan
# ... code ...

Write-Host "[2/3] Processing records..." -ForegroundColor Cyan
# ... code ...

Write-Host "[3/3] Saving results..." -ForegroundColor Cyan
# ... code ...

$duration = (Get-Date) - $startTime
Write-Host "`nCompleted in $($duration.TotalSeconds) seconds" -ForegroundColor Green
```
---
## 🎯 Philosophy: Dependency First

**The Problem:**
- Scripts fail mid-execution with `ModuleNotFoundError`
- Agents run code in global Python instead of project `venv`
- Package version mismatches cause silent failures
- "It worked in testing" but production uses different dependencies
- Multiple isolated venvs (one per project) prevent conflicts

**The Solution:**
- **State before Action**: Never execute code without verifying the environment state
- **Explicit over Implicit**: Do not assume packages exist; check the `project_map.json`
- **Isolation Integrity**: Code must refuse to run if it detects it is outside the designated `venv`
- **Version Lock**: Track exact versions to prevent "works on dev, breaks on prod" scenarios
- **Project Venvs Only**: Each project has its own `.venv/` directory. NO ROOT WORKSPACE VENV exists or should be created.

### Critical: No Root Workspace Venv

❌ **DO NOT CREATE**: `C:\vsWorkspace\.venv/`
✅ **USE INSTEAD**: Project-specific venvs only:
- `C:\vsWorkspace\projects_p\client-bridge\.venv/`
- `C:\vsWorkspace\projects_p\slidesms_v1\.venv/`
- `C:\vsWorkspace\projects_p\web-scraper-jira\.venv/`
- `C:\vsWorkspace\shared-utils\.venv/`

When feeding this document as context to an agent:
- Agent reads which project is being worked on
- Agent activates that project's `.venv/` (e.g., `.\.venv\Scripts\Activate.ps1` inside the project directory)
- Agent does NOT create or modify root workspace venv
- Agent works entirely within the project-specific environment

---

## 🗺️ The Source of Truth: `project_map.json`

To prevent "AI hallucinated dependencies," we maintain a JSON file that maps the file hierarchy to specific requirements.

### Required JSON Structure

```json
{
  "meta": {
    "project_name": "shared-utils",
    "python_version": "3.12",
    "venv_path": ".venv",
    "last_updated": "2025-12-06",
    "verified_by": "agent"
  },
  "dependency_tree": {
    "global_requirements": ["os", "sys", "logging", "pathlib"],
    "modules": [
      {
        "file_path": "scripts/csv_mapper_cleaner.py",
        "script_class": "data_processor",
        "imports_external": ["pandas>=2.1.0", "openpyxl"],
        "imports_internal": [],
        "status": "active",
        "last_verified": "2025-12-06"
      },
      {
        "file_path": "shared_utils/connectors/google_drive.py",
        "script_class": "api_connector",
        "imports_external": ["google-auth", "google-api-python-client"],
        "imports_internal": ["pathlib.Path"],
        "status": "active",
        "last_verified": "2025-12-06"
      },
      {
        "file_path": "scripts/reduce_sql.py",
        "script_class": "text_processor",
        "imports_external": [],
        "imports_internal": ["pathlib.Path", "typing.Set", "typing.Dict"],
        "status": "active",
        "last_verified": "2025-12-06"
      }
    ]
  },
  "dependencies": {
    "pandas": "2.1.0",
    "openpyxl": "latest",
    "google-auth": ">=2.0.0",
    "google-api-python-client": ">=2.0.0",
    "streamlit": "1.40.0",
    "streamlit-drawable-canvas": "0.9.3"
  }
}
```

### 📋 The Rule of Updates

1. **Read First**: Before editing a script, the agent reads `project_map.json`
2. **Update Map**: If a new library is added to the code, `project_map.json` **must** be updated first
3. **Verify**: Run `pip install` based on the JSON map, not the script imports alone
4. **Test**: After updates, run `verify_env.py` to ensure consistency

---

## 🤖 Agent Directives: Environment Setup & Execution

**When this document is provided as context, follow these rules strictly:**

### Never Create Root Workspace Venv
- ❌ DO NOT run: `python -m venv C:\vsWorkspace\.venv`
- ❌ DO NOT run: `python -m venv .venv` from workspace root
- ✅ If `.venv` exists in root: Ignore it entirely, it should not be there

### Activation Protocol
**Before running ANY Python code in a project:**

1. **Identify the project**: Determine which directory is the active project (client-bridge, slidesms_v1, shared-utils, etc.)
2. **Check for existing venv**: Look for `.venv/` in that project directory
3. **Activate if exists**: 
   ```powershell
   # From inside the project directory
   .\.venv\Scripts\Activate.ps1
   ```
4. **Create if missing** (only if you're setting up a new project):
   ```powershell
   cd C:\vsWorkspace\projects_p\[project_name]
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
5. **Verify activation**: Check prompt shows `(.venv)` prefix

### Execution Checklist
- [ ] Confirm prompt shows `(.venv)` before running code
- [ ] Current directory is the project directory (not workspace root)
- [ ] `pip list` shows project-specific packages (not bloated global list)
- [ ] `sys.prefix != sys.base_prefix` returns True (in venv)
- [ ] Required packages from `project_map.json` are installed

### What NOT to Do
- ❌ Run code from workspace root without activating a project venv
- ❌ Install packages in global Python to solve import errors
- ❌ Create temporary venvs for testing (use existing project venvs instead)
- ❌ Modify `.venv` directories directly (use `pip install` instead)
- ❌ Leave venv activated after task completion (document deactivate step)

---

## 🛡️ Pre-Flight Checks: Script Classes

Different types of scripts require different validation levels. We define **script classes** to determine which checks to run.

### Script Class Definitions

| Class | Description | Critical Checks |
|-------|-------------|-----------------|
| `data_processor` | Scripts that read/write files, process CSV/Excel | venv, pandas, file I/O libraries |
| `api_connector` | Scripts that call external APIs | venv, requests/google-auth, network libs |
| `database_handler` | Scripts that connect to databases | venv, connection libs, credentials |
| `text_processor` | Scripts with only stdlib (no external deps) | venv only |
| `utility` | Helper scripts called by other scripts | venv, caller-specific imports |

## ✅ Quick Checklist

Before committing any script:
- [ ] Filename is all lowercase
- [ ] No spaces in filename (use underscores)
- [ ] No numeric prefixes (00_, 01_, etc.)
- [ ] Header block with usage instructions
- [ ] Terminal diagnostics with [step/total] format
- [ ] Completion message with elapsed time

---

### 2. Function Return Value Usage

**Issue Pattern:** Function returns a value but the code doesn't use it or uses a different value.

**Check:**
- [ ] All function returns are either used or intentionally ignored
- [ ] Return values match the variable types expected by callers
- [ ] No mixing of return values with global/class variables

**Example check:**
```python
# Function returns something
result = process_data(df)

# Does the code use 'result' or does it still use 'df'?
# Should be using 'result' from here on
```

---

### 3. Index/Offset Errors

**Issue Pattern:** Off-by-one errors in loops, array access, or range calculations.

**Check:**
- [ ] Loop ranges match expected iteration count
- [ ] Array indices account for 0-based vs 1-based indexing
- [ ] String slicing uses correct start/end positions
- [ ] Row/column numbers in diagnostics match actual data structure

**Example from Session:**
```python
# Excel rows are 1-indexed, pandas is 0-indexed
header_row = 28  # Excel row number
df = pd.read_excel(file, header=header_row - 1)  # Adjust for 0-based ← Important!
```

---

### 4. Conditional Logic Inversions

**Issue Pattern:** Logic checks the opposite of what's intended (if/else swapped).

**Check:**
- [ ] "if empty then remove" (not "if not empty then remove")
- [ ] "if similar then reuse" (not "if different then reuse")
- [ ] Threshold comparisons use correct operator (≥ vs ≤)

**Example:**
```python
# Correct
if empty_pct >= 95.0:  # If 95% or more empty
    columns_to_drop.append(col)

# Wrong (inverted)
if empty_pct < 95.0:  # Would drop columns that AREN'T empty!
    columns_to_drop.append(col)
```

---

### 5. String Matching Patterns

**Issue Pattern:** Regex or string matching doesn't cover all expected patterns.

**Check:**
- [ ] Pattern handles both underscore and non-underscore variants
- [ ] Case sensitivity is correct (should lowercase match uppercase?)
- [ ] Special characters are properly escaped in regex
- [ ] Pattern matches edge cases (empty strings, single characters)

**Example from Session:**
```python
# Original - only matched: column_1, column_2
if '_' in cleaned_col:
    parts = cleaned_col.rsplit('_', 1)
    if len(parts) == 2 and parts[1].isdigit():
        base_name = parts[0]

# Fixed - matches: column_1, column1, column_2, column2
match = re.match(r'^(.+?)(_?\d+)$', cleaned_col)
```

---

### 6. Deprecated API Usage

**Issue Pattern:** Using older pandas/library methods that trigger warnings.

**Check:**
- [ ] `applymap()` → Use `map()` (pandas 2.1+)
- [ ] `append()` → Use `concat()` (pandas 2.0+)
- [ ] Check library documentation for current API
- [ ] Review warnings during first run

**Example from Session:**
```python
# Deprecated
df = df.applymap(lambda x: clean(x))

# Current
df = df.map(lambda x: clean(x))
```

---

### 7. File Extension Assumptions

**Issue Pattern:** Code assumes file format based on extension, but application behavior differs.

**Check:**
- [ ] Verify Excel interprets file correctly (`.csv` vs `.txt` vs `.tsv`)
- [ ] Check if application auto-detects delimiter or uses extension default
- [ ] Test opening exported file in target application

**Example from Session:**
```python
# Problem: Excel treats .csv as comma-delimited even with tabs
output_path = "data_cleaned.csv"  # Excel ignores tabs!

# Solution: Use .txt for tab-delimited files
output_path = "data_cleaned.txt"  # Excel recognizes tabs
```

---

### 8. Data Type Consistency

**Issue Pattern:** Operations mix data types inappropriately (string + int, float vs int).

**Check:**
- [ ] Numeric operations use consistent types
- [ ] String concatenation doesn't mix types without conversion
- [ ] None/null handling is consistent across operations
- [ ] Boolean comparisons use correct types

**Example:**
```python
# Problem
age = "25"
if age > 18:  # TypeError: comparing string to int

# Fix
age = int("25")
if age > 18:  # Works correctly
```

---

### 9. Scope and Visibility

**Issue Pattern:** Variable used before definition or outside its scope.

**Check:**
- [ ] Variables defined before use in all code paths
- [ ] Variables in if/else blocks accessible where needed
- [ ] Function parameters passed correctly
- [ ] Global vs local variable usage is intentional

**Example:**
```python
# Problem
if condition:
    result = process()
print(result)  # Error if condition is False!

# Fix
result = None
if condition:
    result = process()
if result:
    print(result)
```

---

### 10. Edge Case Handling

**Issue Pattern:** Code works for typical cases but fails on edge cases.

**Check:**
- [ ] Empty dataset handling
- [ ] Single row/column handling
- [ ] All-null column handling
- [ ] Duplicate detection with 0 or 1 columns
- [ ] Division by zero protection

**Example from Session:**
```python
# Protected division
empty_pct = (empty_cells / total_cells) * 100 if total_cells > 0 else 0
#                                               ^^^^^^^^^^^^^^^^^^^^^^^^^
#                                               Edge case protection
```

---

## 🔍 Review Process

### Step 1: Scan for Variable References
```python
# Find all places where a variable is used
# Example: Search for "output_path" and verify all references use the same source
```

### Step 2: Trace Data Flow
```
Input → Transform 1 → Transform 2 → Output
        ↓             ↓             ↓
      Check var    Check var    Check var
```

### Step 3: Check Function Signatures
```python
def function(param1: type1, param2: type2) -> return_type:
    # Verify:
    # 1. All params used correctly
    # 2. Return matches declared type
    # 3. All code paths return something
```

### Step 4: Review Conditionals
```python
if condition:    # Does this read naturally?
    action       # Is the action correct for this condition?
else:           # Is the else case handled?
    fallback
```

---

## 📋 Testing Strategy

### 1. Dry Run Review
Before executing, mentally trace through the code with sample data:
```
Given: filename = "data.xlsx", source_type = "sales"
Output should be: "sales_cleaned.txt"
Check: Does the code use source_type or filename.stem?
```

### 2. Diagnostic Validation
Add temporary print statements before execution:
```python
print(f"DEBUG: Using variable '{source_file_type}' for output filename")
print(f"DEBUG: Output path will be: {output_path}")
```

### 3. Small Data Test First
- Test with minimal data (1-2 rows) to verify logic
- Check intermediate outputs (files, logs)
- Verify all expected files are created with correct names

---

## 🚨 Common AI Assistant Pitfalls

### Pitfall 1: Copy-Paste Inconsistency
**What happens:** AI copies code block but forgets to update variable names.

**Example:**
```python
# Section 1
df_original = load_data()

# Section 2 (copied from Section 1)
df_original = process_data()  # Should be df_processed!
```

**How to catch:** Look for duplicate variable names with different purposes.

---

### Pitfall 2: Over-Optimization
**What happens:** AI tries to combine steps and introduces bugs.

**Example:**
```python
# Clear but longer
filtered = remove_empty(df)
deduped = remove_duplicates(filtered)
cleaned = clean_values(deduped)

# "Optimized" but buggy
cleaned = clean_values(remove_duplicates(remove_empty(df)))
# Harder to debug, easy to mess up order
```

**How to catch:** If code feels dense or hard to read, break it apart.

---

### Pitfall 3: Assuming Behavior
**What happens:** AI assumes library/application will behave a certain way.

**Example:**
```python
# AI assumes Excel will detect tabs in .csv files
df.to_csv("output.csv", sep='\t')  # Excel treats as comma-delimited!
```

**How to catch:** Test actual behavior in target application.

---

### Pitfall 4: Incomplete Refactoring
**What happens:** AI changes part of code but misses related sections.

**Example:**
```python
# Changed function signature
def process(data, threshold=95):  # Added threshold parameter
    ...

# But forgot to update this call
result = process(data)  # Still works (uses default) but inconsistent
```

**How to catch:** Search for all function calls when signature changes.

---
## 🔍 Code Review Checklist

Before executing AI-generated code, verify:

### Critical Checks
1. **Variable Consistency**: Same data used consistently (e.g., user input vs derived values)
2. **File Naming**: All outputs use the same naming convention
3. **Index Alignment**: 0-based vs 1-based indexing handled correctly
4. **Pattern Matching**: Regex/conditions cover all expected variants

### Quality Checks
5. **Deprecated APIs**: No warnings for deprecated methods
6. **Edge Cases**: Empty data, nulls, single items handled
7. **Data Types**: Consistent types throughout operations
8. **Logic Flow**: Conditions read naturally and match intent

### Testing Protocol
- Add DEBUG print statements for critical variables
- Test with minimal data first (1-2 rows)
- Verify output filenames match expectations
- Check intermediate files are created correctly