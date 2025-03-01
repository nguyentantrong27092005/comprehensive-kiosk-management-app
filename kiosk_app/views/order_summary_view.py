import os
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from kiosk_app.controllers.order_controller import DataBase, listorders, OrderItem


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = DataBase()
        self.listorders = listorders # TEST
        self.is_used = False
        self.listorders.deleteDuplicateOrder()
        self.setupUi()
        self.signalandslot()

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
        self.setMinimumSize(478, 850)
        # self.resize(478, 850)
        self.setFont(QtGui.QFont("Montserrat", 8))
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

    def setupCentralWidget(self):
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setCentralWidget(self.centralwidget)

    def setupBanner(self):
        "general"
        self.frame_banner = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_banner.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 5))
        self.frame_banner.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_banner.setObjectName("frame_banner")

        self.verticalLayout_banner = QtWidgets.QVBoxLayout(self.frame_banner)
        self.verticalLayout_banner.setContentsMargins(0, 0, 0, 0)
        "label image"
        self.label_banner = QtWidgets.QLabel(self.frame_banner)
        self.label_banner.setObjectName("label_banner")
        self.label_banner.setPixmap(QtGui.QPixmap(f"{self.current_path}/../resources/images/img_banner.jpg"))
        self.label_banner.setScaledContents(True)
        "finally"
        self.verticalLayout_banner.addWidget(self.label_banner)

        self.verticalLayout.addWidget(self.frame_banner)
    def setupHeader(self):
        "general"
        self.frame_headerthanhtoan = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_headerthanhtoan.setObjectName("frame_headerthanhtoan")
        self.frame_headerthanhtoan.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred, 0, 1))
        self.frame_headerthanhtoan.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_headerthanhtoan.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.horizontalLayout_header = QtWidgets.QHBoxLayout(self.frame_headerthanhtoan)
        self.horizontalLayout_header.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_header.setSpacing(0)

        "button quay lại"
        self.pushButton_return = QtWidgets.QPushButton(self.frame_headerthanhtoan)
        self.pushButton_return.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 1, 0))
        self.pushButton_return.setIcon(QtGui.QIcon(f"{self.current_path}/../images/ic_return.png"))
        self.pushButton_return.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_return.setFlat(True)

        "Label text thanh toán"
        self.label_thanhtoan = QtWidgets.QLabel(self.frame_headerthanhtoan)
        self.label_thanhtoan.setObjectName("label_thanhtoan")
        self.label_thanhtoan.setText("Giỏ hàng")
        self.label_thanhtoan.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred, 10, 0))

        "finally"
        self.horizontalLayout_header.addWidget(self.pushButton_return)
        self.horizontalLayout_header.addWidget(self.label_thanhtoan)

        self.verticalLayout.addWidget(self.frame_headerthanhtoan)

    def setupScrollArea(self):
        "general"
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("""
        QScrollBar:vertical {
        width: 6px; 
        background: #f0f0f0;
    }
    QScrollBar::handle:vertical {
        background: #8a8a8a;
        min-height: 5px;
        border-radius: 3px;
    }
""")
        self.scrollArea.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 16))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout_contents = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_contents.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayout_contents.setSpacing(5)
        # tính đoán độ rộng của scrollarea
        l = self.listorders.countListOrders()
        self.scrollAreaWidgetContents.setMinimumSize(320, l * (97+8))

        "productbox"

        for i in range (l):
            p = self.listorders.getItemById(i)
            product = Productbox(p, self.scrollAreaWidgetContents)
            product.deleteChanged.connect(self.updateScrollArea)
            product.quantityChanged.connect(self.updateScrollArea)
            self.verticalLayout_contents.addWidget(product.frame_product)

        "finally"
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.adjustSize()
    def updateScrollArea(self):
        " Xoá widget"
        while self.scrollAreaWidgetContents.layout().count():
            item = self.scrollAreaWidgetContents.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.listorders.deleteDuplicateOrder()
        l = self.listorders.countListOrders()
        " Khời tạo lại"
        for i in range(l):
            p = self.listorders.getItemById(i)
            if p.isdeleted == 1:
                if p.isfree ==1:
                    self.is_used = False
                continue
            else:
                if p.isfree == 1:
                    productfree = ProductboxFree(p, self.scrollAreaWidgetContents)
                    self.verticalLayout_contents.addWidget(productfree.frame_product)
                    self.is_used = True
                    productfree.deleteChanged.connect(self.updateScrollArea)
                else:
                    product = Productbox(p, self.scrollAreaWidgetContents)
                    product.quantityChanged.connect(self.updateScrollArea)
                    self.verticalLayout_contents.addWidget(product.frame_product)
                    product.deleteChanged.connect(self.updateScrollArea)

        self.lineEdit_totaltemp.setText(f"{self.listorders.totalPrice()}")
        self.lineEdit_total.setText(f"{self.listorders.totalPrice()}")
        l_notdeleted = self.listorders.countListOrderNotDeleted()
        self.scrollAreaWidgetContents.setMinimumSize(320, l_notdeleted * (97 + 8))
        self.scrollAreaWidgetContents.adjustSize()
        self.scrollAreaWidgetContents.update()
        self.scrollArea.update()

    def setupPaymentSection(self):
        "general"
        self.frame_paymentsection = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_paymentsection.setObjectName("frame_paymentsection")
        self.frame_paymentsection.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred, 0, 5))
        self.frame_paymentsection.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_paymentsection.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.verticalLayout_paymentsection = QtWidgets.QVBoxLayout(self.frame_paymentsection)
        self.verticalLayout_paymentsection.setContentsMargins(0, 0, 0, 0)
        "label thanh toán"
        self.label_payment2 = QtWidgets.QLabel(self.frame_paymentsection)
        self.verticalLayout_paymentsection.addWidget(self.label_payment2)
        self.label_payment2.setObjectName("label_payment2")
        self.label_payment2.setText("Thanh toán")

        "grid"
        self.gridLayout_payment = QtWidgets.QGridLayout()
        self.gridLayout_payment.setHorizontalSpacing(2)
        self.gridLayout_payment.setVerticalSpacing(4)

        self.label_voucher = QtWidgets.QLabel(self.frame_paymentsection)
        self.lineEdit_voucher = QtWidgets.QLineEdit(self.frame_paymentsection)
        self.label_totaltemp = QtWidgets.QLabel(self.frame_paymentsection)
        self.label_total = QtWidgets.QLabel(self.frame_paymentsection)
        self.lineEdit_totaltemp = QtWidgets.QLineEdit(self.frame_paymentsection)
        self.lineEdit_total = QtWidgets.QLineEdit(self.frame_paymentsection)
        self.pushButton_apply = QtWidgets.QPushButton(self.frame_paymentsection)

        self.lineEdit_voucher.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.lineEdit_voucher.setClearButtonEnabled(True)
        self.lineEdit_voucher.setPlaceholderText("Nhập mã voucher")
        self.lineEdit_totaltemp.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.lineEdit_total.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.lineEdit_totaltemp.setStyleSheet("""
            color: #000000;
            font-weight: 400;
            font-size: 13px;
        """)
        self.lineEdit_total.setStyleSheet("""
                    color: #BD1906;
                    font-weight: bold;
                    font-size: 13px;
                """)

        self.pushButton_apply.setStyleSheet("""
        color: #ffffff;
        background-color: #8a8a8a;
        font-weight: 400;
        font-size: 13px;
        """)
        self.lineEdit_totaltemp.setText(f"{self.listorders.totalPrice()}")
        self.lineEdit_total.setText(f"{self.listorders.totalPrice()}")

        self.lineEdit_totaltemp.setReadOnly(True)
        self.label_voucher.setText("Mã voucher")
        self.label_totaltemp.setText("Tạm tính")
        self.label_total.setText("Tổng thanh toán")
        self.pushButton_apply.setText("Áp dụng")

        self.gridLayout_payment.addWidget(self.label_totaltemp, 0, 0, 1, 1)
        self.gridLayout_payment.addWidget(self.lineEdit_totaltemp, 0, 1, 1, 2)
        self.gridLayout_payment.addWidget(self.label_voucher, 1, 0, 1, 1)
        self.gridLayout_payment.addWidget(self.lineEdit_voucher, 1, 1, 1, 1)
        self.gridLayout_payment.addWidget(self.pushButton_apply, 1, 2, 1, 1)
        self.gridLayout_payment.addWidget(self.label_total, 3, 0, 1, 1)
        self.gridLayout_payment.addWidget(self.lineEdit_total, 3, 1, 1, 2)


        self.verticalLayout_paymentsection.addLayout(self.gridLayout_payment)
        self.verticalLayout.addWidget(self.frame_paymentsection)

        "finally"
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
        with open(f"{self.current_path}/../Resources/style.css", "r") as f:
            self.setStyleSheet(f.read())

    def signalandslot(self):
        self.pushButton_payment.clicked.connect(self.xuly_thanhtoan)
        self.pushButton_return.clicked.connect(self.xuly_quaylai)
        self.pushButton_apply.clicked.connect(self.xuly_apdungvoucher)
    def xuly_thanhtoan(self):
        voucher = self.lineEdit_voucher.text()
        self.xuly_apdungvoucher() # TH người dùng xoá voucher và không muốn dùng nữa
        "Thực hiện lưu mã voucher đã sử dụng "

        "Đến view thanh toán"

    def xuly_quaylai(self):
        pass
    def xuly_apdungvoucher(self):
        # Xoá label cảnh báo nếu đã tồn tại trước đó
        if hasattr(self, "label_warning") and self.label_warning is not None:
            self.label_warning.deleteLater()  # Xóa QLabel
            self.label_warning = None  # Đặt lại thành NoneX
        voucher  = self.lineEdit_voucher.text()
        # nếu người dùng không muốn dùng mã tặng món nữa
        if voucher.strip() == "":
            if self.is_used:
                freeitem = self.listorders.findFreeItem()
                if freeitem:
                    freeitem.isdeleted = 1
                    self.updateScrollArea()
        totaltemp =self.lineEdit_totaltemp.text()
        self.lineEdit_total.setText(totaltemp)
        self.label_warning = QtWidgets.QLabel(self.frame_paymentsection)
        self.label_warning.setStyleSheet("""
                                        color: #BD1906;
                                        font-weight: 400;
                                        font-size: 10px;
                                    """)
        self.label_warning.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        response = self.database.responseVoucher(voucher, float(totaltemp))
        if response == None: # nếu nguười dùng không muốn dùng mã giảm giá nữa
            self.lineEdit_total.setText(totaltemp)
        elif type(response) == str:
            "CẢNH BÁO"
            self.gridLayout_payment.addWidget(self.label_warning, 2, 1, 1, 3)
            self.label_warning.setText(response)
        elif type(response) == float or type(response) == int:
            "GIẢM GIÁ"
            if self.is_used == False:
                self.lineEdit_total.setText(f"{response}")
            else:
                self.gridLayout_payment.addWidget(self.label_warning, 2, 1, 1, 3)
                self.label_warning.setText("Vui lòng chỉ được sử dụng duy nhất 1 mã voucher.")

        else:
            "TẶNG MÓN"
            if not self.is_used: # nếu chưa sử dụng
                p = OrderItem(response[0], response[1], response[2], "", response[3], response[6], 0, 1)
                self.listorders.addItem(p)
                self.listorders.deleteDuplicateOrder()
                self.updateScrollArea()


