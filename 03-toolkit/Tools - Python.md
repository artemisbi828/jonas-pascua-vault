---
aliases:
  - Python
---
[[Tools - Comment Blocks]]
[[Python - Data Structures]]
[[Python - Try, If, Except]]
[[Python - VENV]]


2026-06-29 06:11 PM
```
initialize python by typing `python`
exit powershell -- `ctrl+c`
exit python -- `exit` or `exit()`
# verify library.dateutil installed
from dateutil.relativedelta import relativedelta

---
from datetime import datetime
from dateutil.relativedelta import relativedelta

pairs = [
("2025-11-26 10:00:00.000","2026-06-09 10:30:00.000"),
("2025-11-13 13:10:00.000","2026-05-29 11:00:00.000"),
("2025-12-09 15:55:00.000","2026-06-22 14:45:00.000"),
("2025-12-08 10:00:00.000","2026-06-15 10:45:00.000"),
("2025-12-03 14:50:00.000","2026-06-18 15:50:00.000"),
("2025-11-19 14:45:00.000","2026-06-10 09:15:00.000"),
("2025-11-12 11:00:00.000","2026-06-24 15:00:00.000"),
("2025-11-10 10:30:00.000","2026-05-22 09:30:00.000"),
("2025-12-08 15:00:00.000","2026-06-23 16:15:00.000"),
("2025-12-08 11:00:00.000","2026-06-15 09:45:00.000"),
("2025-11-21 10:45:00.000","2026-06-18 15:30:00.000"),
("2025-11-10 07:20:00.000","2026-06-09 07:10:00.000"),
("2025-12-10 11:00:00.000","2026-06-23 10:40:00.000"),
]

for start, end in pairs:
    s = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
    e = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")

    rd = relativedelta(e, s)

    print(
        f"{start} -> {end} = "
        f"{rd.years*12 + rd.months} months, {rd.days} days"
    )
    
---
from datetime import datetime
from dateutil.relativedelta import relativedelta

start = datetime(2025,11,26,10,0,0)
end   = datetime(2026,6,9,10,30,0)

target = start + relativedelta(months=6)

print("6 month anniversary:", target)
print("Days from anniversary:", (end.date() - target.date()).days)
```



[Package Manager] is [Pip] vs [uv]

```
"""
This is a multi-line block
"""
```





#status/deferred/quick-paste-merge-later 
```
sqlpolyglot
sql-parse
```

That's a great question about a crucial part of managing Python projects!

The `-r` in the command `pip install -r requirements.txt` stands for **requirements file**.

It instructs `pip` to **read and install** all the packages listed line-by-line within the specified file, which is `requirements.txt` in this case.

---

## 💡 Finding Definitions (Help) for `pip` and Python

When you need to know what a flag like `-r` means, or to see the full list of options for a command, you use built-in help features.

### 1. Using `pip`'s Built-in Help

`pip` has a very comprehensive help system built right into the command line.

- **To get general help for `pip`:**

    Bash

```
pip --help
# OR
pip -h
```
    
- **To get specific help for the `install` command (which contains the definition for `-r`):**

    Bash

```
pip install --help
```

    This command will dump a long list of all available options for installing packages, including flags for requirements files, version control systems, and dependency resolution.
    

### 2. Using Python's Built-in Help

The `python` command itself doesn't have a single "help" file for all its flags like `pip` does, but you can find its main options easily:

- **To get help on the Python interpreter executable:**

    Bash

    ```
    python3 --help
    # OR
    python3 -h
    ```

    This will show you common options like running a module with `-m` or optimizing with `-O`.
    

### 3. Using Linux Manual Pages (`man`)

For nearly any command in Linux (including `pip` and `python3`, provided their manual pages are installed), you can use the `man` command (short for manual):

- **Command:**

    Bash

    ```
    man pip
    # OR
    man python3
    ```

    This opens the command's official, comprehensive documentation (the "man page") in a pager like `less`, allowing you to search and scroll through all the details.