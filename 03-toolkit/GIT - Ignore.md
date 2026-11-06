## 🎯 Core Principles

### **DRY (Don't Repeat Yourself)**
Don't commit files that can be **regenerated** from source code or downloaded from registries.

### **SOLID - Single Responsibility**
Repository should contain **source code only** - not build artifacts, dependencies, or runtime artifacts.

### **Separation of Concerns**
Keep configuration separate from code. Personal IDE settings shouldn't affect team members.

### **Efficiency**
Avoid bloating repositories with large, unnecessary files that slow down clones and checkouts.

---

## 📦 File Categories in .gitignore

### 1. **Python Cache Files** (`__pycache__/`, `*.pyc`, `*.pyo`)

**What they are:**
- Compiled bytecode versions of Python files
- Created automatically when Python imports a module
- Speed up subsequent imports by skipping compilation

**Why exclude them:**

❌ **Violates DRY:**
```python
# You write this (source):
def hello():
    return "Hello World"

# Python auto-generates this (bytecode):
# __pycache__/myfile.cpython-312.pyc
# ├─ Binary representation of your code
# └─ Python version-specific (cpython-312)
```

The `.pyc` file is **derived** from your `.py` file. Committing both violates DRY because:
- The `.py` file is the source of truth
- The `.pyc` file will be regenerated automatically on first import
- Different Python versions create different bytecode

❌ **Platform-Specific:**
- `cpython-312.pyc` (Python 3.12)
- `cpython-311.pyc` (Python 3.11)
- Team members with different Python versions will have conflicts

**Example Problem:**
```bash
# Developer A (Python 3.12) commits:
git add __pycache__/utils.cpython-312.pyc

# Developer B (Python 3.11) pulls and runs:
python app.py  # Generates utils.cpython-311.pyc
git status     # Shows conflict - which version to commit?
```

**Correct Approach:**
```bash
# Only commit source:
git add utils.py

# Let each developer generate their own cache:
python app.py  # Auto-creates __pycache__/ locally
```

---

### 2. **Virtual Environments** (`venv/`, `.venv/`, `ENV/`)

**What they are:**
- Isolated Python environments with specific package versions
- Created with `python -m venv .venv`
- Contains thousands of files (Python interpreter copy + all installed packages)

**Why exclude them:**

❌ **Massive Size:**
```
.venv/
├── Lib/
│   └── site-packages/
│       ├── pandas/           # ~50 MB
│       ├── numpy/            # ~30 MB
│       ├── requests/         # ~5 MB
│       └── [hundreds more]
├── Scripts/
│   ├── python.exe           # ~15 MB (copy of Python)
│   └── [executables]
└── [Total: 200+ MB]

# Compare to:
requirements.txt             # 2 KB
```

❌ **Violates DRY:**
Instead of committing the entire venv (200+ MB), commit a **recipe** to recreate it:
```txt
# requirements.txt (the DRY way)
pandas==2.1.0
numpy==1.24.3
requests==2.31.0
```

Anyone can recreate the exact environment:
```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt  # Regenerates everything
```

❌ **Platform-Specific:**
```
# Windows venv:
.venv/Scripts/python.exe         # Windows executable
.venv/Scripts/activate.bat       # Windows batch script

# Linux/Mac venv:
.venv/bin/python                 # Unix executable
.venv/bin/activate               # Unix shell script
```

Committing venv would break cross-platform collaboration.

**Example Problem:**
```bash
# Developer A (Windows) commits venv:
git add .venv/  # 200 MB upload

# Developer B (Mac) pulls:
.venv/Scripts/python.exe  # Error: not executable on Mac
```

**Correct Approach:**
```bash
# Commit the recipe only:
git add requirements.txt

# Each developer creates their own venv:
python -m venv .venv
pip install -r requirements.txt
```

---

### 3. **Build Artifacts** (`build/`, `dist/`, `*.egg-info/`)

**What they are:**
- Output from packaging/building your project
- Created by `python setup.py build` or `pip install -e .`
- Contain compiled code and metadata

**Why exclude them:**

❌ **Regenerable from Source:**
```bash
# Source (what you commit):
pyproject.toml
setup.py
src/
  mypackage/
    __init__.py
    utils.py

# Build artifacts (auto-generated):
build/
  lib/
    mypackage/  # Copy of your source
dist/
  mypackage-1.0.0.tar.gz  # Packaged version
mypackage.egg-info/  # Metadata
```