class Productbox(QtWidgets.QWidget):
    deleteChanged = QtCore.pyqtSignal()
    quantityChanged = QtCore.pyqtSignal()
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.products = product
        self.current_path = os.getcwd()
        self.setupUI()
        self.signalandslot()
    def setupUI(self):
        """general"""
        self.frame_product = QtWidgets.QFrame(self)
        self.frame_product.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Fixed
        ))
        self.frame_product.setMinimumSize(QtCore.QSize(0, 97))
        self.frame_product.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_product)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(5)
        """widgets"""
        self.setupImage() # parent = productbox
        self.setupContent() # parent = productbox
        self.setupPriceBox() #parent = productbox
        """finally"""
    def setupImage(self):
        """general"""
        self.frame_productimage = QtWidgets.QFrame(parent=self.frame_product)
        self.frame_productimage.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 90, 0
        ))
        self.frame_productimage.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_productimage.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.verticalLayout_img = QtWidgets.QVBoxLayout(self.frame_productimage)
        self.verticalLayout_img.setContentsMargins(0, 0, 0, 0)
        """image"""
        self.label_image = QtWidgets.QLabel(parent=self.frame_productimage)
        self.label_image.setPixmap(QtGui.QPixmap(f"{self.current_path}/{self.products.imageurl}"))
        self.label_image.setScaledContents(True)
        self.verticalLayout_img.addWidget(self.label_image)
        """finally"""
        self.horizontalLayout.addWidget(self.frame_productimage)

    def setupContent(self):
        """general"""
        self.frame_productcontent = QtWidgets.QFrame(parent=self.frame_product)
        self.frame_productcontent.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 186, 0
        ))
        self.frame_productcontent.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_productcontent.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.verticalLayout_contents2 = QtWidgets.QVBoxLayout(self.frame_productcontent)
        self.verticalLayout_contents2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_contents2.setSpacing(2)
        """label name"""
        self.label_name = QtWidgets.QLabel(parent=self.frame_productcontent)
        self.label_name.setObjectName("label_name")
        self.label_name.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 2
        ))
        self.label_name.setText(f"{self.products.name}")

        "text edit topping"
        self.textEdit_topping = QtWidgets.QTextEdit(parent=self.frame_productcontent)
        self.textEdit_topping.setObjectName("textEdit_topping")
        self.textEdit_topping.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 4
        ))
        self.textEdit_topping.setReadOnly(True)
        self.textEdit_topping.setText(
            f"{self.products.topping}")
        self.textEdit_topping.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        "quantity"
        # general
        self.frame_quantitybox = QtWidgets.QFrame(parent=self.frame_productcontent)
        self.frame_quantitybox.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 2
        ))
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

        self.label_quantity = QtWidgets.QLabel(self.frame_quantitybox)
        self.label_quantity.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_quantity.setText(f"{self.products.quantity}")
        # finally
        self.horizontalLayout_quantity.addWidget(self.pushbutton_minus)
        self.horizontalLayout_quantity.addWidget(self.label_quantity)
        self.horizontalLayout_quantity.addWidget(self.pushbutton_plus)
        """finally"""
        self.verticalLayout_contents2.addWidget(self.label_name)
        self.verticalLayout_contents2.addWidget(self.textEdit_topping)
        self.verticalLayout_contents2.addWidget(self.frame_quantitybox)

        self.horizontalLayout.addWidget(self.frame_productcontent)
    def setupPriceBox(self):
        """general"""
        self.frame_pricebox = QtWidgets.QFrame(parent=self.frame_product)
        self.frame_pricebox.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 132, 0
        ))
        self.gridLayout_price = QtWidgets.QGridLayout(self.frame_pricebox)
        self.gridLayout_price.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_price.setSpacing(0)
        """button delete"""
        self.pushButton_delete = QtWidgets.QPushButton(self.frame_pricebox)
        self.pushButton_delete.setFlat(True)
        self.pushButton_delete.setIcon(QtGui.QIcon(f"{self.current_path}/../resources/images/ic_delete.png"))
        """label price"""
        self.label_price = QtWidgets.QLabel(self.frame_pricebox)
        self.label_price.setObjectName("label_price")
        self.label_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_price.setText(f"{self.products.price*self.products.quantity}")
        if self.label_price.text() == "0":
            self.label_name.setText(f"{self.products.name} <span style='color: #BD1906;'>(Quà tặng)</span>")

        """finally"""
        self.gridLayout_price.addWidget(self.pushButton_delete, 0, 2, 2, 1)
        self.gridLayout_price.addWidget(self.label_price, 2, 0, 1, 3)

        self.horizontalLayout.addWidget(self.frame_pricebox)

    def signalandslot(self):
        self.pushbutton_minus.clicked.connect(self.minus)
        self.pushbutton_plus.clicked.connect(self.plus)
        self.pushButton_delete.clicked.connect(self.delete)
    def minus(self):
        if self.label_price.text() != "0":
            if self.products.quantity > 1:
                self.products.quantity -= 1
                self.quantityChanged.emit()

    def plus(self):
        if self.label_price.text() != "0":
            self.products.quantity += 1
            self.quantityChanged.emit()
    def delete(self):
        self.products.isdeleted = 1
        self.deleteChanged.emit()

    def createSizePolicy(self, horizontal, vertical, hstretch=0, vstretch=0):
        sizePolicy = QtWidgets.QSizePolicy(horizontal, vertical)
        sizePolicy.setHorizontalStretch(hstretch)
        sizePolicy.setVerticalStretch(vstretch)
        return sizePolicy

