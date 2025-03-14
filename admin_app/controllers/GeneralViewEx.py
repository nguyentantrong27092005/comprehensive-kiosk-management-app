import sys

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QTextCharFormat, QBrush, QColor
from PyQt6.QtCore import QDate



from admin_app.views.GeneralView import GeneralView


class GeneralViewEx(GeneralView):
    def __init__(self):
        super().__init__()
        self.lineEditDate.setPlaceholderText("Chọn thời gian")
        self.lineEditDate.setReadOnly(True)
        self.selected_dates = []

        self.calendarFrame = QtWidgets.QFrame(self)
        self.calendarFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.calendarFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.calendarFrame.setParent(self)

        self.calendarLayout = QtWidgets.QGridLayout(self.calendarFrame)
        self.calendarFrame.setVisible(False)

        # Calendar widget
        self.calendar = QtWidgets.QCalendarWidget()
        self.calendar.setMaximumDate(QDate.currentDate())
        self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)  # Ẩn số thứ tự
        self.calendar.setStyleSheet("""
                            QCalendarWidget {
                                border: 1px solid #ccc;
                                border-radius: 10px;
                                font-size: 13px;
                                background-color: white;
                            }
                            QCalendarWidget QAbstractItemView {
                                selection-background-color: #bd1906;
                                selection-color: white;
                                font-weight: 400;
                            }
                            QTableView {
                                border-radius: 10px;
                            }
                            QCalendarWidget QToolButton {
                                background-color: #ffffff;
                                color: black;
                                border-radius: 5px;
                                padding: 5px;
                                min-width: 90px;
                                min-height: 34px;
                                font-weight: 400;
                            }
                            QCalendarWidget QWidget#qt_calendar_navigationbar { 
                                background-color: #ffffff;
                            }
                            QCalendarWidget QWidget            
                            #qt_calendar_nextmonth { 
                                border: none;
                                qproperty-icon: url('admin_app/resources/images/icon_next.png');
                                min-width: 16px;
                                min-height: 8px;
                                border-radius: 10px;
                                }
                            #qt_calendar_prevmonth {
                                border: none;
                               qproperty-icon: url('admin_app/resources/images/icon_back.png');
                               min-width: 16px;
                                min-height: 8px;
                                border-radius: 10px;
                                }
                            #qt_calendar_monthbutton {
                                min-width: 90px;
                                min-height: 34px;
                                padding-left: 0 6px;
                                border: none;
                            }
                            #qt_calendar_monthbutton::menu-indicator {
                                subcontrol-origin: padding; 
                                subcontrol-position: right center; 
                                margin-left: 12px;
                                margin-right: 8px;
                                }
                            #qt_calendar_yearedit {
                                border: none;
                                min-width: 60px;
                                min-height: 42px;
                                padding: 0px 2px;
                                margin-left: 5px;
                                qproperty-alignment: AlignCenter;}
                            #qt_calendar_yearedit::up-button {
                               image: url('admin_app/resources/images/icon_yearup.png');
                                min-width: 4px;
                                min-height: 4px;
                                padding: 2px;
                                margin: 0px;
                                subcontrol-position: right;
                                }
                            #qt_calendar_yearedit::down-button {
                                image: url("admin_app/resources/images/icon_yeardown.png");
                                min-width: 4px;   
                                min-height: 4px;
                                padding: 2px;
                                margin: 0px;

                                subcontrol-position: left;
                                }
                            #calendarWidget QToolButton::menu-indicator{
                                nonsubcontrol-origin: margin;
                                margin-left: 5px; 
                                margin-right: 10px;}

                        """)

        # Nút chọn ngày
        self.select_button = QtWidgets.QPushButton("Chọn")
        self.select_button.setStyleSheet("""
                            QPushButton {
                                background-color: #bd1906;
                                color: white;
                                font-size: 16px;
                                padding: 10px;
                                border-radius: 10px;
                                font-weight: bold;
                            }
                            QPushButton:pressed {
                                background-color: #ffffff;
                            }
                        """)
        self.cancel_button =QtWidgets.QPushButton("Huỷ")
        self.cancel_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #bd1906;
                                        color: white;
                                        font-size: 16px;
                                        padding: 10px;
                                        border-radius: 10px;
                                        font-weight: bold;
                                    }
                                    QPushButton:pressed {
                                        background-color: #ffffff;
                                    }
                                    QCalendarWidget QTableView {
                                        font-size: 8px;
                                    }
                                            """)
        self.calendarLayout.addWidget(self.calendar, 0, 0, 1, 2)
        self.calendarLayout.setAlignment(self.calendar, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.calendarLayout.addWidget(self.cancel_button, 1, 0, 1, 1)
        self.calendarLayout.addWidget(self.select_button, 1, 1, 1, 1)
        self.calendarFrame.setFixedSize(300, 315)
        self.calendarLayout.setContentsMargins(0, 0, 0, 0)

        self.signalandslot()


    def signalandslot(self):
        self.calendar.clicked.connect(self.handle_date_selection)
        self.cancel_button.clicked.connect(self.hideCalendar)
        self.lineEditDate.mousePressEvent = lambda event: self.showCalendar(event, self.lineEditDate)
        self.select_button.clicked.connect(lambda lineedit: self.showSelectedDate(self.lineEditDate))
    def showSelectedDate(self, lineEditDate):
        self.calendarFrame.setVisible(False)
        dates = "-".join([date.toString("dd/MM/yyyy") for date in self.selected_dates])
        lineEditDate.setText(str(dates))

    def hideCalendar(self):
        self.calendarFrame.setVisible(False)
        self.selected_dates =[]


    def handle_date_selection(self, date):
        """Xử lý khi người dùng chọn ngày"""
        if date in self.selected_dates:
            self.selected_dates.remove(date)
        else:
            if len(self.selected_dates) < 2:
                self.selected_dates.append(date)
            else:
                self.selected_dates = [date]  # Reset nếu chọn ngày thứ 3

        self.selected_dates.sort()
        self.update_highlighted_dates()

    def update_highlighted_dates(self):
        """Thêm màu đỏ ngày chọn"""
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())

        if len(self.selected_dates) == 1:
            self.highlight_dates([self.selected_dates[0]], [])
        elif len(self.selected_dates) == 2:
            start, end = self.selected_dates
            range_dates = [start.addDays(i) for i in range(1, start.daysTo(end))] if start < end else []
            self.highlight_dates([start, end], range_dates)

    def highlight_dates(self, selected_dates, range_dates):
        """Thêm màu dải ngày"""
        selected_fmt = QTextCharFormat()
        selected_fmt.setBackground(QBrush(QColor("#bd1906")))
        selected_fmt.setForeground(QBrush(QColor("white")))

        range_fmt = QTextCharFormat()
        range_fmt.setBackground(QBrush(QColor("#f5ddda")))
        range_fmt.setForeground(QBrush(QColor("#bd1906")))

        for date in selected_dates:
            self.calendar.setDateTextFormat(date, selected_fmt)

        for date in range_dates:
            self.calendar.setDateTextFormat(date, range_fmt)

    def update_calendar(self):
        """Cập nhật lịch khi chọn tháng/năm khác"""
        selected_date = self.calendar.selectedDate()
        # selected_year = int(self.year_selector.currentText())
        selected_year = selected_date.year()
        print(selected_year)
        selected_month = self.month_selector.currentIndex() + 1
        self.calendar.setCurrentPage(selected_year, selected_month)
        # Danh sách ngày đã chọn
    def showCalendar(self, event, lineEdit):
        pos_lineEdit = lineEdit.mapToGlobal(lineEdit.rect().bottomLeft())
        # Tính toán vị trí hiển thị lịch
        cal_width = self.calendarFrame.width()
        cal_height = self.calendarFrame.height()
        screen_rect = QtWidgets.QApplication.primaryScreen().geometry()
        # Nếu lịch bị lấp bên phải màn hình -> đẩy sang trái
        if pos_lineEdit.x() + cal_width > screen_rect.right():
            pos_lineEdit.setX(screen_rect.right() - cal_width - 85)
        self.calendarFrame.move(pos_lineEdit)
        self.calendarFrame.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = GeneralViewEx()
    window.show()
    sys.exit(app.exec())