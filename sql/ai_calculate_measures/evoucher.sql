SELECT
	e.ID,
	e.Name,
	'Giảm giá tổng hoá đơn' AS "Phân Loại",
	IFNULL(SUM(o.EVoucherDiscount),0)  AS "Tổng Giảm Giá",
	SUM(o.TotalPrice) AS "Tổng Doanh Thu",
	CONCAT(DATE_ADD(current_date(), INTERVAL -7 DAY), ' - ', current_date()) AS WEEK_PERIOD
FROM evouchergiamgia egg
INNER JOIN evoucher e
ON e.ID = egg.EVoucherID AND e.StartDate <= DATE_ADD(current_date(), INTERVAL -7 DAY) AND e.EndDate >= DATE_ADD(current_date(), INTERVAL 0 DAY)
LEFT JOIN `order` o
ON egg.ID = o.EVoucherGiamGiaID
WHERE o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -7 DAY) AND current_date()
GROUP BY e.ID, e.Name
UNION ALL
SELECT
	e.ID,
	e.Name,
	'Giảm giá tổng hoá đơn' AS "Phân Loại",
	IFNULL(SUM(o.EVoucherDiscount),0)  AS "Tổng Giảm Giá",
	SUM(o.TotalPrice) AS "Tổng Doanh Thu",
	CONCAT(DATE_ADD(current_date(), INTERVAL -15 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -8 DAY)) AS WEEK_PERIOD
FROM evouchergiamgia egg
INNER JOIN evoucher e
ON e.ID = egg.EVoucherID AND e.StartDate <= DATE_ADD(current_date(), INTERVAL -15 DAY) AND e.EndDate >= DATE_ADD(current_date(), INTERVAL -8 DAY)
LEFT JOIN `order` o
ON egg.ID = o.EVoucherGiamGiaID
WHERE o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -15 DAY) AND DATE_ADD(current_date(), INTERVAL -8 DAY)
GROUP BY e.ID, e.Name
UNION ALL
SELECT
	e.ID,
	e.Name,
	'Giảm giá tổng hoá đơn' AS "Phân Loại",
	IFNULL(SUM(o.EVoucherDiscount),0)  AS "Tổng Giảm Giá",
	SUM(o.TotalPrice) AS "Tổng Doanh Thu",
	CONCAT(DATE_ADD(current_date(), INTERVAL -23 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -16 DAY)) AS WEEK_PERIOD
FROM evouchergiamgia egg
INNER JOIN evoucher e
ON e.ID = egg.EVoucherID AND e.StartDate <= DATE_ADD(current_date(), INTERVAL -23 DAY) AND e.EndDate >= DATE_ADD(current_date(), INTERVAL -16 DAY)
LEFT JOIN `order` o
ON egg.ID = o.EVoucherGiamGiaID
WHERE o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -23 DAY) AND DATE_ADD(current_date(), INTERVAL -16 DAY)
GROUP BY e.ID, e.Name
UNION ALL
SELECT
	e.ID,
	e.Name,
	'Giảm giá tổng hoá đơn' AS "Phân Loại",
	IFNULL(SUM(o.EVoucherDiscount),0)  AS "Tổng Giảm Giá",
	SUM(o.TotalPrice) AS "Tổng Doanh Thu",
	CONCAT(DATE_ADD(current_date(), INTERVAL -31 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -24 DAY)) AS WEEK_PERIOD
FROM evouchergiamgia egg
INNER JOIN evoucher e
ON e.ID = egg.EVoucherID AND e.StartDate <= DATE_ADD(current_date(), INTERVAL -31 DAY) AND e.EndDate >= DATE_ADD(current_date(), INTERVAL -24 DAY)
LEFT JOIN `order` o
ON egg.ID = o.EVoucherGiamGiaID
WHERE o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -31 DAY) AND DATE_ADD(current_date(), INTERVAL -24 DAY)
GROUP BY e.ID, e.Name
UNION ALL
SELECT e.ID,
	   e.Name,
	   'Tặng món' AS "Phân Loại",
	   IFNULL(SUM(od.Discount*od.Amount), 0) AS "Tổng Giảm Giá",
	   IFNULL(SUM(o.TotalPrice), 0) AS "Tổng Doanh Thu",
	   CONCAT(DATE_ADD(current_date(), INTERVAL -7 DAY), ' - ', DATE_ADD(current_date(), INTERVAL 0 DAY)) AS WEEK_PERIOD