class ProductboxFree(QtWidgets.QWidget):
    deleteChanged = QtCore.pyqtSignal()
    # quantityChanged = QtCore.pyqtSignal()
    def __init__(self, product, parent=None):
        super().__init__(parent)  # Fix: Gọi super() đầu tiên
        self.products = product
        self.current_path = os.getcwd()
        self.setupUI()
        self.signalandslot()
    def setupUI(self):
        """general"""
        self.frame_product = QtWidgets.QFrame(self)
        self.frame_product.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Fixed
        ))
        self.frame_product.setMinimumSize(QtCore.QSize(0, 97))
        self.frame_product.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        # self.frame_product.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_product)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(5)
        """widgets"""
        self.setupImage() # parent = productbox
        self.setupContent() # parent = productbox
        self.setupPriceBox() #parent = productbox
        """finally"""
    def setupImage(self):
        """general"""
        self.frame_productimage = QtWidgets.QFrame(parent=self.frame_product)
        self.frame_productimage.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 90, 0
        ))
        self.frame_productimage.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_productimage.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.verticalLayout_img = QtWidgets.QVBoxLayout(self.frame_productimage)
        self.verticalLayout_img.setContentsMargins(0, 0, 0, 0)
        """image"""
        self.label_image = QtWidgets.QLabel(parent=self.frame_productimage)
        self.label_image.setPixmap(QtGui.QPixmap(f"{self.current_path}/{self.products.imageurl}"))
        self.label_image.setScaledContents(True)
        self.verticalLayout_img.addWidget(self.label_image)
        """finally"""
        self.horizontalLayout.addWidget(self.frame_productimage)

    def setupContent(self):
        """general"""
        self.frame_productcontent = QtWidgets.QFrame(parent=self.frame_product)
        self.frame_productcontent.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 186, 0
        ))
        self.frame_productcontent.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_productcontent.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.verticalLayout_contents2 = QtWidgets.QVBoxLayout(self.frame_productcontent)
        self.verticalLayout_contents2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_contents2.setSpacing(2)
        """label name"""
        self.label_name = QtWidgets.QLabel(parent=self.frame_productcontent)
        self.label_name.setObjectName("label_name")
        self.label_name.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 2
        ))
        self.label_name.setText(f"{self.products.name}")

        "text edit topping"
        self.textEdit_topping = QtWidgets.QTextEdit(parent=self.frame_productcontent)
        self.textEdit_topping.setObjectName("textEdit_topping")
        self.textEdit_topping.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 4
        ))
        self.textEdit_topping.setReadOnly(True)
        self.textEdit_topping.setText(
            f"{self.products.topping}")
        self.textEdit_topping.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        "quantity"
        # general
        self.frame_quantitybox = QtWidgets.QFrame(parent=self.frame_productcontent)
        self.frame_quantitybox.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 2
        ))
        self.horizontalLayout_quantity = QtWidgets.QHBoxLayout(self.frame_quantitybox)
        self.horizontalLayout_quantity.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_quantity.setSpacing(0)

        # pushbutton
        self.pushbutton_minus = QtWidgets.QPushButton(parent=self.frame_quantitybox)
        self.pushbutton_plus = QtWidgets.QPushButton(parent=self.frame_quantitybox)
        self.pushbutton_plus.setFlat(True)
        self.pushbutton_minus.setFlat(True)
        self.pushbutton_minus.setIcon(QtGui.QIcon(f"{self.current_path}/../images/ic_minus.png"))
        self.pushbutton_plus.setIcon(QtGui.QIcon(f"{self.current_path}/../images/ic_plus.png"))

        self.label_quantity = QtWidgets.QLabel(self.frame_quantitybox)
        self.label_quantity.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_quantity.setText(f"{self.products.quantity}")
        # finally
        self.horizontalLayout_quantity.addWidget(self.pushbutton_minus)
        self.horizontalLayout_quantity.addWidget(self.label_quantity)
        self.horizontalLayout_quantity.addWidget(self.pushbutton_plus)
        """finally"""
        self.verticalLayout_contents2.addWidget(self.label_name)
        self.verticalLayout_contents2.addWidget(self.textEdit_topping)
        self.verticalLayout_contents2.addWidget(self.frame_quantitybox)

        self.horizontalLayout.addWidget(self.frame_productcontent)
    def setupPriceBox(self):
        """general"""
        self.frame_pricebox = QtWidgets.QFrame(parent=self.frame_product)
        self.frame_pricebox.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 132, 0
        ))
        self.gridLayout_price = QtWidgets.QGridLayout(self.frame_pricebox)
        self.gridLayout_price.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_price.setSpacing(0)
        """button delete"""
        self.pushButton_delete = QtWidgets.QPushButton(self.frame_pricebox)
        self.pushButton_delete.setFlat(True)
        self.pushButton_delete.setIcon(QtGui.QIcon(f"{self.current_path}/../images/ic_delete.png"))
        """label price"""
        self.label_price = QtWidgets.QLabel(self.frame_pricebox)
        self.label_price.setObjectName("label_price")
        self.label_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_price.setText(f"<span style = 'color: #C0BBBB;'><s>{self.products.price*self.products.quantity}</s></span>Free")

        self.label_name.setText(f"{self.products.name} <span style='color: #BD1906;'>(Quà tặng)</span>")

        """finally"""
        self.gridLayout_price.addWidget(self.pushButton_delete, 0, 2, 2, 1)
        self.gridLayout_price.addWidget(self.label_price, 2, 0, 1, 3)

        self.horizontalLayout.addWidget(self.frame_pricebox)

    def signalandslot(self):
        # self.pushbutton_minus.clicked.connect(self.minus)
        # self.pushbutton_plus.clicked.connect(self.plus)
        self.pushButton_delete.clicked.connect(self.delete)

    def delete(self):
        self.products.isdeleted = 1
        self.deleteChanged.emit()

    def createSizePolicy(self, horizontal, vertical, hstretch=0, vstretch=0):
        sizePolicy = QtWidgets.QSizePolicy(horizontal, vertical)
        sizePolicy.setHorizontalStretch(hstretch)
        sizePolicy.setVerticalStretch(vstretch)
        return sizePolicy





# chạy app
app = QtWidgets.QApplication(sys.argv)
window = Ui_MainWindow()
window.show()
app.exec()