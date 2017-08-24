from pathlib import Path

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QStatusBar

from .tab_widget import TabWidget


ICON_PATH = Path(__file__).parent / "../data/hive.png"


class MainWindow(QMainWindow):
    _projectNameTemplate = "Hive NodeWidget Editor - {}"
    _hivemapExtension = "hivemap"
    _untitledFileName = "<Unsaved>"
    _noProjectText = "<No Project>"

    def __init__(self):
        super(MainWindow, self).__init__()

        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        self.setDockNestingEnabled(True)
        self.setWindowTitle(self._projectNameTemplate.format(self._noProjectText))

        # Set application icon
        icon = QIcon()
        file_path = str(ICON_PATH)
        icon.addFile(file_path)
        self.setWindowIcon(icon)

        # Add tab widget
        self._tabWidget = TabWidget()
        self.setCentralWidget(self._tabWidget)

    def editors(self):
        for i in range(self._tabWidget.count()):
            widget = self._tabWidget.widget(i)
            # if isinstance(widget, NodeEditorWidget):
            #     yield widget
            yield widget