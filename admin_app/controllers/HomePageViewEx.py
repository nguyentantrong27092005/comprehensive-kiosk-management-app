import textwrap

import matplotlib.pyplot as plt
import pandas as pd
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import  QDate
from PyQt6.QtWidgets import QStackedWidget, QTableWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

from admin_app.views.HomePageView import HomePageView
from common.sql_func import Database

class HomePageViewController(HomePageView):
    def __init__(self,mainStackedWidget: QStackedWidget, db: Database):
        super().__init__()
        self.mainStackedWidget = mainStackedWidget
        self.db = db
        self.colors = ['#991203','#BD1906', '#CA4738', '#EBBAB4','#F8E8E6']
        self.updateUI()
    def updateUI(self):
        self.currentDate = QDate.currentDate()
        self.selectedDateLineEdit.setText(f"Hôm nay {self.currentDate.toString("dd/MM")}")
        self.compareLastDayLabel.setText(f"so với hôm qua {self.currentDate.addDays(-1).toString('dd/MM')}")
        self.selectedDateLineEdit.setReadOnly(True)

        totalRevenue = self.TongDoanhThu()
        if totalRevenue[1] !=0:
            percent = totalRevenue[0]/totalRevenue[1]*100
            self.gainRevenueButton.setText(f"Tăng {percent:.0f}%")
            self.totalRevenueLabel.setText(f"{totalRevenue[0]:,}đ")
        else:
            self.totalRevenueLabel.setText(f"{totalRevenue[0]:,}đ")
            self.gainRevenueButton.hide()
            self.compareLastDayLabel.hide()

        totalCostDiscount = self.ChiPhiGiamGia()
        self.costLabel.setText(f"Giảm giá và chi phí<br><br><span style = 'font-size: 16px; font-weight: bold;'>{totalCostDiscount:,}đ</span>")
        totalInvoice = self.TongHoaDon()
        if totalInvoice !=0:
            self.invoiceLabel.setText(f"Số hoá đơn<br><span style = 'font-size: 16px; font-weight: bold;'>{totalInvoice:,}</span><br><br>Trung bình {totalRevenue[0]//totalInvoice:.0f}đ/hoá đơn")
        else:
            self.invoiceLabel.setText(
                f"Số hoá đơn<br><span style = 'font-size: 16px; font-weight: bold;'>{totalInvoice:,}</span><br><br>Trung bình {0}đ/hoá đơn")

        totalInvoice_xuly = self.TongHoaDon_dangxuly()
        self.beingProcessed.setText(f"Số hoá đơn hiện đang xử lý<br><br><span style = 'font-size: 16px; font-weight: bold;'>{totalInvoice_xuly:,}</span>")
        # ---------Vẽ biểu đồ
        # 1. Barchart Doanh thu
        self.barChartRevenue()
        self.canvasRevenue = FigureCanvas(self.revenue)
        self.layoutRevenue.addWidget(self.canvasRevenue, 1, 0, 1, 2)
        # 2. LineChart Chương trình khuyến mãi
        self.lineChartPromotion()
        self.canvasPromo = FigureCanvas(self.promo)
        self.layoutPromotion.addWidget(self.canvasPromo, 1, 0, 1, 2)
        # 3. PieChart phương thức thanh toán
        self.canvas = FigureCanvas(plt.figure(figsize=(2, 2.5)))  # khung
        self.layoutPercentTypePayment.addWidget(self.canvas, 1, 0, 1, 2)
        self.pieChartPaymnet()
        # 4. Bảng top 5 sản phẩm doanh thu nhiều nhất
        self.tableChart()
        self.layoutTableTop5.addWidget(self.tableWidgetTop5BestSeller, 1, 0, 1, 2)
        # 5. PieChart Lượt đánh giá
        self.canvas = FigureCanvas(plt.figure(figsize=(2, 2.5)))
        self.layoutPercentReiview.addWidget(self.canvas, 1, 0, 1, 2)
        self.pieChartReviews()
        ###
        self.signalandslot()
    def signalandslot(self):
        self.labelDetailRevenue.mousePressEvent = lambda event: self.detailRevenue()
        self.labelDetailPromotion.mousePressEvent = lambda event: self.detailPromotion()
        self.labelDetailPayment.mousePressEvent = lambda event: self.detailPayment()
        self.labelDetailTop5.mousePressEvent = lambda event: self.detailTop5()
        self.labelDetailReview.mousePressEvent = lambda event: self.detailReview()
        self.pushButtonAI.clicked.connect(self.openWindowAI)
    def detailRevenue(self):
        pass
    def detailPromotion(self):
        pass
    def detailPayment(self):
        pass
    def detailTop5(self):
        pass
    def detailReview(self):
        pass
    def openWindowAI(self):
        pass

    def percentReivew(self):
        sql = """
        SELECT customer_vote, 
           COUNT(*) AS TotalReviews,
           ROUND(COUNT(*) * 100.0 / 
        (SELECT COUNT(*) 
         FROM kioskapp.order 
         WHERE customer_vote IS NOT NULL 
         AND CreateAt >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        ), 2) AS Percent
        FROM kioskapp.order
        WHERE customer_vote IS NOT NULL
        AND CreateAt >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY customer_vote
        ORDER BY customer_vote DESC;"""
        result = self.db.fetch_data(sql)
        return result

    def top5BestSeller(self):
        sql ="""SELECT 
                    f.Name AS TenMon,
                    SUM(od.Amount) AS SoLuongBan,
                    SUM(od.Amount * od.Price) AS DoanhThu
                FROM kioskapp.fooditem f
                JOIN kioskapp.orderdetails od ON f.ID = od.FoodItemID
                JOIN kioskapp.order o ON od.OrderID = o.ID
                WHERE o.Status = 'Done'  
                      AND o.CreateAt >= DATE_SUB(NOW(), INTERVAL 7 DAY)
                GROUP BY f.Name
                ORDER BY DoanhThu DESC
                LIMIT 5;        
                """
        result = self.db.fetch_data(sql)
        return result

    def promotion(self):
        sql = """
        select date(o.CreateAt) as Ngay
        , ev.Name as TenChuongTrinh
        , sum(o.TotalPrice) as TongDoanhThu
        from kioskapp.evoucher ev
        inner join evouchergiamgia evgg
        on ev.ID = evgg.EVoucherID
        left join kioskapp.order o 
        on evgg.ID = o.EVoucherGiamGiaID
        where o.CreateAt >= date_sub(now(), interval 7 day)
        group by ev.ID, date(o.CreateAt)
        union all
        select date (o.CreateAt) as Ngay
        , p.Name as TenChuongTrinh
        , sum(o.TotalPrice) as TongDoanhThu
        from kioskapp.order o 
        join kioskapp.orderdetails od on o.ID = od.OrderID
        join kioskapp.promotion p on p.ID = od.PromotionID
        
        where o.CreateAt >= date_sub(now(), interval 7 day)
        group by p.ID, date(o.CreateAt)
        order by Ngay, TongDoanhThu desc;"""
        result = self.db.fetch_data(sql)
        return result

    def totalRevenueByDate(self):
        sql = """
        SELECT
            SUM(TotalPrice) AS DoanhThu,
        DATE(CreateAt) AS Ngay
        FROM kioskapp.order 
        WHERE CreateAt >= DATE_SUB(current_time(), INTERVAL 7 DAY)
        AND Status = 'done'
        GROUP BY Ngay
        ORDER BY Ngay ASC;"""
        result = self.db.fetch_data(sql)
        return result

    def barChartRevenue(self):
        input_data = self.totalRevenueByDate()
        if not input_data:
            return
        df = pd.DataFrame(input_data, columns=["DoanhThu", "Ngay"])
        df["Ngay"] = pd.to_datetime(df["Ngay"])
        self.revenue = plt.figure(figsize=(4, 3))
        ax = self.revenue.add_subplot(111)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.bar(df["Ngay"], df["DoanhThu"], color="#bd1906", width=0.3)
        ax.set_ylabel("Doanh thu (VNĐ)", fontsize=8, color="#ababab", rotation=0)
        ax.yaxis.set_label_coords(-0.1, 1.02)
        plt.xticks(rotation=0, fontsize=8)
        plt.yticks(fontsize=8)
        plt.tight_layout()

    def lineChartPromotion(self):
        input_data = self.promotion()
        if not input_data:
            return
        df = pd.DataFrame(input_data, columns=["Ngay", "TenChuongTrinh", "TongDoanhThu"])
        df["Ngay"] = pd.to_datetime(df["Ngay"])
        all_days = pd.date_range(start=df["Ngay"].min(), end=df["Ngay"].max())
        unique_promos = df["TenChuongTrinh"].unique()
        full_data = pd.MultiIndex.from_product([all_days, unique_promos], names=["Ngay", "TenChuongTrinh"]).to_frame(index=False)
        df = full_data.merge(df, on=["Ngay", "TenChuongTrinh"], how="left").fillna({"TongDoanhThu": 0})

        self.promo = plt.figure(figsize=(5, 3))
        ax = self.promo.add_subplot(111)
        colors = ["#BD1906", "#5388D8", "#FFA424", "#53D85C", "#000000"]
        wrapped_labels = [textwrap.fill(promo, width=35) for promo in unique_promos]

        for i, promo in enumerate(unique_promos):
            df_promo = df[df["TenChuongTrinh"] == promo]
            ax.plot(df_promo["Ngay"], df_promo["TongDoanhThu"], color=colors[i], linewidth=1, label=wrapped_labels[i])

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))

        ax.set_xlabel("")
        ax.set_ylabel("Doanh thu (VNĐ)", fontsize=8, color="#ababab", rotation=0)
        ax.yaxis.set_label_coords(-0.1, 1.02)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        legend = ax.legend(loc="upper center",bbox_to_anchor=(0.5, -0.2), frameon=False, fontsize=8, ncol= 2,  handletextpad=0.5)
        plt.tight_layout()
        for text, color in zip(legend.get_texts(), colors):
            text.set_color(color)

        plt.grid(True, linestyle="--", alpha=0.5)
        plt.xticks(rotation=0, fontsize=8)
        plt.yticks(fontsize=8)

    def tableChart(self):
        inputData = self.top5BestSeller()
        self.tableWidgetTop5BestSeller = QTableWidget(parent = self.frameTableTop5)
        self.tableWidgetTop5BestSeller.setObjectName('tableWidgetTop5BestSeller')
        self.tableWidgetTop5BestSeller.verticalHeader().setVisible(False)
        self.tableWidgetTop5BestSeller.setRowCount(len(inputData))
        self.tableWidgetTop5BestSeller.setColumnCount(3)
        self.tableWidgetTop5BestSeller.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.tableWidgetTop5BestSeller.setHorizontalHeaderLabels(['STT', 'Tên sản phẩm', 'Doanh thu'])

        for row, fooditem in enumerate(inputData):
            item_stt = QtWidgets.QTableWidgetItem(str(row + 1))
            item_stt.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.tableWidgetTop5BestSeller.setItem(row, 0, item_stt)

            self.tableWidgetTop5BestSeller.setItem(row, 1, QtWidgets.QTableWidgetItem(str(fooditem['TenMon'])))

            item_doanhthu = QtWidgets.QTableWidgetItem(f"{fooditem['DoanhThu']:,}")
            item_doanhthu.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
            self.tableWidgetTop5BestSeller.setItem(row, 2, item_doanhthu)

        self.tableWidgetTop5BestSeller.setStyleSheet("""
            QHeaderView::section {
            background-color: #BD1906;
            color: white;
            font-weight: bold;
            border: None}
            QTableWidget {
            gridline-color: transparent;
            border-radius: 15px;
            margin-top: 10px;
            }
            QHeaderView::section:first {
            border-top-left-radius: 15px;
            }
            QHeaderView::section:last {
            border-top-right-radius: 15px;
            }
            """)
        self.tableWidgetTop5BestSeller.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWidgetTop5BestSeller.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidgetTop5BestSeller.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)

    def pieChartReviews(self):
        input = self.percentReivew()
        review_type = []
        percent = []
        for item in input:
            review_type.append(item['customer_vote'])
            percent.append(float(item['Percent']))
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()
        wedges, _, autotexts = ax.pie(percent, labels=None, autopct='%1.1f%%', colors=self.colors, textprops={'color': 'white'})
        ax.legend(wedges, review_type, loc="lower center",  bbox_to_anchor=(0.5, -0.15), ncol = 5)
        self.canvas.draw()

    def percentTypePayment(self):
        sql = """
        SELECT Payment, 
           COUNT(*) AS TotalAmount,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM kioskapp.order WHERE CreateAt >= DATE_SUB(NOW(), INTERVAL 7 DAY)), 2) AS Percent
        FROM kioskapp.order
        WHERE CreateAt >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY Payment;"""
        result = self.db.fetch_data(sql)
        return result
    def pieChartPaymnet(self):
        input_data = self.percentTypePayment()
        payment_type = []
        percent = []
        for item in input_data:
            payment_type.append(item['Payment'])
            percent.append(float(item['Percent']))
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()
        wedges, _, autotexts=ax.pie(percent, labels=None, autopct='%1.1f%%', colors = self.colors, textprops={'color': 'white'})
        ax.legend(wedges, payment_type,loc="lower center",  bbox_to_anchor=(0.5, -0.15), ncol = 2)

    def TongDoanhThu(self):
        sql = """SELECT COALESCE(SUM(o.TotalPrice), 0) AS TongDoanhThu 
        FROM `order` o
        WHERE DATE(CreateAt) = %s
        AND Status = 'Done';"""
        result = [self.db.fetch_data(sql,f"{self.currentDate.toString('yyyy-MM-dd')}"), self.db.fetch_data(sql,f"{self.currentDate.addDays(-1).toString('yyyy-MM-dd')}")]
        return [result[0][0]['TongDoanhThu'], result[1][0]['TongDoanhThu']]

    def ChiPhiGiamGia(self):
        sql = """SELECT COALESCE(SUM(o.EVoucherDiscount), 0) AS TongChiPhi
        FROM `order` o
        WHERE Status = 'done'
        AND DATE(CreateAt) = %s;"""
        result = self.db.fetch_data(sql, f"{self.currentDate.toString('yyyy-MM-dd')}")
        return result[0]['TongChiPhi']

    def TongHoaDon(self):
        sql ="""SELECT COUNT(*) AS TongSoHoaDon FROM `order`
        WHERE Status = 'Done'
        AND DATE(CreateAt) = %s;"""
        result = self.db.fetch_data(sql, f"{self.currentDate.toString('yyyy-MM-dd')}")
        return result[0]['TongSoHoaDon']

    def TongHoaDon_dangxuly(self):
        sql = """SELECT COUNT(*) AS SoHoaDonDãngXuLy
        FROM `order`
        WHERE Status IN ('inprocess', 'unpaid')
        AND DATE(CreateAt) = %s;"""
        result = self.db.fetch_data(sql, f"{self.currentDate.toString('yyyy-MM-dd')}")
        return result[0]['SoHoaDonDãngXuLy']
