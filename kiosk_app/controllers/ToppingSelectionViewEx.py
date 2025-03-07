import sys
import pymysql
from PyQt6 import QtWidgets
from kiosk_app.models.FoodItem import FoodItem
from kiosk_app.models.Order import OrderItem, Order
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.models.ToppingVariant import Topping, Variant
from kiosk_app.views.ToppingSelectionView import ToppingSelection, Database_ToppingSelection
from kiosk_app.views.order_summary_view import Ui_MainWindow

class ToppingSelectionEx(ToppingSelection):

    def __init__(self, mainStackedWidget: QtWidgets.QStackedWidget, sharedData, db):
        super().__init__()
        self.sharedData = sharedData
        self.db = db
        self.selected_quantity = 1  # Đặt giá trị mặc định là 1 đề phòng người dùng ko thay đổi số lượng
        self.mainStackedWidget = mainStackedWidget
        self.setup_connections()

    def setup_connections(self):
        # Liên kết tới các chức năng Backend
        self.minus.clicked.connect(self.decrease_quantity)
        self.plus.clicked.connect(self.increase_quantity)
        self.add_to_cart.clicked.connect(self.save_selected_items)
        self.add_to_cart.clicked.connect(self.open_order_summary)
        self.order_summary_window = None  # Khởi tạo biến cửa sổ Order Summary

        # Kiểm tra xem slider có tồn tại không trước khi kết nối
        if hasattr(self, "slider"):
            self.slider.valueChanged.connect(self.update_slider_label)
        else:
            print("Món này ko có slider")

    def open_order_summary(self):
        # Mở cửa số Order
        if not self.order_summary_window:
            self.order_summary_window = Ui_MainWindow()
        self.order_summary_window.show()

    def increase_quantity(self):
        #Tăng số lượng
        current_value = int(self.number.text())
        new_value = current_value + 1
        self.number.setText(str(new_value))
        self.selected_quantity = new_value  # Cập nhật số lượng đã chọn

    def decrease_quantity(self):
        # Giảm số lượng nhưng > 1
        current_value = int(self.number.text())
        if current_value > 1:
            new_value = current_value - 1
            self.number.setText(str(new_value))
            self.selected_quantity = new_value  # Cập nhật số lượng đã chọn

    def update_slider_label(self, value):
        # Kéo giảm slider
        self.slider_label.setText(f"{value}%")

    def save_selected_items(self):
        """Lưu những item được chọn khi bấm nút thêm vào giỏ hàng"""

        # Kiểm tra xem có thuộc tính button_sizes không, nếu không thì không cần xử lý
        self.selected_size_data = None
        if hasattr(self, "button_sizes") and self.button_sizes:
            for button, size_id, size_value in self.button_sizes:
                if button.isChecked():
                    self.selected_size_data = (size_id, size_value)

        # Kiểm tra và in ra nếu có size
        if self.selected_size_data:
            print("Selected Size:", self.selected_size_data)
        else:
            print("Món này không có size")

        # Lưu danh sách toppings đã chọn
        self.selected_toppings = []
        for (checkbox, name), (topping_id, _, price, discounted_price, _) in zip(self.checkboxes, self.toppings):
            if checkbox.isChecked():
                topping = Topping(topping_id, name, price, discounted_price) # tạo ra các object topping từ class Topping
                self.selected_toppings.append(topping)

        # chuyển toppings thành data type: tuple
        selectedToppingList = []
        for t in self.selected_toppings:
            selectedToppingList.append((t.id, t.name, t.price, f"{t.discountPrice:,}đ"))

        # In ra kiểm tra
        if selectedToppingList:
            print("selectedToppingList:", selectedToppingList)

        # Lưu danh sách variants đã chọn
        self.selected_variants = []
        for radio_button, variant_id, value in self.radio_list:
            if radio_button.isChecked():
                variant = Variant(variant_id, value) # Tạo ra các object từ variant từ class Variant
                self.selected_variants.append(variant)

        # chuyển variants thành data type: tuple
        selectedVariantList = []
        for v in self.selected_variants:
            selectedVariantList.append((v.id, v.value))

        # In để kiểm tra
        if selectedVariantList:
            print("selectedVariantList:", selectedVariantList)

        # Lấy nội dung ghi chú từ QTextEdit
        self.order_note = self.note_text.toPlainText().strip()

        # Lấy giá trị slider nếu có
        value = self.slider.value() if hasattr(self, 'slider') else None

        # Nếu có slider, thêm vào ghi chú với dấu phẩy, nếu không có ghi chú thì chỉ ghi mỗi slider
        if value is not None:
            if self.order_note:
                self.order_note += f", {value}%"
            else:
                self.order_note = f"{value}%"

        # In ra note + phần trăm slider(nếu có)
        print(f"note: {self.order_note}")

        # lấy số lượng sau khi chọn
        selected_quantity = self.selected_quantity
        print(f"quantity: {selected_quantity}")

        foodItem = FoodItem(1, "trà xoài", 19000, 16000, "Image.png", True) #food_item tự cấp do chưa có hàm truyền qua từ menu

        # Gọi class OrderItem --> Tạo ra OrderItem
        generatedOrderItem = OrderItem(
            foodItem = foodItem,
            quantity = selected_quantity,
            note = self.order_note,
            toppingList = selectedToppingList,
            variantList = selectedVariantList )
        print(f"Thông tin chi tiết về OrderItem: {generatedOrderItem}")
        print('*'*15)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainStackedWidget = QtWidgets.QStackedWidget()
    shareData = SharedDataModel()
    sharedData = Order()
    db = Database_ToppingSelection()
    window = ToppingSelectionEx(mainStackedWidget, sharedData, db)
    window.show()
    sys.exit(app.exec())