[[Tools - Powershell]]

**File Exists**

> Test-Path "C:\Repos\sd-edw\duckdb\sd_edw.duckdb"

Check Architecture
	`systeminfo | findstr /i "System Type"` -- 
	`$env:PROCESSOR_ARCHITECTURE` -- eg AMD64

Check package install
```
#
py -c "import jinja2; print('Jinja2 OK')"
py -c "import sqlglot; print('SQLGlot OK')"

	# -or-
	pip show jinja2  
	pip show sqlglot  
	
	py -m pip show jinja2  
	py -m pip show sqlglot
	
	pip list | findstr jinja  
	pip list | findstr sqlglot


# =============== 
# to install
py -m pip install jinja2  
py -m pip install sqlglot  


```
