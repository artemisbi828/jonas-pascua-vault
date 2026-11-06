Remove a category visually without affecting the proportion calc
## Before
    Channel        | Show-Up Rate
    ---------------+--------------
    Other          | 38.9%
    Non-Digital    | 65.5%
    Digital        | 75.5%
    ---------------+--------------
    Total          | 66.0%
    
## After
    Channel        | Show-Up Rate
    ---------------+--------------
    Non-Digital    | 65.5%
    Digital        | 75.5%
    ---------------+--------------
    Total          | 66.0%
    

Power BI evaluates the measure **once per row**, and **once again for the Total**.

👉 **Key insight:**  
The Total row is **not “in scope”** of the Channel column.


```dax
NPE Show-Up Rate (Hide Other) =
VAR _isRow = ISINSCOPE('Channel'[ChannelGroup])
VAR _cat   = SELECTEDVALUE('Channel'[ChannelGroup])
RETURN
    IF(
        _isRow && _cat = "Other",
        BLANK(),
        [NPE Show-Up Rate]
    )
```

---

When Power BI evaluates a measure, it always asks two questions:

1.  **“At what level am I being evaluated right now?”**  
    (row? total? subtotal? filtered context?)
2.  **“Is there exactly one value for this column right now?”**

*   **`ISINSCOPE()`** answers **Question #1**
*   **`SELECTEDVALUE()`** answers **Question #2**

They are often used together because:

> *“If I’m on a specific row, then I can safely check which category this row represents.”*

***

# 1️⃣ `ISINSCOPE()` — “Am I on a row, or on the total?”

### Plain‑English definition

> **`ISINSCOPE(Column)` tells you whether Power BI is currently evaluating the measure at the level of that column.**

In simpler terms:

*   ✅ **TRUE** → “I am looking at a specific row for this column”
*   ❌ **FALSE** → “I am at a higher level (Total / subtotal / not grouped by this column)”

***

### What `ISINSCOPE(Channel)` returns:

| Where the measure is evaluated | `ISINSCOPE(Channel)` |
| ------------------------------ | -------------------- |
| Other row                      | TRUE                 |
| Non-Digital row                | TRUE                 |
| Digital row                    | TRUE                 |
| Total row                      | FALSE                |


Without `ISINSCOPE()`, Power BI cannot tell:

*   “Am I allowed to apply row-level logic?”
*   “Should I behave differently for totals?”

This is **the** function that lets you say:

> “Do this only on individual rows — not on totals.”

***

# 2️⃣ `SELECTEDVALUE()` — “What single value am I on (if any)?”

### Plain‑English definition

> **`SELECTEDVALUE(Column)` returns the value if there is exactly one value in the current filter context; otherwise it returns BLANK (or a default).**

Think of it as:

> “Tell me the category name — but only if there’s just one.”

***

## Examples

### Example A: On a row

When Power BI is evaluating the **Digital** row:

```DAX
SELECTEDVALUE(Channel[ChannelGroup])
```

✅ Returns:

    "Digital"

Because:

*   The filter context contains exactly **one** Channel value

***

### Example B: On the Total row

On the **Total** row:

```DAX
SELECTEDVALUE(Channel[ChannelGroup])
```

❌ Returns:

    BLANK()

Because:

*   The Total includes **multiple Channel values**
*   There is no single selected value

***

## Why not just use `VALUES()`?

You *could*, but:

*   `VALUES()` returns a **table**
*   `SELECTEDVALUE()` returns a **scalar**
*   Measures need scalars for logic like `IF()`

So `SELECTEDVALUE()` is the safe, clean choice.

***

# 3️⃣ Why they’re powerful **together**

Let’s look at the exact pattern you used:

```DAX
VAR _isRow = ISINSCOPE(Channel[ChannelGroup])
VAR _cat   = SELECTEDVALUE(Channel[ChannelGroup])
```

### What this says in English:

*   `_isRow` → “Am I on an individual channel row?”
*   `_cat` → “If yes, which channel is this?”

Now the logic becomes safe:

```DAX
IF(
    _isRow && _cat = "Other",
    BLANK(),
    [Base Measure]
)
```

### Why this works perfectly

*   On the **“Other” row**:
    *   `_isRow = TRUE`
    *   `_cat = "Other"`
    *   → Return BLANK → row disappears
*   On **Non‑Digital / Digital**:
    *   `_isRow = TRUE`
    *   `_cat ≠ "Other"`
    *   → Show value
*   On **Total**:
    *   `_isRow = FALSE`
    *   Condition fails
    *   → Return base measure → **Total stays 66.0%**

✅ This is why your total did **not** change  
✅ This is why the solution is considered best practice

***

# 4️⃣ Common mistakes this avoids

### ❌ Mistake 1: Filtering out “Other”

```DAX
CALCULATE([Measure], Channel <> "Other")
```

*   Removes “Other” from filter context
*   Total recalculates
*   ❌ Wrong for your requirement

***

### ❌ Mistake 2: Checking category without scope

```DAX
IF(SELECTEDVALUE(Channel)="Other", BLANK(), [Measure])
```

*   Works on rows
*   But Total also sees BLANK()
*   ❌ Breaks totals

***

# 5️⃣ Simple rule of thumb (remember this)

> **If you need different behavior for rows vs totals → use `ISINSCOPE()`**  
> **If you need to know which value a row represents → use `SELECTEDVALUE()`**

Most advanced Power BI measures follow this pattern.

***

# 6️⃣ One more intuitive analogy (real-world)

Imagine a spreadsheet:

*   Each row is a **person**

*   The total row is **“Everyone”**

*   `ISINSCOPE(Person)` asks:
    > “Am I talking about one person, or the whole group?”

*   `SELECTEDVALUE(Person)` asks:
    > “If it’s one person… who is it?”

You would never ask “Who is it?” unless you already knew you were talking about one person — and that’s exactly why these two functions pair so well.

***

If you want, next I can:

*   Show **how this pattern generalizes** to % of total, YoY, hiding rows, or conditional formatting
*   Explain how this differs from `HASONEVALUE()` (closely related, but not identical)
*   Walk through a **debug version** using cards so you can *see* the context change live

Just tell me which direction you want to go.
