SELECT f.CustomID AS MaMon
	  ,f.Name AS TenMon
	  ,c.Name AS NhomMon
	  ,SUM(o.Amount) AS SoLuong
	  ,SUM(o.Discount) AS GiamGia
	  ,SUM(o.Amount * (o.Price - o.Discount)) AS NetDoanhThu
	  ,SUM(o.Amount * (o.Price - o.Discount) - fh.Cost) AS LoiNhuan
FROM fooditem f
LEFT JOIN Category c
    ON c.ID = f.CategoryID
LEFT JOIN orderdetails o
    ON f.ID = o.FoodItemID
LEFT JOIN fooditem_history fh
	ON f.ID = fh.FoodItemID
WHERE 1=1
AND fh.IsEffective = True
#Append Thêm điều kiện lọc vào chỗ này (AND, OR)
GROUP BY f.CustomID
		,f.Name
		,c.Name;