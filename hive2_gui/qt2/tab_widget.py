from PyQt5.QtWidgets import QTabWidget, QTabBar
from PyQt5.QtCore import pyqtSignal


class TabWidget(QTabWidget):
    onTabChanged = pyqtSignal(int)
    onTabRemoved = pyqtSignal(int)
    onTabInserted = pyqtSignal(int)

    def __init__(self):
        QTabWidget.__init__(self)
        self.setTabsClosable(True)
        self._currentTabIndex = None
        self.currentChanged.connect(self._onTabChanged)

    def addTab(self, widget, label, closeable=True):
        tab = QTabWidget.addTab(self, widget, label)

        if not closeable:
            self.tabBar().tabButton(tab, QTabBar.RightSide).resize(0, 0)

        return tab

    def _onTabChanged(self, index):
        previous_index = self._currentTabIndex
        self._currentTabIndex = index

        self.onTabChanged.emit(previous_index)

    def tabRemoved(self, index):
        self.onTabRemoved.emit(index)

    def tabInserted(self, index):
        self.onTabInserted.emit(index)
