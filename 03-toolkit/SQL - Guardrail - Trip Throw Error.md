```sql

declare @rc int = (select count(*)from gold.appointment_sd as asd where asd.patient_id__cc9 is null);

if @rc > 1
throw 50001, 'Validation failed: null patient_id__cc9 exists in gold.appointment_sd; proc: dataops.usp_purge__unused_patient_dimension', 1;
```