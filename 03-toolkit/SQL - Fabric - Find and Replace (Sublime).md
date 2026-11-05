#### AZP Object References --> Fabric.LHS_DEV_Data_Solutions
```
---
CentralC9.dbo. --> LHS_DEV_Data_Solutions.cc9_dbo.
EDW.bi. --> LHS_DEV_Data_Solutions.edw_bi.
EDW.referral. --> LHS_DEV_Data_Solutions.edw_referral.
Lake.sd. --> LHS_DEV_Data_Solutions.lake_sd.
---
```

#### Creating Tables
```
---
DROP TABLE #temptable --> 
#temptable --> edw.my_table
nvarchar --> varchar
tinyint --> int
datetime2(7) --> datetime2(6)
---
```