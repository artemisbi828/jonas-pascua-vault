```sql
alter table gold.cl9cms__patient_status 
add npe_outcome_id int

alter table gold.cl9cms__patient_status 
add constraint [fk__gold__cl9cms__patient_status]
foreign key (npe_outcome_id)
references gold.cl9cms__npe_outcome (npe_outcome_id)
```
