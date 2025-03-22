from typing import List, Dict
from PyQt6 import QtCore, QtGui, QtWidgets
from dotenv import load_dotenv

class GeneralView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.env_values = load_dotenv(dotenv_path='.env')

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1280, 720)
        # widget trung tâm
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)

        # layout chính (dọc)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0) # các khoảng cách xung quanh
        self.verticalLayout.setSpacing(0) # khoảng cách giữa 2 cái

        #---frame header
        self.frameHeader = QtWidgets.QFrame(self.centralwidget)
        # self.frameHeader.setMinimumSize(1280, 60)
        self.layoutHeader = QtWidgets.QHBoxLayout(self.frameHeader)
        self.verticalLayout.addWidget(self.frameHeader)

        # 1. button menu
        self.pushButtonMenu = QtWidgets.QPushButton()
        self.pushButtonMenu.setIcon(QtGui.QIcon('admin_app/resources/images/ic_home.png'))
        self.pushButtonMenu.setIconSize(QtCore.QSize(32, 32))
        self.pushButtonMenu.setText("Trang chủ")
        self.pushButtonMenu.setFlat(True)
        # 2. Label app quản lý
        self.labelApp = QtWidgets.QLabel()
        self.labelApp.setText("<b>App Quản Lý Kiosk</b>")
        self.labelApp.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # 3. Label email
        self.labelEmail = QtWidgets.QLabel()
        self.labelEmail.setObjectName("labelEmail")
        self.labelEmail.setText("")
        self.labelEmail.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight| QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.layoutHeader.addWidget(self.pushButtonMenu)
        self.layoutHeader.addWidget(self.labelApp)
        self.layoutHeader.addWidget(self.labelEmail)

        #---Bottom Frame
        self.frameBottom = QtWidgets.QFrame(self.centralwidget)
        # self.frameBottom.setMinimumSize(1280, 660)
        self.gLayout = QtWidgets.QGridLayout(self.frameBottom)
        self.gLayout.setContentsMargins(0, 0, 0, 0)
        self.gLayout.setVerticalSpacing(0)
        self.gLayout.setHorizontalSpacing(1)
        self.verticalLayout.addWidget(self.frameBottom)

        # 1. Navigation
        self.frameNavigation = QtWidgets.QFrame(self.frameBottom)
        self.frameNavigation.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameNavigation.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.layoutNavigation = QtWidgets.QVBoxLayout(self.frameNavigation)
        self.layoutNavigation.setContentsMargins(0, 0, 0,0 )
        self.layoutNavigation.setSpacing(0)
        #1.1 Tổng doanh thu
        self.pushButtonTotalRevenue = QtWidgets.QPushButton()
        self.pushButtonTotalRevenue.setText("Tổng doanh thu")
        self.pushButtonTotalRevenue.setMinimumHeight(48)
        #1.2. Tổng lợi nhuận
        self.pushButtonTotalProfit = QtWidgets.QPushButton()
        self.pushButtonTotalProfit.setText("Tổng lợi nhuận")
        self.pushButtonTotalProfit.setMinimumHeight(48)
        #1.3. Chuơng trình khuyến mãi
        self.pushButtonCTKM = QtWidgets.QPushButton()
        self.pushButtonCTKM.setText("Chương trình khuyến mãi")
        self.pushButtonCTKM.setMinimumHeight(48)
        #1.4. Mặt hàng bán chạy
        self.pushButtonMHBC = QtWidgets.QPushButton()
        self.pushButtonMHBC.setText("Mặt hàng bán chạy")
        self.pushButtonMHBC.setMinimumHeight(48)
        #1.5. Phương thức thanh toán
        self.pushButtonPaymentMethod = QtWidgets.QPushButton()
        self.pushButtonPaymentMethod.setText("Phương thức thanh toán")
        self.pushButtonPaymentMethod.setMinimumHeight(48)
        #1.6. Hoá đơn
        self.pushButtonInvoice = QtWidgets.QPushButton()
        self.pushButtonInvoice.setText("Hoá đơn")
        self.pushButtonInvoice.setMinimumHeight(48)
        ###
        self.layoutNavigation.addWidget(self.pushButtonTotalRevenue)
        self.layoutNavigation.addWidget(self.pushButtonTotalProfit)
        self.layoutNavigation.addWidget(self.pushButtonCTKM)
        self.layoutNavigation.addWidget(self.pushButtonMHBC)
        self.layoutNavigation.addWidget(self.pushButtonPaymentMethod)
        self.layoutNavigation.addWidget(self.pushButtonInvoice)
        self.layoutNavigation.addStretch(408)
        self.gLayout.addWidget(self.frameNavigation, 0, 0, 2, 1)
        # 2. Thanh chức năng
        self.frameFunc = QtWidgets.QFrame(self.frameBottom)

        self.hLayoutFunc = QtWidgets.QHBoxLayout(self.frameFunc)
        self.hLayoutFunc.setContentsMargins(10, 12, 10, 12)
        self.hLayoutFunc.setSpacing(10)
        self.gLayout.addWidget(self.frameFunc, 0, 1, 1, 1)
        self.labelName = QtWidgets.QLabel()

        #2.0. LineEdit ngày
        self.lineEditDate = QtWidgets.QLineEdit()
        self.hLayoutFunc.addWidget(self.lineEditDate, 190)
        self.lineEditDate.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.lineEditDate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        #2.1. Thanh tìm kiếm
        self.hlayoutSearch = QtWidgets.QHBoxLayout(self.frameFunc)
        self.hlayoutSearch.setContentsMargins(0, 0, 0, 0)
        self.hlayoutSearch.setSpacing(0)
        self.pushButtonSearch = QtWidgets.QPushButton()
        self.pushButtonSearch.setIcon(QtGui.QIcon('admin_app/resources/images/ic_search.png'))
        self.pushButtonSearch.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.lineEditSearch = QtWidgets.QLineEdit()
        self.lineEditSearch.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.lineEditSearch.setPlaceholderText('Tìm kiếm món')
        self.lineEditSearch.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.hlayoutSearch.addWidget(self.lineEditSearch, 150)
        self.hlayoutSearch.addWidget(self.pushButtonSearch, 40)
        #2.2. Combo Box
        self.comboBox = QtWidgets.QComboBox(parent=self.frameFunc)
        self.comboBox.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        #2.3. Button xuất file
        self.pushButtonExport = QtWidgets.QPushButton()
        self.pushButtonSearch.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.pushButtonExport.setIcon(QtGui.QIcon('admin_app/resources/images/icon_dowload.png'))
        self.pushButtonExport.setText(f" Xuất file")
        self.pushButtonExport.setMinimumSize(107, 36)
        ###
        self.hLayoutFunc.addLayout(self.hlayoutSearch, 190)
        self.hLayoutFunc.addStretch(350)
        self.hLayoutFunc.addWidget(self.comboBox, 190)
        self.hLayoutFunc.addWidget(self.pushButtonExport, 107)

        # 3. Content
        self.frameContent = QtWidgets.QFrame(self.frameBottom)
        # self.frameContent.setMinimumSize(1080, 600)
        self.gLayout.addWidget(self.frameContent, 1, 1, 1, 1 )

        # thiết lập các ngôn ngữ và kết nối các slot
        self.gLayout.setRowStretch(0, 1)
        self.gLayout.setRowStretch(1, 11)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setStyleSheetGeneral()
    def setStyleSheetGeneral(self):
        self.setStyleSheet('background-color: rgb(255, 255, 255); font-family: Montserrat; font-size: 14px;')
        self.frameFunc.setStyleSheet("border: 1px solid #EEEEEE; border-radius: 6px")
        self.frameBottom.setStyleSheet("border: 1px solid #EEEEEE; border-radius: 6px")
        self.pushButtonMenu.setStyleSheet("font-weight: bold; text-align: left")
        self.lineEditSearch.setStyleSheet("border: 1px solid #000000;color: #FF2A58;")
        self.pushButtonSearch.setStyleSheet("background-color: #bd1906; ")
        self.comboBox.setStyleSheet("border: 1px solid #000000; color:#FF2A58;")
        self.lineEditDate.setStyleSheet("border: 1px solid #000000;")
        self.pushButtonExport.setStyleSheet("background-color: #bd1906; color: #eeeeee; border-radius: 10px; font-weight: bold;")
        self.frameNavigation.setStyleSheet('font-weight: bold; border: 1px solid #EEEEEE; border-radius: 6px ')

        self.pushButtonTotalRevenue.setStyleSheet("text-align: left; padding-left: 12px; border: None")
        self.pushButtonTotalProfit.setStyleSheet("text-align: left; padding-left: 12px; border: None ")
        self.pushButtonCTKM.setStyleSheet("text-align: left; padding-left: 12px; border: None")
        self.pushButtonMHBC.setStyleSheet("text-align: left; padding-left: 12px; border: None")
        self.pushButtonPaymentMethod.setStyleSheet("text-align: left; padding-left: 12px; border: None")
        self.pushButtonInvoice.setStyleSheet("text-align: left; padding-left: 12px; border: None")


    def retranslateUi(self, MainWindow):
        # thiết lập văn bản cho các widget
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "App quản lý Kiosk"))

class CategoryComboBox(QtWidgets.QComboBox):
    def __init__(self, categories: List[Dict] = [], parent=None):
        super().__init__(parent)
        self.categories = categories
        self.categories.insert(0, {"ID": None, "Name": "Tất cả nhóm món"})
        self.addItems([category["Name"] for category in self.categories])
        self.selected_categories_id = 0
        self.currentIndexChanged.connect(self.selectCategory)

    def setListCategory(self, categories):
        for category in categories:
            self.categories.append(category)
            self.addItem(category["Name"])

    def selectCategory(self):
        selected_category = self.categories[self.currentIndex()]
        self.selected_categories_id = selected_category["ID"]