The build outputs are **derived** from your source code. Anyone can rebuild:
```bash
python -m build  # Regenerates build/, dist/, and .egg-info/
```

❌ **Violates Single Responsibility:**
- Repository = source code storage
- Build system = artifact generation
- These are separate concerns

**Example - NPM Analogy:**
```javascript
// package.json (source - commit this)
{
  "name": "my-app",
  "dependencies": {
    "react": "^18.0.0"
  }
}

// node_modules/ (generated - exclude this)
node_modules/
  react/
    [thousands of files]
```

Same principle: commit the recipe (`package.json`), not the artifacts (`node_modules/`).

---

### 4. **IDE Configuration** (`.vscode/`, `.idea/`, `*.swp`)

**What they are:**
- Personal editor settings and workspace state
- Example: VS Code settings, IntelliJ project files, Vim swap files

**Why exclude them:**

❌ **Personal Preferences:**
```json
// .vscode/settings.json
{
  "editor.fontSize": 14,           // Alice likes small fonts
  "editor.tabSize": 2,              // Alice uses 2-space tabs
  "python.linting.enabled": false   // Alice disabled linting
}

// Bob's preferences:
{
  "editor.fontSize": 18,           // Bob needs larger fonts
  "editor.tabSize": 4,              // Bob uses 4-space tabs (PEP 8)
  "python.linting.enabled": true   // Bob wants linting
}
```

Committing IDE settings forces **your preferences on the team**.

❌ **Tool-Specific:**
Different team members use different tools:
- Alice uses VS Code → `.vscode/`
- Bob uses PyCharm → `.idea/`
- Carol uses Vim → `*.swp`

Why commit all three IDE configs? Each developer should configure their own tool.

**Exception - Project-Wide Standards:**
Some teams *do* commit shared IDE settings for consistency:
```json
// .vscode/settings.json (shared team standard)
{
  "python.linting.pylintEnabled": true,  // Enforce linting
  "editor.formatOnSave": true,           // Auto-format on save
  "[python]": {
    "editor.tabSize": 4                  // PEP 8 standard
  }
}
```

This is acceptable when it enforces **project standards**, not personal preferences.

---

### 5. **Operating System Files** (`.DS_Store`, `Thumbs.db`)

**What they are:**
- Hidden files created by operating systems
- `.DS_Store` (Mac): Folder view settings
- `Thumbs.db` (Windows): Thumbnail cache

**Why exclude them:**

❌ **Platform-Specific:**
```bash
# Mac developer commits:
.DS_Store  # Contains Mac-specific folder metadata

# Windows developer has no .DS_Store, gets this unnecessary file
# Linux developer also confused by Mac metadata
```

❌ **No Code Value:**
These files contain UI preferences (icon positions, view modes), not code logic.

**Example Problem:**
```bash
# Every Mac user commits .DS_Store:
project/
  .DS_Store
  src/
    .DS_Store
    utils/
      .DS_Store

# Result: Dozens of useless files in repo
```

---

### 6. **Logs and Temporary Files** (`*.log`, `logs/`, `*.tmp`)

**What they are:**
- Runtime output and temporary data
- Created during development/testing

**Why exclude them:**

❌ **Runtime Artifacts:**
```python
# Your code generates logs:
import logging
logging.basicConfig(filename='app.log')
logger.info("Started processing")  # Writes to app.log

# app.log content (runtime artifact):
2025-12-06 10:23:45 - Started processing
2025-12-06 10:23:46 - Processed 100 records
2025-12-06 10:23:47 - Error: connection timeout
```

Logs are **outputs** of running your code, not the code itself.

❌ **Contain Sensitive Data:**
```log
2025-12-06 10:30:12 - User login: alice@example.com
2025-12-06 10:30:15 - API Key: sk_live_abc123...
2025-12-06 10:30:18 - Database query: SELECT * FROM users WHERE email='alice@example.com'
```

Committing logs can leak credentials, PII, or debug information.

❌ **Bloat Repository:**
```bash
# Log file grows over time:
app.log      # Day 1:   50 KB
app.log      # Day 30:  15 MB
app.log      # Day 365: 180 MB
```

Git tracks **every version** of committed files. A large log file committed daily bloats the repo.

