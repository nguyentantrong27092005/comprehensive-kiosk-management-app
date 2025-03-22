from PyQt6.QtWidgets import QStackedWidget
from admin_app.models.SharedDataModel import SharedDataModel
from common.sql_func import Database


def change_to_new_widget(mainStackedWidget: QStackedWidget, targetWidget, currentWidget = None):
    mainStackedWidget.addWidget(targetWidget)
    mainStackedWidget.setCurrentWidget(currentWidget)
    if currentWidget:
        mainStackedWidget.removeWidget(currentWidget)

def open_evoucher_statistic_view(mainStackedWidget: QStackedWidget, sharedData: SharedDataModel, db: Database, currentWidget = None):
    from admin_app.controllers.EVoucherViewEx import EVoucherWidgetViewEx
    targetWidget = EVoucherWidgetViewEx(mainStackedWidget, sharedData, db)
    change_to_new_widget(mainStackedWidget, targetWidget, currentWidget)

def open_best_seller_statistic_view(mainStackedWidget: QStackedWidget, sharedData: SharedDataModel, db: Database, currentWidget = None):
    from admin_app.controllers.BestSellerViewEx import BestSellerViewEx
    targetWidget = BestSellerViewEx(mainStackedWidget, sharedData, db)
    change_to_new_widget(mainStackedWidget, targetWidget, currentWidget)

def open_payment_select_statistic_view(mainStackedWidget: QStackedWidget, sharedData: SharedDataModel, db: Database, currentWidget = None):
    from admin_app.controllers.PaymentSelectStatisticViewEx import PaymentSelectViewStatisticsEx
    targetWidget = PaymentSelectViewStatisticsEx(mainStackedWidget, sharedData, db)
    change_to_new_widget(mainStackedWidget, targetWidget, currentWidget)

def open_home_view(mainStackedWidget: QStackedWidget, currentWidget = None):
    mainStackedWidget.setCurrentIndex(1)
    if currentWidget:
        mainStackedWidget.removeWidget(currentWidget)

