from PyQt6.QtWidgets import QApplication, QMainWindow
from kiosk_app.controllers.PaymentSelectViewEx import MainWindowEx

app=QApplication([])
myWindow= MainWindowEx()
myWindow.setupUi(QMainWindow())
myWindow.show()
app.exec()