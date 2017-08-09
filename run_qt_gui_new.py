# Import PySide classes
import ctypes
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from qdarkstyle import load_stylesheet_pyqt5


if __name__ == "__main__":
    # Create a Qt application
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet_pyqt5())

    label_font = QFont()
    label_font.setFamily("Roboto Condensed")
    app.setFont(label_font)

    # Fix for windows tray icon
    app_id = 'hive2.hive2.1.0'
    try:
        windll = ctypes.windll

    except AttributeError:
        pass

    else:
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    from gui_2.view import View
    from gui_2.node import Node
    from gui_2.enums import IOMode

    view = View()
    view.show()

    node = Node("drone")
    node.addField("score.pull_out", IOMode.OUTPUT)
    view.scene().addItem(node)

    # Enter Qt application main loop
    view.move(400,200)

    app.exec_()
    sys.exit()