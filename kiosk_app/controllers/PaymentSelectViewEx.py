from common.sql_func import Database
from kiosk_app.controllers.CashSuccessViewEx import CashSuccessViewEx
from kiosk_app.models.EnumClasses import PaymentMethod
from kiosk_app.views import PaymentSelectView, GeneralView
from kiosk_app.controllers import BankQRViewEx
from PyQt6.QtWidgets import QVBoxLayout, QStackedWidget
from kiosk_app.models.SharedDataModel import SharedDataModel


class PaymentSelectViewEx(GeneralView.GeneralView):
    def __init__(self, mainStackedWidget: QStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.sharedData = sharedData
        self.db = db
        self.mainStackedWidget = mainStackedWidget
        self.paymentSelectWidget = PaymentSelectView.PaymentSelectWidget()
        self.paymentVLayout = QVBoxLayout(self.frame_chung)
        self.paymentVLayout.addWidget(self.paymentSelectWidget)
        self.paymentVLayout.setContentsMargins(0, 0, 0, 0)
        self.paymentSelectWidget.left_section.clicked.connect(self.choose_cash)
        self.paymentSelectWidget.right_section.clicked.connect(self.choose_bank)

    def choose_bank(self):
        self.sharedData.order.paymentMethod = PaymentMethod.bank
        self.db.submit_order_transaction(self.sharedData.order)
        bankQRView = BankQRViewEx.BankQRViewEx(self.mainStackedWidget, self.sharedData, self.db)
        self.mainStackedWidget.addWidget(bankQRView)
        self.mainStackedWidget.setCurrentWidget(bankQRView)

    def choose_cash(self):
        self.sharedData.order.paymentMethod = PaymentMethod.cash
        self.db.submit_order_transaction(self.sharedData.order)
        self.sharedData.reset_data()
        cashSuccessView = CashSuccessViewEx(self.mainStackedWidget, self.sharedData, self.db)
        self.mainStackedWidget.addWidget(cashSuccessView)
        self.mainStackedWidget.setCurrentWidget(cashSuccessView)
        cashSuccessView.pushButton_back.setVisible(True)

