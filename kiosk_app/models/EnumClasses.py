from enum import Enum

#Enum class được sử dụng cho các field enum trong dataset. Mình sẽ quy định hẳn trong này và truy xuất giá trị (dạng số) tương ứng
#để không bị nhầm lẫn khi insert vào db có những cột cần Enum này (ví dụ OrderStatus, Payment)
class OrderStatus(Enum):
    unpaid = 1
    inprogress = 2
    done = 3
    cancelled = 4

class PaymentMethod(Enum):
    cash = 1
    bank = 2