
import pymysql
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QLabel, QVBoxLayout, QFrame, QPushButton, \
    QScrollArea, QWidget, QGroupBox, QGridLayout, QStackedWidget

from kiosk_app.models.FoodItem import FoodItem


# Category Frame
class CategoryFrame(QFrame):
    def __init__(self, image_path, name, category_id, mainwindow):
        super().__init__()
        self.main_window = mainwindow
        self.category_id = category_id  # lấy category_id để load những sp có cùng category_id
        self.setMaximumSize(100, 116)
        self.setStyleSheet("background-color: #f0f0f0")

        self.layout_categoryFrame = QVBoxLayout(self)
        self.layout_categoryFrame.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.img_category = QLabel(self)
        self.img_category.setMaximumSize(90, 90)
        self.img_category.setPixmap(QtGui.QPixmap(image_path))
        self.img_category.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_category.setScaledContents(True)
        self.layout_categoryFrame.addWidget(self.img_category)

        self.name_category = QLabel(name)
        self.name_category.setFont(QtGui.QFont("Montserrat", 8, QtGui.QFont.Weight.Bold))
        self.name_category.setStyleSheet("color: #BD1906;")
        self.name_category.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_categoryFrame.addWidget(self.name_category)

    # xử lý sự kiện khi có click vào categoryFrame
    def mousePressEvent(self, event):
        print(f"Category ID clicked: {self.category_id}")
        self.main_window.load_items(self.name_category.text(), self.category_id)  # lấy tên của category và id
        super().mousePressEvent(event)


