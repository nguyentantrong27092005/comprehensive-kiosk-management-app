from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QFrame, QLabel, QLayout,
)

class StyleFrame(QFrame):
    def __init__(self, bg_color, border_color, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
                    QFrame {{
                        background-color: {bg_color};
                        border: 2px solid {border_color};
                        border-radius: 15px;
                    }}
                """)
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Plain)


class PaymentSelection(StyleFrame):  # Change QWidget to QFrame
    def __init__(self, images, title, bg_color, border_color, parent=None):
        super().__init__(bg_color, border_color, parent)

        # Set fixed height to ensure the border appears
        # self.setMinimumHeight(60)
        # self.setMinimumWidth(140)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Create a layout for the buttons
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)  # Ensure padding inside the border

        # Add buttons
        for img_path in images:
            label = QLabel()
            label.setMargin(10)
            pixmap = QPixmap(img_path)  # Load the image
            label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))  # Scale image to fit
            label.setMinimumSize(60, 60)
            label.setMaximumSize(120, 120)
            label.setScaledContents(True)  # Allow dynamic scaling
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            label.setStyleSheet("border-width: 0px")

            layout.addWidget(label)

        label = QLabel()
        label.setText(title)
        label.setStyleSheet("border-width: 0px; font-size: 12px")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer)
        layout.addWidget(label)
        layout.setStretch(0, 5)
        layout.setStretch(1, 5)
        layout.setStretch(2, 1)

        self.setLayout(layout)


class Payment(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-family: Montserrat; font-size: 15px; background-color: #BD1906;")
        # Create the main layout
        self.vLayoutRedFrame = QVBoxLayout(self)
        self.hLayoutPaymentSelection = QHBoxLayout(self)
        self.vLayoutTitlePayment = QVBoxLayout(self)

        self.mainLayout = QHBoxLayout(self)


        # Create two button sections using the reusable widget
        left_section = PaymentSelection(["../resources/images/bi_cash-coin.png", "../resources/images/icon_cashregister.png"], "Tiền mặt","lightblue", "navy")
        right_section = PaymentSelection(["../resources/images/banktransfer.png", "../resources/images/icon_scanqrcode.png"], "Chuyển khoản","lightgreen", "darkgreen")

        # Add a spacer between the sections
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Add sections to the main layout
        self.hLayoutPaymentSelection.addWidget(left_section)
        self.hLayoutPaymentSelection.addSpacerItem(spacer)
        self.hLayoutPaymentSelection.addWidget(right_section)


        self.paymentTitle = QLabel()
        self.paymentTitle.setText("Vui lòng chọn hình thức thanh toán")
        self.paymentTitle.setStyleSheet("font-weight: 700;")
        self.paymentTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #
        self.vLayoutTitlePayment.addWidget(self.paymentTitle)
        self.vLayoutTitlePayment.addSpacerItem(spacer)
        self.vLayoutTitlePayment.addLayout(self.hLayoutPaymentSelection)
        self.vLayoutTitlePayment.setStretch(1, 7)
        self.vLayoutTitlePayment.setContentsMargins(50, 50, 50, 50)
        self.whiteFrameMainLayout = StyleFrame("white", "white")
        self.whiteFrameMainLayout.setLayout(self.vLayoutTitlePayment)
        self.vLayoutWhiteFrame = QVBoxLayout(self)
        self.vLayoutWhiteFrame.addWidget(self.whiteFrameMainLayout)
        self.redFrameMainLayout = QFrame(self)
        self.redFrameMainLayout.setStyleSheet("background-color: #BD1906;")
        # self.redFrameMainLayout
        self.redFrameMainLayout.setLayout(self.vLayoutWhiteFrame)
        self.vLayoutRedFrame.addWidget(self.redFrameMainLayout)
        self.vLayoutRedFrame.setContentsMargins(26, 64, 26, 64)
        # self.mainLayout.addWidget(self.redFrameMainLayout)
        self.setLayout(self.vLayoutRedFrame)
        self.setWindowTitle("PyQt6 - Modular Button Sections with Borders")
        self.resize(478, 592)
        self.setMinimumSize(478, 592)

if __name__ == '__main__':
    app = QApplication([])
    window = Payment()
    window.show()
    app.exec()
