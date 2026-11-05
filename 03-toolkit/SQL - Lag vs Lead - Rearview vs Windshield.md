From Row.A, need something Row.B --> lead
From Row.B, need something from Row.A --> lag

Lag(5) -- from current row = 0, go 5 rows up
Lead(5) -- from current row = 0, go 5 rows down --> landing = value
Partition By -- same as where statement (dbl check by writing where statement for 1 case and review)
Order By -- how to determine the rows



> [!Example]
> Looking at rolling month forward, if there's more than a 1.5x spike → LAG. The numbers are lagging and we need to "pull" them forward. Vs we're looking at a future month forecast, and we need to pull that back. 

```sql
lag(MyColumn, 1, null) over (partition by a,b order by a) -- pulls data above forward
lead(MyColumn, 1, null) over (partition by a,b order by a) -- pulls data below → back 
```

# How to Remember
### 1. The "Windshield vs. Rearview" Mnemonic

Think of your data as a car you are driving through time:

* **LEAD is your Windshield:** You are looking **forward** at the road ahead. Use this when you want to "pull" a future value (like next month's sales) into your current row.
* **LAG is your Rearview Mirror:** You are looking **back** at the road you already traveled. Use this when you want to "pull" a past value (like last month's sales) into your current row.


---

### 3. The "Row Pointer" Logic

If you are writing SQL or Python, think of the function as a **lasso** you are throwing from your current row:

| Month | Sales | Function | Result (Sales pulled in) |
| --- | --- | --- | --- |
| January | 100 | `LEAD(Sales)` | **150** (reaches down to Feb) |
| February | **150** | `LAG(Sales)` | **100** (reaches up to Jan) |

* **LAG(1)** reaches **up** (backward in the index).
* **LEAD(1)** reaches **down** (forward in the index).

---

### Applying it to your 150% Sales Spike

Since you are looking at **"months forward"** to see if sales spike, you want to know what *will* happen while looking at your current month.

**Your Logic:**

> Is (Next Month's Sales) / (Current Month's Sales) > 1.50?

**The Tool:**
Because you need "Next Month," you use **LEAD**.

* **SQL:** `LEAD(sales, 1) OVER (ORDER BY month)`
* **Python (Pandas):** `df['sales'].shift(-1)` (Note: In Pandas, a negative shift is a "Lead").

**Would you like me to write a specific SQL query or Python snippet to help you calculate that 150% growth threshold?**