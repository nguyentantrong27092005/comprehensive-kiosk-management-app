from typing import List

from payos import PayOS, PaymentData, ItemData
import os
import datetime

from kiosk_app.models.Order import OrderItem, Order

class BankPaymentHandler:
    def __init__(self):
        # load_dotenv(dotenv_path='.env')
        self.currentOrderID = None
        self.currentPaymentLink = None
        self.payOS = PayOS(client_id=os.getenv("CLIENT_ID"), api_key=os.getenv("API_KEY"), checksum_key=os.getenv("CHECKSUM_KEY"))

    @staticmethod
    def transform_items_data(orderItems: List[OrderItem]) -> List[ItemData]:
        return [ItemData(name=orderItem.foodItem.name, quantity=orderItem.quantity, price=orderItem.foodItem.discounted_price) for orderItem in orderItems]

    def create_payment(self, order: Order):
        itemsData = self.transform_items_data(order.orderItems)
        paymentData = PaymentData(orderCode=order.id, amount=order.totalPrice, description="Thanh toan don hang",
                                  items=itemsData, cancelUrl="http://localhost:8000", returnUrl="http://localhost:8000",
                                  expiredAt=int(datetime.datetime.now().timestamp()) + 300)
        try:
            self.currentPaymentLink = self.payOS.createPaymentLink(paymentData=paymentData)
            self.currentOrderID = order.id
        except Exception as e:
            print(f"Payment link creation failed: {e}")

    def get_payment_status(self):
        return self.payOS.getPaymentLinkInformation(orderId = self.currentOrderID).status

    def cancel_current_payment(self):
        self.payOS.cancelPaymentLink(orderId=self.currentOrderID, cancellationReason="Khách hàng huỷ đơn")

