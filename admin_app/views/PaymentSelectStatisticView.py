from decimal import Decimal
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHeaderView
from admin_app.views.GeneralView import GeneralView


class PaymentSelectViewStatistics(GeneralView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Báo cáo phương thức thanh toán")
        self.main_layout = QtWidgets.QVBoxLayout(self.frameContent)
        self.init_ui()
        self.pushButtonPaymentMethod.setStyleSheet(
            "background-color: white; color: red; font-size: 14px; font-weight: bold;")

    def init_ui(self):

        # Tạo khung trên
        top_frame = QtWidgets.QFrame()
        top_layout = QtWidgets.QHBoxLayout()

        # Tạo biểu đồ tròn
        pie_chart_frame = QtWidgets.QFrame()
        pie_chart_layout = QtWidgets.QVBoxLayout()
        pie_chart_frame.setLayout(pie_chart_layout)

        # Tạo biểu đồ đường
        line_chart_frame = QtWidgets.QFrame()
        line_chart_layout = QtWidgets.QVBoxLayout()
        line_chart_frame.setLayout(line_chart_layout)

        # Thêm biểu đồ đường và biểu đồ
        top_layout.addWidget(line_chart_frame, 1)
        top_layout.addWidget(pie_chart_frame, 1)
        top_frame.setLayout(top_layout)

        # Tạo khung dưới
        bottom_frame = QtWidgets.QFrame()
        bottom_layout = QtWidgets.QVBoxLayout()

        # Tạo một QScrollArea để chứa bảng
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Tạo bảng
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["#", "Phương thức thanh toán", "Số hóa đơn", "Tổng tiền"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Thiết lập bảng để có thể cuộn
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        font = QFont()
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)

        # Đưa bảng vào vùng cuộn
        scroll_area.setWidget(self.table)
        bottom_layout.addWidget(scroll_area)
        bottom_frame.setLayout(bottom_layout)

        # Thêm khung trên và khung dưới vào khung chính
        self.main_layout.addWidget(top_frame, 2)
        self.main_layout.addWidget(bottom_frame, 3)
        self.setLayout(self.main_layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PaymentSelectViewStatistics()
    window.show()
    sys.exit(app.exec())
