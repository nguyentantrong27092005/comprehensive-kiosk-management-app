from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QSize
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        self.setMinimumSize(478, 850)
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)

        # Hình ảnh burger
        self.image_label = QLabel()
        pixmap = QPixmap("burger.jpg")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedHeight(180)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        # Nhãn tiêu đề
        self.title_label = QLabel("Đánh giá của khách hàng")
        self.title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFixedHeight(25)
        layout.addWidget(self.title_label)

        # Hàng sao đánh giá
        stars_layout = QHBoxLayout()
        stars_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stars_layout.setSpacing(3)

        self.stars = []
        self.current_rating = 0  # Lưu trạng thái số sao đang chọn

        for i in range(5):
            star_label = QLabel("☆")
            star_label.setFont(QFont("Arial", 22))
            star_label.setStyleSheet("color: black;")
            star_label.mousePressEvent = lambda event, index=i: self.set_rating(index + 1)
            stars_layout.addWidget(star_label)
            self.stars.append(star_label)

        layout.addLayout(stars_layout)

        # Nhãn "Tốt" hoặc "Tệ"
        self.rating_label = QLabel("")
        self.rating_label.setFont(QFont("Arial", 10))
        self.rating_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rating_label.setStyleSheet("color: white;")
        layout.addWidget(self.rating_label)

        # Lưới chứa phản hồi
        self.feedback_grid = QGridLayout()
        self.feedback_grid.setSpacing(5)
        layout.addLayout(self.feedback_grid)

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
        self.update_feedback_buttons(3)  # Mặc định hiển thị phản hồi tiêu cực

        # Nút gửi
        self.submit_button = QPushButton(" Gửi")
        self.submit_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.submit_button.setStyleSheet("background-color: red; color: white; padding: 10px; border-radius: 5px; width: 100%;")
        self.submit_button.setIcon(QIcon("icon.png"))
        self.submit_button.setIconSize(QSize(24, 24))
        self.submit_button.setMinimumHeight(50)
        self.submit_button.clicked.connect(self.show_thank_you_message)  # Hiển thị message box khi bấm nút
        layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def set_rating(self, rating):
        """Cập nhật màu sao và hiển thị chữ Tốt/Tệ"""
        self.current_rating = rating
        for i in range(5):
            if i < rating:
                self.stars[i].setText("⭐")
                self.stars[i].setStyleSheet("color: gold;")
            else:
                self.stars[i].setText("☆")
                self.stars[i].setStyleSheet("color: black;")

        # Cập nhật nhãn chữ
        if rating >= 4:
            self.rating_label.setText("Tốt")
            self.rating_label.setStyleSheet("color: gray; font-size: 12px; font-weight: bold;")
        else:
            self.rating_label.setText("Tệ")
            self.rating_label.setStyleSheet("color: gray; font-size: 12px; font-weight: bold;")

        # Cập nhật phản hồi
        self.update_feedback_buttons(rating)

    def update_feedback_buttons(self, rating):
        """Cập nhật danh sách nút phản hồi với hiệu ứng đổi màu khi bấm"""
        # Xóa nút phản hồi cũ
        for btn in self.feedback_buttons:
            btn.setParent(None)

        self.feedback_buttons = []

        # Chọn danh sách phản hồi phù hợp
        feedback_texts = self.feedback_texts_positive if rating >= 4 else self.feedback_texts_negative

        # Tạo nút phản hồi mới
        for i, text in enumerate(feedback_texts):
            button = QPushButton(text)
            button.setFont(QFont("Arial", 9))
            button.setStyleSheet("padding: 6px; background-color: lightgray; border-radius: 5px;")
            button.setCheckable(True)  # Cho phép bật/tắt trạng thái
            button.clicked.connect(lambda checked, btn=button: self.toggle_feedback_button(btn))
            self.feedback_grid.addWidget(button, i // 2, i % 2)
            self.feedback_buttons.append(button)

    def toggle_feedback_button(self, button):
        """Hàm đổi màu khi nhấn vào nút phản hồi"""
        if button.isChecked():
            button.setStyleSheet("padding: 6px; background-color: green; color: white; border-radius: 5px;")
        else:
            button.setStyleSheet("padding: 6px; background-color: lightgray; border-radius: 5px;")

    def show_thank_you_message(self):
        """Hiển thị hộp thoại cảm ơn khi nhấn nút Gửi"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Cửa hàng Kiosk")
        msg_box.setText("Cảm ơn bạn đã gửi đánh giá!")
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
