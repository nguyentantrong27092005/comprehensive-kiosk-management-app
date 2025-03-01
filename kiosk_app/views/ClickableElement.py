from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame

class ClickableFrame(QFrame):
    """Class để tạo ra QFrame có thể click được"""
    clicked = pyqtSignal()  # Define a custom signal

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit signal when clicked
