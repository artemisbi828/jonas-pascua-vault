Reference (clone) and separate into a distinct table

### Step 1: Create the separate table in Power Query

1. Open **Power Query Editor**.
2. Right-click your existing `D_Dates` query and select **Reference**.
3. Rename this new query to `D_YearMonth_Slicer`.
4. In the ribbon, go to **Choose Columns** and select only:
    
    - `YearMonth_Current`
    - `YYYYMM_Sort`
        
5. Select both columns (Ctrl + Click), right-click, and select **Remove Duplicates**.
    - _This gives you exactly one row per month, satisfying the 1:1 rule._
6. Click **Close & Apply**.