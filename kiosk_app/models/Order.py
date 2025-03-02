from typing import List
from kiosk_app.models.FoodItem import FoodItem
from kiosk_app.models.ToppingVariant import Topping, Variant
from kiosk_app.models.EnumClasses import OrderStatus, PaymentMethod


class OrderItem:
    def __init__(self, foodItem: FoodItem, quantity: int, note: str, evoucherTangMonId: int = None, toppingList:List[Topping] = [], variantList:List[Variant] = []):
        self.foodItem=foodItem #mỗi 1 OrderItem sẽ tương ứng với 1 FoodItem
        self.quantity=quantity #Kèm theo đó là một số thuộc tính khác.
        self.evoucherTangMonId = evoucherTangMonId
        self.toppingList= toppingList
        self.variantList = variantList
        self.note=note

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(food_item={self.foodItem.__repr__()!r}, quantity={self.quantity!r})')

    def __eq__(self, other):
        if isinstance(other, OrderItem): #Function này giúp ta biết được 2 object OrderItem sẽ bằng nhau khi nào. Define function sẽ hiện thực hoá phần so sánh các món có trong giỏ hàng -> chức năng tăng số lượng của một món đã tồn tại trong giỏ hàng nếu món mới được khách thêm giống y đúc.
            return self.foodItem == other.foodItem and self.evoucherTangMonId == other.evoucherTangMonId and self.toppingList == other.toppingList and self.variantList == other.variantList and self.note == other.note

class Order:
    """Đây là class quản lý giỏ hàng, đơn hàng."""
    def __init__(self):
        self.id = None #cập nhật ID sau khi đã submit order vào database
        self.paymentMethod: PaymentMethod = PaymentMethod.cash #Sử dụng enum để pick ra giá trị dạng số của payment method (VD: tiền mặt là cash -> số 1)
        self.isDineIn = True
        self.totalAmount = 0
        self.totalPrice = 0 #Tổng tiền (trước khi giảm từ evoucher)
        self.evoucherDiscount = 0 #Giảm từ evoucher
        self.orderItems: List[OrderItem] = []
        self.evoucherGiamGiaId = None #Cập nhật vào đây khi khách hàng áp mã evoucher hợp lệ
        self.orderStatus = OrderStatus.unpaid
        self.init_calculate_totals()

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(cart_items_amount={self.totalAmount!r}, total_price={self.totalPrice!r})')

    def init_calculate_totals(self):
        cart_length = len(self.orderItems)
        if cart_length > 0:
            for order_item in self.orderItems:
                self.totalAmount += order_item.quantity
                self.totalPrice += order_item.foodItem.discounted_price * order_item.quantity

    def add_new_order_items(self, orderItems: List[OrderItem]):
        """Sử dụng hàm này để thêm món mới vào đơn hàng. Nó sẽ tự động tính lại giá tổng và số lượng của đơn hàng."""
        for orderItem in orderItems:
            self.orderItems.append(orderItem)
            self.totalAmount += orderItem.quantity
            self.totalPrice += orderItem.foodItem.discounted_price * orderItem.quantity

            for topping in orderItem.toppingList:
                self.totalPrice += topping.price * orderItem.quantity

            for variant in orderItem.variantList:
                self.totalPrice += variant.price * orderItem.quantity

    def update_evoucher_díscount(self, isPercent: bool, discountValue: int, minimumPrice: int, maximumDiscount: int):
        """Sử dụng function này sau khi người dùng bấm áp dụng voucher giảm giá, check được trong hệ thống hợp lệ"""
        if self.totalPrice < minimumPrice:
            return False #Chưa đủ điều kiện áp dụng
        if isPercent:
            tempDiscount = self.totalPrice*(1-(discountValue/100))
        else:
            tempDiscount = self.totalPrice-discountValue
        if tempDiscount > maximumDiscount:
            self.evoucherDiscount = maximumDiscount
        else:
            self.evoucherDiscount = tempDiscount
        return True #Đã áp dụng mã giảm

    def modify_existing_order_items(self, index: int):
        pass #Viết hàm chỉnh sửa đơn hàng chỗ này






