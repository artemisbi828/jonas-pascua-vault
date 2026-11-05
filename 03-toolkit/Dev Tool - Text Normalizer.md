```
PROMPT
I want to create a text normalizer. That
- transforms all to lower snake case
- revert abbreviations
- but I want to create a markdown of the rules first so want help detailing more possibilities
```

- snake_case
- no_abbreviation
- double_vs_single__underscore

# Examples

| RULE | BEFORE    | AFTER      |
| ---- | --------- | ---------- |
| 1    | patGUID   | pat_guid   |
| 2    | SnakeCase | snake_case |
| 3    | ctr       | Contract   |
| 4    |           |            |

Rule 1: prefix `_` to these words: 
- code
- guid
- type

Rule 2: lower snake case

Rule 3: De-Abbreviate
- appt or apt → appointment

Rule 4: change protected keywords SQL priority
- Transaction → transactionx
- 123mycolumn → mycolumn123

Rule 5: 
- amount
