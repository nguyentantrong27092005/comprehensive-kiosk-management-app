from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from dotenv import load_dotenv

from common.sql_func import Database
from kiosk_app.controllers.DineSelectViewEx import DineSelectViewEx
from kiosk_app.models.SharedDataModel import SharedDataModel
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv(dotenv_path='.env')
        #Tạo widget chồng để tích hợp nhiều màn hình trên cùng 1 cửa sổ
        self.mainStackedWidget = QStackedWidget()
        self.setCentralWidget(self.mainStackedWidget)
        #Khởi tạo các class dùng chung 1 lần duy nhất
        self.sharedData = SharedDataModel()
        self.db = Database()
        #Khởi tạo các màn hình cố định của app (menu, chọn hình thức phục vụ...)
        self.dineSelectView = DineSelectViewEx(self.mainStackedWidget, self.sharedData, self.db)

        #Thêm các màn hình theo thứ tự
        self.mainStackedWidget.addWidget(self.dineSelectView)
        # self.mainStackedWidget.addWidget(self.paymentSelectView)
        # self.mainStackedWidget.addWidget(self.bankQRView)
        # self.mainStackedWidget.addWidget(self.bankSuccessView)
        # self.mainStackedWidget.addWidget(self.bankFailedView)
        # self.mainStackedWidget.addWidget(self.cashSuccessView)

        self.mainStackedWidget.setCurrentWidget(self.dineSelectView)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())