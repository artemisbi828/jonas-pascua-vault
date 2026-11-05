Quotient Index = DIVIDE([B], [A], BLANK()) - 1

Quotient with Null Handling = SWITCH(True(), 
	ISBLANK([A]), BLANK(), 
	ISBLANK([B]), BLANK(), 
	DIVIDE([B], [A], BLANK()) - 1
	)

> [!less ideal]
> Leads YoY% = IF(ISBLANK([Leads PY]), BLANK(), DIVIDE([Leads], [Leads PY], BLANK()) - 1)