---

### 7. **Test Coverage Reports** (`.coverage`, `htmlcov/`)

**What they are:**
- Reports showing which lines of code are tested
- Generated by `pytest --cov`

**Why exclude them:**

❌ **Regenerable:**
```bash
# Run tests to regenerate:
pytest --cov=mypackage --cov-report=html

# Generates:
.coverage         # Coverage data
htmlcov/          # HTML report
  index.html
  [many files]
```

Coverage reports are **derived** from running tests. Anyone can regenerate them.

❌ **Local Results:**
```
Developer A's coverage: 85%  # They haven't written all tests yet
Developer B's coverage: 92%  # They wrote more tests

# Which coverage report to commit? Neither - let CI/CD generate it
```

**Correct Approach:**
```yaml
# .github/workflows/test.yml (CI generates coverage)
- name: Run tests with coverage
  run: pytest --cov=mypackage --cov-report=xml
- name: Upload to Codecov
  uses: codecov/codecov-action@v3
```

Let the CI system generate and track coverage centrally.

---

## ✅ What *Should* Be Committed

### Source Code
```
✓ *.py              # Python source files
✓ *.js, *.ts        # JavaScript/TypeScript
✓ *.sql             # SQL scripts
✓ *.md              # Documentation
✓ *.yaml, *.json    # Configuration files
```

### Dependency Declarations
```
✓ requirements.txt   # Python dependencies
✓ package.json       # Node.js dependencies
✓ Pipfile            # Pipenv dependencies
✓ pyproject.toml     # Modern Python projects
```

### Project Configuration
```
✓ .gitignore         # Git exclusions
✓ .editorconfig      # Cross-editor standards
✓ pytest.ini         # Test configuration
✓ .flake8            # Linting rules
```

### Documentation
```
✓ README.md          # Project overview
✓ LICENSE            # Legal terms
✓ CONTRIBUTING.md    # Contribution guide
✓ docs/              # Documentation files
```

---

## 🚫 Common Mistakes

### Mistake 1: Committing `.env` Files
```bash
# .env (NEVER COMMIT THIS!)
DATABASE_URL=postgresql://user:password@localhost/db
API_KEY=sk_live_abc123xyz789
SECRET_KEY=super-secret-value-do-not-share
```

**Why it's bad:**
- Exposes secrets to everyone with repo access
- Secrets become part of Git history (hard to remove)
- Different environments need different values

**Correct Approach:**
```bash
# .env.example (commit this template)
DATABASE_URL=postgresql://user:password@localhost/db
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# .env (each developer creates locally)
DATABASE_URL=postgresql://alice:alicepass@localhost/mydb
API_KEY=sk_test_alice123
SECRET_KEY=alice-local-secret
```

### Mistake 2: Committing Large Binary Files
```bash
# DON'T:
git add dataset.csv        # 500 MB
git add model.pkl          # 200 MB
git add video_demo.mp4     # 1 GB
```

**Why it's bad:**
- Bloats repository size permanently
- Slows down clones for everyone
- Git is optimized for **text files**, not binaries

**Correct Approach:**
```bash
# Use Git LFS for large files:
git lfs track "*.csv"
git lfs track "*.pkl"

# Or store externally:
# dataset.csv → S3, Google Drive, DVC
# Reference in README with download instructions
```

---

## 📚 Summary: The Golden Rules

1. **Only commit source code** - not derived artifacts
2. **Commit recipes, not results** - `requirements.txt`, not `venv/`
3. **Keep secrets out** - use `.env.example`, not `.env`
4. **Respect personal preferences** - exclude IDE configs
5. **Think cross-platform** - exclude OS-specific files
6. **Keep repos small** - exclude large binaries
7. **Regenerate, don't commit** - logs, cache, builds

---

## 🔍 Quick Decision Tree

```
Should I commit this file?
│
├─ Is it source code? (*.py, *.js, etc.)
│  └─ YES → Commit it ✓
│
├─ Can it be regenerated from source?
│  └─ YES → Exclude it ✗ (.pyc, venv/, build/)
│
├─ Is it a secret or credential?
│  └─ YES → Exclude it ✗ (.env, *.key)
│
├─ Is it a personal preference?
│  └─ YES → Exclude it ✗ (.vscode/, .idea/)
│
├─ Is it platform-specific?
│  └─ YES → Exclude it ✗ (.DS_Store, Thumbs.db)
│
├─ Is it a runtime artifact?
│  └─ YES → Exclude it ✗ (*.log, *.tmp)
│
└─ Is it a dependency declaration?
   └─ YES → Commit it ✓ (requirements.txt, package.json)
```

