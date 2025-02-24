/*Lấy toàn bộ dữ liệu cho menu món ăn*/
SELECT fi.ID --ID của món
      ,fi.Name --Tên món
      ,fi.IsBestSeller --Flag cho món best seller
      ,fh.Price --Giá chưa giảm bởi promotion
      ,CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice --Giá sau giảm bởi promotion, nếu không có promotion thì vẫn lấy giá gốc. Còn nếu có promotion thì kiểm tra xem promotion đang giảm theo % hay không để áp dụng đúng công thức
      ,fh.ImageURL --Đường dẫn đến hình ảnh của món
      ,p.PromotionID --Lưu lại promotionID cho phần submit order
FROM fooditem fi 
INNER JOIN fooditem_history fh --Join với bảng lịch sử giá của món
    ON fi.ID = fh.FoodItemId
LEFT JOIN promotionfooditem pfi
    ON fi.ID = pfi.FoodItemID
INNER JOIN promotion p
    ON p.ID = pfi.PromotionID
WHERE fi.IsFulltime = True --Được bán toàn thời gian
AND fi.IsEffective = True --Giá hiện tại trong bảng lịch sử giá
UNION --Kết hợp kết quả của 2 câu query, một bên là món bán toàn thời gian, một bên là món bán trong khung ngày giờ cố định.
SELECT fi.ID
    ,fi.Name
    ,fi.IsBestSeller
    ,fh.Price
    ,CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice
    ,fh.ImageURL
    ,p.PromotionID 
FROM fooditem fi 
INNER JOIN fooditem_history fh
    ON fi.id = fh.FoodItemId
LEFT JOIN promotionfooditem pfi
    ON fi.ID = pfi.FoodItemID
INNER JOIN promotion p
    ON p.ID = pfi.PromotionID
WHERE fi.IsFulltime = False 
AND fh.IsEffective = True --Giá hiện tại trong bảng lịch sử giá
AND fi.Days LIKE CONCAT('%',CAST(WEEKDAY(current_timestamp) AS CHAR),'%') --Lấy món được bán trong ngày hôm đó
AND current_time BETWEEN available_time_start AND available_time_end; --Lấy món được bán trong khung giờ hiện tại 


/*Lấy dữ liệu cho menu món ăn của một nhóm món cụ thể*/
SELECT fi.ID 
      ,fi.Name 
      ,fi.IsBestSeller 
      ,fh.Price 
      ,CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice 
      ,fh.ImageURL 
      ,p.PromotionID
FROM fooditem fi 
INNER JOIN fooditem_history fh 
    ON fi.ID = fh.FoodItemId
LEFT JOIN promotionfooditem pfi
    ON fi.ID = pfi.FoodItemID
INNER JOIN promotion p
    ON p.ID = pfi.PromotionID
WHERE fi.IsFulltime = True
AND fi.IsEffective = True 
AND fi.CategoryID = {ID của nhóm món muốn lấy} --Khi khách bấm vào một category cụ thể, ta phải catch CategoryID mà khách hàng chọn. Sau đó truyền vào chỗ này
UNION
SELECT fi.ID
    ,fi.Name
    ,fi.IsBestSeller
    ,fh.Price
    ,CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice
    ,fh.ImageURL
FROM fooditem fi 
INNER JOIN fooditem_history fh
    ON fi.id = fh.FoodItemId
LEFT JOIN promotionfooditem pfi
    ON fi.ID = pfi.FoodItemID
INNER JOIN promotion p
    ON p.ID = pfi.PromotionID
WHERE fi.IsFulltime = False 
AND fh.IsEffective = True
AND fi.Days LIKE CONCAT('%',CAST(WEEKDAY(current_timestamp) AS CHAR),'%') 
AND current_time BETWEEN available_time_start AND available_time_end; 
AND fi.CategoryID = {ID của nhóm món muốn lấy} --Khi khách bấm vào một category cụ thể, ta phải catch CategoryID mà khách hàng chọn. Sau đó truyền vào chỗ này

/*Lấy dữ liệu cho nhóm món*/
SELECT ID --ID của nhóm món
      ,Name --Tên nhóm món
      ,ImageURL --Đường dẫn hình ảnh nhóm món
FROM Category
