
```
---
# Dedup Words
# Amazon Pharmacy Pharmacy → Amazon Pharmacy
= Table.TransformColumns(
    #"Previous Step",
    {
        {
            "Brand",
            each Text.Combine(List.Distinct(Text.Split(_, " ")), " "),
            type text
        }
    }
)
```