---

*Last Updated: December 6, 2025*

---

## 🧩 Case Study: Why `.obsidian/workspace.json` Keeps Coming Back

If this file keeps reappearing after pull/sync, it's usually one of these:

1. You added the rule to `.gitignore`, **but the file was already tracked**.
2. The file still exists in `main`, so merge/pull keeps bringing it back.
3. There is an active merge conflict (`DU` / delete-vs-update) and Git needs an explicit resolution.

### ✅ Correct Ignore Rule

```gitignore
.obsidian/workspace.json
```

> Note: it must be `.gitignore` (not `.ignore`).

### 🔍 Verify Ignore Is Working

Run:

```bash
git check-ignore -v --no-index .obsidian/workspace.json
```

Expected output should reference `.gitignore` and the matching rule.

### 🧼 Stop Tracking It (One-Time)

If already tracked, ignore won't apply until you untrack it:

```bash
git rm --cached -- .obsidian/workspace.json
git add .gitignore
git commit -m "Stop tracking Obsidian workspace file"
```

This removes it from Git history going forward but keeps your local file on disk.

### ⚔️ If It Appears During Merge/Sync (Delete vs Update)

If `git status --short` shows:

```bash
DU .obsidian/workspace.json
```

That means one side deleted it and the other side modified it.

**VS Code UI resolution (no manual merge edits):**
- Source Control → Merge Changes → click `.obsidian/workspace.json`
- Choose **Keep Deleted** (or the equivalent option that keeps the file removed)
- Stage changes and complete merge/sync

CLI equivalent:

```bash
git rm -- .obsidian/workspace.json
git add -A
git commit   # or: git merge --continue
```

### 🧪 Quick Test Checklist

```bash
git status --short
git ls-files -- .obsidian/workspace.json
git check-ignore -v --no-index .obsidian/workspace.json
```

Interpretation:
- `git ls-files` returns nothing → file is not tracked ✅
- `git check-ignore` shows `.gitignore` rule → ignore is active ✅
- `git status` does not show `.obsidian/workspace.json` → success ✅

### 🧠 Team-Level Permanent Fix

If `main` still tracks the file, it can reappear on every sync. The lasting fix is a commit to `main` that:

1. Removes `.obsidian/workspace.json` from tracking
2. Keeps `.obsidian/workspace.json` in `.gitignore`

After that, everyone stops seeing this churn.


---



*Last Updated: December 6, 2025*
----

Had staged files that should be in git.ignore (.pyc files) but had to rm cache in order to have clean branches

The `.pyc` files are staged but shouldn't be committed since we just added [.gitignore](vscode-file://vscode-app/c:/Users/jonas-adam.pascua/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html). Let me unstage them and verify gitignore is working:

Good! The files are unstaged. However, they're still showing as modified because they existed before we added [.gitignore](vscode-file://vscode-app/c:/Users/jonas-adam.pascua/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html). Let me remove them from git tracking:

```

git restore --staged shared_utils/connectors/__pycache__/firestore.cpython-312.pyc shared_utils/connectors/__pycache__/google_drive.cpython-312.pyc; git status

git rm --cached -r shared_utils/**/__pycache__; git status

git rm --cached shared_utils/connectors/__pycache__/firestore.cpython-312.pyc shared_utils/connectors/__pycache__/google_drive.cpython-312.pyc; git status

Perfect! Now the cache files are marked for deletion from git (they'll remain on disk but won't be tracked). Let me commit and push:

```

---
#status/deferred/quick-paste-merge-later 
# Understanding .gitignore: What to Exclude and Why

A comprehensive guide to gitignore patterns and the software engineering principles behind them.

---

## 🎯 Core Principles

### **DRY (Don't Repeat Yourself)**
Don't commit files that can be **regenerated** from source code or downloaded from registries.

### **SOLID - Single Responsibility**
Repository should contain **source code only** - not build artifacts, dependencies, or runtime artifacts.

