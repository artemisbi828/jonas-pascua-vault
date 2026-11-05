> **Stop narrating how the data came to be.  
> Start defining what this thing _is_, why it exists, and how it should be used.**

Your originals weren’t _wrong_ — they were **human explanations**.  
I reformulated them into **system definitions**.


# Explaining A Tool

## **Why Docling Failed**

**Root Cause:** Windows symlink permissions error (`OSError: [WinError 1314]`)

**Details:**

- Docling uses HuggingFace Hub to download ML models (~200 MB)
- HuggingFace cache defaults to creating **symlinks** for efficient storage
- Windows requires **Administrator privileges** to create symlinks
- Your user account lacks these rights → installation/execution failed

**Why We Switched to PyMuPDF:**

- ✅ No symlinks/admin rights needed
- ✅ Lighter weight (~70 MB vs ~200 MB)
- ✅ No ML model downloads
- ❌ Less intelligent structure detection (but we're now parsing raw text)

---
