from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QTableWidget,QSplitter,
    QTableWidgetItem, QHeaderView, QScrollArea
)
import pyqtgraph as pg
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import pymysql,datetime
import sys

class DatabaseManager:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def fetch_data(self):
        query = """
            SELECT f.CustomID AS MaMon, f.Name AS TenMon, c.Name AS NhomMon,
                   SUM(o.Amount) AS SoLuong, SUM(o.Discount) AS GiamGia,
                   SUM(o.Amount * (o.Price - o.Discount)) AS DoanhThu,
                   SUM(o.Amount * (o.Price - o.Discount)) - SUM(fh.Cost) AS LoiNhuan
            FROM fooditem f
            LEFT JOIN Category c ON c.ID = f.CategoryID
            LEFT JOIN orderdetails o ON f.ID = o.FoodItemID
            LEFT JOIN fooditem_history fh ON f.ID = fh.FoodItemID AND fh.IsEffective = TRUE
            GROUP BY f.CustomID, f.Name, c.Name;
        """
        try:
            conn = pymysql.connect(
                host=self.host, user=self.user, password=self.password,
                database=self.database, port=self.port, cursorclass=pymysql.cursors.DictCursor
            )
            with conn.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
            return data
        except pymysql.MySQLError as err:
            print(f"Lỗi truy vấn dữ liệu: {err}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    def fetch_top2_products(self):
        query = """
            WITH RECURSIVE date_series AS (
    -- Tạo dãy ngày từ 30 ngày trước đến hôm nay
    SELECT CURDATE() - INTERVAL 29 DAY AS NgayBan
    UNION ALL
    SELECT NgayBan + INTERVAL 1 DAY
    FROM date_series
    WHERE NgayBan + INTERVAL 1 DAY <= CURDATE()
),
Top2 AS (
    -- Lấy 2 món ăn bán chạy nhất trong 30 ngày qua
    SELECT o.FoodItemID, f.Name, SUM(o.Amount) AS TotalSold
    FROM orderdetails o
    JOIN fooditem f ON o.FoodItemID = f.ID
    WHERE o.CreateAt >= CURDATE() - INTERVAL 30 DAY  -- Lọc chính xác 30 ngày
    GROUP BY o.FoodItemID, f.Name
    ORDER BY TotalSold DESC
    LIMIT 2
)
SELECT 
    ds.NgayBan, 
    t.FoodItemID, 
    t.Name, 
    IFNULL(SUM(o.Amount), 0) AS SoLuong,  -- ✅ Số lượng bán theo ngày
    IFNULL(SUM(o.Amount * o.Price), 0) AS DoanhThu  -- ✅ Doanh thu theo ngày (Số lượng * Giá)
FROM date_series ds
CROSS JOIN Top2 t
LEFT JOIN orderdetails o 
    ON t.FoodItemID = o.FoodItemID 
    AND DATE(o.CreateAt) = ds.NgayBan
GROUP BY ds.NgayBan, t.FoodItemID, t.Name
ORDER BY ds.NgayBan;

        """
        try:
            conn = pymysql.connect(
                host=self.host, user=self.user, password=self.password,
                database=self.database, port=self.port, cursorclass=pymysql.cursors.DictCursor
            )
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.MySQLError as err:
            print(f"Lỗi truy vấn dữ liệu: {err}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()
class MainWindow(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        # Tạo frame chính
        self.main_frame = QFrame(self)
        main_layout = QVBoxLayout(self.main_frame)

        # Tạo frame trên chứa left_frame và right_frame
        self.top_frame = QFrame()
        top_layout = QHBoxLayout(self.top_frame)

        self.left_frame = QFrame()
        self.right_frame = QFrame()

        # Cấu hình kích thước và màu nền
        self.left_frame.setStyleSheet("background-color: white; border: 1px solid black;")
        self.right_frame.setStyleSheet("background-color: white; border: 1px solid black;")

        # Layout cho left_frame
        self.left_frame_layout = QVBoxLayout()
        self.plot_chart(self.left_frame_layout)  # Gọi hàm vẽ biểu đồ
        self.left_frame.setLayout(self.left_frame_layout)

        # Layout cho right_frame
        self.right_frame_layout = QVBoxLayout()
        self.chart_plot(self.right_frame_layout) # gọi hàm để vẽ biểu đ
        self.right_frame.setLayout(self.right_frame_layout)

        # Thêm left_frame và right_frame vào top_frame
        top_layout.addWidget(self.left_frame)
        top_layout.addWidget(self.right_frame)

        # Tạo frame dưới chứa bảng dữ liệu
        self.bottom_frame = QFrame()
        self.bottom_frame.setFixedHeight(300)
        self.bottom_frame.setStyleSheet("background-color: white; border: 1px solid black;")

        # Tạo bảng dữ liệu
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Mã món", "Tên món", "Nhóm món", "Số lượng", "Giảm giá", "Doanh thu", "Lợi nhuận"
        ])
        self.table.setStyleSheet("background-color: white;")
        self.table.setFont(QFont("Arial", 10))

        # Cài đặt tự động co giãn cột
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Bật thanh cuộn dọc
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Ẩn số thứ tự dòng
        self.table.verticalHeader().setVisible(False)

        # Load dữ liệu từ database
        self.load_data()

        # Khu vực cuộn
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.table)

        # Layout cho bottom_frame
        bottom_layout = QVBoxLayout(self.bottom_frame)
        bottom_layout.addWidget(scroll_area)

        # Thêm các frame vào main_layout
        main_layout.addWidget(self.top_frame, 2)
        main_layout.addWidget(self.bottom_frame, 1)

        # Đặt layout chính cho widget
        self.setLayout(main_layout)
        self.setWindowTitle("Chia màn hình với bảng dữ liệu có thanh cuộn")
        self.resize(1200, 790)

    def load_data(self):
        data = self.db_manager.fetch_data()
        if not data:
            print("Không có dữ liệu.")
            return

        self.table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row["MaMon"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row["TenMon"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row["NhomMon"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row["SoLuong"])))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row["GiamGia"])))
            self.table.setItem(row_idx, 5, QTableWidgetItem(str(row["DoanhThu"])))
            self.table.setItem(row_idx, 6, QTableWidgetItem(str(row["LoiNhuan"])))

    import pyqtgraph as pg
    import datetime

    def plot_chart(self, layout):
        data = self.db_manager.fetch_top2_products()
        if not data:
            print("Không có dữ liệu để vẽ biểu đồ.")
            return

        plot_widget = pg.PlotWidget()
        plot_widget.setBackground('w')
        layout.addWidget(plot_widget)

        plot_widget.setLabel("left", "Số lượng bán")
        plot_widget.setLabel("bottom", "Ngày bán")
        plot_widget.setTitle("<b>Số lượng sản phẩm bán chạy trong 30 ngày qua</b>")

        legend = pg.LegendItem(offset=(60, 20))
        legend.setParentItem(plot_widget.getPlotItem())

        colors = ["r", "g", "b", "m", "c", "y"]
        product_sales = {}
        all_timestamps = []
        max_y = 0

        for row in data:
            ngay_ban = row['NgayBan']
            so_luong = float(row['SoLuong'])
            product_sales.setdefault(row['Name'], []).append((ngay_ban, so_luong))

        min_x, max_x = None, None

        for idx, (product, sales) in enumerate(product_sales.items()):
            sales.sort()
            dates, amounts = zip(*sales)
            timestamps = [datetime.datetime.strptime(str(d), "%Y-%m-%d") for d in dates]
            all_timestamps.extend(timestamps)

            max_y = max(max_y, max(amounts))

            if min_x is None or timestamps[0] < min_x:
                min_x = timestamps[0]
            if max_x is None or timestamps[-1] > max_x:
                max_x = timestamps[-1]

            color = colors[idx % len(colors)]
            pen = pg.mkPen(color, width=2)
            plot_data = plot_widget.plot(
                [t.timestamp() for t in timestamps],
                amounts,
                pen=pen, symbol='o', symbolBrush=color
            )
            legend.addItem(plot_data, product)

        # Chia trục Y thành 5 mốc
        step_y = max_y / 5 if max_y > 0 else 1
        yticks = [(i * step_y, str(int(i * step_y))) for i in range(6)]
        plot_widget.setYRange(0, max_y)
        plot_widget.getAxis("left").setTicks([yticks])

        # Chia trục X thành 5 mốc ngày
        time_range = (max_x - min_x).total_seconds()
        step_x = time_range / 5
        xticks = [(min_x.timestamp() + i * step_x, (min_x + datetime.timedelta(seconds=i * step_x)).strftime("%d/%m"))
                  for i in range(6)]

        plot_widget.setXRange(min_x.timestamp(), max_x.timestamp())
        x_axis = plot_widget.getAxis("bottom")
        x_axis.setTicks([xticks])

        # Tắt ký hiệu khoa học trên hai trục
        plot_widget.getAxis("left").enableAutoSIPrefix(False)
        plot_widget.getAxis("bottom").enableAutoSIPrefix(False)

    def chart_plot(self, layout):
        data = self.db_manager.fetch_top2_products()
        if not data:
            print("Không có dữ liệu để vẽ biểu đồ.")
            return

        plot_widget = pg.PlotWidget()
        plot_widget.setBackground('w')
        layout.addWidget(plot_widget)

        plot_widget.setLabel("left", "Doanh thu (VNĐ)")
        plot_widget.setLabel("bottom", "Ngày bán")
        plot_widget.setTitle("<b>Doanh thu theo mặt hàng bán chạy trong 30 ngày qua</b>")

        legend = pg.LegendItem(offset=(60, 20))
        legend.setParentItem(plot_widget.getPlotItem())

        colors = ["r", "b", "p", "m", "c", "y"]
        product_revenue = {}
        all_timestamps = []
        all_amounts = []

        for row in data:
            ngay_ban = row['NgayBan']
            doanh_thu = float(row['DoanhThu'])
            product_revenue.setdefault(row['Name'], []).append((ngay_ban, doanh_thu))
            all_amounts.append(doanh_thu)

        max_y = max(all_amounts) if all_amounts else 0
        ytick_step = max_y / 6 if max_y > 0 else 1
        yticks = [(i, f"{int(i):,}") for i in range(0, int(max_y) + int(ytick_step), int(ytick_step))]

        min_x, max_x = None, None

        for idx, (product, revenues) in enumerate(product_revenue.items()):
            revenues.sort()
            dates, amounts = zip(*revenues)
            timestamps = [datetime.datetime.strptime(str(d), "%Y-%m-%d") for d in dates]
            all_timestamps.extend(timestamps)

            if min_x is None or timestamps[0] < min_x:
                min_x = timestamps[0]
            if max_x is None or timestamps[-1] > max_x:
                max_x = timestamps[-1]

            color = colors[idx % len(colors)]
            pen = pg.mkPen(color, width=2)
            plot_data = plot_widget.plot(
                [t.timestamp() for t in timestamps],
                amounts,
                pen=pen, symbol='o', symbolBrush=color
            )
            legend.addItem(plot_data, product)

        # Cập nhật phạm vi hiển thị
        plot_widget.setYRange(0, max_y)
        plot_widget.setXRange(min_x.timestamp(), max_x.timestamp())

        plot_widget.getAxis('left').setTicks([yticks])

        # Chia trục X thành 5 mốc thời gian chính
        time_range = (max_x - min_x).total_seconds()
        step = time_range / 4  # Chia thành 5 điểm (4 khoảng)
        xticks = [(min_x.timestamp() + i * step, (min_x + datetime.timedelta(seconds=i * step)).strftime("%d/%m"))
                  for i in range(5)]

        x_axis = plot_widget.getAxis("bottom")
        x_axis.setTicks([xticks])

        # Tắt hiển thị ký hiệu khoa học trên trục
        plot_widget.getAxis("left").enableAutoSIPrefix(False)
        plot_widget.getAxis("bottom").enableAutoSIPrefix(False)

if __name__ == "__main__":
    db = DatabaseManager(host="34.101.167.101", user="dev", password="12345678x@X", database="kioskapp")
    app = QApplication(sys.argv)
    window = MainWindow(db)
    window.show()
    sys.exit(app.exec())