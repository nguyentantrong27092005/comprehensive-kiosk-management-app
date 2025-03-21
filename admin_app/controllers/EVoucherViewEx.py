import sys
from datetime import datetime, date, timedelta
from heapq import nlargest

import pandas as pd
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QFileDialog, QMessageBox, QStackedWidget
from collections import defaultdict

from admin_app.controllers.GeneralViewEx import GeneralViewEx
from admin_app.models.SharedDataModel import SharedDataModel
from admin_app.views import EVoucherView
from admin_app.views.GeneralView import GeneralView
from common.sql_func import Database


class EVoucherWidgetViewEx(GeneralViewEx, GeneralView):
    def __init__(self, mainStackedWidget: QStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.mainStackedWidget = mainStackedWidget
        self.db = db

        self.evoucherWidget = EVoucherView.EVoucherWidget()
        # layout chính
        self.evoucherLayout = QVBoxLayout(self.frameContent)
        self.evoucherLayout.addWidget(self.evoucherWidget)

        self.lineEditSearch.hide()
        self.pushButtonSearch.hide()
        self.comboBox.hide()
        # kết nối
        self.select_button.clicked.connect(self.update_dates)
        self.pushButtonExport.clicked.connect(self.export_to_excel)

        #tải dữ liệu lúc đầu, 7 ngày mặc định
        today = date.today()
        self.start_date = today - timedelta(days=7)
        self.end_date = today
        self.load_data(self.start_date, self.end_date)

    def update_dates(self):
        if len(self.selected_dates) == 2:
            self.start_date, self.end_date = self.selected_dates
        elif len(self.selected_dates) == 1:
            self.start_date = self.selected_dates[0]
            self.end_date = self.selected_dates[0]
        else:
            QMessageBox.warning(self, "Lỗi", "Không có ngày nào được chọn")
            return

        print(f"ngày nè: {self.start_date, self.end_date}")
        self.load_data(self.start_date, self.end_date)

    def load_data(self, start_date, end_date):
        self.evoucherWidget.clear_ui()
        self.data = self.fetch_data(start_date, end_date)
        if self.data:
            self.evoucherWidget.update_piechart(self.data["pie_chart_process"])
            self.evoucherWidget.update_linechart(self.data["line_chart_process"])
            self.evoucherWidget.update_table(self.data["table_data"])

    def get_datetime_range(self, start_date, end_date):
        """chuyển đổi ngày thành chuỗi định dạng SQL"""
        if isinstance(start_date, QDate):  # Nếu là QDate thì chuyển đổi
            start_date = start_date.toPyDate()
        if isinstance(end_date, QDate):
            end_date = end_date.toPyDate()
        start_str = start_date.strftime("%Y-%m-%d 00:00:00")
        end_str = end_date.strftime("%Y-%m-%d 23:59:59")
        return start_str, end_str

    def fetch_data(self, start_date, end_date):
        print(f"Debug: start_date = {start_date}, end_date = {end_date}")
        start_str, end_str = self.get_datetime_range(start_date, end_date)

        # pie chart query
        pie_chart_query = """
            SELECT 
                ev.Name AS TenChuongTrinh,  
                o.SoHoaDon,
                COUNT(CASE WHEN evggl.IsUsed = 0 THEN 1 ELSE NULL END) AS SoVoucherChuaSuDung,
                o.TongDoanhThu,  
                o.TongGiamGia  
            FROM evoucher ev
            INNER JOIN evouchergiamgia evgg ON ev.ID = evgg.EVoucherID
            LEFT JOIN evouchergiamgialist evggl ON evgg.ID = evggl.EVoucherGiamGiaID
            INNER JOIN (
                SELECT evgg.ID, 
                       COUNT(o.EVoucherGiamGiaID) AS SoHoaDon,
                       SUM(o.TotalPrice) AS TongDoanhThu,
                       SUM(o.EVoucherDiscount) AS TongGiamGia
                FROM evouchergiamgia evgg
                LEFT JOIN `order` o ON evgg.ID = o.EVoucherGiamGiaID
                WHERE o.CreateAt BETWEEN %s AND %s
                GROUP BY evgg.ID
            ) o ON evgg.ID = o.ID
            GROUP BY evgg.ID

            UNION ALL
            SELECT 
                ev.Name AS TenChuongTrinh,  
                COUNT(DISTINCT o.ID) AS SoHoaDon,
                (
                    SELECT COUNT(*) 
                    FROM evouchertangmonlist evtml 
                    JOIN evouchertangmon evtm_sub ON evtm_sub.ID = evtml.EVoucherTangMonID
                    JOIN evoucher ev_sub ON ev_sub.ID = evtm_sub.EVoucherID
                    WHERE ev_sub.Name = ev.Name 
                      AND evtml.IsUsed = 0
                ) AS SoVoucherChuaSuDung,
                SUM(o.TotalPrice) AS TongDoanhThu,  
                SUM(od.Price * od.Amount) AS TongGiamGia  
            FROM `orderdetails` od 
            JOIN evouchertangmon evtm ON evtm.ID = od.EVoucherTangMonID  
            JOIN evoucher ev ON ev.ID = evtm.EVoucherID  
            JOIN `order` o ON o.ID = od.OrderID
            WHERE o.CreateAt BETWEEN %s AND %s
            GROUP BY ev.Name

            UNION ALL
            SELECT 
                p.Name AS TenChuongTrinh,
                COUNT(DISTINCT o.ID) AS SoHoaDon,
                NULL AS SoVoucherChuaSuDung,
                SUM(o.TotalPrice) AS TongDoanhThu,
                SUM(od.Amount * 
                    CASE 
                        WHEN p.IsPercent = 1 THEN (od.Price * p.Discount / 100)  
                        ELSE od.Discount  
                    END
                ) AS TongGiamGia
            FROM `order` o
            JOIN `orderdetails` od ON o.ID = od.OrderID
            JOIN `promotion` p ON p.ID = od.PromotionID
            WHERE o.CreateAt BETWEEN %s AND %s
            GROUP BY p.Name
        """
        params_pie = (start_str, end_str)*3
        pie_data_raw = self.db.fetch_data(pie_chart_query, *params_pie)

        # lấy top 5 loại chương trình có doanh thu cao nhất
        top_n = 5
        pie_data_process = nlargest(top_n, pie_data_raw, key=lambda x: x.get("TongDoanhThu", 0))
        # tính doanh thu khác (số chương trình > 5)
        if len(pie_data_raw) > top_n:
            total_revenue = 0
            for item in pie_data_raw:
                total_revenue = total_revenue + item.get("TongDoanhThu")

            top_n_revenue = 0
            for item in pie_data_process:
                top_n_revenue = top_n_revenue + item.get("TongDoanhThu")

            other_total = total_revenue - top_n_revenue
            if other_total > 0:
                pie_data_process.append({"TenChuongTrinh": "Khác", "TongDoanhThu": other_total})

        # line chart query
        line_chart_query = """
            WITH AllPrograms AS (
                SELECT ev.Name AS TenChuongTrinh, o.CreateAt, o.TotalPrice
                FROM evoucher ev
                JOIN evouchergiamgia evgg ON ev.ID = evgg.EVoucherID
                LEFT JOIN `order` o ON evgg.ID = o.EVoucherGiamGiaID
                WHERE o.CreateAt BETWEEN %s AND %s
            
                UNION ALL
                SELECT ev.Name AS TenChuongTrinh, o.CreateAt, o.TotalPrice
                FROM `order` o
                JOIN orderdetails od ON o.ID = od.OrderID
                JOIN evouchertangmon evtm ON evtm.ID = od.EVoucherTangMonID
                JOIN evoucher ev ON ev.ID = evtm.EVoucherID
                WHERE o.CreateAt BETWEEN %s AND %s
            
                UNION ALL
                SELECT p.Name AS TenChuongTrinh, o.CreateAt, o.TotalPrice
                FROM `order` o
                JOIN orderdetails od ON o.ID = od.OrderID
                JOIN promotion p ON p.ID = od.PromotionID
                WHERE o.CreateAt BETWEEN %s AND %s
            ),
            TopPrograms AS (
                SELECT TenChuongTrinh
                FROM AllPrograms
                GROUP BY TenChuongTrinh
                ORDER BY SUM(TotalPrice) DESC
                LIMIT 5
            )
            SELECT DATE(CreateAt) AS Ngay, TenChuongTrinh, SUM(TotalPrice) AS TongDoanhThu
            FROM AllPrograms
            WHERE TenChuongTrinh IN (SELECT TenChuongTrinh FROM TopPrograms)
            GROUP BY DATE(CreateAt), TenChuongTrinh;
        """
        params_line = (start_str, end_str) * 3
        line_data = self.db.fetch_data(line_chart_query, *params_line)
        line_chart_process = self.process_line_chart_data(line_data)

        return {
            "pie_chart_process": pie_data_process,
            "line_chart_process": line_chart_process,
            "table_data": pie_data_raw
        }
    def process_line_chart_data(self, line_data):
        """xử lý dữ liệu để tạo biểu đồ đường
        các dòng dữ liệu -> dạng dict"""
        line_chart_dict = defaultdict(lambda: defaultdict(float))
        all_dates = set()
        all_programs = set()

        # Duyệt qua từng dòng dữ liệu và gom nhóm theo ngày & chương trình
        for row in line_data:
            date_str = row["Ngay"].strftime("%Y-%m-%d")
            program = row["TenChuongTrinh"]
            revenue = float(row["TongDoanhThu"] or 0)

            line_chart_dict[date_str][program] += revenue
            all_dates.add(date_str)
            all_programs.add(program)

        # Sắp xếp ngày theo thứ tự tăng dần
        sorted_dates = sorted(all_dates, key=lambda x: datetime.strptime(x, "%Y-%m-%d"))

        # Đảm bảo mỗi chương trình có dữ liệu trong tất cả các ngày
        revenue_dict = {program: [line_chart_dict[date].get(program, 0) for date in sorted_dates] for program in
                        all_programs}

        return {
            "Ngay": [datetime.strptime(date, "%Y-%m-%d") for date in sorted_dates],
            "TenChuongTrinh": list(all_programs),
            "DoanhThu": revenue_dict
        }

    def export_to_excel(self):
        table_data = self.data.get("table_data", [])
        if not table_data:
            QMessageBox.warning(self, "Lỗi", "Không có dữ liệu để xuất")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Lưu file Excel", "", "Excel Files (*.xlsx)")

        # người dùng chọn cancel
        if not file_path:
            return
        try:
            data_to_export = []
            for row in table_data:
                data_row = {"Tên chương trình": row.get("TenChuongTrinh"),
                              "Số hóa đơn": row.get("SoHoaDon"),
                              "Số voucher chưa sử dụng": row.get("SoVoucherChuaSuDung", ""),
                              "Tổng doanh thu": int(row.get("TongDoanhThu")),
                              "Tổng giảm giá": int(row.get("TongGiamGia"))}
                data_to_export.append(data_row)
            df = pd.DataFrame(data_to_export)
            df.to_excel(file_path, index=False, engine="openpyxl")
            QMessageBox.information(self, "Thành công", f"Đã xuất file Excel tại {file_path}")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi xuất file Excel: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainStackedWidget = QtWidgets.QStackedWidget()
    sharedData = SharedDataModel()
    db = Database()
    window = EVoucherWidgetViewEx(mainStackedWidget, sharedData, db)
    window.show()
    sys.exit(app.exec())