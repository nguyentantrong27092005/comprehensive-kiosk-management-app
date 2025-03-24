SELECT e.ID,
	   e.Name,
	   f.ID AS FoodItemID,
	   f.Name AS "Món Tặng"
FROM evouchertangmon etm
INNER JOIN evoucher e
ON e.ID = etm.EVoucherID AND e.StartDate <= DATE_ADD(current_date(), INTERVAL -31 DAY) AND e.EndDate >= DATE_ADD(current_date(), INTERVAL 0 DAY)
INNER JOIN fooditem f
ON f.ID = etm.FoodItemID