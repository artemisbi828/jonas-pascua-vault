Related to [[DAX - TREATAS]]

VAR _type = SELECTEDVALUE(D_Dates_Dynamic[SlicerType])
VAR _grainKeys = VALUES(D_Dates_Dynamic[Grain_DateKey])   -- should be month-start keys when Monthly is selected