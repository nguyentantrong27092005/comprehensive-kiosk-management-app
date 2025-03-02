import time
import qrcode
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QPainter
from common.sql_func import Database
from kiosk_app.controllers.BankCancelDialogEx import BankCancelDialogEx
from kiosk_app.controllers.BankFailedViewEx import BankFailedViewEx
from kiosk_app.controllers.BankSuccessViewEx import BankSuccessViewEx
from kiosk_app.models.EnumClasses import OrderStatus
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.views import BankQRView, GeneralView
from PyQt6.QtWidgets import QVBoxLayout, QStackedWidget
from kiosk_app.controllers.BankPaymentHandler import BankPaymentHandler

class Image(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size, qrcode_modules):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QImage(
            size, size, QImage.Format.Format_RGB16)
        self._image.fill(Qt.GlobalColor.white)

    def pixmap(self):
        return QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            Qt.GlobalColor.black)

    def save(self, stream, kind=None):
        pass


class PaymentCheckThread(QThread):
    """Đây là class sử dụng Thread để chạy kiểm tra trạng thái của thanh toán concurrently với những hoạt động trên UI."""
    paymentReceived = pyqtSignal()  # Signal to emit when payment is successful
    paymentFailed = pyqtSignal()  # Signal for timeout

    def __init__(self, bankPaymentHandler: BankPaymentHandler, timeout=300):
        super().__init__()
        self.bankPaymentHandler = bankPaymentHandler
        self.running = True
        self.timeout = timeout  # Maximum time to wait (seconds)
        self.elapsedTime = 0

    def run(self):
        """Kiểm tra status của thanh toán mỗi ~2s"""
        while self.running and self.elapsedTime < self.timeout:
            startTime = time.perf_counter()
            time.sleep(2)
            status = self.bankPaymentHandler.get_payment_status()
            if status == "PAID":
                self.paymentReceived.emit()
                return
            elif status == "EXPIRED":
                self.paymentFailed.emit()
                return
            endTime = time.perf_counter()
            self.elapsedTime += endTime - startTime

        # If loop exits due to timeout
        if self.running:
            self.paymentFailed.emit()

    def stop(self):
        """Dừng thread"""
        self.running = False

class BankQRViewEx(GeneralView.GeneralView):
    def __init__(self, mainStackedWidget: QStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.mainStackedWidget = mainStackedWidget
        self.sharedData = sharedData
        self.db = db
        self.bankPaymentHandler = BankPaymentHandler()
        self.bankPaymentHandler.create_payment(sharedData.order)
        self.bankQRView = BankQRView.BankQRWidget()
        if self.bankPaymentHandler.currentPaymentLink is not None:
            self.bankQRView.qrCodeImage.setPixmap(qrcode.make(self.bankPaymentHandler.currentPaymentLink.qrCode, box_size=8, image_factory=Image).pixmap().scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
        self.paymentVLayout = QVBoxLayout(self.frame_chung)
        self.paymentVLayout.addWidget(self.bankQRView)
        self.paymentVLayout.setContentsMargins(0, 0, 0, 0)
        self.count = 300 #Mã có hiệu lực trong vòng 5'
        self.bankQRView.countdownTimerLabel.setText(self.secs_to_minsec(self.count))
        self.bankQRView.countdownTimer.timeout.connect(self.show_time)

        #Hiện dialog khi click nút back
        self.pushButton_back.clicked.connect(self.click_back_button)

        #Mở thread để kiểm tra trạng thái thanh toán
        self.paymentCheckThread = PaymentCheckThread(self.bankPaymentHandler)
        self.paymentCheckThread.paymentReceived.connect(self.on_payment_received)
        self.paymentCheckThread.paymentFailed.connect(self.on_payment_timeout)
        self.paymentCheckThread.start()

    def on_payment_received(self):
        """Hàm này sẽ được thực hiện khi check đơn hàng đã được thanh toán. Nó sẽ thực hiện các tác vụ sau:
        - Update status vào db
        - Reset data (bước này chỉ để test, thực tế nó sẽ thực hiện sau khi người dùng feedback)
        - Chuyển sang màn hình thông báo giao dịch thành công.
        - Huỷ màn hình hiện tại"""
        self.update_order_status(OrderStatus.inprogress.value)
        self.sharedData.reset_data()
        bankSuccessView = BankSuccessViewEx(self.mainStackedWidget, self.sharedData, self.db)
        self.mainStackedWidget.addWidget(bankSuccessView)
        self.mainStackedWidget.setCurrentWidget(bankSuccessView)
        self.mainStackedWidget.removeWidget(self)

    def on_payment_timeout(self):
        """Hàm này sẽ được thực hiện khi check đơn hàng đã được thanh toán. Nó sẽ thực hiện các tác vụ sau:
        - Update status vào db
        - Reset data
        - Chuyển sang màn hình thông báo giao dịch thất bại.
        - Huỷ màn hình hiện tại"""
        self.update_order_status(OrderStatus.cancelled.value)
        self.sharedData.reset_data()
        bankFailedView = BankFailedViewEx(self.mainStackedWidget, self.sharedData, self.db, "Thanh toán thất bại!",
                                          "Mã đã hết hạn. Vui lòng đặt đơn hàng mới.")
        self.mainStackedWidget.addWidget(bankFailedView)
        self.mainStackedWidget.setCurrentWidget(bankFailedView)
        self.mainStackedWidget.removeWidget(self)

    def show_time(self):
        self.count -= 1
        self.bankQRView.countdownTimerLabel.setText(self.secs_to_minsec(self.count))
        if self.count <= 0:
            self.bankQRView.countdownTimer.stop()
            self.paymentCheckThread.stop()
            self.on_payment_timeout()

    def secs_to_minsec(self, secs: int):
        mins = secs // 60
        secs = secs % 60
        minsec = f'{mins:02}:{secs:02}'
        return minsec

    def update_order_status(self, status: int):
        query = """
                    UPDATE `order`
                    SET status = %s
                    WHERE ID = %s;
        """
        rows_affected = self.db.do_any_sql(query, status, self.sharedData.order.id)
        if rows_affected:
            print(f"✅ Successfully updated {rows_affected} row(s).")
        else:
            print("❌ Update failed.")

    def click_back_button(self):
        bankCancelDialog = BankCancelDialogEx(self.mainStackedWidget, self.sharedData, self.db, self)
        bankCancelDialog.exec()

    def stop_process(self):
        """Dừng toàn bộ thread và bộ đếm."""
        self.paymentCheckThread.stop()
        self.bankQRView.countdownTimer.stop()


