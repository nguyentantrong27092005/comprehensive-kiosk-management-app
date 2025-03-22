import matplotlib.ticker as mticker
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QTableWidget,
    QHeaderView, QTableWidgetItem
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.dates import DateFormatter


class EVoucherTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(5)
        #self.setSortingEnabled(True)
        self.setHorizontalHeaderLabels(
            ["Tên Chương trình", "Tổng hóa đơn", "Số voucher chưa sử dụng", "Tổng doanh thu", "Tổng giảm giá"])
        header = self.horizontalHeader()
        for col in range(1, 5):
            self.setColumnWidth(col, 190)
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.setStyleSheet("""
        QHeaderView::section {font-family: Arial; font-size: 14px; font-weight: bold; background-color:lightgray;}
        QTableWidget, QTableWidget::item {font-family: Arial; font-size: 12px;}
         {font-size: 12px;}
        """)

    def update_table(self, data):
        self.setRowCount(len(data))
        for row, row_dt in enumerate(data):
            for col, value in enumerate(row_dt.values()):
                if col == 3 or col == 4:
                    formatted_value = f"{float(value):,.0f}"
                    item = QTableWidgetItem(formatted_value)
                else:
                    item = QTableWidgetItem(str(value))

                if col > 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.setItem(row, col, item)


class LineChart(QFrame):
    def __init__(self):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_linechart(self, data):
        self.ax.clear()
        if not data:
            self.canvas.draw()
            return

        dates = data["Ngay"]
        programs = data["TenChuongTrinh"]
        revenues = data["DoanhThu"]
        colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0", "#ffffff"]

        for idx, program in enumerate(programs):
            self.ax.plot(dates, revenues[program], label=program, color=colors[idx % len(colors)], linewidth=1.5)

        self.ax.set_xticks(dates)
        self.ax.xaxis.set_major_formatter(DateFormatter("%d/%m"))
        self.ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{x:,.0f}"))
        self._set_chart_style("Xu hướng doanh thu theo ngày", "Ngày", "Doanh thu")
        self.canvas.draw()

    def _set_chart_style(self, title, xlabel, ylabel):
        font_dict = {'fontsize': 10, 'fontweight': 'bold', 'family': 'Arial'}
        self.ax.set_title(title, fontdict=font_dict)
        self.ax.set_xlabel(xlabel, fontdict=font_dict)
        self.ax.set_ylabel(ylabel, fontdict=font_dict)
        self.ax.tick_params(axis="x", labelsize=8, labelrotation=45)
        self.ax.tick_params(axis="y", labelsize=8)
        self.ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=1, frameon=False,
                       prop={'family': 'Arial', 'size': 8})
        self.figure.tight_layout()
        self.figure.subplots_adjust(bottom=0.4)

class PieChart(QFrame):
    def __init__(self):
        super().__init__()
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_piechart(self, data):
        self.ax.clear()
        if not data:
            self.ax.set_frame_on(False)
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.set_xticklabels([])
            self.ax.set_yticklabels([])
            self.ax.set_title("Phân bổ doanh thu theo chương trình", fontdict={'fontsize': 10, 'fontweight': 'bold', 'family': 'Arial'})
            self.canvas.draw()
            return

        labels = [item["TenChuongTrinh"] for item in data]
        sizes = [item["TongDoanhThu"] for item in data]
        total_revenue = sum(sizes)
        colors = ['#991203', '#BD1906', '#CA4738', '#EBBAB4', '#F8E8E6']

        wedges, texts = self.ax.pie(
            sizes,
            labels=None,
            colors=[colors[min(i, len(colors) - 1)] for i in range(len(sizes))],
            startangle=90,
            labeldistance=None
        )

        percentages = [(size / total_revenue) * 100 for size in sizes]
        legend_labels = [f"{label} ({percent:.1f}%)" for label, percent in zip(labels, percentages)]

        self.ax.legend(
            wedges,
            legend_labels,
            loc="center",
            bbox_to_anchor=(0.5, -0.2),
            ncol=1,
            frameon=False,
            prop={'family': 'Arial', 'size': 8}
        )

        self.ax.set_title("Phân bổ doanh thu theo chương trình", fontdict={'fontsize': 10, 'fontweight': 'bold', 'family': 'Arial'})
        self.figure.tight_layout()
        self.canvas.draw()


class EVoucherWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1080, 600)
        self.evoucherLayout = QVBoxLayout(self)
        self.evoucherLayout.setContentsMargins(0, 0, 0, 0)
        self.evoucherLayout.setSpacing(0)
        self.setup_ui()

    def setup_ui(self):
        self.chartframe = QFrame()
        self.chartframe.setMaximumSize(1080, 500)
        self.chartlayout = QHBoxLayout(self.chartframe)
        self.chartlayout.setContentsMargins(0, 0, 0, 0)
        self.chartlayout.setSpacing(0)

        self.linechart = LineChart()
        self.piechart = PieChart()
        self.chartlayout.addWidget(self.linechart, stretch=0)
        self.chartlayout.addWidget(self.piechart, stretch=0)
        self.evoucherLayout.addWidget(self.chartframe)

        self.table = EVoucherTable()
        self.evoucherLayout.addWidget(self.table)

    def clear_ui(self):
        self.table.setRowCount(0)
        self.linechart.update_linechart({})
        self.piechart.update_piechart([])

    def update_linechart(self, data):
        self.linechart.update_linechart(data)

    def update_piechart(self, data):
        self.piechart.update_piechart(data)

    def update_table(self, data):
        self.table.update_table(data)

    def get_table_data(self):
        # Giả sử self.table_data là dữ liệu hiển thị trên bảng
        return self.table_data  # Trả về dữ liệu bảng đang hiển thị