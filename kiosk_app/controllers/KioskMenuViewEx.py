from functools import partial

from PyQt6.QtWidgets import QStackedWidget, QVBoxLayout

from common.sql_func import Database
# from kiosk_app.controllers.OrderControllerEx import OrderControllerEx
from kiosk_app.controllers.ToppingSelectionViewEx import ToppingSelectionEx

from kiosk_app.controllers.DineSelectViewEx import DineSelectViewEx
from kiosk_app.models.FoodItem import FoodItem
from kiosk_app.models.SharedDataModel import SharedDataModel
from kiosk_app.views import GeneralView, KioskMenuView
from kiosk_app.views.KioskMenuView import CategoryFrame, ProductFrame


class KioskMenuViewEx(GeneralView.GeneralView):
    def __init__(self, mainStackedWidget: QStackedWidget, sharedData: SharedDataModel, db: Database):
        super().__init__()
        self.mainStackedWidget = mainStackedWidget
        self.sharedData = sharedData
        self.db = db

        self.frame_ngang.hide() #ẩn thanh ngang vì không cần

        # self.verticalLayout.setContentsMargins(0,0,0,0)
        # self.verticalLayout.setSpacing(0)
        self.kioskMenuWidget = KioskMenuView.MenuWidget()

        self.menuLayout = QVBoxLayout(self.frame_chung)
        self.menuLayout.addWidget(self.kioskMenuWidget)
        self.frame_chung.setStyleSheet("background-color:#ffffff")

        self.menuLayout.setContentsMargins(0, 0, 0, 0)
        self.menuLayout.setSpacing(0)

        self.load_categories()
        self.load_items(category_name=None, category_id=None)

    def load_categories(self):
        category_query = "SELECT ID, Name, ImageURL FROM Category"
        categories = self.db.fetch_data(category_query) # lấy danh sách của các category (ImageURL, Name, ID)
        print(categories)
        for category in categories:
            category = CategoryFrame(category["ImageURL"], category["Name"], category["ID"], self)
            self.kioskMenuWidget.layout_category.addWidget(category)
        return categories

    def load_items(self, category_name, category_id=None):
        if category_id and category_name:
            self.kioskMenuWidget.groupbox_item.setTitle(category_name)
            self.kioskMenuWidget.groupbox_item.delete_product()

            query = """
                SELECT fi.ID,
                       fi.Name,
                       fi.IsBestSeller,
                       fh.Price,
                       CAST(IF(pfi.FoodItemID IS NOT NULL, 
                               IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), 
                               fh.Price - p.Discount), 
                           fh.Price) AS UNSIGNED) AS DiscountedPrice,
                       fi.ImageURL,
                       pfi.PromotionID
                FROM fooditem fi
                INNER JOIN fooditem_history fh
                    ON fi.ID = fh.FoodItemId
                LEFT JOIN promotionfooditem pfi
                    ON fi.ID = pfi.FoodItemID
                LEFT JOIN (SELECT * FROM promotion WHERE IsEffective = True) p
                    ON p.ID = pfi.PromotionID
                WHERE (fi.IsFulltime = True 
                       OR (fi.Days LIKE CONCAT('%%', CAST(WEEKDAY(current_timestamp) AS CHAR), '%%')
                       AND current_time BETWEEN fi.AvailableStartTime AND fi.AvailableEndTime))
                AND fh.IsEffective = True
                AND fi.CategoryID = %s;
            """
            items = self.db.fetch_data(query, (category_id,))
            #print(f"Dữ liệu trả về: {items}")

        else:
            query = """
                SELECT fi.ID,
                       fi.Name,
                       fi.IsBestSeller,
                       fh.Price,
                       CAST(IF(pfi.FoodItemID IS NOT NULL, 
                               IF(p.IsPercent, fh.Price*(1-(p.Discount/100)), 
                               fh.Price - p.Discount), 
                           fh.Price) AS UNSIGNED) AS DiscountedPrice,
                       fi.ImageURL,
                       pfi.PromotionID
                FROM fooditem fi
                INNER JOIN fooditem_history fh
                    ON fi.ID = fh.FoodItemId
                LEFT JOIN promotionfooditem pfi
                    ON fi.ID = pfi.FoodItemID
                LEFT JOIN (SELECT * FROM promotion WHERE IsEffective = True) p
                    ON p.ID = pfi.PromotionID
                WHERE (fi.IsFulltime = True 
                       OR (fi.Days LIKE CONCAT('%%', CAST(WEEKDAY(current_timestamp) AS CHAR), '%%')
                       AND current_time BETWEEN fi.AvailableStartTime AND fi.AvailableEndTime))
                AND fh.IsEffective = True;
            """
            items = self.db.fetch_data(query)
            #print(f"Dữ liệu trả về: {items}")

        row = 0
        col = 0
        for item in items:
            product_frame = ProductFrame(
                item["ID"],item["ImageURL"], item["Price"],
                item["DiscountedPrice"], item["Name"], item["IsBestSeller"]
            )
            product_frame.productClicked.connect(partial(self.click_product, item))

            self.kioskMenuWidget.groupbox_item.add_product(product_frame, row, col)
            col += 1
            if col == 2:
                col = 0
                row += 1

    def click_product(self, item):
        food_item = FoodItem(
            id = item["ID"],
            name = item["Name"],
            price = item["Price"],
            discounted_price = item["DiscountedPrice"],
            image_url = item["ImageURL"],
            is_best_seller=item["IsBestSeller"],
            promotion_id = item.get("PromotionID")
        )
        self.sharedData.set_selected_item(food_item)
        self.show_addToppingView()
    def show_addToppingView(self):
        addToppingView = ToppingSelectionEx(self.mainStackedWidget, self.sharedData, self.db) # CHECK GIÙM EM KHÚC NÀY
        self.mainStackedWidget.addWidget(addToppingView)
        self.mainStackedWidget.setCurrentWidget(addToppingView)