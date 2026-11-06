::
:=
EQ, GEQ, LEQ, GT, LT, NEQ
≡ -> type: `alt+240`

```json
{
	"column_a": "value_a", 
	"column_b": "value_b",
	"column_c": "value_c"
}
```

```json
{
	"column_a": ["value_a1", "value_a1", "value_a1"],
	"column_b": ["value_b1", "value_b1", "value_b1", , "value_b1"],
	"column_c": ["value_c1"], 
	"column_d": {
		"mssql": "[{keyword}]",
		"snowflake": "\"{keyword}\"",
	    "postgresql": "\"{keyword}\""
	
	}
}
```

```
OPENAI_API_KEY=yoour_api_key_here
FLASK_ENV=development
```

```
[server]
host = "127.09.0.1"
port = 8988

[user]
name = "John Doe"
email = "john@example.com"
```


# File Naming
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

# Professional File Naming & Organization Cheat Sheet

## Context: Finance, Accounting, & Business Intelligence Consulting

### 1. The Golden Rules

- **Lowercase Everything:** Windows is case-insensitive, but Linux/Servers are not. `Report.csv` and `report.csv` are different files to a database. Always use lowercase to avoid "file not found" errors.
- **No Special Characters:** Avoid `! @ # $ % & ( )`. These have special meanings in programming languages.
- **Dates First (Usually):** If the chronological order matters (like monthly close reports), the date goes at the start.
- **Pad Your Numbers:** Use `01` instead of `1` so files sort correctly (e.g., `01, 02... 10`, not `1, 10, 11... 2`).

### 3. Date Formatting (ISO 8601)

Never use "October" or "10-25". Always use **YYYY-MM-DD**.

- **Good:** `2023-11-25_p_and_l.xlsx` (Sorts perfectly by year, then month, then day)
- **Bad:** `11-25-2023_p_and_l.xlsx` (Sorts by month, mixing up years)
- **Bad:** `Nov_25_p_and_l.xlsx` (Sorts alphabetically, confusing April and August)
### 7. Power User Tips for BI/Data

If you are exporting CSVs for Tableau/PowerBI/SQL:

1. **Header Rows:** Apply these naming conventions to your **column headers** inside the file too.
    
    - `Total Revenue` -> `total_revenue`
        
2. **Versioning:** If extracting data, timestamp the filename to the second if possible, or minimally to the day.
    
    - `extract_sales_2023-11-25.csv`