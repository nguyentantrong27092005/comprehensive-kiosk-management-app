from common.sql_func import Database
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.views import GeneralView
from PyQt6.QtWidgets import QVBoxLayout, QStackedWidget
from kiosk_app.views.CashSuccessView import CashSuccessWidget


class CashSuccessViewEx(GeneralView.GeneralView):
    def __init__(self, mainStackedWidget: QStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.mainStackedWidget = mainStackedWidget
        self.sharedData = sharedData
        self.db = db

        #Khởi tạo và thay đổi nội dung màn hình cash success
        self.cashSuccessView = CashSuccessWidget()

        #Thêm vào frame chung
        self.cashSuccessVLayout = QVBoxLayout(self.frame_chung)
        self.cashSuccessVLayout.addWidget(self.cashSuccessView)
        self.cashSuccessVLayout.setContentsMargins(0, 0, 0, 0)

        #Nối nút với hành động
        self.cashSuccessView.confirmButton.clicked.connect(self.back_to_beginning)

    def back_to_beginning(self):
        self.mainStackedWidget.setCurrentIndex(0)
