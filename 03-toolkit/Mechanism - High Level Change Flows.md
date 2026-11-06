**Change State Matrix**
```
A    → A      Retain					# no-change
A    → B      Modify					# update
A    → NULL   Remove					# delete
NULL → A      Create / Add				# insert
NULL → NULL   Empty / No Change			

# classic CRUD
A    → A      Retain
NULL → A      Create
A    → B      Update
A    → NULL   Delete
```

**RAMR matrix**
```
Retain  (A → A)
Add     (NULL → A)
Modify  (A → B)
Remove  (A → NULL)
```


Current
↓
Retain
Modify
Add
Remove

# Synonyms
Modified :: Updated, Changed, Reassigned, Corrected, Adjusted, Replaced, Remapped
Nulled-Out :: Removed: Cleared, Blanked, Deleted, Unset, Expunged, Deassigned, Withdrawn, Released

```
Modified
├─ Updated
├─ Changed
├─ Reassigned
├─ Corrected
├─ Adjusted
├─ Replaced
└─ Remapped

Removed
├─ Cleared
├─ Blanked
├─ Deleted
├─ Unset
├─ Expunged
├─ Deassigned
├─ Withdrawn
└─ Released
```