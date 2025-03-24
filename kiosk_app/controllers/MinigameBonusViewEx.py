from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from common.sql_func import Database
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.views import GeneralView
from PyQt6.QtWidgets import QVBoxLayout

from kiosk_app.views.MiniGameBonusView import MiniGameBonus
from kiosk_app.views.CustomStackedWidget import CustomStackedWidget


class MinigameBonusViewEx(GeneralView.GeneralView):
    def __init__(self, mainStackedWidget: CustomStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.mainStackedWidget = mainStackedWidget
        self.sharedData = sharedData
        self.db = db

        #Khởi tạo và thay đổi nội dung màn hình bank failed
        self.minigameBonusView = MiniGameBonus()
        self.pushButton_back.setText("Hộp quà may mắn")
        self.pushButton_back.setIcon(QtGui.QIcon())        #Thêm vào frame chung
        self.minigameBonusVLayout = QVBoxLayout(self.frame_chung)
        self.minigameBonusVLayout.addWidget(self.minigameBonusView)
        self.minigameBonusVLayout.setContentsMargins(0, 0, 0, 0)
        self.minigameBonusVLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setMaximumHeight(150)
        self.frame_chung.setStyleSheet("background-color: white;")

        #Nối nút với hành động
        self.minigameBonusView.button_confirm.clicked.connect(self.back_to_beginning)

    def back_to_beginning(self):
        self.mainStackedWidget.change_screen_with_index(0, self)
