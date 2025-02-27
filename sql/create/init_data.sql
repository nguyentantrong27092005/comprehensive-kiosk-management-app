USE kioskapp;
INSERT INTO Category (Name, ImageURL)
VALUES
('Đồ uống', '../resources/images/tra.png'),
('Gà', '../resources/images/ga_category.png'),
('Mì', '../resources/images/mi_category.png'),
('Ăn vặt', '../resources/images/anvat_category.png'),
('Topping nước', '../resources/images/toppingnuoc.png');

SELECT * FROM Category;

INSERT INTO fooditem (CategoryID, CustomID, Name, IsBestSeller, IsFulltime, Days, AvailableStartTime, AvailableEndTime, ImageURL)
VALUES
((SELECT ID FROM Category WHERE Name = 'Đồ uống'), 'DRINK01', 'Trà xoài', 1, 1, NULL, NULL, NULL, '../resources/images/traxoai.png'),
((SELECT ID FROM Category WHERE Name = 'Đồ uống'), 'DRINK02', 'Trà đào', 0, 1, NULL, NULL, NULL, '../resources/images/tra.png'),
((SELECT ID FROM Category WHERE Name = 'Đồ uống'), 'DRINK03', 'Trà ổi hồng', 0, 1, NULL, NULL, NULL, '../resources/images/traoihong.png'),
((SELECT ID FROM Category WHERE Name = 'Đồ uống'), 'DRINK04', 'Trà kiwi', 1, 1, NULL, NULL, NULL, '../resources/images/trakiwi.png'),
((SELECT ID FROM Category WHERE Name = 'Đồ uống'), 'DRINK05', 'Trà đặc biệt', 1, 0, '5|6|', TIME('13:00:00'), TIME('17:00:00'), '../resources/images/tradacbiet.png'),
((SELECT ID FROM Category WHERE Name = 'Đồ uống'), 'DRINK06', 'Trà tuesday', 1, 0, '1|', TIME('00:00:00'), TIME('23:59:00'), '../resources/images/tratuesday.png'),
((SELECT ID FROM Category WHERE Name = 'Đồ uống'), 'DRINK07', 'Trà thứ sáu', 1, 0, '4|', TIME('00:00:00'), TIME('23:59:00'), '../resources/images/trathusau.png'),
((SELECT ID FROM Category WHERE Name = 'Gà'), 'CHICKEN01', 'Gà rán truyền thống', 1, 1, NULL, NULL, NULL, '../resources/images/garantruyenthong.png'),
((SELECT ID FROM Category WHERE Name = 'Gà'), 'CHICKEN02', 'Gà chiên mắm tỏi', 1, 1, NULL, NULL, NULL, '../resources/images/gachienmamtoi.png'),
((SELECT ID FROM Category WHERE Name = 'Gà'), 'CHICKEN03', 'Gà đặc biệt', 1, 0, '5|6|', TIME('13:00:00'), TIME('17:00:00'), '../resources/images/gadacbiet.png'),
((SELECT ID FROM Category WHERE Name = 'Gà'), 'CHICKEN04', 'Gà tuesday', 1, 0, '1|', TIME('00:00:00'), TIME('23:59:00'), '../resources/images/gatuesday.png'),
((SELECT ID FROM Category WHERE Name = 'Mì'), 'NOODLES01', 'Mì ý sốt cà', 1, 1, NULL, NULL, NULL, '../resources/images/miysotca.png'),
((SELECT ID FROM Category WHERE Name = 'Mì'), 'NOODLES02', 'Mì ý sốt kem béo', 1, 1, NULL, NULL, NULL, '../resources/images/miysotca.png'),
((SELECT ID FROM Category WHERE Name = 'Mì'), 'NOODLES03', 'Mì trứng truyền thống', 1, 1, NULL, NULL, NULL, '../resources/images/mitrungtruyenthong.png'),
((SELECT ID FROM Category WHERE Name = 'Mì'), 'NOODLES04', 'Mì tuesday', 1, 0, '1|', TIME('00:00:00'), TIME('23:59:00'), '../resources/images/mituesday.png'),
((SELECT ID FROM Category WHERE Name = 'Ăn vặt'), 'SNACK01', 'Khoai chiên truyền thống', 1, 1, NULL, NULL, NULL, '../resources/images/khoaichientruyenthong.png'),
((SELECT ID FROM Category WHERE Name = 'Ăn vặt'), 'SNACK02', 'Khoai chiên đặc biệt', 1, 1, NULL, NULL, NULL, '../resources/images/khoaichientruyenthong.png'),
((SELECT ID FROM Category WHERE Name = 'Topping nước'), 'TOPPING01', 'Trân châu đen', 1, 1, NULL, NULL, NULL, '../resources/images/tranchauden.png'),
((SELECT ID FROM Category WHERE Name = 'Topping nước'), 'TOPPING02', 'Trân châu trắng', 1, 1, NULL, NULL, NULL, '../resources/images/tranchautrang.png'),
((SELECT ID FROM Category WHERE Name = 'Topping nước'), 'TOPPING03', 'Trân châu hoàng kim', 1, 1, NULL, NULL, NULL, '../resources/images/tranchauhoangkim.png'),
((SELECT ID FROM Category WHERE Name = 'Topping nước'), 'TOPPING04', 'Pudding trứng', 1, 1, NULL, NULL, NULL, '../resources/images/puddingtrung.png'),
((SELECT ID FROM Category WHERE Name = 'Topping nước'), 'TOPPING05', 'Đào miếng', 1, 1, NULL, NULL, NULL, '../resources/images/daomieng.png')
;

