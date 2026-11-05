### 1. Removing Special Characters

Use the following regex and replace the matches with an **empty string** (`""`).

- **Regex:** `[#*-]`
- **Action:** Replace with `""` (empty string)

This regex uses a **character set** (`[]`) to match any single occurrence of the characters listed inside: a literal `#`, a literal `*`, or a literal `-`.

**Example:**

|**Original String**|**Regex Application ([#*-])**|**Resulting String**|
|---|---|---|
|`We built a **Client Portal Bridge** using Streamlit.`|`**` and `**` are matched and removed.|`We built a Client Portal Bridge using Streamlit.`|
|`* Features: # File Drop - Upload files`|`*`, `#`, and `-` are matched and removed.|`Features: File Drop Upload files`|

---

### 2. Removing Double Spaces (and greater)

After cleaning the special characters, use this regex to ensure only single spaces remain.

- **Regex:** `\s{2,}`
- **Action:** Replace with a **single space** (`" "`)
- **`\s`**: Matches any **whitespace character** (including space, tab, newline).
- **`{2,}`**: Is a **quantifier** that matches the preceding element (`\s`) **two or more** times.

**Example:**

|**Original String (from Step 1)**|**Regex Application (\s{2,})**|**Resulting String**|
|---|---|---|
|`We built a Client Portal Bridge using Streamlit.`|No match (no double spaces).|`We built a Client Portal Bridge using Streamlit.`|
|`Features: File Drop Upload files`|The double spaces are matched.|`Features: File Drop Upload files`|
In regular expressions, the comma followed by nothing in a quantifier like $\text{`{2,}`}$ is a shorthand notation that signifies the **minimum number of repetitions** without setting a **maximum**.

Here is a breakdown of why this notation is used:

## 🔢 Understanding Regex Quantifiers

The curly braces $\text{`{ }`}$ are used for **precise repetition** (quantifiers) of the preceding element (a character, a character set, or a group). The general syntax is $\text{`{min,max}`}$.

### 1. The Standard Syntax: $\text{`{min,max}`}$

- $\text{`{2,5}`}$ means the preceding element must appear a **minimum of 2** times and a **maximum of 5** times.
    
    - _Example:_ $\text{`a{2,5}`}$ matches $\text{`aa`}$, $\text{`aaa`}$, $\text{`aaaa`}$, or $\text{`aaaaa`}$.
        

---

### 2. The Shorthand: $\text{`{min,}`}$

When you write $\text{`{2,}`}$, it means:

- **Minimum Repetitions:** **2** (The number before the comma).
- **Maximum Repetitions:** **No Limit** or **Infinite** (The absence of a number after the comma).

This makes the expression **greedy** and tells the regex engine to match the element at least the minimum number of times, and then to continue matching it as many times as possible until the end of the line or string (or until a subsequent pattern is satisfied).

|**Quantifier**|**Meaning**|**Example (‘a‘)**|**Matches**|
|---|---|---|---|
|$\text{`{2}`}$|Exactly 2 times|$\text{`a{2}`}$|$\text{`aa`}$|
|$\text{`{2,5}`}$|2 to 5 times|$\text{`a{2,5}`}$|$\text{`aa`}$ to $\text{`aaaaa`}$|
|$\text{`{2,}`}$|**2 or more** times|$\text{`a{2,}`}$|$\text{`aa`}$, $\text{`aaa`}$, $\text{`aaaa`}$, etc. (up to infinity)|

In your specific example, $\text{`\s{2,}`}$:

- $\text{`\s`}$ matches a **whitespace** character.
- $\text{`{2,}`}$ matches **2 or more** of the preceding element ($\text{`\s`}$).

This efficiently targets **double spaces, triple spaces, quadruple spaces, and so on**, allowing you to replace all of them with a single space to normalize the spacing in your text.