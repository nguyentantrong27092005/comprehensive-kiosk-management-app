import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QGridLayout, QHBoxLayout

from common.sql_func import Database
from kiosk_app.controllers.MiniGameFullViewEx import MiniGameFullEx
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.views.FeedbacKhachhangView import FeedbackKhachhangView
from kiosk_app.views.GeneralView import GeneralView
from kiosk_app.views.CustomStackedWidget import CustomStackedWidget


class FeedbackKhachhangEx(GeneralView):
    def __init__(self, mainStackedWidget: CustomStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.sharedData = sharedData
        self.db = db
        self.mainStackedWidget = mainStackedWidget
        self.feedbackKH = FeedbackKhachhangView()
        self.updateUI()
        self.feedbackKHLayout = QtWidgets.QVBoxLayout(self.frame_chung)
        self.feedbackKHLayout.addWidget(self.feedbackKH)
        print(f"{self.sharedData.order.id}")

        # **Khởi tạo các biến khác**
        self.current_rating = 0
        self.feedback_buttons = []
        self.is_submitting = False
        self.setup_connections()
        self.frame_ngang.hide()
        self.setStyleSheetAll()

    def updateUI(self):
        # Hàng sao đánh giá
        stars_layout = QHBoxLayout()
        stars_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stars_layout.setSpacing(3)

        self.stars = []
        self.current_rating = 0  # Lưu trạng thái số sao đang chọn

        for i in range(5):
            star_label = QLabel("☆")
            star_label.setStyleSheet("color: black;font-weight: bold;")
            star_label.setFont(QFont("Arial", 22))
            star_label.mousePressEvent = lambda event, index=i: self.set_rating(index + 1)
            stars_layout.addWidget(star_label)
            self.stars.append(star_label)
        self.feedbackKH.layout.addLayout(stars_layout)

        # Nhãn "Tốt" hoặc "Tệ"
        self.rating_label = QLabel("")
        self.rating_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rating_label.setStyleSheet("color: white;")
        self.feedbackKH.layout.addWidget(self.rating_label)

        # Lưới chứa phản hồi
        self.feedback_grid = QGridLayout()
        self.feedback_grid.setSpacing(10)
        self.feedbackKH.layout.addLayout(self.feedback_grid)

        # Danh sách phản hồi
        self.feedback_texts_negative = [
            "Chất lượng phục vụ kém", "Thời gian chờ đợi lâu",
            "Thức ăn không ngon", "Giá quá cao",
            "Nhân viên không thân thiện", "Không gian chật chội"
        ]
        self.feedback_texts_positive = [
            "Phục vụ tốt", "Thời gian chờ hợp lý",
            "Thức ăn ngon", "Giá cả hợp lý",
            "Nhân viên thân thiện", "Không gian thoáng đãng"
        ]

        self.feedback_buttons = []
        self.feedbackKH.layout.addWidget(self.feedbackKH.submit_button)


    def setup_connections(self):
        if hasattr(self, 'stars'):
            for i in range(len(self.stars)):
                self.stars[i].mousePressEvent = self.create_rating_handler(i + 1)

        try:
            self.feedbackKH.submit_button.clicked.disconnect()
        except TypeError:
            pass

        self.feedbackKH.submit_button.clicked.connect(self.submit_feedback)

    def create_rating_handler(self, rating):
        def handler(event):
            self.set_rating(rating)
        return handler

    def set_rating(self, rating):
        self.current_rating = rating

        # Cập nhật hiển thị sao
        if hasattr(self, 'stars'):
            for i, star in enumerate(self.stars):
                star.setText("⭐" if i < rating else "☆")
                star.setStyleSheet(
                    "font-size: 22pt; color: gold;" if i < rating else "font-size: 22pt; color: black;"
                )

        # Cập nhật nhãn đánh giá
        if hasattr(self, 'rating_label'):
            self.rating_label.setText("Tốt" if rating >= 4 else "Tệ")
            list_fb = ["Rất tệ", "Tệ", "Bình thường", "Tốt", "Rất tốt"]
            self.rating_label.setText(f"{list_fb[rating-1]}")
            self.rating_label.setStyleSheet("font-weight: bold; color: gray;")

        # Xóa hết các lựa chọn phản hồi trước đó
        for button in self.feedback_buttons:
            self.feedback_grid.removeWidget(button)
            button.deleteLater()
            button = None
        self.feedback_buttons = []

        # Cập nhật lại danh sách các nút phản hồi phù hợp với số sao
        self.update_feedback_buttons(rating)

    def update_feedback_buttons(self, rating):
        feedback_texts = self.feedback_texts_positive if rating >= 3 else self.feedback_texts_negative
        for i, text in enumerate(feedback_texts):
            button = QtWidgets.QPushButton(text)
            button.setCheckable(True)
            button.setStyleSheet("""
                QPushButton {
                    border: 1px solid #D4CDCD;
                    border-radius: 5px;
                    background-color: white;
                }
            """)
            button.setMinimumSize(135, 50)
            button.clicked.connect(lambda checked, btn=button: self.toggle_feedback_button(btn))
            self.feedback_grid.addWidget(button, i // 2, i % 2)
            self.feedback_buttons.append(button)

    def toggle_feedback_button(self, button):
        if button.isChecked():
            button.setStyleSheet("background-color: #E2E0E0; border-radius: 5px; border: 1px solid #D4CDCD;")
        else:
            button.setStyleSheet("""
                            QPushButton {
                                border: 1px solid #D4CDCD;
                                border-radius: 5px;
                                background-color: white;
                            }
                        """)

    def submit_feedback(self):
        if self.is_submitting:
            return

        self.is_submitting = True

        if not hasattr(self.sharedData, 'order') or not hasattr(self.sharedData.order, 'id'):
            QtWidgets.QMessageBox.critical(self, "Lỗi", "ID đơn hàng không hợp lệ!")
            self.is_submitting = False
            return

        order_id = self.sharedData.order.id

        if not isinstance(order_id, int):
            QtWidgets.QMessageBox.critical(self, "Lỗi", "ID đơn hàng không hợp lệ!")
            self.is_submitting = False
            return

        if self.current_rating == 0:
            QtWidgets.QMessageBox.critical(self, "Lỗi", "Vui lòng chọn số sao trước khi gửi đánh giá!")
            self.is_submitting = False
            return

        selected_reasons = [btn.text() for btn in self.feedback_buttons if btn.isChecked()]

        if self.db.update_customer_feedback(order_id, self.current_rating, selected_reasons):
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Cửa hàng Kiosk")
            msg_box.setText("Cảm ơn bạn đã đánh giá!")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

            # Đợi người dùng bấm OK rồi mới chuyển màn hình
            if msg_box.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                self.open_minigame_view()
                self.sharedData.reset_data()
        else:
            QtWidgets.QMessageBox.critical(self, "Lỗi", "Không thể lưu đánh giá. Vui lòng thử lại!")
        self.is_submitting = False

    def open_minigame_view(self):
        minigameView = MiniGameFullEx(self.mainStackedWidget, self.sharedData, self.db)
        self.mainStackedWidget.change_screen(minigameView, self)
    def setStyleSheetAll(self):
        self.frame_chung.setStyleSheet("background-color: rgb(255, 255, 255);")

