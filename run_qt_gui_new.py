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
    from gui_2.colours import Colours
    from gui_2.enums import IOMode

    view = View()
    view.show()

    node = Node("drone")
    score_out = node.addField("score.pull_out", IOMode.OUTPUT)

    out_pre_trig = score_out.addRow("pre_triggered")
    out_pre_trig.socket().setColor(Colours.red)
    out_pre_trig.socket().setFancyShading(True)

    new_font = out_pre_trig.label().font()
    new_font.setPointSize(12)
    out_pre_trig.label().setFont(new_font)

    score_out.updateRowGeometries()

    node.addField("print_score", IOMode.INPUT)
    view.scene().addItem(node)
    out_pre_trig = score_out.addRow("triggered")


    # Enter Qt application main loop
    view.move(400,200)

    app.exec_()
    sys.exit()
