from common.sql_func import Database
from kiosk_app.controllers.PaymentSelectViewEx import PaymentSelectViewEx
from kiosk_app.models.FoodItem import FoodItem
from kiosk_app.models.Order import OrderItem
from kiosk_app.models.ToppingVariant import Variant, Topping
from kiosk_app.views import GeneralView
from PyQt6.QtWidgets import QVBoxLayout, QStackedWidget
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.views.DineSelectView import DineSelectWidget


class DineSelectViewEx(GeneralView.GeneralView):
    def __init__(self, mainStackedWidget: QStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.sharedData = sharedData
        self.db = db
        self.mainStackedWidget = mainStackedWidget
        self.dineSelectWidget = DineSelectWidget()
        self.dineVLayout = QVBoxLayout(self.frame_chung)
        self.dineVLayout.addWidget(self.dineSelectWidget)
        self.dineVLayout.setContentsMargins(0, 0, 0, 0)
        self.dineSelectWidget.left_section.clicked.connect(self.choose_dine_out)
        self.dineSelectWidget.right_section.clicked.connect(self.choose_dine_in)

    def choose_dine_out(self):
        self.sharedData.order.isDineIn = 0
        self.test()
        paymentSelectView = PaymentSelectViewEx(self.mainStackedWidget, self.sharedData, self.db)
        self.mainStackedWidget.addWidget(paymentSelectView)
        self.mainStackedWidget.setCurrentWidget(paymentSelectView)

    def choose_dine_in(self):
        self.sharedData.order.isDineIn = 1
        self.test()
        paymentSelectView = PaymentSelectViewEx(self.mainStackedWidget, self.sharedData, self.db)
        self.mainStackedWidget.addWidget(paymentSelectView)
        self.mainStackedWidget.setCurrentWidget(paymentSelectView)

    def test(self):
        query = """
        SELECT fi.ID
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
        fi1 = FoodItem(result[0]['ID'], result[0]['Name'], result[0]['Price'], result[0]['DiscountedPrice']-20000, result[0]['ImageURL'],
                       result[0]['IsBestSeller'], result[0]['PromotionID'])
        fi2 = FoodItem(result[1]['ID'], result[1]['Name'], result[1]['Price'], result[1]['DiscountedPrice']-45000, result[1]['ImageURL'],
                       result[1]['IsBestSeller'], result[1]['PromotionID'])
        print(fi2.discounted_price, fi2.price)
        fi3 = FoodItem(16, "Khoai chiên truyền thống", 29000, 2000, "...", "0", None)
        fi1variant1 = Variant(2, "M", 9000-8000, 2000)
        fi1variant2 = Variant(7, "Bình thường")
        fi2variant1 = Variant(10, "Cay")
        fi1topping1 = Topping(18, "Trân châu đen", 5000, 5000-4000)
        fi1topping2 = Topping(18, "Trân châu đen", 5000, 5000-4000)
        fi2topping1 = Topping(8, "Khoai chiên truyền thống", 29000, 29000-28000)
        fi3variant1 = Variant(9, "Không cay")
        fi3variant2 = Variant(11, "Khoai tây")
        fi3variant3 = Variant(14, "M")
        oi1 = OrderItem(fi1, 2, "Test01-70% Đá", toppingList=[fi1topping1, fi1topping2],
                        variantList=[fi1variant1, fi1variant2])
        oi2 = OrderItem(fi2, 1, "Test02", toppingList=[fi2topping1], variantList=[fi2variant1])
        oi3 = OrderItem(fi3, 1, "Test03", variantList=[fi3variant1, fi3variant2, fi3variant3])
        self.sharedData.order.add_new_order_items([oi1, oi2, oi3])

