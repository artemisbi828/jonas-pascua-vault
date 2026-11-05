
```sql

ALTER TABLE docm.data_source
ADD CONSTRAINT CK_data_source_delivery_completeness_ratio_0_1
CHECK (
    delivery_completeness_ratio IS NULL
    OR (delivery_completeness_ratio >= 0 AND delivery_completeness_ratio < 1)
);
GO

ALTER TABLE docm.data_source
ADD CONSTRAINT CK_data_source_x_0_1_inclusive
CHECK (x IS NULL OR (x >= 0 AND x <= 1));
GO

```