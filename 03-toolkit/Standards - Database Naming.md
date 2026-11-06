related-to: 
- [[Data Medallion Layer - Bronze, Silver, Gold]]
- [[Standards - Database Object Naming]]
- [[Dev Tool - Text Normalizer]]


**General Naming**
- snake_case
- no_abbreviation
- double_vs_single__underscore

|     | **Bronze**                        | **Silver**                               | **Gold**                        |
| --- | --------------------------------- | ---------------------------------------- | ------------------------------- |
|     | Raw --> Trunc + Reload?<br>Bronze | Sanitize<br>Dedup + Null Handling        | Business TFM<br>Unification<br> |
|     | Source Name                       | Source Name<br>No Abb                    |                                 |
|     | + SRC_SYS<br>+ CRT_TS             | + SRC_CRT_TS<br>+ SRC_UPD_TS<br>+ UPD_TS |                                 |
|     |                                   |                                          |                                 |
SRC_SYS -- source -- 
CRT_TS -- actual created timestamp
SRC_CRT_TS -- source created timestamp
SRC_UPD_TS -- source updated timestamp
UPD_TS -- updated timestamp