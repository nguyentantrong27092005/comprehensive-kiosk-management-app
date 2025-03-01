from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QFrame, QLabel, QLayout,
    QStackedWidget,
)
from kiosk_app.views.ClickableElement import ClickableFrame

class StyleFrame(ClickableFrame):
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
            label.setPixmap(pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))  # Scale image to fit
            label.setMaximumSize(120, 120)
            # label.setScaledContents(True)  # Allow dynamic scaling
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            label.setStyleSheet("border-width: 0px")

            layout.addWidget(label)

        label = QLabel()
        label.setText(title)
        label.setStyleSheet("border-width: 0px; font-size: 12px")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer)
        layout.addWidget(label)
        layout.setStretch(0, 5)
        layout.setStretch(1, 5)
        layout.setStretch(2, 1)

        self.setLayout(layout)


class DineSelectWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-family: Montserrat; font-size: 15px; background-color: #BD1906;")
        # Create the main layout
        self.vLayoutWhiteFrame = QVBoxLayout(self)
        self.hLayoutPaymentSelection = QHBoxLayout(self)
        self.vLayoutTitlePayment = QVBoxLayout(self)

        # Create two button sections using the reusable widget
        self.left_section = PaymentSelection(["kiosk_app/resources/images/ic_dineout.png"], "Mang về","lightblue", "navy")
        self.right_section = PaymentSelection(["kiosk_app/resources/images/ic_dinein.png"], "Ăn tại chỗ","lightgreen", "darkgreen")

        # Add a spacer between the sections
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Add sections to the main layout
        self.hLayoutPaymentSelection.addWidget(self.left_section)
        self.hLayoutPaymentSelection.addSpacerItem(spacer)
        self.hLayoutPaymentSelection.addWidget(self.right_section)


        self.paymentTitle = QLabel()
        self.paymentTitle.setText("Vui lòng chọn hình thức phục vụ")
        self.paymentTitle.setStyleSheet("font-weight: 700;")
        self.paymentTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #
        self.vLayoutTitlePayment.addWidget(self.paymentTitle)
        self.vLayoutTitlePayment.addSpacerItem(spacer)
        self.vLayoutTitlePayment.addLayout(self.hLayoutPaymentSelection)
        self.vLayoutTitlePayment.setStretch(1, 7)
        self.vLayoutTitlePayment.setContentsMargins(50, 100, 50, 100)
        self.whiteFrameMainLayout = StyleFrame("white", "white")
        self.whiteFrameMainLayout.setLayout(self.vLayoutTitlePayment)
        self.vLayoutWhiteFrame.addWidget(self.whiteFrameMainLayout)
        self.vLayoutWhiteFrame.setContentsMargins(35, 70, 35, 70)
        self.setLayout(self.vLayoutWhiteFrame)
        self.resize(478, 592)
        self.setMinimumSize(478, 592)



if __name__ == '__main__':
    app = QApplication([])
    window = DineSelectWidget()
    window.show()
    app.exec()
