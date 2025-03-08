#Các class data model sẽ bao gồm các field
#Mục đích tạo các class dạng data model nhầm ràng buộc và thống nhất với nhau cần kéo những data gì, lưu trữ khi app đang chạy để có thể phục vụ cho
#nhiều tác vụ khác nhau. Ví dụ: FoodItem có thể được sử dụng trong màn hình menu, màn hình giỏ hàng, submit order vào database
#Ứng dụng thiết thực là: backend màn hình menu sẽ phụ trách query data của bảng fooditem và mỗi dòng trong kết quả query
#sẽ được khởi tạo thành 1 object FoodItem. Màn hình giỏ hàng (order) có data model là Order và OrderItem rất cần thông tin
#từ FoodItem này. Do đó, khi khách hàng bấm thêm một món vào giỏ hàng, object FoodItem tương ứng của món đó sẽ được truyền cho
#OrderItem -> hình thành sự kết nối chặt chẽ, có ràng buộc về mặt data mà không cần phải tốn công join bảng hoặc query lặp đi lặp lại nhiều lần.
class FoodItem:
    def __init__(self, id: int, name: str, price: int, discounted_price: int, image_url: str, is_best_seller: bool, promotion_id = None):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url
        self.is_best_seller = is_best_seller
        self.discounted_price = discounted_price
        self.promotion_id = promotion_id
        self.discount = self.price - self.discounted_price
        print(f"FoodItem created: {self}")

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(id={self.id!r}, name={self.name!r}), price={self.price!r}')

    def __eq__(self, other):
        if isinstance(other, FoodItem):
            return self.id == other.id and self.promotion_id == other.promotion_id

