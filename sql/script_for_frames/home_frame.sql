/*Lấy toàn bộ dữ liệu cho menu món ăn*/
SELECT fi.ID #ID của món
      ,fi.Name #Tên món
      ,fi.IsBestSeller #Flag cho món best seller
      ,fh.Price #Giá chưa giảm bởi promotion
      ,CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice #Giá sau giảm bởi promotion, nếu không có promotion thì vẫn lấy giá gốc. Còn nếu có promotion thì kiểm tra xem promotion đang giảm theo % hay không để áp dụng đúng công thức
      ,fi.ImageURL #Đường dẫn đến hình ảnh của món
      ,pfi.PromotionID #Lưu lại promotionID cho phần submit order
FROM fooditem fi 
INNER JOIN fooditem_history fh #Join với bảng lịch sử giá của món
    ON fi.ID = fh.FoodItemId
LEFT JOIN promotionfooditem pfi
    ON fi.ID = pfi.FoodItemID
LEFT JOIN (SELECT * FROM promotion WHERE IsEffective = True) p
    ON p.ID = pfi.PromotionID
WHERE (fi.IsFulltime = True OR (fi.Days LIKE CONCAT('%',CAST(WEEKDAY(current_timestamp) AS CHAR),'%') #Lấy món được bán trong ngày hôm đó
								AND current_time BETWEEN fi.AvailableStartTime AND fi.AvailableEndTime)) #Lấy món được bán trong khung giờ hiện tại
AND fh.IsEffective = True;


/*Lấy dữ liệu cho menu món ăn của một nhóm món cụ thể*/
SELECT fi.ID 
      ,fi.Name 
      ,fi.IsBestSeller 
      ,fh.Price 
      ,CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice 
      ,fi.ImageURL
      ,pfi.PromotionID
FROM fooditem fi
INNER JOIN fooditem_history fh
    ON fi.ID = fh.FoodItemId
LEFT JOIN promotionfooditem pfi
    ON fi.ID = pfi.FoodItemID
LEFT JOIN (SELECT * FROM promotion WHERE IsEffective = True) p
    ON p.ID = pfi.PromotionID
WHERE (fi.IsFulltime = True OR (fi.Days LIKE CONCAT('%',CAST(WEEKDAY(current_timestamp) AS CHAR),'%') #Lấy món được bán trong ngày hôm đó
								AND current_time BETWEEN fi.AvailableStartTime AND fi.AvailableEndTime)) #Lấy món được bán trong khung giờ hiện tại
AND fh.IsEffective = True
AND fi.CategoryID = {ID của nhóm món muốn lấy};  #Khi khách bấm vào một category cụ thể, ta phải catch CategoryID mà khách hàng chọn. Sau đó truyền vào chỗ này

/*Lấy dữ liệu cho nhóm món*/
SELECT ID #ID của nhóm món
      ,Name #Tên nhóm món
      ,ImageURL #Đường dẫn hình ảnh nhóm món
FROM Category;