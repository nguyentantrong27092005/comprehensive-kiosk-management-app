import os
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLineEdit


class LoginAppWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.image_path = os.getcwd()
        self.setupMainWindow()
        self.setupContent()

    def setupMainWindow(self):
        self.setObjectName("MainWindow")
        self.setWindowIcon(QIcon(self.image_path))
        self.resize(1280, 720)
        self.setMaximumSize(1280, 720)
        self.setMinimumSize(1280, 720)

        # Layout chính
        self.mainVLayout = QtWidgets.QVBoxLayout(self)
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)

        # Frame đỏ nền
        self.redFrameLogin = QtWidgets.QFrame(self)
        self.redFrameLogin.setStyleSheet("background-color: #BD1906;")
        self.redFrameLogin.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.mainVLayout.addWidget(self.redFrameLogin)
        self.setLayout(self.mainVLayout)

    def setupContent(self):

        # Layout căn giữa toàn bộ nội dung
        self.centerLayout = QtWidgets.QVBoxLayout(self.redFrameLogin)
        self.centerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Frame trắng chứa nội dung các widget
        self.whiteFrame = QtWidgets.QFrame(self.redFrameLogin)
        self.whiteFrame.setObjectName('whiteFrame')
        self.whiteFrame.setStyleSheet("background-color: #ffffff; border-radius: 15px;")
        self.whiteFrame.setFixedSize(585, 522)

        # căn giữa layout
        self.centerLayout.addWidget(self.whiteFrame, alignment=Qt.AlignmentFlag.AlignCenter)

        # Layout chứa nội dung trong whiteFrame
        self.contentVLayout = QtWidgets.QVBoxLayout(self.whiteFrame)
        self.contentVLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contentVLayout.setSpacing(15)  # Tạo khoảng cách giữa các phần tử

        # Tiêu đề ĐĂNG NHẬP
        self.LoginTitle = QtWidgets.QLabel("ĐĂNG NHẬP", self.whiteFrame)
        self.LoginTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.LoginTitle.setStyleSheet("font-weight: bold; font-size: 25px; color: #BD1906;")

        # Email input
        self.LabelEmail = QtWidgets.QLabel("Email:", self.whiteFrame)
        self.InputEmail = QtWidgets.QLineEdit(self.whiteFrame)
        self.InputEmail.setFixedHeight(40)
        self.InputEmail.setPlaceholderText("Nhập email của bạn")
        self.InputEmail.setStyleSheet("border: 2px solid gray; border-radius: 5px;")

        # Mật khẩu input
        self.LabelPassword = QtWidgets.QLabel("Mật khẩu:", self.whiteFrame)
        self.InputPassword = QtWidgets.QLineEdit(self.whiteFrame)
        self.InputPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.InputPassword.setFixedHeight(40)
        self.InputPassword.setPlaceholderText("Nhập mật khẩu")
        self.InputPassword.setStyleSheet("border: 2px solid gray; border-radius: 5px;")

        # Chỉ hiện thi khi đăng nhập lỗi
        self.errorLabel = QtWidgets.QLabel("", self.whiteFrame)
        self.errorLabel.setStyleSheet("color: red; font-size: 12px;")
        self.errorLabel.setVisible(False)  # Ẩn

        # Nút đăng nhập
        self.LoginButton = QtWidgets.QPushButton("Đăng nhập", self.whiteFrame)
        self.LoginButton.setFixedHeight(45)
        self.LoginButton.setStyleSheet("background-color: #BD1906; color: white; font-size: 18px; border-radius: 10px;")

        # Thêm hết widget vào layout
        self.contentVLayout.addWidget(self.LoginTitle)
        self.contentVLayout.addWidget(self.LabelEmail)
        self.contentVLayout.addWidget(self.InputEmail)
        self.contentVLayout.addWidget(self.LabelPassword)
        self.contentVLayout.addWidget(self.InputPassword)
        self.contentVLayout.addWidget(self.errorLabel)
        self.contentVLayout.addSpacing(20)
        self.contentVLayout.addWidget(self.LoginButton)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    myWindow = LoginAppWidget()
    myWindow.show()
    app.exec()
