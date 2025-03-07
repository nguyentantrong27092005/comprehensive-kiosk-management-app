import pymysql
from PyQt6 import QtWidgets, QtGui, QtCore
import sys
from common.sql_func import Database_ToppingSelection

class Database_ToppingSelection:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host="34.101.167.101",
                user="dev",
                password="12345678x@X",
                database="kioskapp",
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
        except pymysql.MySQLError as e:
            self.connection = None

    def fetch_topgroup(self, FoodItemID):
       # Dựa vào ID --> Lấy danh sách nhóm topping
        if not self.connection:
            print("Không có kết nối đến cơ sở dữ liệu.")
            return None

        query = """SELECT tg.ID, tg.Name
                   FROM toppinggroupfooditem tgfi
                   INNER JOIN toppinggroup tg ON tg.ID = tgfi.ToppingGroupID
                   WHERE tgfi.FoodItemID = %s;"""
        try:
            self.cursor.execute(query, (FoodItemID,))
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Lỗi truy vấn fetch_topgroup: {e}")
            return None

    def fetch_each_top(self, ToppingGroupID):
        # Dựa vào ID nhóm topping  --> Lấy danh sách top cụ thể
        if not self.connection:
            print("Không có kết nối đến cơ sở dữ liệu.")
            return None

        query = """SELECT t.ID,
                   fi.Name,
                   fh.Price, 
                   CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price * (1 - (p.Discount / 100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice,
                   fi.ImageURL
            FROM topping t
            INNER JOIN fooditem fi ON fi.ID = t.FoodItemID
            INNER JOIN fooditem_history fh ON fi.ID = fh.FoodItemID
            LEFT JOIN promotionfooditem pfi ON fi.ID = pfi.FoodItemID
            LEFT JOIN promotion p ON p.ID = pfi.PromotionID
            WHERE t.ToppingGroupID = %s;"""
        try:
            self.cursor.execute(query, (ToppingGroupID,))
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Lỗi truy vấn fetch_each_top: {e}")
            return None

    def fetch_all_toppings(self, FoodItemID):
        # Lấy toàn bộ danh sách topping dựa vào FoodItemID
        topping_groups = self.fetch_topgroup(FoodItemID)
        print(topping_groups)
        if not topping_groups:
            print("Không có nhóm topping nào cho món ăn này.")
            return []

        all_toppings = []
        for group in topping_groups:
            toppings = self.fetch_each_top(group['ID'])
            if toppings:
                all_toppings.extend(toppings)

        return all_toppings

    def fetch_variantgroup(self, FoodItemID):
        """Dụa vào ID --> Lấy hết các variant group"""
        if not self.connection:
            return None
        query = """SELECT vg.ID, vg.Name, vg.IsRequired, vg.ViewType, vg.HasPrice
                          FROM variantgroupfooditem vgfi
                          INNER JOIN variantgroup vg ON vg.ID = vgfi.VariantGroupID
                          WHERE vgfi.FoodItemID = %s;"""
        try:
            self.cursor.execute(query, (FoodItemID,))
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Lỗi truy vấn fetch_variantgroup: {e}")
            return None

    def fetch_each_variant(self, VariantGroupID):
        # Dựa vào ID variant grouup --> Lấy hết các variant trong group đó
        if not self.connection:
            return None

        query = """SELECT ID, Value, Price, AdditionalCost
                          FROM variant
                          WHERE variantGroupID = %s;"""
        try:
            self.cursor.execute(query, (VariantGroupID,))
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Lỗi truy vấn fetch_each_variant: {e}")
            return None

    def fetch_all_variants(self, FoodItemID):
        # Lấy toàn bộ danh sách variant
        variant_groups = self.fetch_variantgroup(FoodItemID)
        if not variant_groups:
            return []

        all_variants = []
        for group in variant_groups:
            variants = self.fetch_each_variant(group['ID'])
            if variants:
                all_variants.extend(variants)

        return all_variants

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

