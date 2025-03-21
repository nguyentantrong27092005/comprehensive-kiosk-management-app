import os
from PyQt6 import QtCore, QtGui, QtWidgets

class MiniGameFull(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hộp Quà May Mắn")
        self.resize(478, 592)
        self.setStyleSheet("background-color: white;")
        self.setup_ui()

    def setup_ui(self):

        # Set chiều dọc cho cả layout
        main_layout = QtWidgets.QVBoxLayout(self)
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Grid layout chứa 8 hộp quà
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(20)
        gift_icon_path = "kiosk_app/resources/images/img_hopqua.png"

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