class ProductFrame(QFrame):
    productClicked = pyqtSignal(FoodItem)
    def __init__(self, id,image_path, price, discountedPrice, name, is_bestseller):
        super().__init__()
        self.food_item = FoodItem(id=id, name=name, price=price,
                                  discounted_price=discountedPrice, image_url=image_path, is_best_seller=is_bestseller,
                                  promotion_id=None)
        self.setFixedSize(130, 200)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 2px solid rgba(0, 0, 0, 0.2);
            }
            QLabel {
                border: none;
                background: transparent;
                color: #000000
            }
        """)

        # LAYOUT PRODUCTFRAME
        layout_ProductFrame = QVBoxLayout(self)
        layout_ProductFrame.setContentsMargins(5, 5, 5, 5)
        # layout_ProductFrame.setSpacing(0)

        # Hình ảnh sp
        self.img_product = QLabel()
        self.img_product.setFixedSize(110, 110)
        self.img_product.setPixmap(QtGui.QPixmap(image_path))
        self.img_product.setScaledContents(True)
        layout_ProductFrame.addWidget(self.img_product, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        # giá gốc
        layout_Price = QHBoxLayout()
        layout_ProductFrame.addLayout(layout_Price)
        if price != discountedPrice:
            self.price_product = QLabel(f"{price:,}đ")
            self.price_product.setFont(QtGui.QFont("Montserrat", 8))
            self.price_product.setWordWrap(True)
            self.price_product.setStyleSheet("text-decoration: line-through; color: #C0BBBB;")
            layout_Price.addWidget(self.price_product, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.discountedPrice_product = QLabel(f"{discountedPrice:,}đ")
        self.discountedPrice_product.setFont(QtGui.QFont("Montserrat", 10))
        self.discountedPrice_product.setWordWrap(True)
        self.discountedPrice_product.setStyleSheet("color: #000000")
        layout_Price.addWidget(self.discountedPrice_product, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.name_product = QLabel(name)
        self.name_product.setFont(QtGui.QFont("Montserrat", 10, QtGui.QFont.Weight.Bold))
        self.name_product.setWordWrap(True)
        self.name_product.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if is_bestseller:
            # layout icon + tên sp
            self.layout_ProductName = QHBoxLayout()
            # self.layout_ProductName.setContentsMargins(0, 0, 0, 0)
            self.layout_ProductName.setSpacing(5)
            layout_ProductFrame.addLayout(self.layout_ProductName)

            # hình ảnh icon
            self.img_bestseller = QLabel()
            self.img_bestseller.setFixedSize(30, 30)
            self.img_bestseller.setPixmap(QtGui.QPixmap("kiosk_app/resources/images/bestseller.png"))
            self.img_bestseller.setScaledContents(True)

            # thêm icon và tên vào layout
            self.layout_ProductName.addWidget(self.img_bestseller)
            self.layout_ProductName.addWidget(self.name_product)

        else:
            layout_ProductFrame.addWidget(self.name_product, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        self.productClicked.emit(self.food_item)
class Button(QPushButton):
    def __init__(self, name, icon_path):
        super().__init__()
        self.setText(name)
        self.setIcon(QtGui.QIcon(icon_path))
        self.setIconSize(QtCore.QSize(30, 30))
        self.setFlat(True)  # bỏ viền ở ngoài của nút
        self.setFont(QtGui.QFont("Montserrat", 14, QtGui.QFont.Weight.Bold))
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
class groupbox(QGroupBox):
    def __init__(self, category_name):
        super().__init__()
        self.setTitle(category_name)
        self.setFont(QtGui.QFont("Montserrat", 14, QtGui.QFont.Weight.Bold))
        self.setStyleSheet("color: #bd1906;")
        self.setMaximumHeight(635)
        self.setMinimumWidth(317)
        # layout
        self.layout_groupbox = QVBoxLayout(self)
        # vùng cuộn
        self.scroll_product = QScrollArea()
        self.scroll_product.setWidgetResizable(True)
        self.layout_groupbox.addWidget(self.scroll_product)
        # widget trong vùng cuộn
        self.scroll_widget = QWidget()
        self.scroll_product.setWidget(self.scroll_widget)
        # gridlayout trong widget
        self.gridlayout = QGridLayout(self.scroll_widget)
        self.gridlayout.setSpacing(10)
        self.gridlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

    def add_product(self, product, row, col):
        self.gridlayout.addWidget(product, row, col)

    def delete_product(self):
        while self.gridlayout.count() != 0:
            item = self.gridlayout.takeAt(0).widget()  # lấy widget ở vị trí đầu tiên của gridlayout
            item.setParent(None)


# Main UI
class MenuWidget(QWidget):
    def __init__(self):
        super().__init__()
        # MAIN_LAYOUT
        self.verticalLayout = QVBoxLayout(self)


        # KHUNG CONTENT (frame menu + groupbox)
        self.frame_content = QFrame(self)
        self.frame_content.setStyleSheet("background-color: #ffffff;")
        self.verticalLayout.addWidget(self.frame_content)
        # layout
        self.layout_content = QHBoxLayout(self.frame_content)

        # FRAME MENU (tiêu đề + nội dung)
        self.frame_menu = QFrame(self)
        self.frame_menu.setMinimumSize(125, 635)
        self.layout_content.addWidget(self.frame_menu)
        # layout
        self.layout_menu = QVBoxLayout(self.frame_menu)

        # tiêu đề Menu
        self.menu_header = QLabel("Menu")
        self.menu_header.setFont(QtGui.QFont("Montserrat", 14, QtGui.QFont.Weight.Bold))
        self.menu_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_header.setStyleSheet("background-color: #bd1906; color: #ffffff; border-radius: 5px;")
        self.layout_menu.addWidget(self.menu_header)

        # nội dung Menu
        self.frame_typeMenu = QFrame(self)
        self.frame_typeMenu.setMaximumSize(116, 585)
        # vùng cuộn
        self.scroll_menu = QScrollArea(self.frame_typeMenu)
        self.scroll_menu.setWidgetResizable(True)
        self.layout_menu.addWidget(self.scroll_menu)

        # tạo widget chứa nội dung cuộn -> chèn thêm layout
        self.widget_scroll = QWidget()
        self.scroll_menu.setWidget(self.widget_scroll)  # nhớ chú ý
        # layout chứa category
        self.layout_category = QVBoxLayout(self.widget_scroll)
        self.layout_category.setContentsMargins(0, 10, 0, 10)
        self.layout_category.setSpacing(10)
        self.layout_category.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # GROUPBOX
        self.groupbox_item = groupbox("Tất cả món")
        self.layout_content.addWidget(self.groupbox_item)

        # LAYOUT CHỨA 2 NÚT
        self.layout_2button = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.layout_2button)

        # nút trang chủ
        self.pushButton_home = Button("Trang chủ", "kiosk_app/resources/images/ic_home.png")
        self.layout_2button.addWidget(self.pushButton_home)
        # nút giỏ hàng
        self.pushButton_shoppingcart = Button("Giỏ hàng", "kiosk_app/resources/images/ic_shoppingcart.png")
        self.layout_2button.addWidget(self.pushButton_shoppingcart)

