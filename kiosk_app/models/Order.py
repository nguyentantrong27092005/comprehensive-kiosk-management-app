from typing import List
from kiosk_app.models.FoodItem import FoodItem
from kiosk_app.models.ToppingVariant import Topping, Variant
from kiosk_app.models.EnumClasses import OrderStatus, PaymentMethod


class OrderItem:
    def __init__(self, foodItem: FoodItem, quantity: int, note: str, evoucherTangMonId: int = None, toppingList:List[Topping] = [], variantList:List[Variant] = []):
        self.foodItem=foodItem
        self.quantity=quantity
        self.evoucherTangMonId = evoucherTangMonId
        self.toppingList= toppingList
        self.variantList = variantList
        self.note=note

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(food_item={self.foodItem.__repr__()!r}, quantity={self.quantity!r})')

    def __eq__(self, other):
        if isinstance(other, OrderItem):
            return self.foodItem == other.foodItem and self.evoucherTangMonId == other.evoucherTangMonId and self.toppingList == other.toppingList and self.variantList == other.variantList and self.note == other.note

class Order:
    def __init__(self):
        self.id = None #cập nhật ID sau khi đã submit order vào database
        self.paymentMethod: PaymentMethod = PaymentMethod.cash
        self.isDineIn = True
        self.totalAmount = 0
        self.totalPrice = 0
        self.evoucherDiscount = 0
        self.orderItems: List[OrderItem] = []
        self.evoucherGiamGiaId = None
        self.orderStatus = OrderStatus.unpaid
        self.isExist = False
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
        for orderItem in orderItems:
            self.orderItems.append(orderItem)
            self.totalAmount += orderItem.quantity
            self.totalPrice += orderItem.foodItem.discounted_price * orderItem.quantity

            for topping in orderItem.toppingList:
                self.totalPrice += topping.price * orderItem.quantity

            for variant in orderItem.variantList:
                self.totalPrice += variant.price * orderItem.quantity

            self.isExist = False

    def modify_existing_order_items(self, index: int):
        pass #Viết hàm chỉnh sửa đơn hàng chỗ này






