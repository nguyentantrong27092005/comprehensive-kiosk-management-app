from typing import List

import pymysql
from PyQt6 import QtWidgets, QtGui, QtCore
import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QGroupBox, QRadioButton, QSlider, QLabel, \
    QGridLayout

from common.sql_func import Database
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.models.ToppingVariant import Variant, Topping
from kiosk_app.views.ClickableElement import ClickableLabel


class ToppingSelection(QtWidgets.QWidget):

    def __init__(self, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.setWindowTitle("Chi tiết")
        self.topping_widgets = []
        # self.resize(478,850)  # Set size
        self.setMaximumHeight(850)
        self.temp_total = sharedData.selected_item.discounted_price #Đơn giá
        self.final_total = self.temp_total #Giá sau khi nhân với số lượng
        self.setupUI(sharedData, db)

    def setupUI(self, sharedData: SharedDataModel, db: Database):
        # set layout dọc
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)
        self.sharedData = sharedData
        self.db = db

        # tạo header chứa tiêu đề Chi tiết + button quay lại
        self.title_container = QtWidgets.QWidget()
        self.title_container.setStyleSheet("background-color: #BD1906;")
        self.title_container.setFixedHeight(40)

        self.title_layout = QtWidgets.QHBoxLayout(self.title_container)
        self.title_layout.setContentsMargins(5, 5, 5, 5)

        # button quay lai
        self.back_button = QtWidgets.QPushButton()
        self.back_button.setIcon(QtGui.QIcon('kiosk_app/resources/images/ic_backwhite.png'))
        self.back_button.setIconSize(QtCore.QSize(24, 24))
        self.back_button.setFlat(True)

        # Tiêu đề "Chi tiết"
        self.title_label = QtWidgets.QLabel("Chi tiết")
        self.title_label.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")

        # Dùng stretch để căn giữa
        self.title_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()

        # Thêm header vào giao diện chính
        self.main_layout.addWidget(self.title_container)

        self.contentScrollView = QtWidgets.QScrollArea(self)
        self.contentScrollView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.contentScrollView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.contentScrollView.setWidgetResizable(True)
        self.main_layout.addWidget(self.contentScrollView)

        self.contentWidget = QtWidgets.QWidget()
        self.contentVLayout = QtWidgets.QVBoxLayout()
        self.contentVLayout.setSpacing(10)
        self.contentWidget.setLayout(self.contentVLayout)
        self.contentScrollView.setWidget(self.contentWidget)

        # food_item_id = int(input("Nhập food_item_id muốn xem chi tiết: "))  # thay = ID của món ăn cần lấy
        self.add_to_cart = QPushButton()
        self.add_to_cart.setText(f"Thêm vào giỏ hàng - {self.final_total:,}")
        toppings = self.db.fetch_all_toppings(self.sharedData.selected_item.id)  # trả về danh sách dicts topping
        # Hiển thị số
        self.number = QtWidgets.QLabel("1")
        self.number.setStyleSheet("color: #bd1906; font-size: 23px; font-weight: bold;")
        self.number.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # self.number.setFixedSize(30, 30)

        # Vì dữ liệu topping trả về là dict --> xây dựng hàm chuyển về tuple để cho dễ trích xuất dữ liệu
        # Hàm chuyển đổi thành dữ liệu tuple
        def convert_to_tuples(toppings):
            return [(p["ID"], p["Name"], p["Price"], p["DiscountedPrice"], p["ImageURL"]) for p in toppings]

        product_tuples = convert_to_tuples(toppings)

        # Lấy danh sách nhóm biến thể

        variant_groups = self.db.fetch_variantgroup(self.sharedData.selected_item.id)
        self.visible_variant_groups = []
        self.visible_sliders = []
        if variant_groups:
            for i in variant_groups:
                # RadioList
                if i['ViewType'] == "RadioList":
                    # Lấy danh sách các variant từ DB
                    variants = self.db.fetch_each_variant(i["ID"])
                    variants = [Variant(variant["ID"], variant["Value"], variant["Price"], variant["AdditionalCost"]) for variant in variants]
                    if variants:
                        group_box_radio_list = RadioButtonGroup(self, i["Name"])
                        group_box_radio_list.add_buttons(variants)
                        self.contentVLayout.addWidget(group_box_radio_list)
                        self.visible_variant_groups.append(group_box_radio_list)

                # Buttons
                if i['ViewType'] == "ChonSize":
                    variants = self.db.fetch_each_variant(i["ID"])  # Lấy danh sách size từ DB
                    if variants:
                        variants = [
                            Variant(variant["ID"], variant["Value"], variant["Price"], variant["AdditionalCost"]) for
                            variant in variants]
                        group_box_size = QtWidgets.QGroupBox(i["Name"])
                        horizontal_layout_size = QtWidgets.QHBoxLayout()
                        sizeButtonsGroup = SizeButtonGroup(self)
                        sizeButtonsGroup.add_buttons(variants)
                        horizontal_layout_size.addWidget(sizeButtonsGroup)
                        group_box_size.setLayout(horizontal_layout_size)
                        self.contentVLayout.addWidget(group_box_size)
                        self.visible_variant_groups.append(sizeButtonsGroup)

                #Slider
                if i['ViewType'] == "Slider":
                    slider = CustomSlider(100, i["Name"])
                    self.contentVLayout.addWidget(slider)
                    self.visible_sliders.append(slider)

        # GridView (hiển thị topping)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setFixedHeight(350)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.grid_layout = ToppingGridLayout(self, self.scroll_widget)

        self.toppings = product_tuples # Lấy danh sách tupple từ hàm connver_to_tuples ở trên
        self.grid_layout.addToppingItems(self.toppings)

        self.scroll_widget.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.contentVLayout.addWidget(self.scroll_area)
        if not self.toppings:
            self.scroll_area.setHidden(True)

        # Thêm ô ghi chú
        self.note_label = QtWidgets.QLabel("Ghi chú:")
        self.note_label.setFixedHeight(25)
        self.contentVLayout.addWidget(self.note_label)

        # Thêm ô nhập ghi chú
        self.note_text = QtWidgets.QTextEdit()
        self.note_text.setPlaceholderText("Nhập ghi chú tại đây...")
        self.note_text.setFixedHeight(50)  # Giới hạn chiều cao
        self.contentVLayout.addWidget(self.note_text)

        # Hiển thị thanh số lượng
        self.group_box_quantity = QtWidgets.QGroupBox("Số lượng")
        self.group_box_quantity.setFixedHeight(100)
        self.frame_vertical = QtWidgets.QHBoxLayout()

        # Căn giữa toàn bộ layout
        self.frame_vertical.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Nút trừ
        self.minus = ClickableLabel()
        self.minus.setPixmap(QPixmap("kiosk_app/resources/images/ic_minus").scaled(32,32, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.minus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


        # Nút cộng
        self.plus = ClickableLabel()
        self.plus.setPixmap(
            QPixmap("kiosk_app/resources/images/ic_plus").scaled(32, 32, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.plus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Thêm widget vào layout với khoảng cách nhỏ
        self.frame_vertical.addWidget(self.minus)
        self.frame_vertical.addSpacing(20)  # Khoảng cách giữa nút trừ và số
        self.frame_vertical.addWidget(self.number)
        self.frame_vertical.addSpacing(20)  # Khoảng cách giữa số và nút cộng
        self.frame_vertical.addWidget(self.plus)

        # Gán layout vào group box
        self.group_box_quantity.setLayout(self.frame_vertical)

        # Thêm group box vào main layout
        self.contentVLayout.addWidget(self.group_box_quantity)

        # Nút thêm vào giỏ hàng
        self.add_to_cart.setMinimumHeight(40)
        self.add_to_cart.setIcon(QtGui.QIcon("kiosk_app/resources/images/shopping_cart.png"))
        self.add_to_cart.setIconSize(QtCore.QSize(24, 24))
        self.add_to_cart.setStyleSheet("background-color: #BD1906; color: white; font-weight: bold; border-radius: 15px; font-size: 15px;")
        self.main_layout.addWidget(self.add_to_cart)

    def calculata_total_price(self, price_change=0):
        self.temp_total += price_change
        self.final_total = self.temp_total * int(self.number.text())
        self.add_to_cart.setText(f"Thêm vào giỏ hàng - {self.final_total:,}")

class RadioButtonGroup(QGroupBox):
    def __init__(self, topping_selection_widget: ToppingSelection, title, parent=None):
        super().__init__(title, parent)
        self.layout = QVBoxLayout()
        self.buttons = []
        self.active_button = None
        self.setLayout(self.layout)
        self.topping_selection_widget = topping_selection_widget

    def add_buttons(self, variant_list: List[Variant]):
        for variant in variant_list:
            self.button = CustomRadioButton(variant)
            self.button.clicked.connect(self.on_button_clicked)
            self.layout.addWidget(self.button)
            self.buttons.append(self.button)

        # Set the first button as active by default
        self.active_button = self.buttons[0]
        self.active_button.setChecked(True)
        self.topping_selection_widget.calculata_total_price(self.active_button.variant_value.price)

    def on_button_clicked(self):
        clicked_button = self.sender()
        print(f"New price:{clicked_button.variant_value.price} and old price: {self.active_button.variant_value.price}")
        self.topping_selection_widget.calculata_total_price(clicked_button.variant_value.price - self.active_button.variant_value.price)
        self.active_button = clicked_button
        print(self.active_button.variant_value.value)

class CustomRadioButton(QRadioButton):
    # clicked = pyqtSignal()
    def __init__(self, variant_value: Variant, parent=None):
        super().__init__(parent)
        self.variant_value = variant_value
        self.setCheckable(True)
        self.setText(self.variant_value.value)

    # def mousePressEvent(self, event):
    #     self.clicked.emit()  # Emit signal when clicked

class SizeButtonGroup(QWidget):
    def __init__(self, topping_selection_widget: ToppingSelection):
        super().__init__()
        self.layout = QHBoxLayout()
        self.buttons = []
        self.active_button = None
        self.topping_selection_widget = topping_selection_widget

    def add_buttons(self, size_list: List[Variant]):
        for size in size_list:
            button = SizeButton(size)
            button.setCheckable(True)
            button.clicked.connect(self.on_button_clicked)
            self.layout.addWidget(button)
            self.buttons.append(button)

        # Set the first button as active by default
        self.active_button = self.buttons[0]
        self.active_button.setChecked(True)
        self.topping_selection_widget.calculata_total_price(self.active_button.variant_value.price)

        self.setLayout(self.layout)

    def on_button_clicked(self):
        clicked_button = self.sender()
        # Reset previous active button
        print(f"New price:{clicked_button.variant_value.price} and old price: {self.active_button.variant_value.price}")
        self.topping_selection_widget.calculata_total_price(clicked_button.variant_value.price - self.active_button.variant_value.price)
        if self.active_button:
            # self.active_button.setStyleSheet("")
            self.active_button.setChecked(False)

        # Update the clicked button's style and set it as active
        # clicked_button.setStyleSheet("background-color: lightblue;")
        clicked_button.setChecked(True)
        self.active_button = clicked_button
        print(self.active_button.variant_value.value)


class SizeButton(QPushButton):
    def __init__(self, variant_value: Variant):
        super().__init__()
        self.variant_value = variant_value
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
                                        QPushButton {
                                            border-radius: 20px;  
                                            background-color: #ffffff;
                                            padding: 3px;
                                            border: 1px solid #8a8a8a;
                                            font-size: 12px;
                                        }
                                        QPushButton:hover {
                                            background-color: #d9d9d9;
                                        }
                                        QPushButton:checked { 
                                            background-color: #C00000;
                                            border: 1px solid #B71C1C;
                                            color: white;
                                            font-weight: bold;
                                        }
                                    """)
        self.setText(self.variant_value.value)

class CustomSlider(QGroupBox):
    def __init__(self, default_value, variant_name):
        super().__init__()
        self.default_value = default_value
        self.variant_name = variant_name
        self.current_value = default_value
        self.setupUI()

    def setupUI(self):
        self.setStyleSheet("""
                QGroupBox { 
     border: 1px solid gray; 
     border-radius: 10px; 
 } 
 
 QGroupBox::title { 
    background-color: transparent;
     subcontrol-position: top left; /* position at the top left*/ 
     padding:2 13px;
 } 
        """)
        self.setFixedHeight(100)
        self.setTitle(self.variant_name)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10,30,10,10)
        self.setLayout(main_layout)
        self.setContentsMargins(0,0,0,0)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setValue(self.default_value)
        self.slider.setMaximum(100)
        self.slider_label = QLabel(f"{self.default_value}%")
        self.slider.valueChanged[int].connect(self.change_value)
        self.slider.setStyleSheet("""
                    QSlider::handle:horizontal {
                        background-color: #BD1906;
                        border: 2px solid #BD1906;
                        width: 12px;
                        height: 12px;
                        margin: -6px 0;  /* Center the handle vertically */
                        border-radius: 8px;  /* Make it a circle */
                    }
                    QSlider::groove:horizontal {
                        height: 6px;
                        background: #E0E0E0;
                        border-radius: 3px;
                    }
                    QSlider::sub-page:horizontal {
                        background: #BD1906;
                        border-radius: 3px;
                    }
                """)


        main_layout.addWidget(self.slider, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)
        main_layout.addWidget(self.slider_label, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

    def change_value(self, value):
        self.current_value = value
        self.slider_label.setText(f"{value}%")

class ToppingGridItem(QtWidgets.QWidget):
    clicked = pyqtSignal()

    def __init__(self, topping_id, name, price, discounted_price, image_path):
        super().__init__()
        self.topping_id = topping_id
        self.name = name
        self.price = price
        self.discounted_price = discounted_price
        self.image_path = image_path
        self.topping = Topping(topping_id, name, price, discounted_price)
        self.isChecked = False

        self.setupUI()

    def setupUI(self):
        self.setContentsMargins(10, 10, 10, 10)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.image_label = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap(self.image_path)
        self.image_label.setPixmap(self.pixmap.scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                            QtCore.Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image_label)

        name_label = QtWidgets.QLabel(self.name)
        name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("font-size: 14px; padding-top: 3px;")
        main_layout.addWidget(name_label)

        price_layout = QtWidgets.QHBoxLayout()
        price_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        if self.discounted_price < self.price:
            original_price_label = QtWidgets.QLabel(f"{self.price:,}đ")
            original_price_label.setStyleSheet(
                "color: gray; text-decoration: line-through; font-size: 12px;")
            price_layout.addWidget(original_price_label)

            discounted_price_label = QtWidgets.QLabel(f"{self.discounted_price:,}đ")
            discounted_price_label.setStyleSheet("color: #D35400; font-size: 14px; font-weight: bold;")
            price_layout.addWidget(discounted_price_label)
        else:
            price_label = QtWidgets.QLabel(f"{self.price:,}đ")
            price_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            price_label.setStyleSheet("color: #D35400; font-size: 14px; font-weight: bold;")
            price_layout.addWidget(price_label)

        main_layout.addLayout(price_layout)

        self.checkbox = QtWidgets.QCheckBox()

        checkbox_layout = QtWidgets.QHBoxLayout()
        checkbox_layout.addStretch()
        checkbox_layout.addWidget(self.checkbox)
        checkbox_layout.addStretch()
        main_layout.addLayout(checkbox_layout)
        self.checkbox.clicked.connect(self.mousePressEvent)

        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit signal when clicked
        self.isChecked = not self.isChecked
        self.checkbox.setChecked(self.isChecked)
        print("clicked")

class ToppingGridLayout(QGridLayout):
    def __init__(self, topping_selection_widget: ToppingSelection, parent=None):
        super().__init__(parent)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.selectedToppings: List[Topping] = []
        self.topping_selection_widget = topping_selection_widget

    def addToppingItems(self, toppings):
        for i, (topping_id, name, price, discounted_price, image_path) in enumerate(toppings):
            toppingGridItem = ToppingGridItem(topping_id, name, price, discounted_price, image_path)
            toppingGridItem.clicked.connect(self.click_topping)
            self.addWidget(toppingGridItem, i // 2, i % 2)

    def click_topping(self):
        clicked_button = self.sender()
        for index, existing_topping in enumerate(self.selectedToppings):
            if existing_topping == clicked_button.topping:
                self.selectedToppings.pop(index)
                self.topping_selection_widget.calculata_total_price(-existing_topping.discountPrice)
                print(self.selectedToppings)
                print(f"Remove topping id: {existing_topping.id}")
                return
        self.selectedToppings.append(clicked_button.topping)
        self.topping_selection_widget.calculata_total_price(clicked_button.topping.discountPrice)
        print(self.selectedToppings)
        print(f"Add topping id: {clicked_button.topping_id}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ToppingSelection()
    window.show()
    sys.exit(app.exec())