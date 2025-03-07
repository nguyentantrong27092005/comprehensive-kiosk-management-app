import os
import sys
import pymysql
from PyQt6 import QtCore, QtGui, QtWidgets
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.views.MinigameFullView import MiniGameFull
from kiosk_app.views.MinigameNoBonusView import MiniGameNoBonus
from kiosk_app.views.MinigameBonusView import MiniGameBonus
import random

# em đang tìm cách kết nôis từ sql_func --> nên em đang tạo thử class db --> sau khi em tìm hiểu xong thì em sẽ import qua ạ
class Database_ToppingSelection:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host="34.101.167.101",
                user="dev",
                password="12345678x@X",
                database="kioskapp",
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
        except pymysql.MySQLError as e:
            self.connection = None
            print(f"Database connection error: {e}")

class MiniGameFullEx(MiniGameFull):
    def __init__(self, mainStackedWidget: QtWidgets.QStackedWidget, sharedData, db):
        super().__init__()
        self.sharedData = sharedData
        self.db = db
        self.mainStackedWidget = mainStackedWidget
        self.setup_connections()

    def setup_connections(self):
        for button in self.gift_buttons:
            button.clicked.connect(self.open_random_gift)

    def open_random_gift(self):
        if random.choice([True, False]):  # 50% ra MiniGameBonus, 50% ra MiniGameNoBonus
            self.bonus_window = MiniGameBonus()
            self.bonus_window.show()
        else:
            self.no_bonus_window = MiniGameNoBonus()
            self.no_bonus_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    sharedData = SharedDataModel()
    db = Database_ToppingSelection()
    mainStackedWidget = QtWidgets.QStackedWidget()
    window = MiniGameFullEx(mainStackedWidget, sharedData, db)
    window.show()
    sys.exit(app.exec())