Inner Join -- mutual possibilities
Outer Join -- all possibilities
Left Join -- parent vs child 
	• define which table is on the left and which is on the right
Left Anti -- null or not (+)

CROSS JOIN -- no "on" -- cartesian product
FULL OUTER JOIN (FULL JOIN) -- some on the left, some on the right 

> [!Warning]
> You cannot join on different grains; standardize w GROUP BY then FULL JOIN (eg DateOffice vs DateOfficeAttachment)