import os
from PyQt6 import QtCore, QtGui, QtWidgets

class MiniGameNoBonus(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Kết Quả")
        self.setFixedSize(398, 708)
        self.setStyleSheet("background-color: white;")

        # Layout chính
        layout = QtWidgets.QVBoxLayout(self)

        # Hình ảnh minigame phần may mắn lần sau
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
        image_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "lucknext.png")
        pixmap = QtGui.QPixmap(image_path)
        self.label_image_noluck.setPixmap(pixmap)
        self.label_image_noluck.setScaledContents(True)
        self.label_image_noluck.setFixedSize(250, 150)
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
        layout_two_btns = QtWidgets.QVBoxLayout()

        self.pushButton_gotocart = QtWidgets.QPushButton("Đi tới giỏ hàng", self)
        self.pushButton_gotocart.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size: 15px")
        self.pushButton_gotocart.setFixedSize(150, 40)

        self.pushButton_back = QtWidgets.QPushButton("Bỏ qua", self)
        self.pushButton_back.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size: 15px")
        self.pushButton_back.setFixedSize(150, 40)

        layout_two_btns.addWidget(self.pushButton_gotocart, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_two_btns .addWidget(self.pushButton_back, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(layout_two_btns)


# Khởi chạy ứng dụng
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MiniGameNoBonus()
    window.show()
    sys.exit(app.exec())
