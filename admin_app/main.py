from PyQt6.QtWidgets import QApplication, QMainWindow
from dotenv import load_dotenv

from common.sql_func import Database
from admin_app.controllers.LoginAppViewEx import LoginAppViewEx
from admin_app.controllers.HomePageViewEx import HomePageViewEx
from admin_app.models.SharedDataModel import SharedDataModel
import sys

from kiosk_app.views.CustomStackedWidget import CustomStackedWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #Load file môi trường
        load_dotenv(dotenv_path='.env')

        #Tạo widget chồng để tích hợp nhiều màn hình trên cùng 1 cửa sổ
        self.setWindowTitle('Kiosk Application')
        self.resize(1280, 720)

        self.mainStackedWidget = CustomStackedWidget(self)
        self.setCentralWidget(self.mainStackedWidget)

        #Khởi tạo các class dùng chung 1 lần duy nhất
        self.sharedData = SharedDataModel()
        self.db = Database()

        #Khởi tạo các màn hình cố định của app (menu, chọn hình thức phục vụ...)
        self.loginAppView = LoginAppViewEx(self.mainStackedWidget, self.sharedData, self.db)
        self.homePageView = HomePageViewEx(self.mainStackedWidget, self.sharedData, self.db)

        #Thêm các màn hình theo thứ tự
        self.mainStackedWidget.addWidget(self.loginAppView)
        self.mainStackedWidget.addWidget(self.homePageView)

        #Đặt màn hình đầu tiên
        self.mainStackedWidget.setCurrentWidget(self.loginAppView)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())