from common.sql_func import Database
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.views import BankFailedView, GeneralView
from PyQt6.QtWidgets import QVBoxLayout, QStackedWidget

class BankFailedViewEx(GeneralView.GeneralView):
    def __init__(self, mainStackedWidget: QStackedWidget, sharedData: SharedDataModel, db: Database, title, subtitle):
        super().__init__()
        self.mainStackedWidget = mainStackedWidget
        self.sharedData = sharedData
        self.db = db
        self.title = title
        self.subtitle = subtitle

        #Khởi tạo và thay đổi nội dung màn hình bank failed
        self.bankFailedView = BankFailedView.BankFailedWidget()
        self.bankFailedView.notificationTitle.setText(title)
        self.bankFailedView.instructionSubtitle.setText(subtitle)

        #Thêm vào frame chung
        self.bankFailedVLayout = QVBoxLayout(self.frame_chung)
        self.bankFailedVLayout.addWidget(self.bankFailedView)
        self.bankFailedVLayout.setContentsMargins(0, 0, 0, 0)

        #Nối nút với hành động
        self.bankFailedView.confirmButton.clicked.connect(self.back_to_beginning)

    def back_to_beginning(self):
        self.mainStackedWidget.setCurrentIndex(0)
        self.mainStackedWidget.removeWidget(self)
