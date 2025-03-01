from enum import Enum

class OrderStatus(Enum):
    unpaid = 1
    inprogress = 2
    done = 3
    cancelled = 4

class PaymentMethod(Enum):
    cash = 1
    bank = 2