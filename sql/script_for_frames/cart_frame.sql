/*Check xem voucher người dùng có phải voucher giảm giá không. Nếu đúng thì kiểm tra tiếp voucher đó đã được sd chưa. Nếu chưa thì câu query sẽ trả kết quả*/
SELECT ID #ID của voucher
	  ,EvoucherGiamGiaID #ID của chương trình giảm giá
FROM evouchergiamgialist
WHERE Value = {Mã voucher người dùng nhập}
AND IsUsed = False #Kiểm tra voucher đã sử dụng chưa
LIMIT 1; #Thường chỉ khớp với 1 mã voucher duy nhất, bỏ qua các trường hợp 1 mã có nhiều ID trong bảng evouchergiamgialist

/*Nếu check ra đúng là voucher giảm giá, kiểm tra xem chương trình còn hiệu lực không. Nếu có thì câu query sẽ trả ra kết quả chi tiết chương trình của voucher. 
Sử dụng dữ liệu để áp giảm giá cho tổng đơn hàng.*/
SELECT evgg.ID
	  ,evgg.Discount #Giá trị giảm
	  ,evgg.IsPercent #Flag giảm theo phần trăm
      ,evgg.MinimumPrice #Hoá đơn ít nhất bao nhiêu thì mới được áp mã giảm giá
      ,evgg.MaximumDiscount #Hoá đon được giảm nhiều nhất là bao nhiêu
FROM evouchergiamgia evgg
INNER JOIN evoucher ev
ON ev.ID = evgg.EVoucherID
WHERE evgg.ID = {EvoucherGiamGiaID query được ở câu trên}
AND ev.IsEffective = True; #Chương trình còn hiệu lực


/*Check xem voucher người dùng có phải voucher tặng món và đã qua sử dụng chưa. Nếu đúng thì câu query sẽ trả kết quả. 
Nếu không thì hiện thông báo trên UI evoucher không hợp lệ, hoặc đã bị sử dụng.*/
SELECT ID
	  ,EVoucherTangMonID
FROM evouchertangmonlist
WHERE Value = {Mã voucher người dùng nhập}
AND IsUsed = False; #Kiểm tra voucher đã sử dụng chưa

/*Nếu voucher người dùng là voucher tặng món, sẽ kiểm tra thêm chương trình còn hiệu lực không. Nếu còn hiệu lực thì giỏ hàng sẽ tự động add thông tin sản phẩm được 
tặng vào giỏ hàng theo số lượng đã được setup trong db. Sử dụng câu query sau để lấy dữ liệu món tặng. Nếu query không trả lại kq thì hiện thông báo trên UI evoucher đã hết hạn.*/
SELECT fi.ID
	  ,fi.Name
	  ,fi.ImageURL
	  ,fih.Price
	  ,0 AS DiscountedPrice #Tặng món nên giá sau giảm là 0đ
	  ,evtm.ID AS EvoucherTangMonID
	  ,evtm.Amount #Số lượng món được tặng
      ,evtm.MinimumPrice #Hoá đơn ít nhất bao nhiêu thì mới được áp mã giảm giá
FROM evouchertangmon evtm
INNER JOIN evoucher ev
ON ev.ID = evtm.EVoucherID
INNER JOIN fooditem fi
ON fi.ID = evtm.FoodItemID
INNER JOIN fooditem_history fih
ON fi.ID = fih.FoodItemID
WHERE evtm.EVoucherID = 1
AND ev.IsEffective = TRUE #chương trình còn hiệu lực không
AND fih.IsEffective = TRUE;