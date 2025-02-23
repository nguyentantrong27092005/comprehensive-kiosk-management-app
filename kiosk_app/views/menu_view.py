
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt



class typeProductFrame(QtWidgets.QFrame):
    def __init__(self, image_path, name):
        super().__init__()
        self.setMaximumSize(100, 116)

        self.layout_product = QtWidgets.QVBoxLayout(self)
        self.layout_product.setContentsMargins(0, 0, 0, 0)
        self.layout_product.setSpacing(0)

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
    def __init__(self, image_path, price, name):
        super().__init__()
        self.setMaximumSize(130, 180)
        self.setStyleSheet("""
            ProductFrame {
                border-radius: 10px;
                border: 2px solid rgba(0, 0, 0, 50); /* Viền nhẹ */

            }
        """)
        self.layout_product = QtWidgets.QVBoxLayout(self)
        self.layout_product.setContentsMargins(5, 5, 5, 5)
        self.layout_product.setSpacing(0)

        self.img_menu = QtWidgets.QLabel(self)
        self.img_menu.setMaximumSize(120, 120)
        self.img_menu.setPixmap(QtGui.QPixmap(image_path))
        self.img_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_menu.setScaledContents(True)
        self.layout_product.addWidget(self.img_menu)

        self.label_price = QtWidgets.QLabel(price)
        self.label_price.setMaximumSize(120, 25)
        self.label_price.setFont(QtGui.QFont("Segoe UI", 10))
        self.label_price.setStyleSheet("color: #000000;")
        self.label_price.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_product.addWidget(self.label_price)

        self.label_menu = QtWidgets.QLabel(name)
        self.label_menu.setMaximumSize(120, 25)
        self.label_menu.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
        self.label_menu.setStyleSheet("color: #000000;")

        self.label_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_product.addWidget(self.label_menu)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(478, 850)

        # widget trung tâm
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # layout chính (dọc), gồm 3 phần
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0) # các khoảng cách xung quanh
        self.verticalLayout.setSpacing(0) # khoảng cách giữa 2 cái

        # label hình ảnh
        self.label_image = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_image.setMaximumSize(478, 150)
        self.label_image.setPixmap(QtGui.QPixmap("ha/quang-cao-la-gi-peakads.png"))
        self.label_image.setScaledContents(True)
        self.verticalLayout.addWidget(self.label_image)

        # tạo khung chứa nội dung
        self.frame_chung = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_chung.setStyleSheet("background-color: #ffffff;")
        self.frame_chung.setMaximumSize(QtCore.QSize(478, 650))
        self.verticalLayout.addWidget(self.frame_chung)

        # tạo layout dọc cho 2 frame
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_chung)

        # tạo frame menu
        self.frame_menu = QtWidgets.QFrame(self.centralwidget)
        self.frame_menu.setMaximumSize(125, 635)
        self.layout_menu = QtWidgets.QVBoxLayout(self.frame_menu)

        # tiêu đề trong frame menu
        self.label_headerMenu =   QtWidgets.QLabel("Menu")
        self.label_headerMenu.setMaximumSize(116, 50)
        self.label_headerMenu.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.label_headerMenu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_headerMenu.setStyleSheet("background-color: #bd1906; color: #ffffff; border-radius: 5px;")
        self.layout_menu.addWidget(self.label_headerMenu)

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
        self.verticalLayout_menu.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        products = [
            ("ha/trà.png", "Trà"),
            ("ha/lẩu1.png", "Lẩu"),
            ("ha/trà.png", "Trà"),
            ("ha/lẩu1.png", "Lẩu"),
            ("ha/trà.png", "Trà"),
            ("ha/lẩu1.png", "Lẩu"),
            ("ha/trà.png", "Trà"),
        ]

        for image, name in products:
            item = typeProductFrame(image, name)
            self.verticalLayout_menu.addWidget(item)
        # Đặt widget chứa nội dung cuộn
        self.scroll_menu.setWidget(self.widget_scroll)
        self.horizontalLayout.addWidget(self.frame_menu)


        # GroupBox Trà
        self.groupBox_tea = QtWidgets.QGroupBox("Trà")
        self.groupBox_tea.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.groupBox_tea.setStyleSheet("color: #bd1906;")
        self.groupBox_tea.setMaximumSize(QtCore.QSize(317, 635))
        self.horizontalLayout.addWidget(self.groupBox_tea)

        # Tạo vùng cuộn trong groupBox_tea
        self.scroll_tea = QtWidgets.QScrollArea(self.groupBox_tea)
        self.scroll_tea.setWidgetResizable(True)
        self.scroll_tea.setWidget(QtWidgets.QWidget())
        self.layout_tea = QtWidgets.QGridLayout(self.scroll_tea.widget())
        self.layout_tea.setContentsMargins(0, 0, 0, 0)
        self.layout_tea.setSpacing(10)
        self.layout_tea.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Thêm các sản phẩm vào groupBox_tea
        tea_products = [
            ("ha/trà đào.png", "50.000đ", "Trà đào"),
            ("ha/trà xoài.png", "45.000đ", "Trà xoài"),
            ("ha/trà vải.png", "55.000đ", "Trà vải"),
            ("ha/trà kiwi.png", "60.000đ", "Trà kiwi"),
            ("ha/trà dâu.png", "40.000đ", "Trà dâu"),
            ("ha/trà đào.png", "50.000đ", "Trà đào"),
            ("ha/trà xoài.png", "45.000đ", "Trà xoài"),
            ("ha/trà vải.png", "55.000đ", "Trà vải"),
            ("ha/trà kiwi.png", "60.000đ", "Trà kiwi"),
            ("ha/trà dâu.png", "40.000đ", "Trà dâu"),
        ]

        row, col = 0, 0
        for image, price, name in tea_products:
            item = ProductFrame(image, price, name)
            self.layout_tea.addWidget(item, row, col)
            col += 1
            if col == 2:  # 2 cột mỗi hàng
                col = 0
                row += 1

        self.groupBox_tea.setLayout(QtWidgets.QVBoxLayout())
        self.groupBox_tea.layout().addWidget(self.scroll_tea)

        # thanh ngang
        self.frame_ngang = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_ngang.setObjectName("frame_ngang")
        self.frame_ngang.setMaximumSize(QtCore.QSize(478, 50))
        self.frame_ngang.setStyleSheet("background-color: #bd1906")
        self.verticalLayout.addWidget(self.frame_ngang)
        # tạo layout ngang để chứa 2 nút
        self.horizontalLayout1 = QtWidgets.QHBoxLayout(self.frame_ngang)
        self.horizontalLayout1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout1.setSpacing(0)

        # nút trang chủ
        self.pushButton_home = QtWidgets.QPushButton("Trang chủ", self.frame_ngang)
        self.pushButton_home.setObjectName("pushButton_home")
        self.pushButton_home.setIcon(QtGui.QIcon("icon/home.png"))
        self.pushButton_home.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_home.setFlat(True) # bỏ viền ở ngoài của nút
        self.pushButton_home.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.pushButton_home.setStyleSheet("""
            QPushButton#pushButton_home {
                color: #ffffff;
                padding: 5px;
                border-radius: 0px;
            }
            QPushButton#pushButton_home:pressed {
                background-color:#a61505;
            }
        """)
        self.horizontalLayout1.addWidget(self.pushButton_home)

        # nút giỏ hàng
        self.pushButton_shoppingcart = QtWidgets.QPushButton("Giỏ hàng", self.frame_ngang)
        self.pushButton_shoppingcart.setIcon(QtGui.QIcon("icon/shopping_cart.png"))
        self.pushButton_shoppingcart.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_shoppingcart.setFlat(True) # bỏ viền ở ngoài của nút
        self.pushButton_shoppingcart.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        self.pushButton_shoppingcart.setStyleSheet("""
                QPushButton {
                    color: #ffffff;
                    padding: 5px;
                    border-radius: 0px;
                }
                QPushButton:pressed {
                    background-color:#a61505;
                }
        """)
        self.horizontalLayout1.addWidget(self.pushButton_shoppingcart)
