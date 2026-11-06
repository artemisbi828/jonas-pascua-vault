```
-- Run this in DAX Query View to see all your hard work
EVALUATE
FILTER(
    SELECTCOLUMNS(
        INFO.MEASURES(),
        "Measure", [Name],
        "Definition", [Description]
    ),
    NOT(ISBLANK([Definition]))
)
```