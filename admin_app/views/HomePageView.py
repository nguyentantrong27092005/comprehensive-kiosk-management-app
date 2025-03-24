from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from dotenv import load_dotenv


class HomePageView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.env_values = load_dotenv(dotenv_path='.env')

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setSpacing(0)

        # 1---frame header
        self.frameHeader = QtWidgets.QFrame(self.centralwidget)
        self.layoutHeader = QtWidgets.QHBoxLayout(self.frameHeader)
        self.verticalLayout.addWidget(self.frameHeader)

        # 1. button menu
        self.pushButtonMenu = QtWidgets.QPushButton()
        self.pushButtonMenu.setIcon(QtGui.QIcon('admin_app/resources/images/ic_menu.png'))
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
        self.labelEmail.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.layoutHeader.addWidget(self.pushButtonMenu)
        self.layoutHeader.addWidget(self.labelApp)
        self.layoutHeader.addWidget(self.labelEmail)

        self.verticalLayout.addWidget(self.frameHeader)

        # 2---Bottom Frame
        self.frameBottom = QtWidgets.QFrame(self.centralwidget)
        self.gLayout = QtWidgets.QGridLayout(self.frameBottom)
        self.gLayout.setContentsMargins(0, 0, 0, 10)
        self.gLayout.setSpacing(0)

        self.verticalLayout.addWidget(self.frameBottom)

        # 1. Navigation
        self.frameNavigation = QtWidgets.QFrame(self.frameBottom)
        self.frameNavigation.setObjectName('frameNavigation')
        self.frameNavigation.setMaximumWidth(180)
        self.frameNavigation.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameNavigation.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.layoutNavig = QtWidgets.QGridLayout(self.frameNavigation)
        self.layoutNavig.setContentsMargins(10, 30, 15, 40)
        self.layoutNavig.setHorizontalSpacing(8)
        self.layoutNavig.setVerticalSpacing(30)

        # 1.1.button
        self.pushButtonBaoCao = QtWidgets.QPushButton()
        self.pushButtonThucDon = QtWidgets.QPushButton()
        self.pushButtonChuongTrinh = QtWidgets.QPushButton()
        self.pushButtonThanhToan = QtWidgets.QPushButton()
        # self.pushButtonAI = QtWidgets.QPushButton()

        self.pushButtonBaoCao.setIcon(QtGui.QIcon('admin_app/resources/images/icon_report.png'))
        self.pushButtonThucDon.setIcon(QtGui.QIcon('admin_app/resources/images/icon_fastfood.png'))
        self.pushButtonChuongTrinh.setIcon(QtGui.QIcon('admin_app/resources/images/icon_promosale.png'))
        self.pushButtonThanhToan.setIcon(QtGui.QIcon('admin_app/resources/images/icon_payment.png'))
        self.pushButtonBaoCao.setIconSize(QtCore.QSize(32, 32))
        self.pushButtonThucDon.setIconSize(QtCore.QSize(32, 32))
        self.pushButtonChuongTrinh.setIconSize(QtCore.QSize(32, 32))
        self.pushButtonThanhToan.setIconSize(QtCore.QSize(32, 32))

        self.pushButtonBaoCao.setMinimumSize(50, 50)
        self.pushButtonThucDon.setMinimumSize(50, 50)
        self.pushButtonChuongTrinh.setMinimumSize(50, 50)
        self.pushButtonThanhToan.setMinimumSize(50, 50)

        self.layoutNavig.addWidget(self.pushButtonBaoCao, 0, 0)
        self.layoutNavig.addWidget(self.pushButtonThucDon, 1, 0)
        self.layoutNavig.addWidget(self.pushButtonChuongTrinh, 2, 0)
        self.layoutNavig.addWidget(self.pushButtonThanhToan, 3, 0)
        # 1.2.label
        self.labelBaoCao = QtWidgets.QLabel("<b>Báo cáo</b>")
        self.labelThucDon = QtWidgets.QLabel("<b>Thực đơn</b>")
        self.labelChuongTrinh = QtWidgets.QLabel("<b>Chương Trình</b>")
        self.labelThanhToan = QtWidgets.QLabel("<b>Thanh Toán</b>")
        # self.labelAI = QtWidgets.QLabel("<b>Trợ lý AI</b>")

        self.layoutNavig.addWidget(self.labelBaoCao, 0, 1)
        self.layoutNavig.addWidget(self.labelThucDon, 1, 1)
        self.layoutNavig.addWidget(self.labelChuongTrinh, 2, 1)
        self.layoutNavig.addWidget(self.labelThanhToan, 3, 1)
        # self.layoutNavig.addWidget(self.labelAI, 4, 1)
        spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                       QtWidgets.QSizePolicy.Policy.Expanding)
        self.layoutNavig.addItem(spacer, 5, 0)

        #1.3. ScrollArea
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setObjectName('scrollArea')
        self.scrollAreaLayout = QtWidgets.QVBoxLayout()
        self.scrollArea.setMinimumHeight(680)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.scrollAreaLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidget)
        self.scrollAreaLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollAreaLayout.addStretch()
        self.scrollAreaWidget.adjustSize()

        #1.3.1. Thanh trên cùng
        self.headerFrame = QtWidgets.QFrame()
        self.headerFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.headerFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.headerFrame.setMinimumHeight(124)

        self.headerLayout = QtWidgets.QGridLayout(self.headerFrame)
        self.scrollAreaLayout.addWidget(self.headerFrame)

        self.revenueLabel = QtWidgets.QLabel(self.headerFrame)
        self.revenueLabel.setText("Doanh thu")
        self.totalRevenueLabel = QtWidgets.QLabel(self.headerFrame)
        self.compareLastDayLabel = QtWidgets.QLabel(self.headerFrame)
        self.gainRevenueButton = QtWidgets.QPushButton(self.headerFrame)
        self.selectedDateLineEdit = QtWidgets.QLineEdit(self.headerFrame)

        self.gainRevenueButton.setMinimumSize(QtCore.QSize(119, 35))
        self.gainRevenueButton.setIconSize(QtCore.QSize(24, 24))
        self.gainRevenueButton.setIcon(QtGui.QIcon(f"admin_app/resources/images/icon_gain.png"))
        self.selectedDateLineEdit.setFixedSize(QtCore.QSize(162, 29))
        self.selectedDateLineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        spacer = QtWidgets.QSpacerItem(550, 1, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)

        self.headerLayout.addWidget(self.revenueLabel, 0, 0, 1, 1)
        self.headerLayout.addWidget(self.totalRevenueLabel, 1, 0, 1, 1)
        self.headerLayout.addWidget(self.gainRevenueButton, 1, 2, 1, 1)
        self.headerLayout.addWidget(self.compareLastDayLabel, 1, 3, 1, 1)
        # self.headerLayout.setRowStretch(0, 80)
        self.headerLayout.addWidget(self.selectedDateLineEdit, 0, 4, 1, 1)
        self.headerLayout.addItem(spacer, 0, 3)

        #1.3.2. 3 hộp thông tin
        self.threeBoxLayout = QtWidgets.QHBoxLayout()
        self.threeBoxLayout.setContentsMargins(50, 0, 50, 0)
        self.scrollAreaLayout.addLayout(self.threeBoxLayout)

        # self.threeBoxLayout.setSpacing(100)
        self.costLabel = QtWidgets.QLabel()
        self.invoiceLabel = QtWidgets.QLabel()
        self.beingProcessed = QtWidgets.QLabel()

        self.costLabel.setMinimumSize(QtCore.QSize(250, 100))
        self.invoiceLabel.setMinimumSize(QtCore.QSize(250, 100))
        self.beingProcessed.setMinimumSize(QtCore.QSize(250, 100))

        self.threeBoxLayout.addWidget(self.costLabel)
        self.threeBoxLayout.addWidget(self.invoiceLabel)
        self.threeBoxLayout.addWidget(self.beingProcessed)

        self.gLayout.addWidget(self.frameNavigation, 0, 0, 1, 1)
        self.gLayout.addWidget(self.scrollArea, 0, 1, 1, 2)

        #1.3.3. Label báo cáo tk 7 ngày
        self.reportNameLabel = QtWidgets.QLabel()
        self.scrollAreaLayout.addWidget(self.reportNameLabel)
        self.reportNameLabel.setText("<b style = 'font-size: 16px;'>Báo cáo thống kê 7 ngày gần nhất</b>")
        self.reportNameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        #1.4.LAYOUT chứa biểu đồ
        self.layoutChart = QtWidgets.QGridLayout()
        self.scrollAreaLayout.addLayout(self.layoutChart)

        # 1.4.1. Doanh thu và lợi nhuận
        self.frameRevenue = QtWidgets.QFrame()
        self.frameRevenue.setObjectName('frameRevenue')
        self.layoutRevenue = QtWidgets.QGridLayout(self.frameRevenue)
        self.labelRevenue = QtWidgets.QLabel("<b>Doanh thu và lợi nhuận trong 7 ngày gần nhất<b>")
        self.layoutRevenue.addWidget(self.labelRevenue, 0, 0, 1, 1)
        self.labelDetailRevenue = QtWidgets.QLabel('<span style ="color: #bd1906;">Chi tiết</span>')
        self.labelDetailRevenue.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.layoutRevenue.addWidget(self.labelDetailRevenue, 0, 1, 1, 1)

        # 1.4.2. Doanh thu theo chương trình khuyến mãi
        self.framePromotion = QtWidgets.QFrame()
        self.framePromotion.setObjectName('framePromotion')
        self.layoutPromotion = QtWidgets.QGridLayout(self.framePromotion)
        self.labelPromotion = QtWidgets.QLabel("<b>Doanh thu theo chương trình khuyến mãi<b>")
        self.layoutPromotion.addWidget(self.labelPromotion, 0, 0, 1, 1)
        self.labelDetailPromotion = QtWidgets.QLabel('<span style ="color: #bd1906;">Chi tiết</span>')
        self.labelDetailPromotion.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.layoutPromotion.addWidget(self.labelDetailPromotion, 0, 1, 1, 1)

        # 1.4.3. Phương thức thanh toán
        self.framePercentTypyPayment = QtWidgets.QFrame()
        self.framePercentTypyPayment.setObjectName('framePercentTypyPayment')
        self.layoutPercentTypePayment = QtWidgets.QGridLayout(self.framePercentTypyPayment)
        self.labelPieChartPayment = QtWidgets.QLabel("<b>Phương thức thanh toán<b>")
        self.layoutPercentTypePayment.addWidget(self.labelPieChartPayment, 0, 0, 1, 1)
        self.labelDetailPayment = QtWidgets.QLabel('<span style ="color: #bd1906;">Chi tiết</span>')
        self.labelDetailPayment.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.layoutPercentTypePayment.addWidget(self.labelDetailPayment, 0, 1, 1, 1)

        # 1.4.4. Top 5 mặt hàng bán chạy
        self.frameTableTop5 = QtWidgets.QFrame()
        self.frameTableTop5.setObjectName('frameTableTop5')
        self.layoutTableTop5 = QtWidgets.QGridLayout(self.frameTableTop5)
        self.labelTable = QtWidgets.QLabel("<b> Top 5 sản phẩm bán chạy nhất")
        self.layoutTableTop5.addWidget(self.labelTable, 0, 0, 1, 1)
        self.labelDetailTop5 = QtWidgets.QLabel('<span style ="color: #bd1906;">Chi tiết</span>')
        self.labelDetailTop5.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.layoutTableTop5.addWidget(self.labelDetailTop5, 0, 1, 1, 1)

        # 1.4.5. Lượt đánh giá
        self.framePercentReiview = QtWidgets.QFrame()
        self.framePercentReiview.setObjectName('framePercentReview')
        self.layoutPercentReiview = QtWidgets.QGridLayout(self.framePercentReiview)
        self.labelPieChartReivew= QtWidgets.QLabel("<b>Lượt đánh giá<b>")
        self.labelDetailReview = QtWidgets.QLabel('<span style ="color: #bd1906;">Chi tiết</span>')
        self.labelDetailReview.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.layoutPercentReiview.addWidget(self.labelPieChartReivew, 0, 0, 1, 1)
        self.layoutPercentReiview.addWidget(self.labelDetailReview, 0, 1, 1, 1)

        # 2.1. AI Recommendation
        self.frameAIRecommendation = QtWidgets.QFrame()
        self.frameAIRecommendation.setObjectName('frameAIRecommendation')
        self.layoutAIRecommendation = QtWidgets.QVBoxLayout(self.frameAIRecommendation)
        self.labelAIRecommendation = QtWidgets.QLabel("<b>Lời khuyên từ AI<b>")
        self.labelAIRecommendation.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layoutAIRecommendation.addWidget(self.labelAIRecommendation)
        self.scrollAreaLayout.addWidget(self.frameAIRecommendation)

        ###
        self.framePercentTypyPayment.setMinimumSize(310,323)
        self.framePercentReiview.setMinimumSize(310,323)
        self.frameTableTop5.setMinimumSize(310,323)
        self.framePromotion.setMinimumSize(530, 297)
        self.frameRevenue.setMinimumSize(530, 297)
        self.frameAIRecommendation.setMinimumHeight(700)


        self.layoutChart.addWidget(self.frameRevenue, 0, 0, 1, 3)
        self.layoutChart.addWidget(self.framePromotion, 0, 3, 1, 3)
        self.layoutChart.addWidget(self.framePercentTypyPayment, 1, 0, 1, 2)
        self.layoutChart.addWidget(self.frameTableTop5, 1, 2, 1, 2)
        self.layoutChart.addWidget(self.framePercentReiview, 1, 4, 1, 2)


        self.setStyleSheetAll()

    def setStyleSheetAll(self):
        self.centralwidget.setStyleSheet("background-color: rgb(255, 255, 255); font-family: Montserrat; font-size: 14px;")
        self.pushButtonMenu.setStyleSheet("font-weight: bold; text-align: left")
        self.headerFrame.setStyleSheet("background-color: #bd1906")
        self.revenueLabel.setStyleSheet("color: white; font-size: 16px;")
        self.totalRevenueLabel.setStyleSheet("font-size: 24pt; color: white; font-weight: bold; ")
        self.gainRevenueButton.setStyleSheet("color: #bd1906; background-color: #F9EDEB; border-radius: 8px; padding-left: 10px;")
        self.compareLastDayLabel.setStyleSheet("color: white;")
        self.selectedDateLineEdit.setStyleSheet("background-color: #fff; border-radius: 10px;")
        self.costLabel.setStyleSheet("background-color: #F9EDEB; color: #bd1906; border-radius: 15px; padding-left: 15px;")
        self.invoiceLabel.setStyleSheet("background-color: #F9EDEB; color: #bd1906;  border-radius: 15px; padding-left: 15px;")
        self.beingProcessed.setStyleSheet("background-color: #F9EDEB; color: #bd1906;  border-radius: 15px; padding-left: 15px;")
        self.frameNavigation.setStyleSheet("""
            QFrame#frameNavigation {
                border: 1px solid #D9D9D9;
            }
        """)
        self.scrollArea.setStyleSheet("""
                    QScrollArea#scrollArea {
                        border: 1px solid #D9D9D9;
                    }
                     QFrame#framePercentTypyPayment, 
                     QFrame#framePercentReview,
                     QFrame#frameTableTop5,
                     QFrame#framePromotion,
                     QFrame#frameRevenue {
                        border: 1px solid #D9D9D9; 
                        border-radius: 10px;}
                     QScrollBar:vertical {
                     width: 6px; 
                     background: #f0f0f0;
                     }
                     QScrollBar::handle:vertical{
                     background: #ababab;
                     min-height: 5px;
                     border-radius: 3px;}
                """)
        self.pushButtonThucDon.setStyleSheet('border-radius: 10px; border: 1px solid #D9D9D9')
        self.pushButtonChuongTrinh.setStyleSheet('border-radius: 10px; border: 1px solid #D9D9D9')
        self.pushButtonBaoCao.setStyleSheet('border-radius: 10px; border: 1px solid #D9D9D9')
        self.pushButtonThanhToan.setStyleSheet('border-radius: 10px; border: 1px solid #D9D9D9')
        # self.pushButtonAI.setStyleSheet('border-radius: 10px; border: 1px solid #D9D9D9')

    def createSizePolicy(self, horizontal, vertical, hstretch=0, vstretch=0):
        sizePolicy = QtWidgets.QSizePolicy(horizontal, vertical)
        sizePolicy.setHorizontalStretch(hstretch)
        sizePolicy.setVerticalStretch(vstretch)







