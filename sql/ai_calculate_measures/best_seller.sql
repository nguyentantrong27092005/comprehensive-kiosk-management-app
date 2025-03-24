SELECT f.CustomID AS MaMon, f.Name AS TenMon, c.Name AS NhomMon,
       SUM(o.Amount) AS SoLuong, SUM(o.Discount) AS GiamGia,
       SUM(o.Amount * (o.Price - o.Discount)) AS DoanhThu,
       SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0)) AS LoiNhuan,
       CONCAT(DATE_ADD(current_date(), INTERVAL -7 DAY), ' - ', current_date()) AS WEEK_PERIOD
FROM fooditem f
LEFT JOIN Category c ON c.ID = f.CategoryID
LEFT JOIN (SELECT * FROM orderdetails o WHERE o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -7 DAY) AND current_date()) o
ON f.ID = o.FoodItemID
LEFT JOIN fooditem_history fh ON f.ID = fh.FoodItemID AND fh.IsEffective = TRUE
GROUP BY f.CustomID, f.Name, c.Name
UNION ALL
SELECT f.CustomID AS MaMon, f.Name AS TenMon, c.Name AS NhomMon,
       SUM(o.Amount) AS SoLuong, SUM(o.Discount) AS GiamGia,
       SUM(o.Amount * (o.Price - o.Discount)) AS DoanhThu,
       SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0)) AS LoiNhuan,
       CONCAT(DATE_ADD(current_date(), INTERVAL -15 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -8 DAY)) AS WEEK_PERIOD
FROM fooditem f
LEFT JOIN Category c ON c.ID = f.CategoryID
LEFT JOIN (SELECT * FROM orderdetails o WHERE o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -15 DAY) AND DATE_ADD(current_date(), INTERVAL -8 DAY)) o
ON f.ID = o.FoodItemID
LEFT JOIN fooditem_history fh ON f.ID = fh.FoodItemID AND fh.IsEffective = TRUE
GROUP BY f.CustomID, f.Name, c.Name
UNION ALL
SELECT f.CustomID AS MaMon, f.Name AS TenMon, c.Name AS NhomMon,
       SUM(o.Amount) AS SoLuong, SUM(o.Discount) AS GiamGia,
       SUM(o.Amount * (o.Price - o.Discount)) AS DoanhThu,
       SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0)) AS LoiNhuan,
       CONCAT(DATE_ADD(current_date(), INTERVAL -23 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -16 DAY)) AS WEEK_PERIOD
FROM fooditem f
LEFT JOIN Category c ON c.ID = f.CategoryID
LEFT JOIN (SELECT * FROM orderdetails o WHERE o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -23 DAY) AND DATE_ADD(current_date(), INTERVAL -16 DAY)) o
 ON f.ID = o.FoodItemID
LEFT JOIN fooditem_history fh ON f.ID = fh.FoodItemID AND fh.IsEffective = TRUE
GROUP BY f.CustomID, f.Name, c.Name
UNION ALL
SELECT f.CustomID AS MaMon, f.Name AS TenMon, c.Name AS NhomMon,
       SUM(o.Amount) AS SoLuong, SUM(o.Discount) AS GiamGia,
       SUM(o.Amount * (o.Price - o.Discount)) AS DoanhThu,
       SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0)) AS LoiNhuan,
       CONCAT(DATE_ADD(current_date(), INTERVAL -31 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -24 DAY)) AS WEEK_PERIOD
FROM fooditem f
LEFT JOIN Category c ON c.ID = f.CategoryID
LEFT JOIN (SELECT * FROM orderdetails o WHERE o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -31 DAY) AND DATE_ADD(current_date(), INTERVAL -24 DAY)) o
 ON f.ID = o.FoodItemID
LEFT JOIN fooditem_history fh ON f.ID = fh.FoodItemID AND fh.IsEffective = TRUE
GROUP BY f.CustomID, f.Name, c.Name;