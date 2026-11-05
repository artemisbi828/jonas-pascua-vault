When comparing A vs B, we want to see all the following
1. datatypes = flat (convert if necessary to varchar)
2. left <> right
3. left or right null
4. null both

**IDEA 1:** True, False, Blank → could be valuable due to a missing procedure 
IDEA 2: Force → "0" or "Unknown"
