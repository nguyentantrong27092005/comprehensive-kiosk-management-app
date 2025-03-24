from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from common.sql_func import Database
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.views import GeneralView
from PyQt6.QtWidgets import QVBoxLayout

from kiosk_app.views.MiniGameNoBonusView import MiniGameNoBonus
from kiosk_app.views.CustomStackedWidget import CustomStackedWidget


class MinigameNoBonusViewEx(GeneralView.GeneralView):
    def __init__(self, mainStackedWidget: CustomStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.mainStackedWidget = mainStackedWidget
        self.sharedData = sharedData
        self.db = db

        #Khởi tạo và thay đổi nội dung màn hình bank failed
        self.minigameNoBonusView = MiniGameNoBonus()
        self.frame_ngang.hide()
        #Thêm vào frame chung
        self.minigameNoBonusVLayout = QVBoxLayout(self.frame_chung)
        self.minigameNoBonusVLayout.addWidget(self.minigameNoBonusView)
        self.minigameNoBonusVLayout.setContentsMargins(0, 0, 0, 0)
        self.minigameNoBonusVLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setMaximumHeight(150)
        self.frame_chung.setStyleSheet("background-color: white;")

        #Nối nút với hành động
        self.minigameNoBonusView.pushButton_confirm.clicked.connect(self.back_to_beginning)

    def back_to_beginning(self):
        self.mainStackedWidget.change_screen_with_index(0, self)
