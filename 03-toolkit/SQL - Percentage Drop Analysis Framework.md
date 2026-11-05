# Volume decomposition before percentage analysis
Percentages lie when denominators or numerators silently change.

“Is the numerator missing, or did the denominator grow?”

Did numerator drop?
Did denomintaor drop? 
Did mapping change? 

Raw daily counts (not %)
7‑day rolling averages
Pre vs post dip absolute deltas

Classic pipeline failure signatures

CaseStarts steady, Smile Express near‑zero → lookup / key failure
CaseStarts suddenly inflated → duplication or late‑arriving rows
Smile Express steady, CaseStarts increase → upstream flag logic changed

3. Key‑path integrity checks (join fallout analysis)
Most pipeline issues present as silent left‑join fallout.
Common failure modes

TxPlanKey missing / late
ContractKey arrives before dimension sync
Lookup logic changes but historical backfill doesn’t
