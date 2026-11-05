simpler
```
# search for "SourceSystemId" in A1 (respective)
=IFERROR((XMATCH(TRUE,ISNUMBER(SEARCH("SourceSystemId",A1)),0)), "")
```

create a mapping table (Table2)
```
=LET(
  txt, B2
  ,
  keys, Table2[contains],
  vals, Table2[aggregation_type],
  pos, XMATCH(TRUE, ISNUMBER(SEARCH(keys, txt)), 0),
  IFERROR(INDEX(vals, pos), "")
)
```

B2