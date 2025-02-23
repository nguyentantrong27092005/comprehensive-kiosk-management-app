import os

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow


class typeProductFrame(QtWidgets.QFrame):
    def __init__(self, image_path, name):
        super().__init__()
        self.setMaximumSize(100, 116)
        self.setStyleSheet("background-color: #f0f0f0")

        self.layout_product = QtWidgets.QVBoxLayout(self)
        self.layout_product.setContentsMargins(0, 0, 0, 0)
        self.layout_product.setSpacing(0)
        self.layout_product.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.img_menu = QtWidgets.QLabel(self)
        self.img_menu.setMaximumSize(90, 90)
        self.img_menu.setPixmap(QtGui.QPixmap(image_path))
        self.img_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_menu.setScaledContents(True)
        self.layout_product.addWidget(self.img_menu)

        self.label_menu = QtWidgets.QLabel(name)
        self.label_menu.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
        self.label_menu.setStyleSheet("color: #BD1906;")
        self.label_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_product.addWidget(self.label_menu)


class ProductFrame(QtWidgets.QFrame):
    def __init__(self, image_path, price, name, isbestseller):
        super().__init__()
        self.current_path = os.getcwd()
        self.setMinimumSize(130, 180)
        self.setStyleSheet("""
            ProductFrame {
                border-radius: 10px;
                border: 2px solid rgba(0, 0, 0, 0.2); /* Viền nhẹ */
            }
        """)
        self.layout_product = QtWidgets.QVBoxLayout(self)
        self.layout_product.setContentsMargins(5, 5, 5, 5)
        self.layout_product.setSpacing(0)
        self.layout_product.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.img_menu = QtWidgets.QLabel(self)
        self.img_menu.setMaximumSize(120, 120)
        self.img_menu.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.img_menu.setPixmap(QtGui.QPixmap(image_path))
        self.img_menu.setScaledContents(True)
        self.img_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_product.addWidget(self.img_menu)
        # self.img_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_price = QtWidgets.QLabel(price)
        self.label_price.setMinimumHeight(20)
        self.label_price.setFont(QtGui.QFont("Segoe UI", 10))
        self.label_price.setStyleSheet("color: #000000;")
        self.label_price.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout_product.addWidget(self.label_price)


        self.label_productname = label_name(name)
        if isbestseller == 1:
            self.add_bestseller()
        else:
            self.label_productname.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout_product.addWidget(self.label_productname)

    def add_bestseller(self):
        self.layout_productname = QtWidgets.QHBoxLayout()
        self.layout_product.addLayout(self.layout_productname)
        self.layout_productname.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_productname.setSpacing(10)

        self.img_bestseller = QtWidgets.QLabel(self)
        self.img_bestseller.setMaximumSize(30, 30)
        self.img_bestseller.setPixmap(QtGui.QPixmap(f"{self.current_path}/../resources/images/bestseller.png"))
        # self.img_bestseller.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.img_bestseller.setScaledContents(True)
        self.layout_productname.addWidget(self.img_bestseller)

        self.label_productname.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_productname.addWidget(self.label_productname)
class label_name(QtWidgets.QLabel):
    def __init__(self, name):
        super().__init__(name)
        self.setMaximumHeight(35)
        self.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
        self.setStyleSheet("color: #000000;")
        self.setWordWrap(True)


class Button(QtWidgets.QPushButton):
    def __init__(self, name, icon_path):
        super().__init__(name)

        self.setIcon(QtGui.QIcon(icon_path))
        self.setIconSize(QtCore.QSize(30, 30))
        self.setFlat(True)  # bỏ viền ở ngoài của nút
        self.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.setStyleSheet("""
                    QPushButton {
                        background-color: #bd1906;
                        color: #ffffff;
                        padding: 5px;
                        border-radius: 0px;
                    }
                    QPushButton:pressed {
                        background-color:#a61505;
                    }
                """)
