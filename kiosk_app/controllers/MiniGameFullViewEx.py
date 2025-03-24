import sys
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QVBoxLayout

from common.sql_func import Database
from kiosk_app.controllers.MinigameBonusViewEx import MinigameBonusViewEx
from kiosk_app.controllers.MinigameNoBonusViewEx import MinigameNoBonusViewEx
from kiosk_app.models.SharedDataModel import SharedDataModel
import random

from kiosk_app.views.GeneralView import GeneralView
from kiosk_app.views.MiniGameFullView import MiniGameFull
from kiosk_app.views.CustomStackedWidget import CustomStackedWidget


class MiniGameFullEx(GeneralView):
    def __init__(self, mainStackedWidget: CustomStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.sharedData = sharedData
        self.db = db
        self.mainStackedWidget = mainStackedWidget
        self.minigameFullView = MiniGameFull()
        self.frame_ngang.hide()
        self.minigameFullVLayout = QVBoxLayout(self.frame_chung)
        self.minigameFullVLayout.addWidget(self.minigameFullView)
        self.minigameFullVLayout.setContentsMargins(0, 0, 0, 0)
        self.label_image.setMaximumHeight(150)
        self.setup_connections()

    def setup_connections(self):
        for button in self.minigameFullView.gift_buttons:
            button.clicked.connect(self.open_random_gift)

    def open_random_gift(self):
        if random.choice([True, False]):  # 50% ra MiniGameBonus, 50% ra MiniGameNoBonus
            bonus_window = MinigameBonusViewEx(self.mainStackedWidget, self.sharedData, self.db)
            self.mainStackedWidget.change_screen(bonus_window, self)
        else:
            no_bonus_window = MinigameNoBonusViewEx(self.mainStackedWidget, self.sharedData, self.db)
            self.mainStackedWidget.change_screen(no_bonus_window, self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    sharedData = SharedDataModel()
    db = Database()
    mainStackedWidget = QtWidgets.QStackedWidget()
    window = MiniGameFullEx(mainStackedWidget, sharedData, db)
    window.show()
    sys.exit(app.exec())