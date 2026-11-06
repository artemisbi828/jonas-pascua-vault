
**Templateize**: create usable pattern (metadata-driven)
**Parameterize**: replace hard coded values with variables
**Instantiate**: generate many outputs from one definition

> instantiate one document per source system

**Expand**: loop through entities 


```
Scheduler :: Manager                         # Cron, Windows Task Scheduler, Fabric Schedule
	↓
Orchestrator :: Head Chef                    # triggers (m) commands, notifies, archives 
	↓                                          ADF, Cron + Master Script, Fabric Pipeline
Executor / Runner / Worker :: Line Cook      # one command, does one thing
	↓                                          Jobs
Query / Script :: Recipe
	↓
Config :: Recipe Card
	↓
Parameters :: Ingredients
	↓
Outputs / Dataset :: Dish 
	↓
CSV / Parquet :: Takeout Container
	↓
Log File :: Kitchen Notes
	↓
Log File :: Kitchen Workflow
```

Collider: A-B testing
Generator: Script (eg Python) to use template-sql + parameters --> sql-outputs
Utility: Tool (Python Utility)

# Script Components
```
Source Code
    ↓
Tokenizer / Lexer
    ↓
Parser
    ↓
Syntax Tree (AST)
    ↓
Validator / Binder
    ↓
Optimizer
    ↓
Compiler / Translator
    ↓
Runtime / Interpreter
    ↓
Operating System
    ↓
CPU
```

# Mental Model: From Source Code → CPU

## TL;DR

The most common conceptual mistake is treating this as a single pipeline. It is actually **three different domains**:

1. **Language Processing** (Tokenizer → Parser → AST → Binder)
2. **Program Transformation** (Optimizer → Compiler/Translator)
3. **Program Execution** (Runtime → OS → CPU)

Each layer answers a different question:

|Layer|Question|
|---|---|
|Tokenizer|What are the words?|
|Parser|How are the words structured?|
|AST|What is the program's shape?|
|Binder/Validator|What do names mean?|
|Optimizer|How can this be improved?|
|Compiler|How is it converted for execution?|
|Runtime|How is it executed safely?|
|OS|How are machine resources managed?|
|CPU|How are instructions physically executed?|

---

# Section 1

## 1. Definition Table

|Concept|Description|Example|
|---|---|---|
|Source Code|Human-readable instructions written in a programming language. This is the author's intent, not something CPUs directly understand.|`x = a + b`|
|Tokenizer (Lexer)|Breaks source code into tokens (keywords, identifiers, operators, literals). It does not understand meaning or structure.|`"x" "=" "a" "+" "b"`|
|Parser|Converts tokens into grammatical structure based on language rules. Detects syntax errors.|Assignment expression tree|
|AST (Abstract Syntax Tree)|Simplified structural representation of program meaning. Removes unnecessary syntax details.|Assign(x, Add(a,b))|
|Validator / Binder|Resolves names, types, scopes, references, imports, symbols. Answers "what does this identifier mean?"|`a` refers to local variable, not global|
|Optimizer|Rewrites program into a more efficient but equivalent form.|`2+3` → `5`|
|Compiler / Translator|Converts program representation into another form. Could be machine code, bytecode, SQL, JavaScript, etc.|C# → IL|
|Runtime / Interpreter|Executes program behavior, manages memory, exceptions, garbage collection, etc.|.NET CLR|
|Operating System|Coordinates hardware resources and provides system services.|Windows/Linux|
|CPU|Physical processor executing machine instructions.|Intel, AMD, ARM|

---

# 2. Relationships (Lower → Higher)

```text
Physical Execution
└── CPU

Hardware Management
└── Operating System

Program Execution
└── Runtime / Interpreter

Program Conversion
└── Compiler / Translator
    └── Optimizer

Program Understanding
└── Validator / Binder
    └── AST
        └── Parser
            └── Tokenizer

Human Authoring
└── Source Code
```

---

# 3. Why They Are Different

## Tokenizer vs Parser

Tokenizer:

```text
Input:
x = a + b

Output:
[x][=][a][+][b]
```

