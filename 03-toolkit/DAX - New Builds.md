**Refresh Cadence**: Nightly (maxDateKey = Yesterday())
**Month-To-Date:** Current Month goes up MTD for YOY Comps
# Standard Sizing
Canvas Size: 16:9
Default Slicer Font Values: SegoeUI 10
# Standard Objects
- F_OfficeDayStats
- D_Dates
- D_Offices
- *M_Report*
- *F_LastRefreshed*
- *D_RowLevelSecurity*
- *D_Toggles*

# Formating DataTypes 
DateTime → ISO Date
Thousands comma separator

```
Row Level Security: `Restricted` Role; `D_RowLevelSecurity` as Table Filter;  `[Email] == USERNAME()` as Rules
```


![Pasted image 20260212133118.png]![Pasted image 20260212133121.png]
![Pasted image 20260212133130.png]
![Pasted image 20260212133141.png]


# Data Cleansing
> [!info]
> Use views to do left joins to see if there are issues. 
> 
> Most common culprits:
> - **Facts** -- use `D_Dates` and `D_Locations` as predicates in building the 
> - **Row Level Security** -- offices assigned that are not clinics or active locations

![Pasted image 20260111110125.png]
### OFC TEMPLATE
OfficeKey
Name
RollUp

### EMP TEMPLATE
EmployeeKey
Email
CommonName, FirstName, LastName
ManagerEmployeeKey
JobTitleKey

### ODS TEMPLATE -- 
DateKey
OfficeKey
Production_TotalAmount
Collection_TotalAmount → TrendingPerformance
CaseStart_NetProduction_TotalAmount
CaseStart_TotalCount
CaseStart_ConversionCount
CaseStart_AutoPay_IsStartedCount
CaseStart_AutoPay_IsCandidateCount
CaseStart_DownPaymentAmount
AppointmentsHistoric_NPETotalCount → dnm-showUpRate
AppointmentsHistoric_NPEDismissedCount → nmr-showUpRate

### GUIDANCE
Flags are prefixed → "Is"
SUMS → TotalAmount ($)
If it can be calculated (eg AverageCaseFee (CS_TotalAmount/CS_TotalCount) , NonCaseStartProduction (NetPDX - CS_TotalAmount)
OfficeNameAlias → sdrs.OfficeNameAlias
TeamNameAlias → sdrs.Teams (will also store team imgs)