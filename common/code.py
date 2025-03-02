import os
from random import random

from PyQt6 import QtCore, QtGui, QtWidgets

class UI_noluck(QtWidgets.QDialog):
    """Cửa sổ hiển thị kết quả mở hộp quà --- không trúng gì hết"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kết Quả")
        self.setFixedSize(398, 708)
        self.setStyleSheet("background-color: white;")

        # Layout chính
        layout = QtWidgets.QVBoxLayout(self)

        # Hình ảnh minigame phần no luck
        self.label_image_main = QtWidgets.QLabel(self)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "bannermngame.png")
        pixmap = QtGui.QPixmap(image_path)
        self.label_image_main.setPixmap(pixmap)
        self.label_image_main.setFixedHeight(150)
        self.label_image_main.setScaledContents(True)
        self.label_image_main.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_image_main)

        # Spacer để căn giữa ảnh "Better Luck Next Time"
        layout.addStretch(1)

        # Ảnh chúc may mắn lần sau (Better Luck Next Time)
        self.label_image_noluck = QtWidgets.QLabel(self)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "lucknext.png")
        pixmap = QtGui.QPixmap(image_path)
        self.label_image_noluck.setPixmap(pixmap)
        self.label_image_noluck.setScaledContents(True)
        self.label_image_noluck.setFixedSize(250, 150)  # Điều chỉnh kích thước ảnh
        self.label_image_noluck.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Layout ngang để căn giữa ảnh
        image_layout = QtWidgets.QHBoxLayout()
        image_layout.addStretch(1)
        image_layout.addWidget(self.label_image_noluck)
        image_layout.addStretch(1)
        layout.addLayout(image_layout)

        # Label chúc may mắn lần sau
        self.label_lucknext = QtWidgets.QLabel("Chúc bạn may mắn lần sau!", self)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_lucknext.setFont(font)
        self.label_lucknext.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_lucknext)

        # Spacer để đẩy hai button xuống góc dưới
        layout.addStretch(1)

        # Layout ngang chứa hai button
        button_layout = QtWidgets.QVBoxLayout()

        self.pushButton_gotocart = QtWidgets.QPushButton("Đi tới giỏ hàng", self)
        self.pushButton_gotocart.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size: 15px")
        self.pushButton_gotocart.setFixedSize(150, 40)
        self.pushButton_gotocart.clicked.connect(self.accept)

        self.pushButton_back = QtWidgets.QPushButton("Bỏ qua", self)
        self.pushButton_back.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size: 15px")
        self.pushButton_back.setFixedSize(150, 40)
        self.pushButton_back.clicked.connect(self.reject)

        button_layout.addWidget(self.pushButton_gotocart, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.pushButton_back, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(button_layout)

class UI_luck(QtWidgets.QDialog):
    """Cửa sổ hiển thị kết quả mở trúng voucher"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kết Quả")
        self.setFixedSize(398, 708)

        # Nền trắng
        self.setStyleSheet("background-color: white;")

        layout_doc = QtWidgets.QVBoxLayout(self)

        # Hình ảnh minigame phần may mắn
        self.label_image_luck = QtWidgets.QLabel(self)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "bannermngame.png")
        pixmap = QtGui.QPixmap(image_path)
        self.label_image_luck.setPixmap(pixmap)
        self.label_image_luck.setScaledContents(True)
        self.label_image_luck.setFixedHeight(150)
        layout_doc.addWidget(self.label_image_luck)

        # Chúc mừng bạn đã nhận được
        self.label_text1 = QtWidgets.QLabel("Chúc mừng bạn đã nhận được")
        self.label_text1.setStyleSheet("color: purple; font-weight: bold; font-size: 12px;")
        self.label_text1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Fix lỗi
        layout_doc.addWidget(self.label_text1)

        # Hình ảnh mã voucher
        self.label_image_voucher = QtWidgets.QLabel()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "voucher.png")
        pixmap = QtGui.QPixmap(image_path)
        self.label_image_voucher.setPixmap(pixmap)
        self.label_image_voucher.setScaledContents(True)
        self.label_image_voucher.setFixedHeight(150)
        layout_doc.addWidget(self.label_image_voucher)

        # Hình ảnh tên gọi voucher
        self.label_text2 = QtWidgets.QLabel("1 MÃ VOUCHER 50%")
        self.label_text2.setStyleSheet("font-weight: bold; font-size: 30px; color: red;")
        self.label_text2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_doc.addWidget(self.label_text2)

        # Layout chứa 2 nút
        layout_doc2 = QtWidgets.QVBoxLayout()

        # Button đi đến giỏ hàng
        self.button_gotocart = QtWidgets.QPushButton("Đi đến giỏ hàng")
        self.button_gotocart.setStyleSheet("background-color: red; color: white; font-size: 15px; font-weight: bold;")
        self.button_gotocart.setFixedSize(150, 40)
        self.button_gotocart.clicked.connect(self.accept)
        layout_doc2.addWidget(self.button_gotocart, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Button bỏ qua
        self.button_back = QtWidgets.QPushButton("Bỏ qua")
        self.button_back.setStyleSheet("background-color: red; color: white; font-size: 15px; font-weight: bold;")
        self.button_back.setFixedSize(150, 40)
        self.button_back.clicked.connect(self.reject)
        layout_doc2.addWidget(self.button_back, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        layout_doc.addLayout(layout_doc2)

class Ui_MainWindow(object):
        """Màn hình Minigame chính"""
        def setupUi(self, MainWindow):
            MainWindow.setWindowTitle("Hộp Quà May Mắn")
            MainWindow.setFixedSize(398, 708)

            self.centralwidget = QtWidgets.QWidget(MainWindow)
            MainWindow.setCentralWidget(self.centralwidget)

            # Đặt nền trắng cho toàn bộ giao diện
            MainWindow.setStyleSheet("background-color: white;")
            self.centralwidget.setStyleSheet("background-color: white;")

            main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

            # Ảnh tiêu đề
            self.label_image = QtWidgets.QLabel()
            base_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "img_bannerminigame.png")
            pixmap = QtGui.QPixmap(image_path)
            self.label_image.setPixmap(pixmap)
            self.label_image.setScaledContents(True)
            self.label_image.setFixedHeight(150)  # Size cho ảnh minigame
            main_layout.addWidget(self.label_image)

            # Tiêu đề chính
            # Layout chứa nút và tiêu đề
            button_layout1 = QtWidgets.QHBoxLayout()

            # Nút quay lại
            self.button_back = QtWidgets.QPushButton()
            base_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "img_backbutton.png")
            self.button_back.setIcon(QtGui.QIcon(icon_path))
            self.button_back.setIconSize(QtCore.QSize(30, 30))
            button_layout1.addWidget(self.button_back)

            # khoảng trống giữa nút và tiêu đề
            spacer = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Policy.Fixed,
                                               QtWidgets.QSizePolicy.Policy.Minimum)
            button_layout1.addItem(spacer)

            # Tiêu đề chính
            self.label_title = QtWidgets.QLabel("Hộp Quà May Mắn")
            self.label_title.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
            self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)  # Căn giữa theo chiều dọc
            self.label_title.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                               QtWidgets.QSizePolicy.Policy.Preferred)
            button_layout1.addWidget(self.label_title)

            main_layout.addLayout(button_layout1)

            # grid_ Layout chứa 8 hộp quà
            grid_layout = QtWidgets.QGridLayout()
            grid_layout.setSpacing(20)

            base_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "img_hopqua.png")

            self.boxes = []

            for i in range(8):
                button = QtWidgets.QPushButton()
                button.setFixedSize(100, 100)
                button.setIcon(QtGui.QIcon(icon_path))
                button.setIconSize(QtCore.QSize(80, 80))  # Hộp quà nhỏ hơn button

                # Kết nối nút với hàm xử lý khi nhấn
                button.clicked.connect(lambda _, idx_box=i: self.open_gift(idx_box))

                self.boxes.append(button)
                grid_layout.addWidget(button, i // 2, i % 2)

            main_layout.addLayout(grid_layout)

        # Hàm mở hộp quà ra
        def open_gift(self, index):
            if index in [1, 3, 5, 7]:  # Hộp quà 1, 2, 3, 4 (chỉ số từ 0)
                dialog = UI_noluck()
            else:
                dialog = UI_luck()

            dialog.exec()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())