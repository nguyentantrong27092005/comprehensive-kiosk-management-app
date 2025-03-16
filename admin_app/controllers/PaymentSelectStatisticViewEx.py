import sys
import datetime
from collections import Counter
import pymysql
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView
from admin_app.controllers.GeneralViewEx import GeneralViewEx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from common.sql_func import db

class Database_LoginApp:
    def __init__(self, host="34.80.75.195", user="dev", password="KTLTnhom4@", database="kioskapp", port=3306):
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            print("Kết nối thành công!")
        except pymysql.MySQLError as e:
            self.connection = None
            print(f"Lỗi kết nối MySQL: {e.args}")

    def fetch_all_orders(self, start_date=None, end_date=None):
        if self.connection is None:
            print("không thể thực hiện truy vấn vì kết nối database thất bại.")
            return None
        try:
            query = """
            SELECT Payment, TotalPrice, CreateAt
            FROM `order`
            """
            params = ()

            if start_date and end_date:
                if len(start_date) == 10:
                    start_date += " 00:00:00"
                if len(end_date) == 10:
                    end_date += " 23:59:59"

                query += " WHERE CreateAt BETWEEN %s AND %s"
                params = (start_date, end_date)

            query += " ORDER BY CreateAt DESC;"
            self.cursor.execute(query, params)
            all_orders = self.cursor.fetchall()
            return all_orders
        except pymysql.MySQLError as e:
            print(f"Lỗi truy vấn MySQL: {e.args}")
            return None

db = Database_LoginApp()



