from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, \
    QMessageBox
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QSize
import sys


class FeedbackKhachhangView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Nhãn tiêu đề
        self.title_label = QLabel("Đánh giá của khách hàng")
        self.title_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFixedHeight(40)
        self.layout.addWidget(self.title_label)

        # Nút gửi
        self.submit_button = QPushButton(" Gửi")
        self.submit_button.setStyleSheet(
            "background-color: #bd1906; color: white; padding: 10px; border-radius: 10px; font-size: 15px; font-weight: bold;")
        self.submit_button.setIcon(QIcon("kiosk_app/resources/images/ic_submit.png"))
        self.submit_button.setIconSize(QSize(24, 24))
        self.submit_button.setMinimumSize(440, 50)


