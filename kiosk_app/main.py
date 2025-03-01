from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton, QVBoxLayout
from dotenv import load_dotenv, dotenv_values

from common.sql_func import Database
from kiosk_app.controllers.DineSelectViewEx import DineSelectViewEx
from kiosk_app.models.SharedDataModel import SharedDataModel
# from views import BankSuccessView, BankFailedView, BankQRView, GeneralView, PaymentSelectView, CashSuccessView
from .controllers import PaymentSelectViewEx
import threading
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv(dotenv_path='.env')
        #Tạo widget chồng để tích hợp nhiều màn hình trên cùng 1 cửa sổ
        self.mainStackedWidget = QStackedWidget()
        self.setCentralWidget(self.mainStackedWidget)
        self.sharedData = SharedDataModel()
        self.db = Database()
        #Khởi tạo toàn bộ màn hình của app
        self.dineSelectView = DineSelectViewEx(self.mainStackedWidget, self.sharedData, self.db)
        # self.paymentSelectView = PaymentSelectViewEx.PaymentSelectViewEx(self.mainStackedWidget)
        # self.bankQRView = BankQRView.BankQRWidget()
        # self.bankSuccessView = BankSuccessView.BankSuccessWidget()
        # self.bankFailedView = BankFailedView.BankFailedWidget()
        # self.cashSuccessView = CashSuccessView.CashSuccessWidget()

        self.mainStackedWidget.addWidget(self.dineSelectView)
        # self.mainStackedWidget.addWidget(self.paymentSelectView)
        # self.mainStackedWidget.addWidget(self.bankQRView)
        # self.mainStackedWidget.addWidget(self.bankSuccessView)
        # self.mainStackedWidget.addWidget(self.bankFailedView)
        # self.mainStackedWidget.addWidget(self.cashSuccessView)

        self.mainStackedWidget.setCurrentWidget(self.dineSelectView)

        #Thiết lập hành động chuyển màn hình giữa các frame khi click
        # self.paymentSelectView.left_section.clicked.connect(lambda: self.mainStackedWidget.setCurrentWidget(self.cashSuccessView))
        # self.paymentSelectView.right_section.clicked.connect(self.choose_bank)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())