SELECT * FROM fooditem;

INSERT INTO fooditem_history (FoodItemID, Price, Cost, IsEffective)
VALUES
(1, 22000, 8000, 1),
(2, 19000, 6000, 1),
(3, 19000, 6000, 1),
(4, 22000, 7900, 0),
(4, 20000, 8200, 0),
(4, 21000, 7900, 1),
(5, 26000, 7900, 0),
(5, 32000, 9200, 1),
(6, 32000, 9200, 1),
(7, 32000, 9200, 1),
(8, 55000, 15500, 1),
(9, 59000, 16500, 1),
(10, 69000, 20500, 1),
(11, 69000, 18500, 1),
(12, 55000, 15500, 1),
(13, 51000, 14500, 1),
(14, 45000, 10500, 1),
(15, 65000, 17500, 1),
(16, 29000, 5600, 1),
(17, 45000, 5600, 1),
(18, 5000, 1000, 1),
(19, 7000, 1200, 1),
(20, 7000, 1200, 1),
(21, 8000, 1400, 1),
(22, 7000, 1200, 1);

SELECT * FROM fooditem_history;

INSERT INTO promotion (Name, Discount, IsPercent, StartDate, EndDate, IsEffective)
VALUES
('Siêu sale tháng 2,3', 15, 1, TIMESTAMP("2025-02-01",  "00:00:00"), TIMESTAMP("2025-03-31",  "00:00:00"), 1),
('Kick sale cho trà còn tồn', 3000, 0, TIMESTAMP("2025-02-24",  "00:00:00"), TIMESTAMP("2025-03-31",  "00:00:00"), 1),
('Test chương trình hết hạn', 3000, 0, TIMESTAMP("2025-02-24",  "00:00:00"), TIMESTAMP("2025-02-27",  "00:00:00"), 1);

SELECT * FROM promotion;

INSERT INTO promotionfooditem (PromotionID, FoodItemID)
VALUES
(1, 8),
(1, 9),
(1, 12),
(1, 13),
(2, 2),
(2, 4),
(3, 14);

SELECT * FROM promotionfooditem;

INSERT INTO variantgroup (Name, IsRequired, ViewType, HasPrice)
VALUES
('[Đồ uống] Chọn size', 1, 'ChonSize', 1),
('[Đồ uống] Chọn đá', 1, 'Slider', 0),
('[Đồ uống] Chọn đường', 1, 'RadioList', 0),
('[Thức ăn] Chọn độ cay', 1, 'RadioList', 0),
('[Khoai] Chọn loại khoai', 1, 'RadioList', 0),
('[Khoai] Chọn size', 1, 'ChonSize', 1),
('[Khoai đặc biệt] Chọn vị', 1, 'RadioList', 1);

SELECT * FROM variantgroup;

INSERT INTO variant (VariantGroupID, Value, Price, AdditionalCost)
VALUES
(1, 'S', 0, 0),
(1, 'M', 9000, 2000),
(1, 'L', 16000, 5500),
(1, 'XL', 20000, 7000),
(3, 'Không đường', 0, 0),
(3, 'Ít đường', 0, 0),
(3, 'Bình thường', 0, 0),
(3, 'Nhiều đường', 0, 0),
(4, 'Không cay', 0, 0),
(4, 'Cay', 0, 0),
(5, 'Khoai tây', 0, 0),
(5, 'Khoai lang', 0, 0),
(6, 'S', 0, 0),
(6, 'M', 7000, 2000),
(6, 'L', 11000, 4000),
(7, 'Lắc phô mai', 0, 0),
(7, 'Sốt chua ngọt', 4000, 1200);

SELECT * FROM variant;

INSERT INTO variantgroupfooditem (VariantGroupID, FoodItemID)
SELECT vg.ID AS VariantGroupID
	  ,fi.ID AS FoodItemID
FROM fooditem fi
INNER JOIN Category c
ON c.ID = fi.CategoryID
JOIN variantgroup vg
WHERE c.Name = 'Đồ uống'
AND vg.Name LIKE '%Đồ uống%';

INSERT INTO variantgroupfooditem (VariantGroupID, FoodItemID)
SELECT vg.ID AS VariantGroupID
	  ,fi.ID AS FoodItemID
FROM fooditem fi
INNER JOIN Category c
ON c.ID = fi.CategoryID
JOIN variantgroup vg
WHERE c.Name <> 'Đồ uống' AND c.Name <> 'Topping nước'
AND vg.Name LIKE '%Thức ăn%';