Parser:

```text
Assignment
├── Variable x
└── Add
    ├── a
    └── b
```

**Boundary**

```text
Tokenizer = words
Parser = grammar
```

---

## Parser vs AST

Parser creates a syntactic structure.

AST creates a semantic structure.

Example:

```c
(((a+b)))
```

Parser cares.

AST does not.

AST may simplify to:

```text
Add(a,b)
```

**Boundary**

```text
Parser = language grammar
AST = program meaning structure
```

---

## AST vs Binder

AST knows:

```text
Customer.Name
```

Binder knows:

```text
Which Customer?
Which Name?
What datatype?
```

**Boundary**

```text
AST = shape
Binder = meaning
```

This distinction is especially important in semantic models, SQL engines, and Power BI expression engines.

---

## Binder vs Optimizer

Binder ensures correctness.

Optimizer improves performance.

Example:

```sql
SELECT *
FROM Customers
WHERE 1 = 1
```

Binder:

```text
Valid query
```

Optimizer:

```text
Remove unnecessary filter
```

**Boundary**

```text
Binder = valid?
Optimizer = efficient?
```

---

## Compiler vs Runtime

Compiler:

```text
Transforms code
```

Runtime:

```text
Executes code
```

Example (.NET):

```text
C#
 ↓
Compiler
 ↓
IL
 ↓
CLR Runtime
 ↓
CPU
```

**Boundary**

```text
Compiler creates executable form.
Runtime runs executable form.
```

---

## Runtime vs OS

Runtime manages language concerns.

OS manages machine concerns.

Runtime:

```text
Garbage Collection
Exception Handling
Type Safety
```

OS:

```text
Memory Allocation
Processes
Threads
Files
Networking
```

**Boundary**

```text
Runtime = program environment
OS = machine environment
```

---

## OS vs CPU

OS:

```text
Coordinator
```

CPU:

```text
Worker
```

OS schedules work.

CPU performs work.

**Boundary**

```text
OS decides what runs.
CPU executes instructions.
```

---

# 4. Why the Distinction Matters

## Performance Tuning

Wrong:

```text
"The compiler is slow."
```

Actual possibilities:

```text
Binder expensive
Optimizer expensive
Runtime expensive
OS scheduling issue
CPU bottleneck
```

Different layer = different fix.

---

## Debugging

Syntax Error:

```text
Parser
```

Type Error:

```text
Binder
```

Slow Query:

```text
Optimizer
```

Memory Leak:

```text
Runtime
```

High CPU:

```text
OS/CPU
```

---

## Data Platform Analogy (Power BI / SQL)

Useful mapping for your BI background:

|Data Platform|Compiler World|
|---|---|
|DAX Text|Source Code|
|SQL Text|Source Code|
|DAX Parser|Parser|
|Query Plan Tree|AST|
|Semantic Model Resolution|Binder|
|Query Optimizer|Optimizer|
|VertiPaq/SQL Plan Generation|Compiler|
|Analysis Services Engine|Runtime|
|Windows|OS|
|CPU Cores|CPU|

This is why semantic models behave very similarly to programming languages.

---

# 5. Final Mental Model (Simple)

Think of a company:

```text
Source Code
    Employee Request

Tokenizer
    Reads words

Parser
    Builds form

AST
    Standardized document

Binder
    Validates identities and references

Optimizer
    Improves workflow

Compiler
    Converts into actionable tasks

Runtime
    Executes tasks

Operating System
    Allocates organizational resources

CPU
    Individual workers doing the labor
```

---

# Section 2 — ASCII Trees (Obsidian.md)

## Hierarchical Structure

```text
Source Code
│
├── Tokenizer
│
├── Parser
│
├── AST
│
├── Validator / Binder
│
├── Optimizer
│
├── Compiler / Translator
│
├── Runtime / Interpreter
│
├── Operating System
│
└── CPU
```

---

## Semantic Dependency Tree

