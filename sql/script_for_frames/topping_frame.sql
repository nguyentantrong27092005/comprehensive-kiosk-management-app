/*Lấy dữ liệu variant của món cụ thể*/
SELECT vg.ID #Mã nhóm chọn variant (variant là chọn đường, chọn đá…)
	  ,vg.Name #Tên nhóm variant
	  ,vg.IsRequired #Flag bắt buộc phải chọn
	  ,vg.ViewType #dạng slider, radio button
      ,vg.HasPrice #variant có tính thêm tiền hay không
FROM variantgroupfooditem vgfi
INNER JOIN variantgroup vg
    ON vg.ID = vgfi.VariantGroupID
WHERE vgfi.FoodItemID = {Id_của_món_đang_được_chọn};


/*1 món có nhiều variant group => thực hiện query variant của từng variantGroup*/
SELECT ID
	  ,Value #các option bên trong của variant
      ,Price #giá của variant nếu có
      ,AdditionalCost #giá cost của variant
FROM variant
WHERE VariantGroupID = {variant_group_id từ câu query phía trên};


/*Lấy dữ liệu cho phần ToppingGroup*/
SELECT tg.ID #ID của topping group cho món ăn đang được chọn
FROM toppinggroupfooditem tgfi
INNER JOIN toppinggroup tg
    ON tg.ID = tgfi.ToppingGroupID
WHERE tgfi.FoodItemID = {Id_của_món_đang_được_chọn}
LIMIT 1; #1 món chỉ có 1 topping group

/*Lấy dữ liệu cụ thể topping của ToppingGroup*/
SELECT t.ID
	  ,fi.Name
	  ,fh.Price #Giá chưa giảm
	  ,CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice #Đã giải thích ở trên
      ,fi.ImageURL
FROM topping t
INNER JOIN fooditem fi
    ON fi.ID = t.FoodItemID
INNER JOIN fooditem_history fh
    ON fi.ID = fh.FoodItemID
LEFT JOIN promotionfooditem pfi
    ON fi.ID = pfi.FoodItemID
LEFT JOIN promotion p
    ON p.ID = pfi.PromotionID
WHERE t.ToppingGroupID = {ID của topping group đã được query ở câu trên};

/*2 câu query cho topping ở trên có thể gộp như sau*/
SELECT t.ID
	,fi.Name
	,fh.Price #Giá chưa giảm
	,CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice #Đã giải thích ở trên
    ,fi.ImageURL
FROM topping t
INNER JOIN fooditem fi
    ON fi.ID = t.FoodItemID
INNER JOIN fooditem_history fh
    ON fi.ID = fh.FoodItemID
LEFT JOIN promotionfooditem pfi
    ON fi.ID = pfi.FoodItemID
LEFT JOIN promotion p
    ON p.ID = pfi.PromotionID
WHERE t.ToppingGroupID = (
                            SELECT tg.ID 
                            FROM toppinggroupfooditem tgfi
                            INNER JOIN toppinggroup tg
                                ON tg.ID = tgfi.ToppingGroupID
                            WHERE tgfi.FoodItemID = {Id_của_món_đang_được_chọn}
                            LIMIT 1
                        );