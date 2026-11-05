`input` → `power qry engine` → `load back new table` → power pivot

# Named Ranges Bridge Gap
Valid in formulas but not in data validation screen so named ranges bridgge.

Formulas → Name Manager → New
account_list referse to =Accounts[AccountName]
Use the named range in your data validation

### Bonus: Exclude blanks or sort alphabetically, define named range:
=SORT(FILTER(Accounts[AccountName], Accounts[AccountName] <> ""))


![Pasted image 20260203114555.png]