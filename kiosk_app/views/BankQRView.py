import os

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QSpacerItem, QSizePolicy
from PyQt6 import QtCore, QtGui, QtWidgets
import os
import qrcode
import datetime


class BankQRWidget(QtWidgets.QWidget): #Thiết kế dưới dạng QWidget để thêm vào frame chung của màn hình chung
    def __init__(self):
        super().__init__()
        self.setupUi()


    def setupUi(self):
        self.current_path = os.getcwd()
        self.setupMainWindow()
        self.setupQRSection()
        # self.setupStyleSheet()

    def setupMainWindow(self):
        self.setObjectName("MainWindow")
        self.resize(478, 592)
        self.setFixedSize(478, 592)
        self.setStyleSheet("background-color: #BD1906; font-family: Montserrat; font-size: 15px;")
        self.mainVLayout = QtWidgets.QVBoxLayout(self)
        self.mainVLayout.setObjectName("mainVLayout")
        self.mainVLayout.setContentsMargins(26, 64, 26, 64)
        self.redFrame = QtWidgets.QFrame(self)
        self.redFrame.setStyleSheet("background-color: #BD1906;")
        self.mainVLayout.addWidget(self.redFrame)
        self.setLayout(self.mainVLayout)

    def setupQRSection(self):
        self.whiteFrame = QtWidgets.QFrame(self)
        self.whiteFrame.setStyleSheet("background-color: white; border-radius: 15px;")

        self.contentVLayout = QtWidgets.QVBoxLayout(self)
        self.contentVLayout.setObjectName("verticalLayout")
        self.contentVLayout.setSpacing(0)
        spacer = QSpacerItem(40, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.instructionTitle = QtWidgets.QLabel(self)
        self.instructionTitle.setObjectName("instructionTitle")
        self.instructionTitle.setText("Vui lòng quét mã QR bên dưới để thanh toán")
        self.instructionTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructionTitle.setStyleSheet("font-weight: 700;")
        self.qrCodeImage = QtWidgets.QLabel(self)
        self.qrCodeImage.setObjectName("qrCodeImage")
        self.qrCodeImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdownTimerLabel = QtWidgets.QLabel(self)
        self.countdownTimerLabel.setObjectName("countdownTimerLabel")
        self.countdownTimerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdownTimer = QTimer(self)
        self.countdownTimer.start(1000)

        self.contentVLayout.addSpacerItem(spacer)
        self.contentVLayout.addWidget(self.instructionTitle)
        self.contentVLayout.addWidget(self.qrCodeImage)
        self.contentVLayout.addWidget(self.countdownTimerLabel)
        self.contentVLayout.addSpacerItem(spacer)
        self.whiteFrame.setLayout(self.contentVLayout)
        self.whiteFrameVLayout = QtWidgets.QVBoxLayout(self)
        self.whiteFrameVLayout.setObjectName("whiteFrameVLayout")
        self.whiteFrameVLayout.addWidget(self.whiteFrame)
        self.redFrame.setLayout(self.whiteFrameVLayout)




if __name__ == '__main__':
    app=QApplication([])
    myWindow= BankQRWidget()
    myWindow.show()
    app.exec()