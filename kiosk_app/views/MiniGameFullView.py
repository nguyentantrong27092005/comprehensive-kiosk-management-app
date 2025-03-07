import os
from PyQt6 import QtCore, QtGui, QtWidgets

class MiniGameFull(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hộp Quà May Mắn")
        self.setFixedSize(398, 708)
        self.setStyleSheet("background-color: white;")
        self.setup_ui()

    def setup_ui(self):

        # Set chiều dọc cho cả layout
        main_layout = QtWidgets.QVBoxLayout(self)

        # Ảnh tiêu đề
        self.label_image = QtWidgets.QLabel()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "img_bannerminigame.png")
        pixmap = QtGui.QPixmap(image_path)
        self.label_image.setPixmap(pixmap)
        self.label_image.setScaledContents(True)
        self.label_image.setFixedHeight(150)  # Kích thước ảnh minigame
        main_layout.addWidget(self.label_image)

        # Layout chứa nút quay lại và tiêu đề
        button_layout1 = QtWidgets.QHBoxLayout()

        # Nút quay lại
        self.button_back = QtWidgets.QPushButton()
        icon_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "img_backbutton.png")
        self.button_back.setIcon(QtGui.QIcon(icon_path))
        self.button_back.setIconSize(QtCore.QSize(30, 30))
        button_layout1.addWidget(self.button_back)

        # khoảng trống giữa nút và tiêu đề
        spacer = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        button_layout1.addItem(spacer)

        # Tiêu đề chính
        self.label_title = QtWidgets.QLabel("Hộp Quà May Mắn")
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_title.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        button_layout1.addWidget(self.label_title)

        main_layout.addLayout(button_layout1)

        # Grid layout chứa 8 hộp quà
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(20)
        gift_icon_path = os.path.join(base_dir, "..", "kiosk_app", "resources", "images", "img_hopqua.png")

        self.gift_buttons = []  # Danh sách các nút hộp quà

        for i in range(8):
            button = QtWidgets.QPushButton()
            button.setFixedSize(100, 100)
            button.setIcon(QtGui.QIcon(gift_icon_path))
            button.setIconSize(QtCore.QSize(80, 80))
            self.gift_buttons.append(button)  # Lưu vào danh sách
            grid_layout.addWidget(button, i // 2, i % 2)

        main_layout.addLayout(grid_layout)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = MiniGameFull()
    widget.show()
    sys.exit(app.exec())
