Related to: [[DAXM]], [[PBI]], [[DAXQ]], [TMDL]

# Freq
[[DAX - Ratios -- DIVIDE, YOY%]]
[[DAX - Dates Previous Year (PY or LY)]]
[[DAX - Force FORMAT()]]
[[DAX - FORMAT()]]
[[DAX - Rounding]]

# Dates
[[DAX - AsOfDate]]
[[DAX - DateValue]]
[[DAX - Create Measure between 2 Dates]]
[[DAX - DateDiff]]
[[DAX - Add WDE and Holiday Columns]]
[[DAX - Count Rows]]
[[DAX - Convert 2025-02-01 to 202502]]
[[DAX - Convert YEAR to TEXT]]
[[DAX - Dynamic Date Filter]]

# Create Tables
[[DAX - Create Tables]]
[[DAX - CALCULATETABLE]]
[[DAX - CALCULATE]]

# Add Columns
[[DAX - Add Column]]
# NEW Techniques
[[DAX - New Learning]]
[[DAX - TREATAS]]
[[DAX - ISINSCOPE, SELECTEDVALUE - Exclude Category or Dim]]
[[DAX - Calculation Groups]]
[[DAX - Calculation Groups - Shield]]
[[DAX - REMOVEFILTERS]]
[[DAX - KEEPFILTERS, CROSSFILTER]]
[[DAX - Create DAX Format for Obsidian]]

# Research
[[DAX - SQL → DAX Cheat Sheet]]
[[DAX - UDF (Research)]]
[PBI - Sankey Diagram (Waterfall Chart)]

# DEBUG
[[DAX - Debug Sort Column Issue]]
[DAX - Debug - CopyPaste but Object.Chart has Diff-X-Axis]


Choosing between DAX and Power Query is rarely about which one is "better" and more about **where** the logic should live in the data pipeline.

For your normalization project, you actually need **both**, but for very different reasons.

---

### DAX vs. Power Query: The Quick Comparison

| Feature | Power Query (M) | DAX (Measures) |
| --- | --- | --- |
| **When it runs** | During **Data Refresh** | Every time you **click a Slicer** |
| **Primary Goal** | Shaping, Cleaning, ETL | Analysis, Aggregation, Comparison |
| **Performance** | Makes the report **faster** (Pre-calculated) | Can make reports **laggy** (On-the-fly) |
| **Data Visibility** | Creates physical columns you can see | Returns a single value (in a card/chart) |
| **Storage** | Increases file size (adds a column) | Uses CPU/RAM (no physical storage) |

---

### In Your Case: The Specific Strategy

You should follow the **"Roche’s Maxim"** of data: *Transform data as far upstream as possible (Power Query), and as far downstream as necessary (DAX).*

#### 1. Use Power Query for the "Weight" Column

Because a specific date (e.g., MLK Day 2026) is *always* going to have a weight of 0, this is **static logic**. It doesn't change based on what a user clicks in your report.

* **For:** Adding the weight here means the calculation happens once during the night (at refresh). Power BI then compresses that column, making it extremely fast to sum up later.
* **Against:** If you have millions of dates, adding columns in Power Query can slightly increase your file size.

#### 2. Use DAX for the "Normalization" Measure

Normalization requires dividing your **Sales/Work** by the **Weight**. Because "Sales" changes based on which office, department, or product the user selects, this must be a DAX Measure.

* **For:** It reacts instantly to filters. If a user filters for "Office A," the DAX measure sums only the sales and only the weights for *that* office.
* **Against:** If you try to do the "normalization" division in a Power Query column, it will be wrong the moment you try to aggregate multiple days.

---

### General "Rule of Thumb"

* **Use Power Query if:** You are creating a "flag" (IsHoliday), a "bucket" (Age Group), or doing text cleaning. If the result is the same regardless of what the user filters, **put it in Power Query.**
* **Use DAX if:** You are calculating a ratio (Percentage), a Year-over-Year comparison, or anything that needs to "react" to a slicer. If the result changes when you change a filter, **it must be a DAX Measure.**

### The Downside of DAX Calculated Columns

Be careful with **DAX Calculated Columns** (not measures). They are often the "worst of both worlds" because they are calculated after the data is loaded, meaning they don't benefit from the high-efficiency compression that Power Query columns do. They can bloat your model and slow down the initial load without providing the dynamic flexibility of a measure.

**Would you like me to show you how to set up a "Holiday Table" in Power Query that connects to your main calendar so you don't have to hard-code dates every year?**