FROM evouchertangmon etm
LEFT JOIN orderdetails od
ON etm.ID = od.EVoucherTangMonID AND od.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -7 DAY) AND DATE_ADD(current_date(), INTERVAL 0 DAY)
LEFT JOIN `order` o
ON o.ID = od.OrderID
INNER JOIN evoucher e
ON e.ID = etm.EVoucherID AND e.StartDate <= DATE_ADD(current_date(), INTERVAL -7 DAY) AND e.EndDate >= DATE_ADD(current_date(), INTERVAL 0 DAY)
GROUP BY e.ID, e.Name
UNION ALL
SELECT e.ID,
	   e.Name,
	   'Tặng món' AS "Phân Loại",
	   IFNULL(SUM(od.Discount*od.Amount), 0) AS "Tổng Giảm Giá",
	   IFNULL(SUM(o.TotalPrice), 0) AS "Tổng Doanh Thu",
	   CONCAT(DATE_ADD(current_date(), INTERVAL -15 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -8 DAY)) AS WEEK_PERIOD
FROM evouchertangmon etm
LEFT JOIN orderdetails od
ON etm.ID = od.EVoucherTangMonID AND od.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -15 DAY) AND DATE_ADD(current_date(), INTERVAL -8 DAY)
LEFT JOIN `order` o
ON o.ID = od.OrderID
INNER JOIN evoucher e
ON e.ID = etm.EVoucherID AND e.StartDate <= DATE_ADD(current_date(), INTERVAL -15 DAY) AND e.EndDate >= DATE_ADD(current_date(), INTERVAL -8 DAY)
GROUP BY e.ID, e.Name
UNION ALL
SELECT e.ID,
	   e.Name,
	   'Tặng món' AS "Phân Loại",
	   IFNULL(SUM(od.Discount*od.Amount), 0) AS "Tổng Giảm Giá",
	   IFNULL(SUM(o.TotalPrice), 0) AS "Tổng Doanh Thu",
	   CONCAT(DATE_ADD(current_date(), INTERVAL -23 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -16 DAY)) AS WEEK_PERIOD
FROM evouchertangmon etm
LEFT JOIN orderdetails od
ON etm.ID = od.EVoucherTangMonID AND od.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -23 DAY) AND DATE_ADD(current_date(), INTERVAL -16 DAY)
LEFT JOIN `order` o
ON o.ID = od.OrderID
INNER JOIN evoucher e
ON e.ID = etm.EVoucherID AND e.StartDate <= DATE_ADD(current_date(), INTERVAL -23 DAY) AND e.EndDate >= DATE_ADD(current_date(), INTERVAL -16 DAY)
GROUP BY e.ID, e.Name
UNION ALL
SELECT e.ID,
	   e.Name,
	   'Tặng món' AS "Phân Loại",
	   IFNULL(SUM(od.Discount*od.Amount), 0) AS "Tổng Giảm Giá",
	   IFNULL(SUM(o.TotalPrice), 0) AS "Tổng Doanh Thu",
	   CONCAT(DATE_ADD(current_date(), INTERVAL -31 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -24 DAY)) AS WEEK_PERIOD
FROM evouchertangmon etm
LEFT JOIN orderdetails od
ON etm.ID = od.EVoucherTangMonID AND od.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -31 DAY) AND DATE_ADD(current_date(), INTERVAL -24 DAY)
LEFT JOIN `order` o
ON o.ID = od.OrderID
INNER JOIN evoucher e
ON e.ID = etm.EVoucherID AND e.StartDate <= DATE_ADD(current_date(), INTERVAL -31 DAY) AND e.EndDate >= DATE_ADD(current_date(), INTERVAL -24 DAY)
GROUP BY e.ID, e.Name;