from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt



class OrderWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        self.scrollArea = QtWidgets.QScrollArea()
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
        self.scrollArea.setMinimumHeight(300)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.verticalLayout_contents = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_contents.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.verticalLayout_contents.setSpacing(5)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.adjustSize()


        self.frame_paymentsection = QtWidgets.QFrame()
        self.frame_paymentsection.setObjectName("frame_paymentsection")
        self.frame_paymentsection.setSizePolicy(self.createSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred, 0, 5))
        self.frame_paymentsection.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_paymentsection.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.verticalLayout_paymentsection = QtWidgets.QVBoxLayout(self.frame_paymentsection)
        self.verticalLayout_paymentsection.setContentsMargins(0, 0, 0, 0)
        self.label_payment = QtWidgets.QLabel(self.frame_paymentsection)
        self.verticalLayout_paymentsection.addWidget(self.label_payment)
        self.label_payment.setObjectName("label_payment2")
        self.label_payment.setText("Thanh toán")
        self.gridLayout_payment = QtWidgets.QGridLayout()
        self.gridLayout_payment.setHorizontalSpacing(2)
        self.gridLayout_payment.setVerticalSpacing(4)
        self.label_voucher = QtWidgets.QLabel(self.frame_paymentsection)
        self.label_warning = QtWidgets.QLabel(self.frame_paymentsection)
        self.lineEdit_voucher = QtWidgets.QLineEdit(self.frame_paymentsection)
        self.label_totaltemp = QtWidgets.QLabel(self.frame_paymentsection)
        self.label_total = QtWidgets.QLabel(self.frame_paymentsection)
        self.lineEdit_totaltemp = QtWidgets.QLineEdit(self.frame_paymentsection)
        self.lineEdit_total = QtWidgets.QLineEdit(self.frame_paymentsection)
        self.pushButton_apply = QtWidgets.QPushButton(self.frame_paymentsection)
        self.lineEdit_voucher.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.label_warning.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
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

        self.pushButton_payment = QtWidgets.QPushButton()
        self.pushButton_payment.setObjectName("pushButton_payment")
        self.pushButton_payment.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred, 0, 1
        ))
        self.pushButton_payment.setText("Thanh toán")

        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addWidget(self.frame_paymentsection)
        self.mainLayout.addWidget(self.pushButton_payment)
        self.setStyleSheetAll()


    def createSizePolicy(self, horizontal, vertical, hstretch=0, vstretch=0):
        sizePolicy = QtWidgets.QSizePolicy(horizontal, vertical)
        sizePolicy.setHorizontalStretch(hstretch)
        sizePolicy.setVerticalStretch(vstretch)
        return sizePolicy
    def setStyleSheetAll(self):
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
        self.pushButton_payment.setStyleSheet("""
                border-radius: 6px;
                background: #bd1906;
                color: #ffffff;                
                font-weight: 700;""")
        self.pushButton_apply.setStyleSheet("""
                background: #8a8a8a;
                color: #ffffff;""")
        self.label_payment.setStyleSheet("""
                font-weight: 700;""")

