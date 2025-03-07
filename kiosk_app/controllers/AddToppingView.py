from PyQt6 import QtWidgets, QtGui, QtCore
import sys
import pymysql

# Class khởi tạo CSDL
class Database:
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
            print("Kết nối cơ sở dữ liệu thành công!")
        except pymysql.MySQLError as e:
            print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")
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
            print("Đã đóng kết nối với cơ sở dữ liệu.")


class AddTopping(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chi tiết")
        self.topping_widgets = []
        self.resize(398, 708)  # Set size
        self.setupUI()

    def setupUI(self):

        # Set main layout dọc chính cho kiosk
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Thanh tiêu đề
        self.title_label = QtWidgets.QLabel("Chi tiết")
        self.title_label.setStyleSheet(
            "background-color: #BD1906; color: white; padding: 10px; font-weight: bold; font-family: Arial; font-size: 16px;")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Label căn giữa
        self.main_layout.addWidget(self.title_label)

        db = Database()
        food_item_id = int(input("Nhập food_item_id muốn xem chi tiết: "))  # thay = ID của món ăn cần lấy
        toppings = db.fetch_all_toppings(food_item_id)  # trả về danh sách dicts topping
        db.close_connection()

        # Vì dữ liệu topping trả về là dict --> xây dựng hàm chuyển về tuple để cho dễ trích xuất dữ liệu
        # Hàm chuyển đổi thành dữ liệu tuple
        def convert_to_tuples(toppings):
            return [(p["Name"], p["Price"], p["DiscountedPrice"], p["ImageURL"]) for p in toppings]

        product_tuples = convert_to_tuples(toppings)
        db = Database()

        # Lấy danh sách nhóm biến thể

        variant_groups = db.fetch_variantgroup(food_item_id)

        if variant_groups:
            for i in variant_groups:

                # RadioList
                if i['ViewType'] == "RadioList":
                    self.group_box_radio_list = QtWidgets.QGroupBox(i["Name"])
                    self.vertical_layout_radio = QtWidgets.QVBoxLayout()
                    self.radio_list = []

                    # Lấy danh sách các variant của từng nhóm variant
                    variants = db.fetch_each_variant(i["ID"])
                    if variants:
                        for variant in variants:
                            radio_button = QtWidgets.QRadioButton(variant["Value"])
                            self.radio_list.append(radio_button)
                            self.vertical_layout_radio.addWidget(radio_button)

                    # Thêm layout vào group box và vào main layout
                    self.group_box_radio_list .setLayout(self.vertical_layout_radio)
                    self.main_layout.addWidget(self.group_box_radio_list )

                # Buttons
                if i['ViewType'] == "ChonSize":
                    self.group_box_size = QtWidgets.QGroupBox(i["Name"])
                    self.horizontal_layout_size = QtWidgets.QHBoxLayout()
                    self.button_sizes = []

                    variants = db.fetch_each_variant(i["ID"])
                    if variants:
                        for variant in variants:
                            button_size = QtWidgets.QPushButton(variant["Value"])
                            self.button_sizes.append(button_size)
                            self.horizontal_layout_size.addWidget(button_size)
                    self.group_box_size.setLayout(self.horizontal_layout_size)
                    self.main_layout.addWidget(self.group_box_size)

                #Slider
                if i['ViewType'] == "Slider":
                    self.group_box_slider = QtWidgets.QGroupBox(i["Name"])
                    variants = db.fetch_each_variant(i["ID"])
                    self.horizontial_layout_slider = QtWidgets.QHBoxLayout()
                    self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)  # Slider nằm ngang
                    self.slider.setMinimum(0)
                    self.slider.setMaximum(100)
                    self.slider.setValue(50)  # Giá trị mặc định 50%
                    self.slider_label = QtWidgets.QLabel("50%")  # Hiển thị phần trăm thật còn mấy cái trên là đang mặc định
                    self.slider.valueChanged.connect(self.update_slider_label)  # Kết nối sự kiện thay đổi
                    self.horizontial_layout_slider.addWidget(self.slider)
                    self.horizontial_layout_slider.addWidget(self.slider_label)
                    self.group_box_slider.setLayout(self.horizontial_layout_slider)
                    self.main_layout.addWidget(self.group_box_slider)

        # GridView (hiển thị topping)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.scroll_widget)

        self.toppings = product_tuples # Lấy danh sách tupple từ hàm connver_to_tuples ở trên

        for i, (name, price, discounted_price, image_path) in enumerate(self.toppings):
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

        # Hiển thị thanh số lượng
        self.group_box_quantity = QtWidgets.QGroupBox("Số lượng")
        self.frame_vertical = QtWidgets.QHBoxLayout()

        # Căn phải toàn bộ layout
        self.frame_vertical.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Nút trừ
        self.minus = QtWidgets.QPushButton("-")
        self.minus.setFixedSize(50, 50)
        self.minus.setStyleSheet("color: red; font-size: 30px; font-weight: bold;")

        # Nút cộng
        self.plus = QtWidgets.QPushButton("+")
        self.plus.setFixedSize(50, 50)
        self.plus.setStyleSheet("color: red; font-size: 30px; font-weight: bold;")

        # Hiển thị số
        self.number = QtWidgets.QLabel("1")
        self.number.setStyleSheet("color: red; font-size: 40px; font-weight: bold;")  # Tăng kích thước số 1
        self.number.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Căn giữa
        self.number.setFixedSize(70, 70)  # Làm cho số 1 lớn hơn hai nút bên cạnh

        # Add vào layout ngang
        self.frame_vertical.addWidget(self.minus)
        self.frame_vertical.addWidget(self.number)
        self.frame_vertical.addWidget(self.plus)

        # Add vào group bõ
        self.group_box_quantity.setLayout(self.frame_vertical)  # setlayout vì căn khổ cho layout
        self.main_layout.addWidget(self.group_box_quantity)

        # Nút thêm vào giỏ hàng
        self.add_to_cart = QtWidgets.QPushButton("Thêm vào giỏ hàng")
        self.add_to_cart.setMinimumSize(454, 32)
        self.add_to_cart.setIcon(QtGui.QIcon("D:\\avcnro3i9.jpg"))
        self.add_to_cart.setIconSize(QtCore.QSize(24, 24))
        self.add_to_cart.setStyleSheet("background-color: #BD1906; color: white; font-weight: bold")
        self.main_layout.addWidget(self.add_to_cart)

    # hàm hiển thị phần trăm slider
    def update_slider_label(self, value):
        self.slider_label.setText(f"{value}%")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AddTopping()
    window.show()
    sys.exit(app.exec())