### **Separation of Concerns**
Keep configuration separate from code. Personal IDE settings shouldn't affect team members.

### **Efficiency**
Avoid bloating repositories with large, unnecessary files that slow down clones and checkouts.

---

## 📦 File Categories in .gitignore

### 1. **Python Cache Files** (`__pycache__/`, `*.pyc`, `*.pyo`)

**What they are:**
- Compiled bytecode versions of Python files
- Created automatically when Python imports a module
- Speed up subsequent imports by skipping compilation

**Why exclude them:**

❌ **Violates DRY:**
```python
# You write this (source):
def hello():
    return "Hello World"

# Python auto-generates this (bytecode):
# __pycache__/myfile.cpython-312.pyc
# ├─ Binary representation of your code
# └─ Python version-specific (cpython-312)
```

The `.pyc` file is **derived** from your `.py` file. Committing both violates DRY because:
- The `.py` file is the source of truth
- The `.pyc` file will be regenerated automatically on first import
- Different Python versions create different bytecode

❌ **Platform-Specific:**
- `cpython-312.pyc` (Python 3.12)
- `cpython-311.pyc` (Python 3.11)
- Team members with different Python versions will have conflicts

**Example Problem:**
```bash
# Developer A (Python 3.12) commits:
git add __pycache__/utils.cpython-312.pyc

# Developer B (Python 3.11) pulls and runs:
python app.py  # Generates utils.cpython-311.pyc
git status     # Shows conflict - which version to commit?
```

**Correct Approach:**
```bash
# Only commit source:
git add utils.py

# Let each developer generate their own cache:
python app.py  # Auto-creates __pycache__/ locally
```

---

### 2. **Virtual Environments** (`venv/`, `.venv/`, `ENV/`)

**What they are:**
- Isolated Python environments with specific package versions
- Created with `python -m venv .venv`
- Contains thousands of files (Python interpreter copy + all installed packages)

**Why exclude them:**

❌ **Massive Size:**
```
.venv/
├── Lib/
│   └── site-packages/
│       ├── pandas/           # ~50 MB
│       ├── numpy/            # ~30 MB
│       ├── requests/         # ~5 MB
│       └── [hundreds more]
├── Scripts/
│   ├── python.exe           # ~15 MB (copy of Python)
│   └── [executables]
└── [Total: 200+ MB]

# Compare to:
requirements.txt             # 2 KB
```

❌ **Violates DRY:**
Instead of committing the entire venv (200+ MB), commit a **recipe** to recreate it:
```txt
# requirements.txt (the DRY way)
pandas==2.1.0
numpy==1.24.3
requests==2.31.0
```

Anyone can recreate the exact environment:
```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt  # Regenerates everything
```

❌ **Platform-Specific:**
```
# Windows venv:
.venv/Scripts/python.exe         # Windows executable
.venv/Scripts/activate.bat       # Windows batch script

# Linux/Mac venv:
.venv/bin/python                 # Unix executable
.venv/bin/activate               # Unix shell script
```

Committing venv would break cross-platform collaboration.

**Example Problem:**
```bash
# Developer A (Windows) commits venv:
git add .venv/  # 200 MB upload

# Developer B (Mac) pulls:
.venv/Scripts/python.exe  # Error: not executable on Mac
```

**Correct Approach:**
```bash
# Commit the recipe only:
git add requirements.txt

# Each developer creates their own venv:
python -m venv .venv
pip install -r requirements.txt
```

---

### 3. **Build Artifacts** (`build/`, `dist/`, `*.egg-info/`)

**What they are:**
- Output from packaging/building your project
- Created by `python setup.py build` or `pip install -e .`
- Contain compiled code and metadata

**Why exclude them:**

❌ **Regenerable from Source:**
```bash
# Source (what you commit):
pyproject.toml
setup.py
src/
  mypackage/
    __init__.py
    utils.py

# Build artifacts (auto-generated):
build/
  lib/
    mypackage/  # Copy of your source
dist/
  mypackage-1.0.0.tar.gz  # Packaged version
mypackage.egg-info/  # Metadata
```

The build outputs are **derived** from your source code. Anyone can rebuild:
```bash
python -m build  # Regenerates build/, dist/, and .egg-info/
```

❌ **Violates Single Responsibility:**
- Repository = source code storage
- Build system = artifact generation
- These are separate concerns

