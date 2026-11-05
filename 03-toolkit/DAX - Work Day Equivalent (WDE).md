---
aliases:
  - WDE
---

> [!info] Summary
WDE takes the 1-day-equivalent of all the production-days for the month
> 	-- any quotients (Δ) should be shielded from WDE (no expected change)
> 	-- for current month -- should shield b/c it's misleading


Best to do this in TSQL layer → ODS has [[SQL - Rolling Total]] of WDE and MonthKey has Sum() of WDE
In a given month, what is sum(workingdays)
when comparing NOV-2025 vs NOV 2024


### **1. Work-Day Equivalent (WDE) Normalization**

**The Problem:** Raw Year-over-Year (YoY) comparisons are often distorted by "calendar noise"—the shifting number of Mondays vs. Sundays and the placement of holidays. **The Specialized Solution:** I engineer custom weight-based calendars that standardize "Daily Capacity." By assigning precise decimal weights to weekdays, weekends, and holiday proximity (e.g., 0.667 for pre-holiday ramp-downs), I neutralize calendar variance. **Executive Value:** This allows leadership to distinguish between a "slow month" and a "short month," ensuring that productivity and revenue metrics are evaluated on a true apple-to-apples basis.
