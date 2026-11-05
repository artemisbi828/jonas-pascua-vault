

```
[^A-Za-z]       # select all numeric chars
^[0-9]+$        # get numeric, one or more digits `[0-9]+` $ → end of line 

s$              # get all objects that end with `s` and the end of the line
^\s+            # get all leading spaces at start of line, `\s` non-white space `+` 1+ instance
```

| ^           | beginning of line      |
| ----------- | ---------------------- |
| $           | end of line            |
| +           | more than one instance |
| [A-Za-z]    | alphaB                 |
| `[^A-Za-z]` | non-alphaB             |


---
[[REGEX - Obsidian - Find and Replace]]
[[REGEX - get A45 or TC45]]
[[REGEX - From DblQuote to DblQuote]]
[[REGEX - Remove Pound, Asterisk, Dash, Double Spaces]]

# ⚡ Quick Regular Expression (Regex) Cheat Sheet

Regular expressions are patterns used to match character combinations in strings.

| **Pattern**                            | **Description**                                                       | **Example Match**                             |
| -------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------- |
| **Basic Characters**                   |                                                                       |                                               |
| `.`                                    | Matches **any single character** (except newline).                    | `c` in `cat`                                  |
| `[abc]`                                | Matches any **one of the characters** in the set.                     | `a`, `b`, or `c`                              |
| `[^abc]`                               | Matches any character **NOT** in the set.                             | `d` in `dog`                                  |
| `[a-z]`                                | Matches any character in the **range** (e.g., lowercase letters).     | `k` in `king`                                 |
| **Quantifiers (How Many)**             |                                                                       |                                               |
| `*`                                    | Matches **0 or more** of the preceding element.                       | `a` in `b`, `a` in `cat`, `aaaa` in `aaaat`   |
| `+`                                    | Matches **1 or more** of the preceding element.                       | `at` in `cat`, `aa` in `baaab`                |
| `?`                                    | Matches **0 or 1** of the preceding element (makes it optional).      | `colou` in `color` or `colour`                |
| `{n}`                                  | Matches **exactly $n$** of the preceding element.                     | `a{3}` matches `aaa`                          |
| `{n,m}`                                | Matches **between $n$ and $m$** (inclusive) of the preceding element. | `a{2,4}` matches `aa`, `aaa`, or `aaaa`       |
| **Metacharacters (Special Sequences)** |                                                                       |                                               |
| `\d`                                   | Matches a **digit** (0-9).                                            | `5` in `v5`                                   |
| `\w`                                   | Matches a **word character** (a-z, A-Z, 0-9, and underscore `_`).     | `f` in `file`                                 |
| `\s`                                   | Matches a **whitespace character** (space, tab, newline).             | `sp` or `tab` in `hi there`                   |
| `\D`                                   | Matches a **non-digit**. (Opposite of `\d`).                          | `v` in `v5`                                   |
| `\W`                                   | Matches a **non-word character**. (Opposite of `\w`).                 | `!` in `hello!`                               |
| `\S`                                   | Matches a **non-whitespace character**. (Opposite of `\s`).           | `h` in `hi there`                             |
| **Anchors (Position)**                 |                                                                       |                                               |
| `^`                                    | Matches the **start** of the string.                                  | `^cat` matches `catdog` but not `dogcat`      |
| `$`                                    | Matches the **end** of the string.                                    | `cat$` matches `dogcat` but not `catdog`      |
| `\b`                                   | Matches a **word boundary**.                                          | `\bcat\b` matches `cat` but not `caterpillar` |
| **Grouping and Alternatives**          |                                                                       |                                               |
| `( )`                                  | **Groups** patterns and creates a captured group.                     | `(ab)+` matches `ab`, `abab`, etc.            |
| `(a\|b)`                               | Matches **either** pattern `a` or pattern `b`.                        | `(cat\|dog)` matches `cat` or `dog`           |

---