**Example - NPM Analogy:**
```javascript
// package.json (source - commit this)
{
  "name": "my-app",
  "dependencies": {
    "react": "^18.0.0"
  }
}

// node_modules/ (generated - exclude this)
node_modules/
  react/
    [thousands of files]
```

Same principle: commit the recipe (`package.json`), not the artifacts (`node_modules/`).

---

### 4. **IDE Configuration** (`.vscode/`, `.idea/`, `*.swp`)

**What they are:**
- Personal editor settings and workspace state
- Example: VS Code settings, IntelliJ project files, Vim swap files

**Why exclude them:**

❌ **Personal Preferences:**
```json
// .vscode/settings.json
{
  "editor.fontSize": 14,           // Alice likes small fonts
  "editor.tabSize": 2,              // Alice uses 2-space tabs
  "python.linting.enabled": false   // Alice disabled linting
}

// Bob's preferences:
{
  "editor.fontSize": 18,           // Bob needs larger fonts
  "editor.tabSize": 4,              // Bob uses 4-space tabs (PEP 8)
  "python.linting.enabled": true   // Bob wants linting
}
```

Committing IDE settings forces **your preferences on the team**.

❌ **Tool-Specific:**
Different team members use different tools:
- Alice uses VS Code → `.vscode/`
- Bob uses PyCharm → `.idea/`
- Carol uses Vim → `*.swp`

Why commit all three IDE configs? Each developer should configure their own tool.

**Exception - Project-Wide Standards:**
Some teams *do* commit shared IDE settings for consistency:
```json
// .vscode/settings.json (shared team standard)
{
  "python.linting.pylintEnabled": true,  // Enforce linting
  "editor.formatOnSave": true,           // Auto-format on save
  "[python]": {
    "editor.tabSize": 4                  // PEP 8 standard
  }
}
```

This is acceptable when it enforces **project standards**, not personal preferences.

---

### 5. **Operating System Files** (`.DS_Store`, `Thumbs.db`)

**What they are:**
- Hidden files created by operating systems
- `.DS_Store` (Mac): Folder view settings
- `Thumbs.db` (Windows): Thumbnail cache

**Why exclude them:**

❌ **Platform-Specific:**
```bash
# Mac developer commits:
.DS_Store  # Contains Mac-specific folder metadata

# Windows developer has no .DS_Store, gets this unnecessary file
# Linux developer also confused by Mac metadata
```

❌ **No Code Value:**
These files contain UI preferences (icon positions, view modes), not code logic.

**Example Problem:**
```bash
# Every Mac user commits .DS_Store:
project/
  .DS_Store
  src/
    .DS_Store
    utils/
      .DS_Store

# Result: Dozens of useless files in repo
```

---

### 6. **Logs and Temporary Files** (`*.log`, `logs/`, `*.tmp`)

**What they are:**
- Runtime output and temporary data
- Created during development/testing

**Why exclude them:**

❌ **Runtime Artifacts:**
```python
# Your code generates logs:
import logging
logging.basicConfig(filename='app.log')
logger.info("Started processing")  # Writes to app.log

# app.log content (runtime artifact):
2025-12-06 10:23:45 - Started processing
2025-12-06 10:23:46 - Processed 100 records
2025-12-06 10:23:47 - Error: connection timeout
```

Logs are **outputs** of running your code, not the code itself.

❌ **Contain Sensitive Data:**
```log
2025-12-06 10:30:12 - User login: alice@example.com
2025-12-06 10:30:15 - API Key: sk_live_abc123...
2025-12-06 10:30:18 - Database query: SELECT * FROM users WHERE email='alice@example.com'
```

Committing logs can leak credentials, PII, or debug information.

❌ **Bloat Repository:**
```bash
# Log file grows over time:
app.log      # Day 1:   50 KB
app.log      # Day 30:  15 MB
app.log      # Day 365: 180 MB
```

Git tracks **every version** of committed files. A large log file committed daily bloats the repo.

---

### 7. **Test Coverage Reports** (`.coverage`, `htmlcov/`)

**What they are:**
- Reports showing which lines of code are tested
- Generated by `pytest --cov`

**Why exclude them:**

❌ **Regenerable:**
```bash
# Run tests to regenerate:
pytest --cov=mypackage --cov-report=html

# Generates:
.coverage         # Coverage data
htmlcov/          # HTML report
  index.html
  [many files]
```

