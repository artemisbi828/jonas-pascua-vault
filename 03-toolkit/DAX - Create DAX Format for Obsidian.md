#status/deferred/quick-paste-merge-later 

Codeblock Formatter

Obsidian does not have a dedicated, native "DAX Formatter" plugin (like the Prettier plugin for JavaScript) that runs automatically inside a code block. This is largely because the DAX language is niche compared to web development languages.

However, you can achieve a professional formatting workflow using a combination of existing tools or by building a custom "Formating Bridge."

---

## 1. The "Community" Workaround (Best for most users)

The most robust way to get DAX formatting in Obsidian right now is to use **Tabular Editor** as your engine and **Text Transporter** or **Templater** to bring it in.

### The "DAX Query" Syntax Highlighting

Obsidian uses **Prism.js** for code highlighting. To ensure your DAX looks correct, always use the `dax` identifier:

```markdown
```dax
EVALUATE
SUMMARIZECOLUMNS(
    'D_Dates'[YearMonth],
    "Total Sales", [Net Production TY]
)
```

```

---

## 2. How to Create a Custom DAX Formatter for Obsidian

If you want a one-click "Format my DAX" button inside Obsidian, you can build a bridge to the **DaxFormatter.com API** (by SQLBI) using the **Templater** plugin.

### Prerequisites

1. Install the **Templater** plugin.
2. Enable "User System Command Functions."

### The "Logic" Bridge

You can create a small script (Python or Node.js) that sits on your computer. When you trigger a hotkey in Obsidian, Templater sends your unformatted DAX to the script, the script calls the SQLBI API, and returns the formatted code.

**Step 1: Create a python script (`format_dax.py`):**

```python
import sys
import requests

def format_dax(dax_query):
    # This is a simplified example; SQLBI API requires an API key for high volume
    url = "https://www.daxformatter.com/api/daxformatter/format"
    payload = {"Dax": dax_query, "ListSeparator": ",", "DecimalSeparator": "."}
    response = requests.post(url, json=payload)
    return response.json().get("FormattedDax", dax_query)

if __name__ == "__main__":
    input_dax = sys.stdin.read()
    print(format_dax(input_dax))

```

**Step 2: Create a Templater Template:**
Create a new file called `Format DAX` in your templates folder:

```javascript
<%*
const selection = tp.file.selection();
const formatted = await tp.user.format_dax_cmd({input: selection});
const output = "```dax\n" + formatted + "\n```";
tR += output;
%>

```

---

## 3. The "Styling" Fix (CSS Snippets)

If you just want the *visuals* of the code block to look more like Power BI or DAX Studio, you can add a **CSS Snippet** to Obsidian.

1. Go to `Settings > Appearance > CSS Snippets`.
2. Create a file named `dax-style.css`:

```css
/* Custom highlighting for DAX functions in code blocks */
.language-dax .token.function {
    color: #02599d; /* Power BI Blue */
    font-weight: bold;
}
.language-dax .token.keyword {
    color: #af5700; /* Evaluation keywords */
}
.language-dax .token.string {
    color: #228b22; /* Table/Column references */
}

```

---

## 4. Obsidian Cheat Sheet: DAX Documentation Tips

Since you are building a vault for your Power BI project, use these Markdown tricks to make your DAX notes more readable:

| Feature | Markdown Syntax | Use Case |
| --- | --- | --- |
| **Callouts** | `> [!NOTE]` | To explain the "Why" behind a measure. |
| **Footnotes** | `[^1]` | To reference SQL sources or View names. |
| **Internal Links** | `[MeasureName]` | To link to related measures (Measure Branching). |
| **Backlinks** | Linked Mentions | To see every report page using a specific column. |

### The "Modern Robust" Recommendation

For your 2026 project, the most efficient way to maintain DAX in Obsidian is:

1. Write and format your DAX in **Tabular Editor** (it has a built-in formatter).
2. Copy and paste into Obsidian using the ````dax` block.
3. Use the **Dataview** plugin to automatically generate a table of all the measures you've documented in your vault.

**Would you like me to write a Dataview query that lists all your documented measures and their status (e.g., "In Progress" vs "Production")?**