class OrderItemBox(QtWidgets.QFrame):
    def __init__(self, OrderItem):
        super().__init__()
        self.orderItem = OrderItem
        self.setupUI()
        self.setStyleSheetAll()

    def setupUI(self):
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setMinimumSize(QtCore.QSize(0, 110))

        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setSpacing(5)

        self.frameOrderImage = QtWidgets.QFrame()
        self.frameOrderImage.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 90, 0
        ))
        self.frameOrderImage.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameOrderImage.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.verticalLayout_img = QtWidgets.QVBoxLayout(self.frameOrderImage)
        self.verticalLayout_img.setContentsMargins(0, 0, 0, 0)
        self.label_image = QtWidgets.QLabel(parent=self.frameOrderImage)
        self.label_image.setPixmap(QtGui.QPixmap(f"kiosk_app/{self.orderItem.foodItem.image_url}"))
        self.label_image.setScaledContents(True)
        self.verticalLayout_img.addWidget(self.label_image)

        self.frameOrderContent = QtWidgets.QFrame()
        self.frameOrderContent.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 200, 0
        ))
        self.frameOrderContent.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameOrderContent.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.verticalLayout_contents = QtWidgets.QVBoxLayout(self.frameOrderContent)
        self.verticalLayout_contents.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_contents.setSpacing(2)
        self.label_name = QtWidgets.QLabel(parent=self.frameOrderContent)
        self.label_name.setObjectName("label_name")
        self.label_name.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 2
        ))
        self.label_name.setText(f"<b>{self.orderItem.foodItem.name}</b>")

        self.textEdit_topping = QtWidgets.QTextEdit(parent=self.frameOrderContent)
        self.textEdit_topping.setObjectName("textEdit_topping")
        self.textEdit_topping.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 4
        ))
        self.textEdit_topping.setReadOnly(True)
        self.textEdit_topping.setText(str(', '.join([variant.value for variant in self.orderItem.variantList])) +'\n'+str(', '.join([topping.name for topping in self.orderItem.toppingList]))+ '\n' + str(self.orderItem.note))
        self.textEdit_topping.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.frameQuantityOrder = QtWidgets.QFrame(parent=self.frameOrderContent)
        self.frameQuantityOrder.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 0, 2
        ))
        self.horizontalLayout_quantity = QtWidgets.QHBoxLayout(self.frameQuantityOrder)
        self.horizontalLayout_quantity.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_quantity.setSpacing(0)
        self.pushbutton_minus = QtWidgets.QPushButton(parent=self.frameQuantityOrder)
        self.pushbutton_plus = QtWidgets.QPushButton(parent=self.frameQuantityOrder)
        self.pushbutton_plus.setFlat(True)
        self.pushbutton_minus.setFlat(True)
        self.pushbutton_minus.setIcon(QtGui.QIcon(f"kiosk_app/resources/images/ic_minus.png"))
        self.pushbutton_plus.setIcon(QtGui.QIcon(f"kiosk_app/resources/images/ic_plus.png"))
        self.label_quantity = QtWidgets.QLabel(self.frameQuantityOrder)
        self.label_quantity.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_quantity.setText(f"{self.orderItem.quantity}")
        self.horizontalLayout_quantity.addWidget(self.pushbutton_minus)
        self.horizontalLayout_quantity.addWidget(self.label_quantity)
        self.horizontalLayout_quantity.addWidget(self.pushbutton_plus)

        self.verticalLayout_contents.addWidget(self.label_name)
        self.verticalLayout_contents.addWidget(self.textEdit_topping)
        self.verticalLayout_contents.addWidget(self.frameQuantityOrder)

        self.framePriceOrder = QtWidgets.QFrame()
        self.framePriceOrder.setSizePolicy(self.createSizePolicy(
            QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored, 100, 0
        ))
        self.gridLayout_price = QtWidgets.QGridLayout(self.framePriceOrder)
        self.gridLayout_price.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_price.setSpacing(0)
        self.pushButton_delete = QtWidgets.QPushButton(self.framePriceOrder)
        self.pushButton_delete.setFlat(True)
        self.pushButton_delete.setIcon(QtGui.QIcon("kiosk_app/resources/images/ic_delete.png"))
        self.label_price = QtWidgets.QLabel(self.framePriceOrder)
        self.label_price.setObjectName("label_price")
        self.label_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_price.setText(f"<span style = 'color: #C0BBBB; font-size: 11px;'><s>{self.orderItem.foodItem.price:,}</s></span>{self.orderItem.foodItem.discount:,}")
        self.gridLayout_price.addWidget(self.pushButton_delete, 0, 2, 2, 1)
        self.gridLayout_price.addWidget(self.label_price, 2, 0, 1, 3)

        self.mainLayout.addWidget(self.frameOrderImage)
        self.mainLayout.addWidget(self.frameOrderContent)
        self.mainLayout.addWidget(self.framePriceOrder)

    def createSizePolicy(self, horizontal, vertical, hstretch=0, vstretch=0):
        sizePolicy = QtWidgets.QSizePolicy(horizontal, vertical)
        sizePolicy.setHorizontalStretch(hstretch)
        sizePolicy.setVerticalStretch(vstretch)
        return sizePolicy

    def setStyleSheetAll(self):
        self.textEdit_topping.setStyleSheet("""
        border: None;
        color: #8a8a8a""")
        self.label_price.setStyleSheet("""
        font-size: 13px;
        color: #bd1906;
        font-weight: 700;""")




