# Alter Tables
```sql
ALTER TABLE log
ALTER COLUMN created_at SET DEFAULT current_timestamp;

SET VARIABLE user_name = 'jpascua';
INSERT INTO log (
    comment,
    created_by
)
VALUES (
    'Testing',
    getvariable('user_name')
);

```
