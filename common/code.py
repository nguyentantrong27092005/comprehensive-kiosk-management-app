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
        self.label_image_main.setPixmap(QtGui.QPixmap("D:/ktlt_đồ án/minigame-choi-vui-trung-lon-01590979733.jpg"))
        self.label_image_main.setFixedHeight(150)
        self.label_image_main.setScaledContents(True)
        self.label_image_main.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_image_main)

        # Spacer để căn giữa ảnh "Better Luck Next Time"
        layout.addStretch(1)

        # Ảnh chúc may mắn lần sau (Better Luck Next Time)
        self.label_image_noluck = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(
            r"D:\hoccode\QT Designer\TEST\doanktlt\anh\pngtree-better-luck-next-time-setback-fail-png-image_10561842.png")
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
        self.pushButton_gotocart.setStyleSheet("background-color: red; color: white; font-weight: bold")
        self.pushButton_gotocart.setFixedSize(150, 40)
        self.pushButton_gotocart.clicked.connect(self.accept)

        self.pushButton_back = QtWidgets.QPushButton("Bỏ qua", self)
        self.pushButton_back.setStyleSheet("background-color: red; color: white; font-weight: bold")
        self.pushButton_back.setFixedSize(150, 40)
        self.pushButton_back.clicked.connect(self.reject)

        button_layout.addWidget(self.pushButton_gotocart, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.pushButton_back, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(button_layout)


class UI_luck(QtWidgets.QDialog):
    """Cửa sổ hiển thị kết quả mở hộp quà"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kết Quả")
        self.setFixedSize(398, 708)

        # Nền trắng
        self.setStyleSheet("background-color: white;")

        layout_doc = QtWidgets.QVBoxLayout(self)

        # Hình ảnh minigame phần may mắn
        self.label_image_luck = QtWidgets.QLabel(self)
        self.label_image_luck.setPixmap(QtGui.QPixmap("D:\ktlt_đồ án\minigame-choi-vui-trung-lon-01590979733.jpg"))
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
        self.label_image_voucher.setPixmap(QtGui.QPixmap("D:\ktlt_đồ án\images.png"))
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
        self.label_image.setPixmap(
            QtGui.QPixmap("D:/hoccode/QT Designer/TEST/doanktlt/anh/subiz-minigame-la-gi-e1704609883891.jpg"))
        self.label_image.setScaledContents(True)
        self.label_image.setFixedHeight(150) #Size cho ảnh minigame
        main_layout.addWidget(self.label_image)

        # Tiêu đề chính
        # Layout chứa nút và tiêu đề
        button_layout1 = QtWidgets.QHBoxLayout()

        # Nút quay lại
        self.button_back = QtWidgets.QPushButton()
        pixmap = QtGui.QPixmap(
            r"D:\hoccode\QT Designer\TEST\doanktlt\anh\png-clipart-button-question-mark-computer-icons-check-mark-back-button-text-black-thumbnail.png")
        icon = QtGui.QIcon(pixmap)
        self.button_back.setIcon(icon)
        self.button_back.setIconSize(QtCore.QSize(30, 30))
        button_layout1.addWidget(self.button_back)

        # khoảng trống giữa nút và tiêu đề
        spacer = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        button_layout1.addItem(spacer)

        # Tiêu đề chính
        self.label_title = QtWidgets.QLabel("Hộp Quà May Mắn")
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)  # Căn giữa theo chiều dọc
        self.label_title.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        button_layout1.addWidget(self.label_title)

        main_layout.addLayout(button_layout1)

        # grid_ Layout chứa 6 hộp quà
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(20)

        image_path = "D:/hoccode/QT Designer/TEST/doanktlt/anh/hop-qua-vivo-tai-nghe-op-lung-mieng-dan-600x600.jpg"
        self.boxes = []

        for i in range(8):
            button = QtWidgets.QPushButton()
            button.setFixedSize(100, 100)
            button.setStyleSheet(f"border-image: url({image_path}); border-radius: 10px;")

            # Hộp quà số 0, 2, 4 gọi open_gift()
            if i%2 ==0:
                button.clicked.connect(lambda _, x=i: self.open_gift(x))
            # Hộp quà số 1, 3, 5 gọi open_gift_1()
            else:
                button.clicked.connect(lambda _, x=i: self.open_gift_1(x))

            self.boxes.append(button)
            grid_layout.addWidget(button, i // 2, i % 2)  # 2 hàng, 3 cột

        main_layout.addLayout(grid_layout)

    def open_gift(self, box_number):
        dialog = UI_luck(self.centralwidget)
        dialog.exec()

    def open_gift_1(self, box_number):
        dialog = UI_noluck(self.centralwidget)
        dialog.exec()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())