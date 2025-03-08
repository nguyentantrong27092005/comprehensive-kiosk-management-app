from kiosk_app.models.Order import Order
from PyQt6.QtCore import QObject, pyqtSignal
#Đây là class dùng để share data giữa các màn hình với nhau. Nó sẽ luôn được truyền qua lại giữa các màn hình.
class SharedDataModel(QObject):
    data_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.order: Order = Order()
        self.selected_item = None

    def set_selected_item(self, item):
        """Sử dụng hàm này để update id của object vừa được bấm vào. Ví dụ: FoodItemID của món được chọn trên menu"""
        self.selected_item = item
        self.data_updated.emit()  # Notify listeners
        print(f"Item đã được chọn: {self.selected_item}")
    def get_selected_item(self):
        """Sử dụng hàm này để lấy id của object vừa được bấm vào. Ví dụ: Màn hình topping query các dữ liệu có liên quan đến món được chọn."""
        return self.selected_item

    def reset_data(self):
        self.order: Order = Order()
        self.selected_item = None
