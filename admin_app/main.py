from PyQt6.QtCore import Qt, QTimer, QSize, QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLabel
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
        self.resize(478, 850)

        self.mainStackedWidget = CustomStackedWidget(self)
        self.setCentralWidget(self.mainStackedWidget)

        #Countdown timer
        self.count = 150
        self.countdownTimerLabel = QLabel(self)
        self.countdownTimerLabel.setObjectName("countdownTimerLabel")
        self.countdownTimerLabel.setGeometry(QRect(410, 160, 61, 21))
        self.countdownTimerLabel.setStyleSheet("background-color: #BD1906; font-family: Montserrat; font-size: 10px; color: white; border: 2px solid white;")
        self.countdownTimerLabel.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.countdownTimerLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.countdownTimer = QTimer(self)
        self.countdownTimer.start(1000)

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
        # self.countdownTimerLabel.setHidden(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())