```text
CPU
▲
│ executes
│
Operating System
▲
│ hosts
│
Runtime
▲
│ runs
│
Compiled Output
▲
│ produced by
│
Compiler
▲
│ transforms
│
Optimizer
▲
│ improves
│
Binder
▲
│ resolves meaning
│
AST
▲
│ represents structure
│
Parser
▲
│ builds structure
│
Tokenizer
▲
│ extracts tokens
│
Source Code
```

---

## Lifecycle Flow

```text
Authoring Phase
─────────────────────
Source Code

Language Understanding
─────────────────────
Tokenizer
→ Parser
→ AST
→ Binder

Transformation Phase
─────────────────────
Optimizer
→ Compiler

Execution Phase
─────────────────────
Runtime
→ Operating System
→ CPU
```

---

# Section 3 — Concept Catalog

## Source Code

### Purpose

Express human intent.

### Scope

Language-specific instructions.

### Dependencies

Language grammar.

### Limitations

Not executable directly.

### Anti-Patterns

```text
Confusing source code with execution.
Assuming written order equals execution order.
```

---

## Tokenizer

### Purpose

Extract symbols.

### Scope

Characters → tokens.

### Dependencies

Lexical rules.

### Limitations

Cannot understand meaning.

### Anti-Patterns

```text
Expecting lexer to validate logic.
Expecting lexer to understand types.
```

---

## Parser

### Purpose

Verify grammar.

### Scope

Tokens → structure.

### Dependencies

Language syntax.

### Limitations

Does not resolve meaning.

### Anti-Patterns

```text
Assuming parsed code is valid code.
```

A program can parse successfully and still fail binding.

---

## AST

### Purpose

Represent program structure.

### Scope

Semantic representation.

### Dependencies

Parser output.

### Limitations

Meaning may still be unresolved.

### Anti-Patterns

```text
Using AST as symbol table.
Using AST as execution plan.
```

---

## Binder

### Purpose

Attach meaning.

### Scope

Names, symbols, scopes, types.

### Dependencies

AST.

### Limitations

Not focused on performance.

### Anti-Patterns

```text
Optimizing before binding.
Resolving names during execution.
```

---

## Optimizer

### Purpose

Improve execution efficiency.

### Scope

Equivalent transformations.

### Dependencies

Bound program.

### Limitations

Cannot change semantics.

### Anti-Patterns

```text
Changing behavior.
Micro-optimizing before correctness.
```

---

## Compiler

### Purpose

Generate executable representation.

### Scope

Translation.

### Dependencies

Validated program.

### Limitations

Execution not guaranteed.

### Anti-Patterns

```text
Treating compilation as execution.
```

---

## Runtime

### Purpose

Execute language behavior.

### Scope

Memory, exceptions, execution.

### Dependencies

Compiled output.

### Limitations

Dependent on OS resources.

### Anti-Patterns

```text
Implementing OS responsibilities.
```

---

## Operating System

### Purpose

Manage machine resources.

### Scope

Hardware abstraction.

### Dependencies

Hardware.

### Limitations

Does not understand application semantics.

### Anti-Patterns

```text
Assuming OS understands business logic.
```

---

## CPU

### Purpose

Execute machine instructions.

### Scope

Primitive operations.

### Dependencies

Hardware architecture.

### Limitations

No understanding of programming abstractions.

### Anti-Patterns

```text
Thinking CPU understands:
- Objects
- Classes
- SQL
- DAX
- Business rules
```

CPU only understands machine instructions.

---

## Most Common Semantic Collisions

```text
Parser      ≠ Binder
AST         ≠ Execution Plan
Compiler    ≠ Runtime
Runtime     ≠ Operating System
OS          ≠ Hardware
CPU         ≠ Program
```

### ELI5

```text
Tokenizer = reads words

Parser = builds sentence

AST = diagram of sentence

Binder = determines what names refer to

Optimizer = improves sentence

Compiler = translates sentence

Runtime = carries out instructions

OS = manages the workplace

CPU = worker doing the actual labor
```

**Would you like 1–2 worked examples for either:**

1. C#/.NET (Roslyn → CLR), or
2. SQL/DAX query processing (closer to semantic models, Power BI, and query engines)?