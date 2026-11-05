In Power BI (specifically Power Query/M), a **User-Defined Function (UDF)** is essentially a reusable "recipe." Instead of writing the same complex transformation logic (like your 364-day shift) inside every table, you write it once, name it, and call it like a standard tool (e.g., `Date.AddDays`).

### 1. What is a UDF in PBI?

In context of your current project, a UDF replaces **copy-pasted code**.

- **What it replaces:** It replaces the need to manually sync logic between your Fact table (`OfficeDayStats`) and your Dimension table (`Dates`). Without a UDF, if you change your shift logic from 364 days to 365, you'd have to remember to edit the code in both tables. With a UDF, you edit it once.
    
- **Utility:** It centralizes your "Source of Truth." It allows you to transform "as data comes in" by wrapping your SQL source inside the function.
    

---

### 2. Concrete Steps to Setup a UDF

We will turn your **364-Day Shift** logic into a function called `fnShiftDate`.

#### Step A: Create the "Brain" (The Function)

1. In Power BI, click **Get Data > Blank Query**.
    
2. Open the **Advanced Editor** and paste this:
    

Code snippet

```
(DateToShift as date, DaysToMove as number) as date =>
let
    ShiftedDate = Date.AddDays(DateToShift, DaysToMove)
in
    ShiftedDate
```

3. Rename this query to **fnShiftDate**. You will notice the icon changes to a "function" icon ($f_x$).
    

#### Step B: Create the "Anchor" (The Value)

Create another blank query named **GlobalShift** to calculate the shift amount based on your Fact table:

Code snippet

```
let
    Source = Sql.Database("ARTEMIS", "NVS", [Query="SELECT MAX(DateKey) as MaxDate FROM sdrs.vw_F_OfficeDayStats"]),
    FactMaxDate = Date.From(Source{0}[MaxDate]),
    Yesterday = Date.From(DateTime.LocalNow()) - #duration(1, 0, 0, 0),
    RawGap = Duration.Days(Yesterday - FactMaxDate),
    WeekAlignedShift = Number.RoundDown(RawGap / 7) * 7
in
    WeekAlignedShift
```

---

### 3. Usage & Testing

Now that you have the **Tool** (`fnShiftDate`) and the **Input** (`GlobalShift`), you can apply it to your Date table.

#### Step C: Implementation

Go to your `Dates` table query and use the function in a transformation step:

Code snippet

```
let
    Source = Sql.Database("ARTEMIS", "NVS", [Query="SELECT * FROM sdrs.vw_D_Dates"]),
    // Instead of writing logic here, we call our function and our global variable
    ApplyShift = Table.TransformColumns(Source, {
        {"DateKey", each fnShiftDate(_, GlobalShift), type date},
        {"EndOfMonth", each fnShiftDate(_, GlobalShift), type date}
    })
in
    ApplyShift
```

---

### 4. How to "Test Usage" to Understand Deeper

To truly master UDFs, test these three things:

1. **Test the Input:** Go to the **fnShiftDate** query. You will see an "Invoke" box. Type in a random date (e.g., `2022-01-01`) and a number (e.g., `364`). Click **Invoke**. It will create a new table showing the result. If the result is correct, your logic is sound.
    
2. **Test the Dependency:** Change the logic inside **fnShiftDate** (e.g., change `Date.AddDays` to `Date.AddMonths`). You will notice that _every_ table using that function updates instantly. This is the "Utility" in action.
    
3. **Test for "Dry" Type Casting:** You can modify the UDF to handle the type casting so you never have to manually reset the date fields again.
    

> **Revised UDF for "Clean" Types:**
> 
> Code snippet
> 
> ```
> (inputDate as any, days as number) as date => 
> Date.From(Date.AddDays(Date.From(inputDate), days))
> ```

---

### Why this is the "Best Approach"

By using a UDF combined with a Global Variable (`GlobalShift`):

- **Fact Table:** Call the function on your Fact table dates.
    
- **Date Table:** Call the function on your Date table dates.
    
- **Result:** They are mathematically guaranteed to stay in sync because they are drinking from the same straw.
    

**Would you like me to help you bundle the complex Year/Month label correction logic into a single "CleanLabels" UDF as well?**