from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame

class ClickableFrame(QFrame):
    clicked = pyqtSignal()  # Define a custom signal

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Emit signal when clicked
