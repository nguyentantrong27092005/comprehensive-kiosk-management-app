from PyQt6.QtWidgets import QStackedWidget


class CustomStackedWidget(QStackedWidget):
    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)
        self.mainWindow = mainWindow

    def change_screen(self, targetView, currentView=None, timer_hidden=False):
        """Define current View to delete the current view in stacked widget"""
        self.addWidget(targetView)
        self.setCurrentWidget(targetView)
        if currentView:
            self.removeWidget(currentView)
        if timer_hidden:
            self.hide_timer()
        else:
            self.reset_timer()

    def change_screen_with_index(self, index, currentView=None, timer_hidden=False):
        """Define current View to delete the current view in stacked widget"""
        self.setCurrentIndex(index)
        if currentView:
            self.removeWidget(currentView)
        if index == 0:
            self.hide_timer()
        else:
            self.reset_timer()
        if index == 1:
            kioskMenuView = self.currentWidget()
            kioskMenuView.kioskMenuWidget.pushButton_shoppingcart.icon_widget.setCount(self.mainWindow.sharedData.order.totalAmount)

    def reset_timer(self):
        try:
            self.mainWindow.countdownTimer.timeout.disconnect(self.show_time)
        except TypeError:
            pass
        self.mainWindow.countdownTimerLabel.setHidden(False)
        self.mainWindow.count = 150
        self.mainWindow.countdownTimerLabel.setText(self.secs_to_minsec(self.mainWindow.count))
        self.mainWindow.countdownTimer.timeout.connect(self.show_time)

    def hide_timer(self):
        self.mainWindow.countdownTimerLabel.setHidden(True)
        try:
            self.mainWindow.countdownTimer.timeout.disconnect(self.show_time)
        except TypeError:
            pass

    def show_time(self):
        self.mainWindow.count -= 1
        self.mainWindow.countdownTimerLabel.setText(self.secs_to_minsec(self.mainWindow.count))
        if self.mainWindow.count <= 0:
            self.mainWindow.countdownTimer.stop()
            if self.currentIndex() == 1:
                self.change_screen_with_index(0)
            else:
                self.change_screen_with_index(0, self.currentWidget())
            self.mainWindow.sharedData.reset_data()

    def secs_to_minsec(self, secs: int):
        mins = secs // 60
        secs = secs % 60
        minsec = f'{mins:02}:{secs:02}'
        return minsec