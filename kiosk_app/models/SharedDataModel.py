from kiosk_app.models.Order import Order
from PyQt6.QtCore import QObject, pyqtSignal

class SharedDataModel(QObject):
    data_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.order: Order = Order()
        self.selected_item = None

    def set_selected_item(self, item):
        """Update the selected item and notify all widgets"""
        self.selected_item = item
        self.data_updated.emit()  # Notify listeners

    def get_selected_item(self):
        """Retrieve the current selected item"""
        return self.selected_item

    def reset_data(self):
        self.order: Order = Order()
        self.selected_item = None
