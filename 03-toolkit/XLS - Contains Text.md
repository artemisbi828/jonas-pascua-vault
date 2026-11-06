
```bash
# Case Insensitive
=ISNUMBER(SEARCH("text", A1))

# Case Sensitive
=ISNUMBER(FIND("text", A1))

=IF(ISNUMBER(SEARCH("text", A1)), "Yes", "No")
=OR(ISNUMBER(SEARCH("apple", A1)), ISNUMBER(SEARCH("banana", A1))) #M strings
=SUMPRODUCT(--ISNUMBER(SEARCH(B1:B5, A1)))>0 # contains substring from a list dynamic
```
