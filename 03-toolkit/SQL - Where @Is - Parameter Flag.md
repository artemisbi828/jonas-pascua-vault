Best practice is to make it 3 state -- bit + null

```sql
DECLARE @is_patient_ledger bit = 1;  -- 1 patient, 0 insurance, NULL both

...

AND (
      @is_patient_ledger IS NULL
   OR (@is_patient_ledger = 1 AND t.pipGUID IS NULL)
   OR (@is_patient_ledger = 0 AND t.pipGUID IS NOT NULL)
)

```