class ToppingSelection(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chi tiết")
        self.topping_widgets = []
        self.resize(398,708)  # Set size
        self.setupUI()

    def setupUI(self):
        # set layout dọc
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # tạo header chứa tiêu đề Chi tiết + button quay lại
        self.title_container = QtWidgets.QWidget()
        self.title_container.setStyleSheet("background-color: #BD1906;")
        self.title_container.setFixedHeight(40)

        self.title_layout = QtWidgets.QHBoxLayout(self.title_container)
        self.title_layout.setContentsMargins(5, 5, 5, 5)

        # button quay lai
        self.back_button = QtWidgets.QPushButton("←")
        self.back_button.setFixedSize(24, 24)
        self.back_button.setStyleSheet("""
                    background-color: white;
                    color: #BD1906;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    border-radius: 12px;
                """)

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

        db = Database_ToppingSelection()

        # food_item_id = int(input("Nhập food_item_id muốn xem chi tiết: "))  # thay = ID của món ăn cần lấy
        food_item_id = 13
        toppings = db.fetch_all_toppings(food_item_id)  # trả về danh sách dicts topping
        db.close_connection()

        # Vì dữ liệu topping trả về là dict --> xây dựng hàm chuyển về tuple để cho dễ trích xuất dữ liệu
        # Hàm chuyển đổi thành dữ liệu tuple
        def convert_to_tuples(toppings):
            return [(p["ID"], p["Name"], p["Price"], p["DiscountedPrice"], p["ImageURL"]) for p in toppings]

        product_tuples = convert_to_tuples(toppings)
        db = Database_ToppingSelection()

        # Lấy danh sách nhóm biến thể

        variant_groups = db.fetch_variantgroup(food_item_id)

        if variant_groups:
            for i in variant_groups:
                # RadioList
                if i['ViewType'] == "RadioList":
                    self.group_box_radio_list = QtWidgets.QGroupBox(i["Name"])
                    self.vertical_layout_radio = QtWidgets.QVBoxLayout()
                    self.radio_list = []  # Chỉ lưu radio button và ID, Value

                    # Lấy danh sách các variant từ DB
                    variants = db.fetch_each_variant(i["ID"])
                    db.close_connection()

                    if variants:
                        for variant in variants:
                            radio_button = QtWidgets.QRadioButton(variant["Value"])
                            self.radio_list.append((radio_button, variant["ID"], variant["Value"]))  # Lưu ID & Value
                            self.vertical_layout_radio.addWidget(radio_button)

                    self.group_box_radio_list.setLayout(self.vertical_layout_radio)
                    self.main_layout.addWidget(self.group_box_radio_list)

                # Buttons
                if i['ViewType'] == "ChonSize":
                    self.group_box_size = QtWidgets.QGroupBox(i["Name"])
                    self.horizontal_layout_size = QtWidgets.QHBoxLayout()
                    self.button_sizes = []

                    variants = db.fetch_each_variant(i["ID"])  # Lấy danh sách size từ DB
                    if variants:
                        for variant in variants:
                            button_size = QtWidgets.QPushButton(variant["Value"])
                            button_size.setFixedSize(40, 40)  # Kích thước nhỏ hơn
                            button_size.setCheckable(True)
                            # chỉnh bo tròn
                            button_size.setStyleSheet("""
                                QPushButton {
                                    border-radius: 20px;  
                                    background-color: #f0f0f0;
                                    padding: 3px;
                                    border: 1px solid #ccc;
                                    font-size: 12px;
                                }
                                QPushButton:hover {
                                    background-color: #d9d9d9;
                                }
                                QPushButton:checked { 
                                    background-color: #888888;  /* Màu xám khi được chọn */
                                    color: white;
                                    border: 2px solid #0056b3;
                                }
                            """)

                            self.button_sizes.append((button_size, variant["ID"], variant["Value"]))
                            self.horizontal_layout_size.addWidget(button_size)

                    self.group_box_size.setLayout(self.horizontal_layout_size)
                    self.main_layout.addWidget(self.group_box_size)

                #Slider
                if i['ViewType'] == "Slider":
                    self.group_box_slider = QtWidgets.QGroupBox(i["Name"])
                    self.group_box_layout = QtWidgets.QVBoxLayout()
                    self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
                    self.slider.setMinimum(0)
                    self.slider.setMaximum(100)
                    self.slider.setValue(50)  # Đặt mặc định là 50%
                    self.slider_label = QtWidgets.QLabel("50%")
                    self.group_box_layout.addWidget(self.slider)
                    self.group_box_layout.addWidget(self.slider_label)
                    self.group_box_slider.setLayout(self.group_box_layout)
                    self.main_layout.addWidget(self.group_box_slider)
                    self.setLayout(self.main_layout)

        # GridView (hiển thị topping)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.scroll_widget)

        self.toppings = product_tuples # Lấy danh sách tupple từ hàm connver_to_tuples ở trên
        self.selected_toppings = []
        self.checkboxes = []

        for i, (topping_id, name, price, discounted_price, image_path) in enumerate(self.toppings):
            topping_layout = QtWidgets.QVBoxLayout()
            topping_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            topping_layout.setContentsMargins(10, 10, 10, 10)

            image_label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(image_path)
            image_label.setPixmap(pixmap.scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                QtCore.Qt.TransformationMode.SmoothTransformation))
            image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            topping_layout.addWidget(image_label)

            name_label = QtWidgets.QLabel(name)
            name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            name_label.setStyleSheet("font-size: 14px; padding-top: 3px;")
            topping_layout.addWidget(name_label)

            price_layout = QtWidgets.QHBoxLayout()
            price_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            if discounted_price < price:
                original_price_label = QtWidgets.QLabel(f"{price:,}đ")
                original_price_label.setStyleSheet(
                    "color: gray; text-decoration: line-through; font-size: 12px;")
                price_layout.addWidget(original_price_label)

                discounted_price_label = QtWidgets.QLabel(f"{discounted_price:,}đ")
                discounted_price_label.setStyleSheet("color: #D35400; font-size: 14px; font-weight: bold;")
                price_layout.addWidget(discounted_price_label)
            else:
                price_label = QtWidgets.QLabel(f"{price:,}đ")
                price_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                price_label.setStyleSheet("color: #D35400; font-size: 14px; font-weight: bold;")
                price_layout.addWidget(price_label)

            topping_layout.addLayout(price_layout)

            checkbox = QtWidgets.QCheckBox()
            self.checkboxes.append((checkbox, name))  # Thêm checkbox và tên vào danh sách

            checkbox_layout = QtWidgets.QHBoxLayout()
            checkbox_layout.addStretch()
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.addStretch()
            topping_layout.addLayout(checkbox_layout)

            self.grid_layout.addLayout(topping_layout, i // 2, i % 2)

        self.scroll_widget.setLayout(self.grid_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        # Thêm ô ghi chú
        self.note_label = QtWidgets.QLabel("Ghi chú:")
        self.main_layout.addWidget(self.note_label)

        # Thêm ô nhập ghi chú
        self.note_text = QtWidgets.QTextEdit()
        self.note_text.setPlaceholderText("Nhập ghi chú tại đây...")
        self.note_text.setFixedHeight(50)  # Giới hạn chiều cao
        self.main_layout.addWidget(self.note_text)

        # Hiển thị thanh số lượng
        self.group_box_quantity = QtWidgets.QGroupBox("Số lượng")
        self.group_box_quantity.setFixedHeight(70)
        self.frame_vertical = QtWidgets.QHBoxLayout()

        # Căn giữa toàn bộ layout
        self.frame_vertical.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Nút trừ
        self.minus = QtWidgets.QPushButton("-")
        self.minus.setFixedSize(40, 40)
        self.minus.setStyleSheet("color: red; font-size: 30px; font-weight: bold;")

        # Hiển thị số
        self.number = QtWidgets.QLabel("1")
        self.number.setStyleSheet("color: red; font-size: 30px; font-weight: bold;")
        self.number.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.number.setFixedSize(30, 30)

        # Nút cộng
        self.plus = QtWidgets.QPushButton("+")
        self.plus.setFixedSize(40, 40)
        self.plus.setStyleSheet("color: red; font-size: 30px; font-weight: bold;")

        # Thêm widget vào layout với khoảng cách nhỏ
        self.frame_vertical.addWidget(self.minus)
        self.frame_vertical.addSpacing(7)  # Khoảng cách giữa nút trừ và số
        self.frame_vertical.addWidget(self.number)
        self.frame_vertical.addSpacing(7)  # Khoảng cách giữa số và nút cộng
        self.frame_vertical.addWidget(self.plus)

        # Gán layout vào group box
        self.group_box_quantity.setLayout(self.frame_vertical)

        # Thêm group box vào main layout
        self.main_layout.addWidget(self.group_box_quantity)

        # Nút thêm vào giỏ hàng
        self.add_to_cart = QtWidgets.QPushButton("Thêm vào giỏ hàng")
        self.add_to_cart.setMinimumSize(454, 32)
        self.add_to_cart.setIcon(QtGui.QIcon("kiosk_app/resources/images/icon_add_to_cart.png"))
        self.add_to_cart.setIconSize(QtCore.QSize(24, 24))
        self.add_to_cart.setStyleSheet("background-color: #BD1906; color: white; font-weight: bold")
        self.main_layout.addWidget(self.add_to_cart)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ToppingSelection()
    window.show()
    sys.exit(app.exec())