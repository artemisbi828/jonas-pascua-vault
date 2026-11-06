```sql
select
    *
from (
    values ('Comments', 'Appointment Comment'),
           ('DateKey', 'Appointment Date Time'),
           ('AppointmentStartDateTime', 'Appointment Date Time'),
           ('AppointmentSID', 'Appointment SID'),
           ('AppointmentStatusKey', 'Appointment Status'),
           ('CancelledBy_EmployeeKeyRaw', 'Cancel By Staff Name'),
           ('CancelledDateTime', 'Cancel Date Time'),
           ('CancelledType', 'Cancellation Reason'),
           ('CancelledComment', 'Cancellation Remarks'),
           ('AppointmentEndDateTime', 'Check Out Date Time'),
           ('CheckedInBy_EmployeeKeyRaw', 'Checked In By Staff Name'),
           ('CreatedDateKey', 'Create Date For Wait Time'),
           ('DefaultProvider_EmployeeKeyRaw', 'Default Provider Name'),
           ('CreatedBy_EmployeeKeyRaw', 'Made by Staff Name'),
           ('VisitProvider_EmployeeKeyRaw', 'Visit Provider Staff Name')
) x ([dbo.Appointments], [ldTable])
for json path, root('Data') -- root(… is optional
```

```sql
select     JSON_OBJECT(
        'firstName': eds2.FirstName,
        'lastName': eds2.LastName,
        'address': eds2.Address,
        'firmId': '302B6C46-CCDE-48C6-95D8-81FB7105C7CC',
        'zip': CAST(eds2.ZipCode AS VARCHAR),
        'city': eds2.City,
        'state': eds2.State
    ) AS Payload
```