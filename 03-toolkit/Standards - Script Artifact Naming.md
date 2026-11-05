related-to: 
- [[Standard - Notation - Icons and Emojis and ASCII]]
- [Standards - Database Naming]
```table-of-contents
```
# Summary
### Artifact or Object Naming
- code block it
- lower case
- singular
- snake casing
- remove brackets `[]` except SQL protected words

`upn__xi__employee_code`: fan in from upn to employee code
`employee_code__xo__work_assignment`: fan out from employee code to work assignment (jobtitle x officecode)
`access_exception_override`: 
`division_region_managers`: 

| strata | layer, level, tier, rollup, hierarchy |
| ------ | ------------------------------------- |

---
### Transforms
- current --> point-in-time (PIT)
- qualified --> filtered, not-wide-open
- ~~and~~ --> `+`

### File Naming
20260707_2100__requester_short_descrip.filetype
.bup.docx
### Script Naming
Use naming convention `3 part versioning`

> __version__ = "0.0.3"



### Dates
- 2026-07-07
- TUE 0900 AM - 0700 PM 
- Prefer human intuitive -- shorter and easier to read
	`Apr 03 to Apr 05` vs 2026-04-03 to 2026-04-05
	`26, DEC 03 to '26, JAN 05` vs 2026-04-03 to 2026-04-05
	use the other for file naming or precise technical writing
	


# Why Snake_Case?
"Snake_case" is the industry standard for Database Engineering (SQL) and Python. **The "Double Click" Factor:** In most text editors and IDEs, if you double-click `shiny_guacamole`, it selects the whole string. If you double-click `shiny-guacamole`, it usually only selects one word.
- Avoid spaces -- break command line scripts, URL links, and often cause errors in data ingestion pipelines (SQL/Python). In a BI context, spaces are your enemy.
- Avoid hyphens -- BI/Finance world, a hyphen is mathematically a **minus sign**. If you ever have to reference a filename in a script or formula, `q1-report` can look like "variable q1 minus variable report."
## Snake Casing Rules
```
prefix "_"
  name
  code
  type
  title
  layer
  access
  id

suffix "_"
  is
  has
```


# Avoid "Final"
In Finance, nothing is ever truly "Final". Use version numbers or status tags.

- ❌ `budget_v2_final_revised_REAL.xlsx`
- ✅ `2023_budget_v04.xlsx`
- ✅ `2023_budget_draft.xlsx` -> `2023_budget_approved.xlsx`

# Client Naming
**Template:** `[date]_[client_code]_[project_type]_[detail]_[version].[ext]`

**Examples:**

- **BI Project:** `acme_sales_dashboard_v03.pbix`
- **Accounting:** `2023-10_globex_month_end_close.xlsx`
- **Contracting:** `2023-11-01_stark_industries_sow_signed.pdf`

# Folders
Depth level should be max 3-4 levels
```
/clients
    /acme_corp
        /01_admin          (Contracts, SOWs, NDAs)
        /02_financials     (Raw data, CSVs, Excel models)
            /2023
            /2024
        /03_deliverables   (Final PDFs, PowerBI files)
    /globex_inc
        /...
/templates             (Your internal reuseable models)
/archive               (Old projects; keep your active folders lean)
```

# ISO 8601
2025-05-12