Coverage reports are **derived** from running tests. Anyone can regenerate them.

❌ **Local Results:**
```
Developer A's coverage: 85%  # They haven't written all tests yet
Developer B's coverage: 92%  # They wrote more tests

# Which coverage report to commit? Neither - let CI/CD generate it
```

**Correct Approach:**
```yaml
# .github/workflows/test.yml (CI generates coverage)
- name: Run tests with coverage
  run: pytest --cov=mypackage --cov-report=xml
- name: Upload to Codecov
  uses: codecov/codecov-action@v3
```

Let the CI system generate and track coverage centrally.

---

## ✅ What *Should* Be Committed

### Source Code
```
✓ *.py              # Python source files
✓ *.js, *.ts        # JavaScript/TypeScript
✓ *.sql             # SQL scripts
✓ *.md              # Documentation
✓ *.yaml, *.json    # Configuration files
```

### Dependency Declarations
```
✓ requirements.txt   # Python dependencies
✓ package.json       # Node.js dependencies
✓ Pipfile            # Pipenv dependencies
✓ pyproject.toml     # Modern Python projects
```

### Project Configuration
```
✓ .gitignore         # Git exclusions
✓ .editorconfig      # Cross-editor standards
✓ pytest.ini         # Test configuration
✓ .flake8            # Linting rules
```

### Documentation
```
✓ README.md          # Project overview
✓ LICENSE            # Legal terms
✓ CONTRIBUTING.md    # Contribution guide
✓ docs/              # Documentation files
```

---

## 🚫 Common Mistakes

### Mistake 1: Committing `.env` Files
```bash
# .env (NEVER COMMIT THIS!)
DATABASE_URL=postgresql://user:password@localhost/db
API_KEY=sk_live_abc123xyz789
SECRET_KEY=super-secret-value-do-not-share
```

**Why it's bad:**
- Exposes secrets to everyone with repo access
- Secrets become part of Git history (hard to remove)
- Different environments need different values

**Correct Approach:**
```bash
# .env.example (commit this template)
DATABASE_URL=postgresql://user:password@localhost/db
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# .env (each developer creates locally)
DATABASE_URL=postgresql://alice:alicepass@localhost/mydb
API_KEY=sk_test_alice123
SECRET_KEY=alice-local-secret
```

### Mistake 2: Committing Large Binary Files
```bash
# DON'T:
git add dataset.csv        # 500 MB
git add model.pkl          # 200 MB
git add video_demo.mp4     # 1 GB
```

**Why it's bad:**
- Bloats repository size permanently
- Slows down clones for everyone
- Git is optimized for **text files**, not binaries

**Correct Approach:**
```bash
# Use Git LFS for large files:
git lfs track "*.csv"
git lfs track "*.pkl"

# Or store externally:
# dataset.csv → S3, Google Drive, DVC
# Reference in README with download instructions
```

---

## 📚 Summary: The Golden Rules

1. **Only commit source code** - not derived artifacts
2. **Commit recipes, not results** - `requirements.txt`, not `venv/`
3. **Keep secrets out** - use `.env.example`, not `.env`
4. **Respect personal preferences** - exclude IDE configs
5. **Think cross-platform** - exclude OS-specific files
6. **Keep repos small** - exclude large binaries
7. **Regenerate, don't commit** - logs, cache, builds

---

## 🔍 Quick Decision Tree

```
Should I commit this file?
│
├─ Is it source code? (*.py, *.js, etc.)
│  └─ YES → Commit it ✓
│
├─ Can it be regenerated from source?
│  └─ YES → Exclude it ✗ (.pyc, venv/, build/)
│
├─ Is it a secret or credential?
│  └─ YES → Exclude it ✗ (.env, *.key)
│
├─ Is it a personal preference?
│  └─ YES → Exclude it ✗ (.vscode/, .idea/)
│
├─ Is it platform-specific?
│  └─ YES → Exclude it ✗ (.DS_Store, Thumbs.db)
│
├─ Is it a runtime artifact?
│  └─ YES → Exclude it ✗ (*.log, *.tmp)
│
└─ Is it a dependency declaration?
   └─ YES → Commit it ✓ (requirements.txt, package.json)
```

---

*Last Updated: December 6, 2025*
