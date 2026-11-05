---
definition: a way to _describe math with text_, so computers can render it beautifully.
---


**TL;DR (EIL5)**

- **LaTeX** is a way to _describe math with text_, so computers can render it beautifully.
- It was made for scientists/engineers to write formulas reliably and consistently.
- **Obsidian works** because it supports **MathJax/KaTeX** (math renderers).
- **Azure DevOps doesn’t** because its Markdown renderer **does not support LaTeX math**.
- **There is no native fix** in Azure DevOps today—only workarounds.

---



## What is LaTeX syntax? (EIL5)

Imagine telling a computer:

> “This is a fraction. Put ρ·v·L on top, μ on the bottom.”

Instead of drawing it by hand, you **describe** it with text:

# 3 Ways

Re = (ρ · v · L) / μ


$$ \frac{ \text{Contract Starts from Start Needed Status} }{ \text{Dismissed NPE Resulting in Start Needed Status} } $$

$$ {Start Needed Recapture Rate} = \frac{\mathrm{Contract\ Starts}} {\mathrm{Dismissed\ NPEs}} $$



```latex
$$ {Start Needed Recapture Rate} = \frac{\mathrm{Contract\ Starts}} {\mathrm{Dismissed\ NPEs}} $$

$
Re = \frac{\rho v L}{\mu}
$
```

$$ {Conversion Rate} = \frac{\mathrm{3\ Contract\ Starts (True: 1)}} {\mathrm{1\ NPE\ Dismissed}} = 3  $$
LaTeX is:

- **A markup language** (like HTML, but for documents and math)
- **Declarative**: you say _what_ something is, not _how_ to draw it
- Especially great at **math, symbols, and equations**

Result (when supported):

Re=ρvLμRe = \frac{\rho v L}{\mu}

---

## Tiny historical context (why it exists)

- **Donald Knuth** (1970s) created **TeX** to typeset math properly for books.
- **LaTeX** (Lamport TeX, 1980s) wrapped TeX so normal humans could use it.
- It became the **de facto standard** for:
    - Scientific papers
    - Engineering formulas
    - Academic publishing

Key idea:

> _Math should look correct everywhere, forever._

---

## Why it’s useful (especially for you)

LaTeX math:

- ✅ Is **platform‑independent**
- ✅ Is **unambiguous** (great for specs & governance)
- ✅ Scales from quick notes → peer‑reviewed papers
- ✅ Is readable _as text_ **and** beautiful when rendered

This is why tools like:

- Obsidian
- Jupyter
- Notion
- GitHub (partially)

…support it.

---

## Why it works in **Obsidian** but NOT in **Azure DevOps**

### Obsidian

- Uses **MathJax / KaTeX**
- Explicitly supports:
    - Inline math: `$x^2$`
    - Block math: `$ ... $`
- Actively renders LaTeX expressions

### Azure DevOps Markdown

- Uses a **restricted CommonMark renderer**
- **Does NOT include a math engine**
- Treats `$ ... $` as plain text

So Azure DevOps sees this:

$Re = \frac{\rho v L}{\mu}$



…and says:

> “Cool story bro. I don’t know how to draw math.”

---

## Can LaTeX math be made to work in Azure DevOps?

### ❌ Native support

**No.**  
As of now, Azure DevOps **does not support LaTeX or MathJax** in:

- Wiki
- README.md
- PR descriptions
- Work items

Microsoft has intentionally kept the renderer minimal.

---

## ✅ Practical workarounds (ranked)

### ✅ 1. Render as an image (most reliable)

- Create the formula elsewhere (LaTeX → PNG/SVG)
- Embed it:

``

✅ Works everywhere  
❌ Loses editability/searchability

---

### ✅ 2. ASCII / pseudo‑math (engineering‑friendly)

For specs and governance docs:

✅ Fast  
✅ Readable  
✅ Diff‑friendly  
❌ Not pretty

---

### ✅ 3. Code block with LaTeX (documentation intent only)

Useful when the _definition_ matters more than rendering:

```latex
Re = \frac{\rho v L}{\mu}
```


✅ Preserves canonical math definition  
✅ Copy‑pasteable  
❌ Still not rendered

---

### ⚠️ 4. Link out

Store math‑heavy docs in:

- Obsidian
- GitHub
- PDF Then link from Azure DevOps.

✅ Clean separation  
❌ Context switch for readers

---

## Executive‑level takeaway

- **LaTeX ≠ Markdown**
- LaTeX math requires a **math rendering engine**
- **Obsidian has one; Azure DevOps does not**
- This is a **platform limitation**, not user error
- Use **images or ASCII math** in ADO; keep canonical math elsewhere

If you want, I can:

- Give you an **ADO‑safe math style guide**
- Produce **SVG equations** optimized for wiki embedding
- Recommend a **single‑source‑of‑truth pattern** (Obsidian ↔ ADO)