class PaymentSelectViewStatisticsEx(GeneralViewEx):

    def __init__(self, start_date, end_date):
        super().__init__()
        self.setWindowTitle("Báo cáo phương thức thanh toán")
        self.main_layout = QtWidgets.QVBoxLayout(self.frameContent)
        self.init_ui()
        # Gọi hai hàm tạo bảng và đường luôn --> hiển thị dữ liệu thống kê 1 tháng gần nhất
        self.create_piechart_and_table(start_date, end_date)
        self.create_payment_chart(start_date, end_date)
        self.pushButtonPaymentMethod.setStyleSheet(
            "background-color: white; color: red; font-size: 14px; font-weight: bold;")

    # Lấy ngày bắt đầu
    def getStartDate(self):
        if self.selected_dates:
            return min(self.selected_dates).toString('yyyy-MM-dd')

    # Lấy ngày kết thúc
    def getEndDate(self):
        if self.selected_dates:
            return max(self.selected_dates).toString('yyyy-MM-dd')

    # Hiển thị ngày bắt đầu -- kết thúc đã chọn
    def showDateSelected(self):
        self.calendarFrame.setVisible(False)

        start_date = self.getStartDate()
        end_date = self.getEndDate()

        if start_date and end_date:
            dates = f"{start_date} - {end_date}"
            self.lineEditDate.setText(dates)

        # Cập nhật bảng và biểu đồ
        self.create_piechart_and_table(start_date, end_date)
        self.create_payment_chart(start_date, end_date)

    def init_ui(self):

        # Tạo khung trên
        top_frame = QtWidgets.QFrame()
        top_layout = QtWidgets.QHBoxLayout()

        # Tạo biểu đồ tròn
        pie_chart_frame = QtWidgets.QFrame()
        pie_chart_layout = QtWidgets.QVBoxLayout()
        self.pie_chart_figure, self.pie_chart_ax = plt.subplots(figsize=(6, 6)) # Tạo biểu đồ tròn bằng Matplotlib
        self.pie_chart_display = FigureCanvas(self.pie_chart_figure) #Chuyển biểu đồ thành Widget
        self.pie_chart_display.setFixedSize(600, 400)
        pie_chart_layout.addWidget(self.pie_chart_display)
        pie_chart_frame.setLayout(pie_chart_layout)

        # Tạo biểu đồ đường
        line_chart_frame = QtWidgets.QFrame()
        line_chart_layout = QtWidgets.QVBoxLayout()
        self.line_chart_figure, self.line_chart_ax = plt.subplots(figsize=(6, 6))
        self.line_chart_display = FigureCanvas(self.line_chart_figure)
        self.line_chart_display.setFixedSize(600, 400)
        line_chart_layout.addWidget(self.line_chart_display)
        line_chart_frame.setLayout(line_chart_layout)

        # Thêm biểu đồ đường và biểu đồ
        top_layout.addWidget(line_chart_frame, 1)
        top_layout.addWidget(pie_chart_frame, 1)
        top_frame.setLayout(top_layout)

        # Tạo khung dưới
        bottom_frame = QtWidgets.QFrame()
        bottom_layout = QtWidgets.QVBoxLayout()

        # Tạo một QScrollArea để chứa bảng
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Tạo bảng
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["#", "Phương thức thanh toán", "Số hóa đơn", "Tổng tiền"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Thiết lập bảng để có thể cuộn
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        font = QFont()
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)

        # Đưa bảng vào vùng cuộn
        scroll_area.setWidget(self.table)
        bottom_layout.addWidget(scroll_area)
        bottom_frame.setLayout(bottom_layout)

        # Thêm khung trên và khung dưới vào khung chính
        self.main_layout.addWidget(top_frame, 2)
        self.main_layout.addWidget(bottom_frame, 3)
        self.setLayout(self.main_layout)

    # Hàm vẽ biểu đồ đường
    def create_payment_chart(self, start_date, end_date):

        orders = db.fetch_all_orders(start_date, end_date)

        for order in orders:
            if isinstance(order['CreateAt'], str):
                order['CreateAt'] = datetime.datetime.strptime(order['CreateAt'], '%Y-%m-%d')

        first_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        last_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        num_days = (last_date - first_date).days + 1

        date_counts = {first_date + datetime.timedelta(days=i): {'cash': 0, 'bank': 0} for i in range(num_days)}

        for order in orders:
            date = order['CreateAt'].date()
            if order['Payment'] == 'cash':
                date_counts[date]['cash'] += 1
            else:
                date_counts[date]['bank'] += 1

        dates = list(date_counts.keys())
        cash_values = [date_counts[date]['cash'] for date in dates]
        bank_values = [date_counts[date]['bank'] for date in dates]

        # Xóa biểu đồ cũ
        self.line_chart_ax.clear()

        # Vẽ biểu đồ mới
        self.line_chart_ax.plot(dates, bank_values, linestyle='-', color='#f39c12', marker='o', label='Chuyển khoản')
        self.line_chart_ax.plot(dates, cash_values, linestyle='-', color='#2980b9', marker='o', label='Tiền mặt')

        # Trục x thay đổi
        step = max(1, len(dates) // 10)
        self.line_chart_ax.set_xticks(dates[::step])
        self.line_chart_ax.set_xticklabels([date.strftime('%d/%m') for date in dates][::step], rotation=30, ha='right')

        # Thiết lập tiêu đề và nhãn
        self.line_chart_ax.set_title(f"Thống kê phương thức thanh toán từ {first_date.strftime('%d/%m/%Y')} đến {last_date.strftime('%d/%m/%Y')}", fontsize=10, fontweight="bold")
        self.line_chart_ax.set_xlabel("Thời gian")
        self.line_chart_ax.set_ylabel("Số đơn hàng")
        self.line_chart_ax.legend()
        self.line_chart_ax.grid(True, linestyle="--", alpha=0.6)

        # Cập nhật biểu đồ
        self.line_chart_display.draw()

    # Hàm vẽ biểu đồ tròn và bảng
    def create_piechart_and_table(self, start_date, end_date):

        orders = db.fetch_all_orders(start_date, end_date)
        payment_counts = Counter(order['Payment'] for order in orders)
        payment_totals = {method: sum(order['TotalPrice'] for order in orders if order['Payment'] == method) for method in payment_counts}

        self.table.setRowCount(len(payment_counts))
        for row, (method, count) in enumerate(payment_counts.items()):
            total = payment_totals[method]
            method_display = "Chuyển khoản" if method == "bank" else "Tiền mặt"

            for col, value in enumerate([row + 1, method_display, count, f"{total:,.0f}"]):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

        # Xóa biểu đồ cũ
        self.pie_chart_ax.clear()

        if payment_counts:
            labels = ["Chuyển khoản" if key == "bank" else "Tiền mặt" for key in payment_counts.keys()]
            values = list(payment_counts.values())

            self.pie_chart_ax.pie(values, autopct='%1.1f%%', startangle=140, colors=['#2980b9', '#f39c12'],
                                  explode=[0.1 if v == max(values) else 0 for v in values], shadow=True,
                                  textprops={'fontsize': 12, 'fontweight': 'bold'})

            self.pie_chart_ax.legend(labels, loc="upper center", bbox_to_anchor=(0.5, -0.02),
                                     ncol=2, fontsize=10, frameon=True)

            self.pie_chart_ax.set_title("Tỉ lệ phương thức thanh toán", fontsize=14, fontweight="bold")

        # Cập nhật lại biểu đồ mới
        self.pie_chart_display.draw()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    today = datetime.datetime.today().date()
    start_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    window = PaymentSelectViewStatisticsEx(start_date, end_date)
    window.show()
    sys.exit(app.exec())
