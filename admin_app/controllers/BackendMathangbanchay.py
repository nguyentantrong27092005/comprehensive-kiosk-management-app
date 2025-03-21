import sys
import datetime
import pymysql
import pyqtgraph as pg
from PyQt6.QtCore import Qt, QTimer, QDate
from PyQt6.QtGui import QFont
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QTableWidget,
    QSplitter, QSizePolicy, QTableWidgetItem, QHeaderView, QScrollArea, QMessageBox,     QComboBox, QFileDialog
)
from admin_app.views.GeneralView import GeneralView
from admin_app.controllers.GeneralViewEx import GeneralViewEx
from datetime import datetime, timedelta

from common.sql_func import DatabaseManager


class MathangbanchayEx(GeneralViewEx):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        if not hasattr(self, "frameContent") or self.frameContent is None:
            raise AttributeError("self.frameContent chưa được tạo trong setupUi()")
        self.selected_dates.append(QDate.currentDate().addDays(-30))
        self.selected_dates.append(QDate.currentDate())

        # Thêm combo box nếu frameContent hợp lệ
        self.comboBox.addItem("Tất cả nhóm món")
        categories = self.db_manager.fetch_categories()
        print("Categories to add to combo box:", categories)  # Log kiểm tra

        # Thêm danh sách categories vào combo box
        self.comboBox.addItems(categories)

        # Kết nối sự kiện khi người dùng chọn một nhóm món
        self.comboBox.currentIndexChanged.connect(self.on_select_button_clicked)
        #xuatfile
        self.pushButtonExport.clicked.connect(self.xuatfile)
        # Thêm combo box vào layout
        main_layout = QVBoxLayout(self.frameContent)
        top_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        self.plot_widget = pg.PlotWidget()
        left_layout.addWidget(self.plot_widget)

        right_layout = QVBoxLayout()
        self.revenue_widget = pg.PlotWidget()
        right_layout.addWidget(self.revenue_widget)

        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        top_widget.setFixedHeight(250)
        top_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        top_layout.addLayout(left_layout, 1)
        top_layout.addLayout(right_layout, 1)

        # Sử dụng lineEditSearch và pushButton từ GeneralViewEx
        self.lineEditSearch.setPlaceholderText("Nhập từ khóa tìm kiếm...")
        self.pushButtonSearch.clicked.connect(self.on_select_button_clicked)

        main_layout.addWidget(top_widget, 2)
        self.pushButtonMHBC.setStyleSheet(
            "background-color: white; color: red; font-size: 14px; font-weight: bold;"
        )

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Mã món", "Tên món", "Nhóm món", "Số lượng", "Giảm giá", "Doanh thu", "Lợi nhuận"
        ])
        self.table.setStyleSheet("background-color: white;")
        self.table.setFont(QFont("Arial", 10))
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.verticalHeader().setVisible(False)
        self.load_data()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.table)

        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.addWidget(scroll_area)
        bottom_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        main_layout.addWidget(bottom_widget, 1)

        self.update_plots()
        self.select_button.clicked.connect(self.on_select_button_clicked)

    def on_category_changed(self, index):
        selected_category = self.comboBox.currentText()
        print(f"Selected category: {selected_category}")

        # Gọi load_data với category được chọn
        self.load_data(category=selected_category)

        # Gọi cập nhật biểu đồ sau khi dữ liệu bảng đã thay đổi
        self.update_plots(category=selected_category)

    def load_data(self, start_date=None, end_date=None, keyword=None, category=None):
        # Lấy dữ liệu từ cơ sở dữ liệu dựa trên nhóm món được chọn
        data = self.db_manager.fetch_data(start_date, end_date, keyword, category)
        print(data)
        if not data:
            QMessageBox.warning(None, "No Data", "Không có dữ liệu.")
            return

        # Xóa dữ liệu cũ trong bảng
        self.table.setRowCount(0)

        # Đổ dữ liệu mới vào bảng
        self.table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row["MaMon"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row["TenMon"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row["NhomMon"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row["SoLuong"])))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row["GiamGia"])))
            self.table.setItem(row_idx, 5, QTableWidgetItem(str(row["DoanhThu"])))
            self.table.setItem(row_idx, 6, QTableWidgetItem(str(row["LoiNhuan"])))

        # Cập nhật lại thanh trượt
        self.table.updateGeometry()
        self.table.adjustSize()

    def update_plots(self, keyword=None, category=None):
        self.lineEditSearch.clear()

        data = self.db_manager.fetch_top2_products(keyword=keyword, category=category)

        if not data:
            QMessageBox.warning(None, "No Data", "Không có dữ liệu để vẽ biểu đồ.")
            return

        self.plot_chart(self.plot_widget, data)
        self.chart_plot(self.revenue_widget, data)

    def on_select_button_clicked(self):
        if not self.selected_dates or len(self.selected_dates) < 2:
            QMessageBox.warning(None, "Invalid Date", "Vui lòng chọn đủ ngày bắt đầu và kết thúc.")
            return
        keyword = self.lineEditSearch.text().strip() if self.lineEditSearch.text() is not None or "" else None
        selected_category = self.comboBox.currentText() if self.comboBox.currentText() != "Tất cả nhóm món" else None

        start_date = self.selected_dates[0].toString("yyyy-MM-dd")
        end_date = self.selected_dates[-1].toString("yyyy-MM-dd")

        # Lấy dữ liệu biểu đồ dựa trên khoảng thời gian
        data = self.db_manager.fetch_top2_products(start_date, end_date, keyword=keyword, category=selected_category)
        if not data:
            QMessageBox.warning(None, "No Data", "Không có dữ liệu trong khoảng thời gian này.")
            return
        self.plot_chart(self.plot_widget, data)
        self.chart_plot(self.revenue_widget, data)

        # Lấy dữ liệu bảng dựa trên khoảng thời gian
        self.load_data(start_date, end_date, keyword=keyword, category=selected_category)

    def on_search_button_clicked(self):
        keyword = self.lineEditSearch.text()
        if not keyword:
            QMessageBox.warning(None, "Invalid Input", "Vui lòng nhập từ khóa tìm kiếm.")
            return

        # Cập nhật bảng và biểu đồ dựa trên từ khóa
        self.load_data(keyword=keyword)
        self.update_plots(keyword=keyword)

    def plot_chart(self, plot_widget, data):
        plot_widget.clear()
        plot_widget.setBackground('w')
        plot_widget.setLabel("left", "Số lượng bán")
        plot_widget.setLabel("bottom", "Ngày bán")
        plot_widget.setTitle("<b>Số lượng sản phẩm bán chạy</b>")

        # Xóa ghi chú cũ (nếu có)
        if hasattr(self, 'plot_legend'):
            self.plot_legend.clear()
        else:
            self.plot_legend = pg.LegendItem(offset=(60, 20))
            self.plot_legend.setParentItem(plot_widget.getPlotItem())

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
            timestamps = [datetime.strptime(str(d), "%Y-%m-%d") for d in dates]
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
            self.plot_legend.addItem(plot_data, product)  # Thêm ghi chú mới

        step_y = max_y / 5 if max_y > 0 else 1
        yticks = [(i * step_y, str(int(i * step_y))) for i in range(6)]
        plot_widget.setYRange(0, max_y)
        plot_widget.getAxis("left").setTicks([yticks])

        time_range = (max_x - min_x).total_seconds()
        step_x = time_range / 5
        xticks = [(min_x.timestamp() + i * step_x, (min_x + timedelta(seconds=i * step_x)).strftime("%d/%m"))
                  for i in range(6)]

        plot_widget.setXRange(min_x.timestamp(), max_x.timestamp())
        x_axis = plot_widget.getAxis("bottom")
        x_axis.setTicks([xticks])

        plot_widget.getAxis("left").enableAutoSIPrefix(False)
        plot_widget.getAxis("bottom").enableAutoSIPrefix(False)

    def chart_plot(self, plot_widget, data):
        plot_widget.clear()
        plot_widget.setBackground('w')
        plot_widget.setLabel("left", "Doanh thu (VNĐ)")
        plot_widget.setLabel("bottom", "Ngày bán")
        plot_widget.setTitle("<b>Doanh thu theo mặt hàng bán chạy</b>")

        # Xóa ghi chú cũ (nếu có)
        if hasattr(self, 'revenue_legend'):
            self.revenue_legend.clear()
        else:
            self.revenue_legend = pg.LegendItem(offset=(60, 20))
            self.revenue_legend.setParentItem(plot_widget.getPlotItem())

        colors = ["r", "b", "p", "m", "c", "y"]
        product_revenue = {}
        all_amounts = []
        all_timestamps = []  # Khai báo biến all_timestamps

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
            timestamps = [datetime.strptime(str(d), "%Y-%m-%d") for d in dates]
            all_timestamps.extend(timestamps)  # Sử dụng biến all_timestamps

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
            self.revenue_legend.addItem(plot_data, product)  # Thêm ghi chú mới

        plot_widget.setYRange(0, max_y)
        plot_widget.setXRange(min_x.timestamp(), max_x.timestamp())
        plot_widget.getAxis('left').setTicks([yticks])

        time_range = (max_x - min_x).total_seconds()
        step = time_range / 4
        xticks = [(min_x.timestamp() + i * step, (min_x + timedelta(seconds=i * step)).strftime("%d/%m"))
                  for i in range(5)]

        x_axis = plot_widget.getAxis("bottom")
        x_axis.setTicks([xticks])

        plot_widget.getAxis("left").enableAutoSIPrefix(False)
        plot_widget.getAxis("bottom").enableAutoSIPrefix(False)

    def xuatfile(self):
        # Lấy số hàng và cột từ bảng
        row_count = self.table.rowCount()
        col_count = self.table.columnCount()

        if row_count == 0 or col_count == 0:
            QMessageBox.warning(self, "Lỗi", "Không có dữ liệu để xuất")
            return

        # Chuẩn bị dữ liệu từ bảng
        headers = [self.table.horizontalHeaderItem(i).text() for i in range(col_count)]
        data = []
        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        # Hiển thị hộp thoại chọn file
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Lưu file Excel", "", "Excel Files (*.xlsx)"
        )

        if not file_path:  # Người dùng hủy
            return

        try:
            # Tạo DataFrame và xuất file
            df = pd.DataFrame(data, columns=headers)
            df.to_excel(file_path, index=False, engine="openpyxl")
            QMessageBox.information(
                self, "Thành công", f"Đã xuất file Excel thành công tại:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Lỗi", f"Lỗi khi xuất file Excel:\n{str(e)}"
            )

if __name__ == "__main__":
    # Khởi tạo kết nối cơ sở dữ liệu
    db = DatabaseManager(host="34.80.75.195", user="dev", password="KTLTnhom4@", database="kioskapp")

    # Khởi chạy ứng dụng PyQt
    app = QApplication(sys.argv)
    window = MathangbanchayEx(db)
    window.show()
    sys.exit(app.exec())