INSERT INTO variantgroupfooditem (VariantGroupID, FoodItemID)
SELECT vg.ID AS VariantGroupID
	  ,fi.ID AS FoodItemID
FROM fooditem fi
JOIN variantgroup vg
WHERE fi.Name LIKE 'Khoai%'
AND vg.Name LIKE '%Khoai]%';

INSERT INTO variantgroupfooditem (VariantGroupID, FoodItemID)
SELECT vg.ID AS VariantGroupID
	  ,fi.ID AS FoodItemID
FROM fooditem fi
JOIN variantgroup vg
WHERE fi.Name = 'Khoai chiên đặc biệt'
AND vg.Name LIKE '%Khoai đặc biệt]%';

SELECT * FROM variantgroupfooditem;

INSERT INTO toppinggroup (Name)
VALUES
('Gà'),
('Đồ uống'),
('Đồ ăn vặt'),
('Mì');

SELECT * FROM toppinggroup;

INSERT INTO toppinggroupfooditem (ToppingGroupID, FoodItemID)
SELECT (SELECT ID FROM toppinggroup WHERE Name = 'Gà' LIMIT 1)
	,fi.ID
FROM fooditem fi
INNER JOIN Category c
ON c.ID = fi.CategoryID
WHERE c.Name = 'Gà'
UNION
SELECT (SELECT ID FROM toppinggroup WHERE Name = 'Đồ uống' LIMIT 1)
	,fi.ID
FROM fooditem fi
INNER JOIN Category c
ON c.ID = fi.CategoryID
WHERE c.Name = 'Đồ uống'
UNION
SELECT (SELECT ID FROM toppinggroup WHERE Name = 'Đồ ăn vặt' LIMIT 1)
	,fi.ID
FROM fooditem fi
INNER JOIN Category c
ON c.ID = fi.CategoryID
WHERE c.Name = 'Ăn vặt'
UNION
SELECT (SELECT ID FROM toppinggroup WHERE Name = 'Mì' LIMIT 1)
	,fi.ID
FROM fooditem fi
INNER JOIN Category c
ON c.ID = fi.CategoryID
WHERE c.Name = 'Mì';

SELECT * FROM toppinggroupfooditem;

INSERT INTO topping (ToppingGroupID, FoodItemID)
SELECT (SELECT ID FROM toppinggroup WHERE Name = 'Gà')
	  ,ID
FROM fooditem
WHERE CustomID LIKE 'SNACK%' OR CustomID LIKE 'DRINK%'
UNION
SELECT (SELECT ID FROM toppinggroup WHERE Name = 'Đồ ăn vặt')
	  ,ID
FROM fooditem
WHERE CustomID LIKE 'NOODLES%' OR CustomID LIKE 'CHICKEN%'
UNION
SELECT (SELECT ID FROM toppinggroup WHERE Name = 'Đồ uống')
	  ,ID
FROM fooditem
WHERE CustomID LIKE 'TOPPING%';

SELECT * FROM topping;

INSERT INTO evoucher (Name, Category, StartDate, EndDate, IsEffective)
VALUES
('Chương trình tặng nước tháng 2,3', 'Tang mon', TIMESTAMP("2025-02-01",  "00:00:00"), TIMESTAMP("2025-03-31",  "00:00:00"), 1),
('Chương trình khách hàng bóc thăm may mắn', 'Giam gia', TIMESTAMP("2025-02-01",  "00:00:00"), TIMESTAMP("2025-03-31",  "00:00:00"), 1);

SELECT * FROM evoucher;

INSERT INTO evouchergiamgia (EVoucherID, Discount, IsPercent, MinimumPrice, MaximumDiscount)
VALUES
(2, 15, 1, 250000, 70000);

SELECT * FROM evouchergiamgia;

INSERT INTO evouchergiamgialist (EVoucherGiamGiaID, Value, IsUsed)
VALUES
(1, 'TESTGIAMGIA01', 0),
(1, 'TESTGIAMGIA02', 0),
(1, 'TESTGIAMGIA03', 0),
(1, 'TESTGIAMGIA04', 0),
(1, 'TESTGIAMGIA05', 0),
(1, 'TESTGIAMGIA06', 0);

SELECT * FROM evouchergiamgialist;

INSERT INTO evouchertangmon (EVoucherID, FoodItemID, MinimumPrice, Amount)
VALUES
(1, (SELECT ID FROM fooditem WHERE Name = 'Trà đào'), 250000, 2),
(1, (SELECT ID FROM fooditem WHERE Name = 'Trà xoài'), 250000, 1)
;

SELECT * FROM evouchertangmon;

INSERT INTO evouchertangmonlist (EVoucherTangMonID, Value, IsUsed)
VALUES
(1, 'TESTTANGMON01', 0),
(1, 'TESTTANGMON02', 0),
(1, 'TESTTANGMON03', 0),
(1, 'TESTTANGMON04', 0),
(1, 'TESTTANGMON05', 0),
(1, 'TESTTANGMON06', 0);

SELECT * FROM evouchertangmonlist;