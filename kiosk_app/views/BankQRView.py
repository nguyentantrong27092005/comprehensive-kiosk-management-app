import os

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QSpacerItem, QSizePolicy
from PyQt6 import QtCore, QtGui, QtWidgets
import os
import qrcode
import datetime

class Image(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size, qrcode_modules):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QtGui.QImage(
            size, size, QtGui.QImage.Format.Format_RGB16)
        self._image.fill(QtCore.Qt.GlobalColor.white)

    def pixmap(self):
        return QtGui.QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QtGui.QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.GlobalColor.black)

    def save(self, stream, kind=None):
        pass


class BankQRWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()


    def setupUi(self):
        self.current_path = os.getcwd()
        self.setupMainWindow()
        self.setupQRSection()
        # self.setupStyleSheet()

    def setupMainWindow(self):
        self.count = 300
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
        self.qrCodeImage.setPixmap(qrcode.make("00020101021238590010A000000727012900069704180115V3CAS31435208230208QRIBFTTA5303704540420005802VN62350831CSLLVD6H0X2 Thanh toan don hang6304C2A2", box_size=8, image_factory=Image).pixmap().scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        self.qrCodeImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdownTimerLabel = QtWidgets.QLabel(self)
        self.countdownTimerLabel.setObjectName("countdownTimerLabel")
        self.countdownTimerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdownTimerLabel.setText(self.secs_to_minsec(self.count))
        self.countdownTimer = QTimer(self)
        self.countdownTimer.timeout.connect(self.showTime)
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

    def showTime(self):
        self.count -= 1
        self.countdownTimerLabel.setText(self.secs_to_minsec(self.count))

    def secs_to_minsec(self, secs: int):
        mins = secs // 60
        secs = secs % 60
        minsec = f'{mins:02}:{secs:02}'
        return minsec


if __name__ == '__main__':
    app=QApplication([])
    myWindow= BankQRWidget()
    myWindow.show()
    app.exec()