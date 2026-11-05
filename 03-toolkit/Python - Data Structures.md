Here is your Python data structures guide, optimized for Obsidian with callouts, proper code syntax highlighting, and a clean layout.

Lorem (...) epi
# Learning
2026-04-10 01:37 PM
```
# JSS (Jonas Style Sheet)
all equal := {a, b, c, d} 
ordered, mutable := [a,b]
ordered, immutable := (a,b)
key-value pairs := { a: b,c,d }

```

# 🐍 Python Data Structures: Quick Reference

> [!abstract] Overview
> 
> | Structure | Syntax | Mutable? | Ordered? | Duplicates? | Access Method |
> | :--- | :--- | :--- | :--- | :--- | :--- |
> | List | [1, "a"] | Yes | Yes | Yes | list[0] (Index) |
> | Tuple | (1, "a") | **No** | Yes | Yes | tuple[0] (Index) |
> | Set | {1, "a"} | Yes | **No** | **No** | "a" in set (Check) |
> | Dictionary | {"k": 1} | Yes | Yes* | Keys: No | dict["k"] (Key) |

* _Note: As of Python 3.7+, Dictionaries maintain insertion order. Sets remain unordered._

---
## 📋 List

The Go-To Collection

Use this for simple collections where order matters and you need to modify items (e.g., a to-do list or scores).

Python

```
# Creation
my_list = ["apple", "banana", 100, "apple"]

# Access (zero-based index)
print(my_list[1])  # Output: 'banana'

# Change an item
my_list[0] = "cherry" # ['cherry', 'banana', 100, 'apple']

# Add an item
my_list.append(200)   # ['cherry', 'banana', 100, 'apple', 200]
```

---

## 🔒 Tuple

The List of Constants

Use for data that should never change (coordinates, RGB values). It signals that the collection is constant and can be used as a Dictionary key.

> [!info] Immutability
> 
> Tuples cannot be changed after creation. This makes them safer for fixed data.

Python

```
# Creation
my_tuple = ("apple", "banana", 100, "apple")

# Access (same as a list)
print(my_tuple[1])  # Output: 'banana'

# Attempt to change (THIS WILL CAUSE AN ERROR)
# my_tuple[0] = "cherry"  # Raises a TypeError
```

---

## 💎 Set

The Unique Collection

Use when uniqueness is vital or when you need to check "is this item in here?" extremely fast.

Python

```
# Creation (duplicates are automatically removed)
my_set = {"apple", "banana", 100, "apple"}
print(my_set)      # Output: {100, 'banana', 'apple'}

# Add an item
my_set.add("cherry")

# Check for membership (High performance)
print("banana" in my_set)  # Output: True
```

---

## 📖 Dictionary

The Labeled Collection

Perfect for labeled data like user profiles or configuration settings.

> [!warning] Syntax Requirement
> 
> Dictionaries must use a colon : to separate keys from values and commas , between pairs.

Python

```
# Creation
my_dict = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Access (use the key name)
print(my_dict["name"])  # Output: 'Alice'

# Change a value
my_dict["age"] = 31

# Add a new key-value pair
my_dict["job"] = "Engineer"
```

---

.NET type (string, int, [bool], arrays: [string[]], custom types)

Hashtable is like Dictionary except

- PowerShell: A standard Hashtable (@{}) is unordered. If you put items in as A, B, C, they might come out as B, A, C. (To fix this in PowerShell, you must use [ordered]@{}).
- Powershell can save .NET objects -- like a running Process, a Service Controller, or a complex DateTime object while JSON is just text

- Get-Date -- is dynamic, when saved as JSON -- it dies and becomes static string