from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHeaderView, QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy, QTableWidget, QScrollArea

from admin_app.views.GeneralView import GeneralView


class PaymentSelectViewStatistics(GeneralView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mặt hàng ban chay")
        self.main_layout = QtWidgets.QVBoxLayout(self.frameContent)
        self.init_ui()
        self.pushButtonMHBC.setStyleSheet(
            "background-color: white; color: red; font-size: 14px; font-weight: bold;")

    def init_ui(self):
        top_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        right_layout = QVBoxLayout()

        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        top_widget.setFixedHeight(250)
        top_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        top_layout.addLayout(left_layout, 1)
        top_layout.addLayout(right_layout, 1)

        # Sử dụng lineEditSearch và pushButton từ GeneralViewEx
        self.lineEditSearch.setPlaceholderText("Nhập từ khóa tìm kiếm...")

        self.main_layout.addWidget(top_widget, 2)
        self.pushButtonMHBC.setStyleSheet(
            "background-color: white; color: red; font-size: 14px; font-weight: bold;"
        )

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Mã món", "Tên món", "Nhóm món", "Số lượng", "Giảm giá", "Doanh thu", "Lợi nhuận"
        ])
        self.table.setStyleSheet("background-color: white;")
        self.table.setFont(QFont("Arial", 10))
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.verticalHeader().setVisible(False)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.table)

        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.addWidget(scroll_area)
        bottom_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Thêm khung trên và khung dưới vào khung chính
        self.main_layout.addWidget(top_widget, 2)
        self.main_layout.addWidget(bottom_widget, 3)
        self.setLayout(self.main_layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PaymentSelectViewStatistics()
    window.show()
    sys.exit(app.exec())