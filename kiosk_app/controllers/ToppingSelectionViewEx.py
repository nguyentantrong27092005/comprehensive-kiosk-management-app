import sys
import pymysql
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QVBoxLayout

from common.sql_func import Database
from kiosk_app.models.FoodItem import FoodItem
from kiosk_app.models.Order import OrderItem, Order
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.models.ToppingVariant import Topping, Variant
from kiosk_app.views.CustomStackedWidget import CustomStackedWidget
from kiosk_app.views.GeneralView import GeneralView
from kiosk_app.views.ToppingSelectionView import ToppingSelection
from kiosk_app.controllers.OrderSummaryViewEx import OrderSummaryViewEx


class ToppingSelectionEx(GeneralView):
    def __init__(self, mainStackedWidget: CustomStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.sharedData = sharedData
        self.db = db
        self.selected_quantity = 1  # Đặt giá trị mặc định là 1 đề phòng người dùng ko thay đổi số lượng
        self.mainStackedWidget = mainStackedWidget
        self.toppingSelectionView = ToppingSelection(sharedData, db)
        self.setup_connections()
        self.toppingSelectionVLayout = QVBoxLayout(self.frame_chung)
        self.toppingSelectionVLayout.setContentsMargins(0,0,0,0)
        self.toppingSelectionVLayout.addWidget(self.toppingSelectionView)
        self.frame_chung.setStyleSheet("background-color: white")
        self.frame_ngang.setHidden(True)
        self.frame_chung.setContentsMargins(0,0,0,0)

    def setup_connections(self):
        # Liên kết tới các chức năng Backend
        self.toppingSelectionView.minus.clicked.connect(self.decrease_quantity)
        self.toppingSelectionView.plus.clicked.connect(self.increase_quantity)
        self.toppingSelectionView.add_to_cart.clicked.connect(self.save_selected_items)
        self.toppingSelectionView.back_button.clicked.connect(self.click_back_button)
        self.order_summary_window = None  # Khởi tạo biến cửa sổ Order Summary

        # Kiểm tra xem slider có tồn tại không trước khi kết nối
        if hasattr(self, "slider"):
            self.toppingSelectionView.slider.valueChanged.connect(self.update_slider_label)
        else:
            print("Món này ko có slider")

    def click_back_button(self):
        self.mainStackedWidget.change_screen_with_index(1, self)
        currentWidget = self.mainStackedWidget.currentWidget()
        currentWidget.load_items(category_name=None, category_id=None)
        currentWidget.kioskMenuWidget.groupbox_item.setTitle("Tất cả món")

    def open_order_summary(self):
        # Mở cửa số Order
        order_summary_window = OrderSummaryViewEx(self.mainStackedWidget, self.sharedData, self.db)
        self.mainStackedWidget.change_screen(order_summary_window, self)

    def increase_quantity(self):
        #Tăng số lượng
        current_value = int(self.toppingSelectionView.number.text())
        new_value = current_value + 1
        self.toppingSelectionView.number.setText(str(new_value))
        self.selected_quantity = new_value  # Cập nhật số lượng đã chọn
        self.toppingSelectionView.calculata_total_price()

    def decrease_quantity(self):
        # Giảm số lượng nhưng > 1
        current_value = int(self.toppingSelectionView.number.text())
        if current_value > 1:
            new_value = current_value - 1
            self.toppingSelectionView.number.setText(str(new_value))
            self.selected_quantity = new_value  # Cập nhật số lượng đã chọn
            self.toppingSelectionView.calculata_total_price()

    def update_slider_label(self, value):
        # Kéo giảm slider
        self.toppingSelectionView.slider_label.setText(f"{value}%")

    def save_selected_items(self):
        """Lưu những item được chọn khi bấm nút thêm vào giỏ hàng"""

        # Kiểm tra xem có thuộc tính button_sizes không, nếu không thì không cần xử lý
        selectedVariantList = []
        for visible_variant_group in self.toppingSelectionView.visible_variant_groups:
            selectedVariantList.append(visible_variant_group.active_button.variant_value)

        # In ra kiểm tra
        if self.toppingSelectionView.grid_layout.selectedToppings:
            print("selectedToppingList:", self.toppingSelectionView.grid_layout.selectedToppings)


        # In để kiểm tra
        if selectedVariantList:
            print("selectedVariantList:", selectedVariantList)

        # Lấy nội dung ghi chú từ QTextEdit
        self.order_note = self.toppingSelectionView.note_text.toPlainText().strip()

        # Nếu có slider, thêm vào ghi chú với dấu phẩy, nếu không có ghi chú thì chỉ ghi mỗi slider
        for slider in self.toppingSelectionView.visible_sliders:
            if self.order_note:
                self.order_note += f", {slider.title()}: {slider.current_value}%"
            else:
                self.order_note = f"{slider.title()}: {slider.current_value}%"

        # In ra note + phần trăm slider(nếu có)
        print(f"note: {self.order_note}")

        # lấy số lượng sau khi chọn
        print(f"quantity: {self.selected_quantity}")

        # Gọi class OrderItem --> Tạo ra OrderItem
        generatedOrderItem = OrderItem(
            foodItem = self.sharedData.selected_item,
            quantity = self.selected_quantity,
            note = self.order_note,
            toppingList = self.toppingSelectionView.grid_layout.selectedToppings,
            variantList = selectedVariantList )
        print(generatedOrderItem.total_item_price, generatedOrderItem.foodItem.discounted_price, generatedOrderItem.foodItem.price)
        #Kiểm tra món đã tồn tại chưa, nếu rồi thì cộng thêm số lượng
        existing_items = self.sharedData.order.orderItems
        found = False
        for item in existing_items:
            if item == generatedOrderItem:
                item.quantity += self.selected_quantity
                item.total_item_price += generatedOrderItem.total_item_price
                found = True
                break
        if not found:
            self.sharedData.order.add_new_order_items([generatedOrderItem])
        self.open_order_summary()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainStackedWidget = QtWidgets.QStackedWidget()
    sharedData = SharedDataModel()
    db = Database()
    window = ToppingSelectionEx(mainStackedWidget, sharedData, db)
    window.show()
    sys.exit(app.exec())