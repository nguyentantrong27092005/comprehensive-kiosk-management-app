SELECT
    CONCAT(DATE_ADD(current_date(), INTERVAL -31 DAY), ' - ', current_date()) AS MONTH_PERIOD,
    IFNULL(SUM(o.Amount * (o.Price - o.Discount)), 0) AS "Doanh Thu",
    IFNULL(SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0)), 0) AS "Lợi Nhuận",
    IFNULL(
        (SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0))) / NULLIF(SUM(o.Amount * (o.Price - o.Discount)), 0),
        0
    ) AS "Biên Lợi Nhuận"
FROM
    (SELECT 1) AS dummy
LEFT JOIN orderdetails o ON o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -31 DAY) AND current_date()
LEFT JOIN fooditem_history fh ON o.FoodItemID = fh.FoodItemID AND fh.IsEffective = TRUE
UNION ALL
SELECT
    CONCAT(DATE_ADD(current_date(), INTERVAL -63 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -32 DAY)) AS MONTH_PERIOD,
    IFNULL(SUM(o.Amount * (o.Price - o.Discount)), 0) AS "Doanh Thu",
    IFNULL(SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0)), 0) AS "Lợi Nhuận",
    IFNULL(
        (SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0))) / NULLIF(SUM(o.Amount * (o.Price - o.Discount)), 0),
        0
    ) AS "Biên Lợi Nhuận"
FROM
    (SELECT 1) AS dummy
LEFT JOIN orderdetails o ON o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -63 DAY) AND DATE_ADD(current_date(), INTERVAL -32 DAY)
LEFT JOIN fooditem_history fh ON o.FoodItemID = fh.FoodItemID AND fh.IsEffective = TRUE
UNION ALL
SELECT
    CONCAT(DATE_ADD(current_date(), INTERVAL -95 DAY), ' - ', DATE_ADD(current_date(), INTERVAL -64 DAY)) AS MONTH_PERIOD,
    IFNULL(SUM(o.Amount * (o.Price - o.Discount)), 0) AS "Doanh Thu",
    IFNULL(SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0)), 0) AS "Lợi Nhuận",
    IFNULL(
        (SUM(o.Amount * (o.Price - o.Discount)) - SUM(IFNULL(fh.Cost, 0))) / NULLIF(SUM(o.Amount * (o.Price - o.Discount)), 0),
        0
    ) AS "Biên Lợi Nhuận"
FROM
    (SELECT 1) AS dummy
LEFT JOIN orderdetails o ON o.CreateAt BETWEEN DATE_ADD(current_date(), INTERVAL -95 DAY) AND DATE_ADD(current_date(), INTERVAL -64 DAY)
LEFT JOIN fooditem_history fh ON o.FoodItemID = fh.FoodItemID AND fh.IsEffective = TRUE;