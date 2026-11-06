### `CALCULATETABLE(...)` = “evaluate this table expression under modified filter context”

- `CALCULATETABLE` is like `CALCULATE`, but returns a **table** instead of a scalar.
- It takes your base table expression (`VALUES(DateKey)`) and then applies filter modifiers (your extra arguments) to change the context in which it’s evaluated.

SQL analogue: “wrap it in a query where you override / replace the WHERE clause logic”.