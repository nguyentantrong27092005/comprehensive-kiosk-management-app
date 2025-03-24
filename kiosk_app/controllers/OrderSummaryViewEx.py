from PyQt6 import QtCore

from PyQt6.QtWidgets import QVBoxLayout

from common.sql_func import Database
from kiosk_app.models.FoodItem import FoodItem
from kiosk_app.models.Order import OrderItem
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.models.ToppingVariant import Variant, Topping
from kiosk_app.views import GeneralView
from kiosk_app.views.OrderView import OrderWidget, OrderItemBox
from kiosk_app.controllers.PaymentSelectViewEx import PaymentSelectViewEx
from kiosk_app.views.CustomStackedWidget import CustomStackedWidget


class OrderSummaryViewEx(GeneralView.GeneralView):

    def __init__(self, mainStackedWidget: CustomStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.sharedData = sharedData
        self.db = db
        self.mainStackedWidget = mainStackedWidget

        # Khởi tạo màn hình giỏ hàng
        self.orderWidget = OrderWidget()
        # Thêm vào frame chung
        self.orderSummaryVLayout = QVBoxLayout(self.frame_chung)
        # Tuỳ chỉnh màn hình
        self.resize(398, 500)
        self.orderSummaryVLayout.addWidget(self.orderWidget)
        self.orderSummaryVLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_chung.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.addOrderItemBox()
        self.signalAndSlot_OrderWidget()
        # Else
        self.updatePrice()
    def processVoucher(self, voucher, totalPrice):
        """Xử lý logic áp dụng voucher
        :return: str: cảnh báo | dict: evouchergiamgia | list: freeitem | None"""
        if not voucher:
            self.reset_voucher_order()
            return None
        #TH Giám giá
        evoug = self.checkisEffectiveGiamGia(voucher)
        if isinstance(evoug, list):
            if self.sharedData.order.evoucherGiamGiaId is None and self.sharedData.order.isAppliedVoucher:
                self.removeFreeItem()
            evoug = evoug[0]
            result = self.sharedData.order.update_evoucher_discount(isPercent=evoug['IsPercent'], discountValue=evoug['Discount'], minimumPrice=evoug['MinimumPrice'], maximumDiscount=evoug['MaximumDiscount'])
            if result:
                self.updatePrice(False)
                self.sharedData.order.evoucherGiamGiaId = evoug['ID']
                self.sharedData.order.isAppliedVoucher = True
                return evoug
            else:
                self.reset_voucher_order()
                return "Bạn chưa đủ điều kiện áp dụng mã voucher này."
        #TH Tặng món
        else:
            evout, evou = self.checkIsEffectiveTangMon(voucher)
            if isinstance(evout, list):
                freeItems = []
                if self.sharedData.order.evoucherGiamGiaId is None and self.sharedData.order.isAppliedVoucher:
                    self.removeFreeItem()
                elif self.sharedData.order.evoucherGiamGiaId is not None and self.sharedData.order.isAppliedVoucher:
                    self.reset_voucher_order()
                elif any(item.is_free for item in
                         self.sharedData.order.orderItems) and self.sharedData.order.isAppliedVoucher:
                    self.reset_voucher_order()
                if self.sharedData.order.totalPrice > evout[0]['MinimumPrice']:
                    for item in evout:
                        freeItems.append(item)
                    self.addFreeItem(freeItems)
                    self.sharedData.order.isAppliedVoucher = True
                    return freeItems
                else:
                    self.reset_voucher_order()
                    return "Bạn không đủ điều kiện để áp dụng mã voucher này."

        if isinstance(evoug, str) and isinstance(evout, str):
            return evoug
    def removeFreeItem(self):
        """Hàm dùng để xoá tất cả freeItem có trong giỏ hàng và update lại giỏ hàng"""
        free_items = [item for item in self.sharedData.order.orderItems if item.evoucherTangMonId is not None]
        for item in free_items:
            if item.is_free:
                print("------", item)
                self.sharedData.order.remove_order_item(item)
        self.sharedData.order.evoucherDiscount = 0
        self.updateOrder()

    def addFreeItem(self, freeItems):
        self.sharedData.order.evoucherDiscount = 0
        for item in freeItems:
            fooditem = FoodItem(item['ID'], item['Name'], item['Price'], item['DiscountedPrice'], item['ImageURL'], item['IsBestSeller'])
            orderitem = OrderItem(fooditem, item['Amount'],"", evoucherTangMonId=item['EvoucherTangMonID'], is_free=True)# chuyển note = None
            self.sharedData.order.add_new_order_items([orderitem])
            # self.sharedData.order.evoucherDiscount += (item['Price'] - item['DiscountedPrice'])*item['Amount']
        self.updateOrder(is_free=True)

    def checkVoucherGiamGiaIsUsed(self, voucher):
        """Kiểm tra voucher giảm giá đã được sử dụng chưa?"""
        sql = f"""
            SELECT ID 
            ,EvoucherGiamGiaID
            FROM evouchergiamgialist
            WHERE Value = %s
            AND IsUsed = False 
            LIMIT 1"""
        result = self.db.fetch_data(sql, voucher)
        return result # list | None
    def checkisEffectiveGiamGia(self, voucher):
        """
        Kiểm tra chương trình giảm giá còn hiệu lực không?
        :return: list(1) thông tin chi tiết của evouchergiamgia | cảnh báo hết hạn/ bị sử dụng/hết hiệu lực
        """""
        evou = self.checkVoucherGiamGiaIsUsed(voucher)
        if evou:
            evouchergiamgiaID = evou[0]['EvoucherGiamGiaID']
            sql = f"""
               SELECT evgg.ID
                     ,evgg.Discount #Giá trị giảm
                     ,evgg.IsPercent #Flag giảm theo phần trăm
                     ,evgg.MinimumPrice #Hoá đơn ít nhất bao nhiêu thì mới được áp mã giảm giá
                     ,evgg.MaximumDiscount #Hoá đon được giảm nhiều nhất là bao nhiêu
               FROM evouchergiamgia evgg
               INNER JOIN evoucher ev
               ON ev.ID = evgg.EVoucherID
               WHERE evgg.ID = %s
               AND ev.IsEffective = True"""
            result = self.db.fetch_data(sql, evouchergiamgiaID)
            if result:
                return result
            else:
                return "Rất tiếc! Mã voucher đã hết hạn sử dụng."
        return "Mã voucher không hợp lệ hoặc đã bị sử dụng."
    def checkisUsedTangMon(self, voucher):
        """Kiểm tra voucher tặng món đã được sử dụng chưa?
        :return : List (1) | None"""
        sql = f"""
        SELECT ID
              ,EVoucherTangMonID
              ,IsUsed
        FROM evouchertangmonlist
        WHERE Value = %s
        AND IsUsed = False #Kiểm tra voucher đã sử dụng chưa"""
        result = self.db.fetch_data(sql, voucher)
        return result
    def checkIsEffectiveTangMon(self, voucher):
        """:returns: List | Cảnh báo hết hạn/ bị sử dụng/ không hợp lệ và evouchertangmon"""
        evou = self.checkisUsedTangMon(voucher)
        if evou:
            evouchertangmonID = evou[0]['EVoucherTangMonID']
            sql = f"""
            SELECT fi.ID
                  ,fi.Name
                  ,fi.ImageURL
                  ,fih.Price
                  ,0 AS DiscountedPrice 
                  ,evtm.ID AS EvoucherTangMonID
                  ,evtm.Amount 
                  ,evtm.MinimumPrice 
                  ,fi.IsBestSeller
            FROM evouchertangmon evtm
            INNER JOIN evoucher ev
            ON ev.ID = evtm.EVoucherID
            INNER JOIN fooditem fi
            ON fi.ID = evtm.FoodItemID
            INNER JOIN fooditem_history fih
            ON fi.ID = fih.FoodItemID
            WHERE evtm.ID = %s
            AND ev.IsEffective = TRUE 
            AND fih.IsEffective = TRUE"""
            result = self.db.fetch_data(sql, evouchertangmonID)
            if result:
                return result, evou
            return "Rất tiếc! Mã voucher đã hết hạn sử dụng.", None
        else:
            return "Mã voucher không hợp lệ hoặc đã được sử dụng.", None

    def addOrderItemBox(self):
        totalitem = len(self.sharedData.order.orderItems)
        self.orderWidget.scrollAreaWidgetContents.setMinimumSize(320, 130*totalitem)
        for item in self.sharedData.order.orderItems:
            OrderItemBox = OrderItemBoxEx(item)
            OrderItemBox.quantityChanged.connect(self.extendUpdatePrice)
            OrderItemBox.deleteChanged.connect(self.updateOrder)
            self.orderWidget.verticalLayout_contents.addWidget(OrderItemBox)

    def extendUpdatePrice(self):
        print(f"Before update price: {self.sharedData.order.isAppliedVoucher}")
        if self.sharedData.order.isAppliedVoucher:
            self.processApplyVoucher()
        else:
            self.updatePrice()
        print(f"After update price: {self.sharedData.order.isAppliedVoucher}")

    def updatePrice(self, is_all = True):
        """
        cập nhập tạm tính và tổng thanh toán
        :param is_all: True --> cập nhập cả 2 | False --> cập nhập tổng thanh toán
        """
        self.sharedData.order.totalPrice = 0
        self.sharedData.order.init_calculate_totals()
        self.orderWidget.lineEdit_total.setText(f"{self.sharedData.order.totalPrice - self.sharedData.order.evoucherDiscount:,.0f}")
        if is_all:
            self.orderWidget.lineEdit_totaltemp.setText(f"{self.sharedData.order.totalPrice-self.sharedData.order.evoucherDiscount:,}")


    def updateOrder(self, deleted_orderitem=None, is_free = False):
        """
        :param : id = None| id = fooditemID --> Xoá orderitem trên db
        """
        while self.orderWidget.scrollAreaWidgetContents.layout().count():
            item = self.orderWidget.scrollAreaWidgetContents.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        if deleted_orderitem:
            self.sharedData.order.remove_order_item(Item=deleted_orderitem)
            self.sharedData.order.evoucherDiscount = 0# ----Đảm bảo update giá sau khi xoá sản phẩm
        # nếu xoá sp free thì phải tính lại evoucerDiscount
        if is_free:
            self.sharedData.order.evoucherDiscount = 0  # ----Đảm bảo update giá sau khi xoá sản phẩm
            for freeitem in self.sharedData.order.orderItems:
                if freeitem.is_free:
                    print(freeitem)
                    self.sharedData.order.evoucherDiscount += (freeitem.foodItem.discounted_price)*freeitem.quantity
                    print("DISCOUNT_PRICE",freeitem.foodItem.discounted_price,"QUANTITY", freeitem.quantity)
                    print("EVOUCHERDISCOUT",self.sharedData.order.evoucherDiscount)
        self.addOrderItemBox()
        self.updatePrice()

    def signalAndSlot_OrderWidget(self):
        self.orderWidget.pushButton_payment.clicked.connect(self.processPayment)
        self.orderWidget.pushButton_apply.clicked.connect(self.processApplyVoucher)
        self.pushButton_back.clicked.connect(self.processBack)

    def processPayment(self):
        paymentSelectViewEx = PaymentSelectViewEx(self.mainStackedWidget, self.sharedData, self.db)
        self.mainStackedWidget.change_screen(paymentSelectViewEx, self)

    def processApplyVoucher(self):
        if self.orderWidget.label_warning.text()!="":
            self.orderWidget.label_warning.hide()
        voucher = self.orderWidget.lineEdit_voucher.text().strip()
        respone = self.processVoucher(voucher, self.sharedData.order.totalPrice)
        if isinstance(respone, str):
            self.orderWidget.label_warning.setText(f"<span style = 'color: #bd1906; font-size: 13px;'>{respone}</span>")
            self.orderWidget.gridLayout_payment.addWidget(self.orderWidget.label_warning, 2, 1, 1, 3)
            self.orderWidget.label_warning.show()
            self.sharedData.order.evoucherDiscount = 0
            # self.reset_voucher_order()
            self.updatePrice()

        elif isinstance(respone, list):
            self.updatePrice(False)
            self.sharedData.order.isAppliedVoucher = True
        elif not respone:
            print(type(respone))
            self.sharedData.order.evoucherDiscount = 0
            self.removeFreeItem()
            self.updatePrice()
            self.sharedData.order.isAppliedVoucher = False
        print(self.sharedData.order.evoucherGiamGiaId)
        print(self.sharedData.order.totalAmount)
        print(self.sharedData.order.totalPrice)
        print(self.sharedData.order.evoucherDiscount)

    def processBack(self):
        self.mainStackedWidget.change_screen_with_index(1, self)
        self.reset_voucher_order()
        currentWidget = self.mainStackedWidget.currentWidget()
        currentWidget.load_items(category_name=None, category_id=None)
        currentWidget.kioskMenuWidget.groupbox_item.setTitle("Tất cả món")

    def reset_voucher_order(self):
        self.sharedData.order.evoucherGiamGiaId = None
        self.sharedData.order.evoucherDiscount = 0
        self.updateOrder()
        self.removeFreeItem()
        self.sharedData.order.isAppliedVoucher = False

    def test(self):
        """Code này để test cho dữ liệu giỏ hàng."""
        query = """
        SELECT fi .ID
              ,fi.Name
              ,fi.IsBestSeller
              ,fh.Price
              ,CAST(IF(pfi.FoodItemID IS NOT NULL, IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), fh.Price - p.Discount), fh.Price) AS UNSIGNED) AS DiscountedPrice
              ,fi.ImageURL
              ,pfi.PromotionID
        FROM fooditem fi
        INNER JOIN fooditem_history fh
            ON fi.ID = fh.FoodItemId
        LEFT JOIN promotionfooditem pfi
            ON fi.ID = pfi.FoodItemID
        LEFT JOIN (SELECT * FROM promotion WHERE IsEffective = True) p
            ON p.ID = pfi.PromotionID
        WHERE (fi.IsFulltime = True OR (fi.Days LIKE CONCAT('%%',CAST(WEEKDAY(current_timestamp) AS CHAR),'%%') #Lấy món được bán trong ngày hôm đó
                                        AND current_time BETWEEN fi.AvailableStartTime AND fi.AvailableEndTime)) #Lấy món được bán trong khung giờ hiện tại
        AND fh.IsEffective = True
        AND fi.CategoryID = %s
        """
        result = [self.db.fetch_data(query, 1)[0], self.db.fetch_data(query, 2)[0]]
        fi1 = FoodItem(result[0]['ID'], result[0]['Name'], result[0]['Price'], result[0]['DiscountedPrice'] - 20000,
                       result[0]['ImageURL'],
                       result[0]['IsBestSeller'], result[0]['PromotionID'])
        fi2 = FoodItem(result[1]['ID'], result[1]['Name'], result[1]['Price'], result[1]['DiscountedPrice'] - 45000,
                       result[1]['ImageURL'],
                       result[1]['IsBestSeller'], result[1]['PromotionID'])
        fi3 = FoodItem(16, "Khoai chiên truyền thống", 1000000, 2000, "...", False, None)
        fi1variant1 = Variant(2, "M", 9000 - 8000, 2000)
        fi1variant2 = Variant(7, "Bình thường")
        fi2variant1 = Variant(10, "Cay")
        fi1topping1 = Topping(18, "Trân châu đen", 5000, 5000 - 4000)
        fi1topping2 = Topping(18, "Trân châu đen", 5000, 5000 - 4000)
        fi2topping1 = Topping(8, "Khoai chiên truyền thống", 29000, 29000 - 28000)
        fi3variant1 = Variant(9, "Không cay")
        fi3variant2 = Variant(11, "Khoai tây")
        fi3variant3 = Variant(14, "M")
        oi1 = OrderItem(fi1, 2, "Test01-70% Đá", toppingList=[fi1topping1, fi1topping2],
                        variantList=[fi1variant1, fi1variant2])
        oi2 = OrderItem(fi2, 1, "Test02", toppingList=[fi2topping1], variantList=[fi2variant1])
        oi3 = OrderItem(fi3, 7, "Test03", variantList=[fi3variant1, fi3variant2, fi3variant3])
        self.sharedData.order.add_new_order_items([oi1, oi2, oi3])

class OrderItemBoxEx(OrderItemBox):
    deleteChanged = QtCore.pyqtSignal(object, bool)
    quantityChanged = QtCore.pyqtSignal()

    def __init__(self,OrderItem ):
        super().__init__(OrderItem)
        if not self.layout():
            self.setupUI()
        if OrderItem.is_free:
            self.label_price.setText(
                f"<span style = 'color: #C0BBBB; font-size: 11px;'><s>{self.orderItem.foodItem.price:,}</s></span><span style = 'color: #bd1906;'>Free</span>")
        self.signalandslot()

    def signalandslot(self):
        self.pushButton_delete.clicked.connect(self.processDeleteOrderItem)
        self.pushbutton_minus.clicked.connect(self.processMinusQuantity)
        self.pushbutton_plus.clicked.connect(self.processPlusQuantity)

    def processPlusQuantity(self):
        if self.orderItem.is_free:#--sản phẩm tặng không cho phép thay đổi số lượng
            pass
        else:
            self.orderItem.quantity += 1
            self.orderItem.calculate_item_price()
            self.orderItem.total_item_price = self.orderItem.calculate_item_price()
            self.label_quantity.setText(str(self.orderItem.quantity))
            self.quantityChanged.emit()

    def processMinusQuantity(self):
        if self.orderItem.is_free: #--sản phẩm tặng không cho phép thay đổi số lượng
            pass
        elif self.orderItem.quantity > 1:
            self.orderItem.quantity -= 1
            self.orderItem.total_item_price = self.orderItem.calculate_item_price()
            self.label_quantity.setText(str(self.orderItem.quantity))
            self.quantityChanged.emit()

    def processDeleteOrderItem(self):
        """xoá trên hoá đơn"""
        self.deleteChanged.emit(self.orderItem, self.orderItem.is_free)