class header(QtWidgets.QLabel):
    def __init__(self, name):
        super().__init__(name)
        self.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("background-color: #bd1906; color: #ffffff; border-radius: 5px;")
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(478, 850)

        # widget trung tâm
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.current_path = os.getcwd()
        # LAYOUT CHÍNH, gồm 3 phần
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)

        # BANNER
        self.label_banner = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_banner.setMinimumSize(478, 150)
        self.label_banner.setPixmap(QtGui.QPixmap(f"{self.current_path}/../resources/images/quang-cao-la-gi-peakads.png"))
        self.label_banner.setScaledContents(True)
        self.verticalLayout.addWidget(self.label_banner)

        # KHUNG CONTENT
        self.frame_chung = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_chung.setStyleSheet("background-color: #ffffff;")
        # self.frame_chung.setMinimumSize(QtCore.QSize(478, 650))
        self.verticalLayout.addWidget(self.frame_chung)


        # Layout cho khung content
        self.layout_content = QtWidgets.QHBoxLayout(self.frame_chung)

        # self.verticalLayout.addLayout(self.layout_content)

        # tạo frame menu
        self.frame_menu = QtWidgets.QFrame(self.centralwidget)
        self.frame_menu.setMaximumSize(125, 635)
        self.layout_content.addWidget(self.frame_menu)
        self.layout_menu = QtWidgets.QVBoxLayout(self.frame_menu)

        # tiêu đề trong frame menu
        menu_header = header("Menu")
        self.layout_menu.addWidget(menu_header)

        # nội dung trong frame menu
        self.frame_typeMenu = QtWidgets.QFrame(self.centralwidget)
        self.frame_typeMenu.setMaximumSize(116 ,585)
        # Tạo vùng cuộn trong frame menu
        self.scroll_menu = QtWidgets.QScrollArea(self.frame_typeMenu)
        self.scroll_menu.setWidgetResizable(True)
        self.layout_menu.addWidget(self.scroll_menu)


        # tạo widget chứa nội dung cuộn -> chèn thêm layout
        self.widget_scroll = QtWidgets.QWidget(self.scroll_menu)
        self.verticalLayout_menu = QtWidgets.QVBoxLayout(self.widget_scroll)
        self.verticalLayout_menu.setContentsMargins(0, 10, 0, 10)
        self.verticalLayout_menu.setSpacing(10)
        self.verticalLayout_menu.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        products = [
            (f"{self.current_path}/../resources/images/tra.png", "Trà"),
            (f"{self.current_path}/../resources/images/tra.png", "Lẩu"),
            (f"{self.current_path}/../resources/images/tra.png", "Trà"),
            (f"{self.current_path}/../resources/images/tra.png", "Lẩu"),
            (f"{self.current_path}/../resources/images/tra.png", "Trà"),
            (f"{self.current_path}/../resources/images/tra.png", "Lẩu"),
            (f"{self.current_path}/../resources/images/tra.png", "Trà"),
        ]

        for image, name in products:
            item = typeProductFrame(image, name)
            self.verticalLayout_menu.addWidget(item)
        # Đặt widget chứa nội dung cuộn
        self.scroll_menu.setWidget(self.widget_scroll)



        # GroupBox Trà
        self.groupBox_tea = QtWidgets.QGroupBox("Trà")
        self.groupBox_tea.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.groupBox_tea.setStyleSheet("color: #bd1906;")
        self.groupBox_tea.setMinimumSize(QtCore.QSize(317, 635))
        self.layout_content.addWidget(self.groupBox_tea)

        # Tạo vùng cuộn trong groupBox_tea
        self.scroll_tea = QtWidgets.QScrollArea(self.groupBox_tea)
        self.scroll_tea.setWidgetResizable(True)
        self.scroll_tea.setWidget(QtWidgets.QWidget())
        self.layout_tea = QtWidgets.QGridLayout(self.scroll_tea.widget())
        # self.layout_tea.setContentsMargins(0, 0, 0, 0)
        self.layout_tea.setSpacing(10)
        # self.layout_tea.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Thêm các sản phẩm vào groupBox_tea
        tea_products = [
            (f"{self.current_path}/../resources/images/traxoai.png", "50.000đ", "Trà đào cam sả chanh", 1),
            (f"{self.current_path}/../resources/images/traxoai.png", "45.000đ", "Trà xoài", 0),
            (f"{self.current_path}/../resources/images/traxoai.png", "55.000đ", "Trà vải bông tuyết hoa", 0),
            (f"{self.current_path}/../resources/images/traxoai.png", "60.000đ", "Trà kiwi", 1),
            (f"{self.current_path}/../resources/images/traxoai.png", "40.000đ", "Trà dâu", 0),
            (f"{self.current_path}/../resources/images/traxoai.png", "50.000đ", "Trà đào", 1),
            (f"{self.current_path}/../resources/images/traxoai.png", "45.000đ", "Trà xoài", 0),
            (f"{self.current_path}/../resources/images/traxoai.png", "55.000đ", "Trà vải", 0),
            (f"{self.current_path}/../resources/images/traxoai.png", "60.000đ", "Trà kiwi", 0),
            (f"{self.current_path}/../resources/images/traxoai.png", "40.000đ", "Trà dâu", 0),
        ]
        row, col = 0, 0

        for image, price, name, isbestseller in tea_products:
            product_frame = ProductFrame(image, price, name, isbestseller)
            self.layout_tea.addWidget(product_frame, row, col)
            col += 1
            if col == 2:
                col = 0
                row += 1

        self.groupBox_tea.setLayout(QtWidgets.QVBoxLayout())
        self.groupBox_tea.layout().addWidget(self.scroll_tea)

        # LAYOUT CHỨA 2 NÚT
        self.layout_2button = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.layout_2button)

        # nút trang chủ
        self.pushButton_home = Button("Trang chủ", f"{self.current_path}/../resources/images/home.png")
        self.layout_2button.addWidget(self.pushButton_home)

        # nút giỏ hàng
        self.pushButton_shoppingcart = Button("Giỏ hàng", f"{self.current_path}/../resources/images/shopping_cart.png")
        self.layout_2button.addWidget(self.pushButton_shoppingcart)
class MainWindow_Ext(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow

    def show(self):
        self.MainWindow.show()

app = QApplication([])
window = MainWindow_Ext()
window.setupUi(QMainWindow())
window.show()
app.exec()




