import os

from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.current_path = os.getcwd()
        self.setupMainWindow()
        self.setupCentralWidget()
        self.setupBanner()
        self.setupHeader()
        self.setupScrollArea()
        self.setupPaymentSection()
        self.setupPaymentButton()
        self.setupMenuBar()
        self.setupStatusBar()
        # self.setupStyltSheet()

    def setupMainWindow(self):
        self.setObjectName("MainWindow")
        self.resize(478, 850)
        self.setFont(QtGui.QFont("Montserrat", 8))
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

    def setupCentralWidget(self):
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setCentralWidget(self.centralwidget)

    def setupBanner(self):
        self.frame_banner = QtWidgets.QFrame(parent=self.centralwidget)
        # self.frame_banner.setObjectName("frame_banner")
        self.frame_banner.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 5))
        self.frame_banner.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_banner.setObjectName("frame_banner")
        self.verticalLayout_banner = QtWidgets.QVBoxLayout(self.frame_banner)
        # Chỉnh layout sát lề frame
        self.verticalLayout_banner.setContentsMargins(0, 0, 0, 0)
        # Thêm hình ảnh banner
        self.label_banner = QtWidgets.QLabel(self.frame_banner)
        self.label_banner.setObjectName("label_banner")
        self.label_banner.setPixmap(QtGui.QPixmap(f"{self.current_path}/../resources/images/img_banner.jpg"))
        self.label_banner.setScaledContents(True)

        self.verticalLayout_banner.addWidget(self.label_banner)

        self.verticalLayout.addWidget(self.frame_banner)
    def setupHeader(self):
        self.frame_headerthanhtoan = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_headerthanhtoan.setObjectName("frame_headerthanhtoan")
        self.frame_headerthanhtoan.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred, 0, 1))
        self.frame_headerthanhtoan.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        # Bỏ viền của frame
        self.frame_headerthanhtoan.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        # Áp horizontal layout, sát lề
        self.horizontalLayout_header = QtWidgets.QHBoxLayout(self.frame_headerthanhtoan)
        self.horizontalLayout_header.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_header.setSpacing(0)

        # Button quay lại
        self.pushButton_return = QtWidgets.QPushButton(self.frame_headerthanhtoan)
        self.pushButton_return.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 1, 0))
        self.pushButton_return.setIcon(QtGui.QIcon(f"{self.current_path}/../resources/images/ic_return.png"))
        self.pushButton_return.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_return.setFlat(True)

        # Label text thanh toán
        self.label_thanhtoan = QtWidgets.QLabel(self.frame_headerthanhtoan)
        self.label_thanhtoan.setObjectName("label_thanhtoan")
        self.label_thanhtoan.setText("Giỏ hàng")
        self.label_thanhtoan.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred, 10, 0))

        # Add button và label vào layout
        self.horizontalLayout_header.addWidget(self.pushButton_return)
        self.horizontalLayout_header.addWidget(self.label_thanhtoan)

        #Add vào central
        self.verticalLayout.addWidget(self.frame_headerthanhtoan)

    def setupScrollArea(self):
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 17))
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout_contents = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        # căn trên widget bên trong
        self.verticalLayout_contents.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        # add widget
        self.setupProductBox()
        self.setupProductBox()
        self.setupProductBox()
        self.setupProductBox()
        self.setupProductBox()
        self.setupProductBox()

        # add vào central widget
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
    def setupProductBox(self):
        self.frame_product = QtWidgets.QFrame(parent=self.scrollAreaWidgetContents)
        self.frame_product.setObjectName("frame_product")
        self.frame_product.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Fixed
        ))
        # cỡ nhỏ nhất
        self.frame_product.setMinimumSize(QtCore.QSize(0, 97))

        self.frame_product.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        # self.frame_product.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        # add layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_product)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(0)

        # add vào layout của scrollarea
        self.verticalLayout_contents.addWidget(self.frame_product)
        # add widget
        self.setupProductImage()
        self.setupProductContent()
        self.setupPriceBox()

    def setupProductImage(self):
        self.frame_productimage = QtWidgets.QFrame(parent=self.frame_product)
        self.frame_productimage.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 90, 0
        ))
        self.frame_productimage.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_productimage.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        # layout
        self.verticalLayout_img = QtWidgets.QVBoxLayout(self.frame_productimage)
        self.verticalLayout_img.setContentsMargins(0, 0, 0, 0)
        self.label_image = QtWidgets.QLabel(parent=self.frame_productimage)
        self.label_image.setPixmap(QtGui.QPixmap(f"{self.current_path}/../resources/images/img_banhtrangtron.png"))
        self.label_image.setScaledContents(True)
        self.verticalLayout_img.addWidget(self.label_image)

        self.horizontalLayout.addWidget(self.frame_productimage)
    def setupProductContent(self):
        self.frame_productcontent = QtWidgets.QFrame(parent=self.frame_product)
        self.frame_productcontent.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored,186, 0
        ))
        self.frame_productcontent.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_productcontent.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        # layout
        self.verticalLayout_contents2 = QtWidgets.QVBoxLayout(self.frame_productcontent)
        self.verticalLayout_contents2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_contents2.setSpacing(2)
        # label tên sản phẩm
        self.label_name = QtWidgets.QLabel(parent=self.frame_productcontent)
        self.label_name.setObjectName("label_name")
        self.label_name.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored,0, 2
        ))
        self.verticalLayout_contents2.addWidget(self.label_name)
        self.label_name.setText("Bánh tráng trộn")

        # text topping
        self.textEdit_topping = QtWidgets.QTextEdit(parent=self.frame_productcontent)
        self.textEdit_topping.setObjectName("textEdit_topping")
        self.textEdit_topping.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored,0, 4
        ))
        self.textEdit_topping.setReadOnly(True)
        self.textEdit_topping.setText("4 Miếng Gà + 1 Mì Ý Gà viên + 2 Ly Pepsi (vừa)")

        self.verticalLayout_contents2.addWidget(self.textEdit_topping)

        # quantity
        self.setupQuantityBox()
        # thêm vào productbox
        self.horizontalLayout.addWidget(self.frame_productcontent)

    def setupQuantityBox(self):
        self.frame_quantitybox = QtWidgets.QFrame(parent=self.frame_productcontent)
        self.frame_quantitybox.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 2
        ))
        # layout
        self.horizontalLayout_quantity = QtWidgets.QHBoxLayout(self.frame_quantitybox)
        self.horizontalLayout_quantity.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_quantity.setSpacing(0)
        # pushbutton
        self.pushbutton_minus = QtWidgets.QPushButton(parent=self.frame_quantitybox)
        self.pushbutton_plus = QtWidgets.QPushButton(parent=self.frame_quantitybox)
        self.pushbutton_plus.setFlat(True)
        self.pushbutton_minus.setFlat(True)
        self.pushbutton_minus.setIcon(QtGui.QIcon(f"{self.current_path}/../resources/images/ic_minus.png"))
        self.pushbutton_plus.setIcon(QtGui.QIcon(f"{self.current_path}/../resources/images/ic_plus.png"))
        # label
        self.label_quantity = QtWidgets.QLabel(self.frame_quantitybox)
        self.label_quantity.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_quantity.setText("2")

        # add widget
        self.horizontalLayout_quantity.addWidget(self.pushbutton_minus)
        self.horizontalLayout_quantity.addWidget(self.label_quantity)
        self.horizontalLayout_quantity.addWidget(self.pushbutton_plus)
        # add layout horizontal
        self.verticalLayout_contents2.addWidget(self.frame_quantitybox)
    def setupPriceBox(self):
        self.frame_pricebox = QtWidgets.QFrame(parent=self.frame_product)
        self.frame_pricebox.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 132, 0
        ))
        self.gridLayout_price = QtWidgets.QGridLayout(self.frame_pricebox)
        self.gridLayout_price.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_price.setSpacing(0)
        # delete
        self.pushButton_delete = QtWidgets.QPushButton(self.frame_pricebox)
        self.pushButton_delete.setFlat(True)
        self.pushButton_delete.setIcon(QtGui.QIcon(f"{self.current_path}/../resources/images/ic_delete.png"))
        # price
        self.label_price = QtWidgets.QLabel(self.frame_pricebox)
        self.label_price.setObjectName("label_price")
        self.label_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_price.setText("168 000")
        # add delete và price vào grid
        self.gridLayout_price.addWidget(self.pushButton_delete, 0, 2, 2, 1)
        self.gridLayout_price.addWidget(self.label_price, 2, 0, 1, 3)

        self.horizontalLayout.addWidget(self.frame_pricebox)

    def setupPaymentSection(self):

        self.frame_paymentsection = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_paymentsection.setObjectName("frame_paymentsection")
        self.frame_paymentsection.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred, 0, 4))
        self.frame_paymentsection.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_paymentsection.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        # layout
        self.verticalLayout_paymentsection = QtWidgets.QVBoxLayout(self.frame_paymentsection)
        self.verticalLayout_paymentsection.setContentsMargins(0, 0, 0, 0)
        # label thanh toán
        self.label_payment2 = QtWidgets.QLabel(self.frame_paymentsection)
        self.verticalLayout_paymentsection.addWidget(self.label_payment2)
        self.label_payment2.setObjectName("label_payment2")
        self.label_payment2.setText("Thanh toán")

        # form
        self.formLayout_payment = QtWidgets.QFormLayout()
        self.formLayout_payment.setSpacing(6)

        self.label_voucher = QtWidgets.QLabel(self.frame_paymentsection)
        self.lineEdit_voucher = QtWidgets.QLineEdit(self.frame_paymentsection)
        self.lineEdit_voucher.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.formLayout_payment.addRow(self.label_voucher, self.lineEdit_voucher)

        self.label_total = QtWidgets.QLabel(self.frame_paymentsection)
        self.lineEdit_total = QtWidgets.QLineEdit(self.frame_paymentsection)
        self.lineEdit_total.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.label_voucher.setText("Mã voucher")
        self.label_total.setText("Tổng thanh toán")

        self.formLayout_payment.addRow(self.label_total, self.lineEdit_total)

        self.verticalLayout_paymentsection.addLayout(self.formLayout_payment)
        self.verticalLayout.addWidget(self.frame_paymentsection)

        # central widget
        self.verticalLayout.addWidget(self.frame_paymentsection)
    def setupPaymentButton(self):
        self.pushButton_payment = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_payment.setObjectName("pushButton_payment")
        self.pushButton_payment.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred, 0, 1
        ))
        self.pushButton_payment.setText("Thanh toán")
        self.verticalLayout.addWidget(self.pushButton_payment)
    def createSizePolicy(self, horizontal, vertical, hstretch=0, vstretch=0):
        sizePolicy = QtWidgets.QSizePolicy(horizontal, vertical)
        sizePolicy.setHorizontalStretch(hstretch)
        sizePolicy.setVerticalStretch(vstretch)
        return sizePolicy
    def setupMenuBar(self):
        pass

    def setupStatusBar(self):
        pass


    def setupStyltSheet(self):
        with open(f"{self.current_path}/../resources/style.css", "r") as f:
            self.setStyleSheet(f.read())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec())