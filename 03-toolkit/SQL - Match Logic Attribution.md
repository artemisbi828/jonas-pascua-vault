to dedup, partition by key, then use below --> prioritize matches
	`order by case when keyword = keyword then 1 else 2 end` 
then can also use this --> fuzzy prio and set nulls as last
	isnull(sort_order, 99)