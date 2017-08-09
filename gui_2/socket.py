from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsWidget


class Socket(QGraphicsWidget):
    def __init__(self, parent, colour: QColor, fancy_shading: bool = False):
        super().__init__(parent)

        self._color = colour
        self._fancyShading = fancy_shading
        self._userData = None

    def color(self):
        return self._color

    def setColor(self, color):
        self._color = color

    def userData(self):
        return self._userData

    def setUserData(self):
        return self._userData

    def fancyShading(self):
        return self._fancyShading

    def setFancyShading(self, shading):
        self._fancyShading = shading

    def mousePressEvent(self, *args, **kwargs):
        print("PRINT", self.parentItem()._name)

    def boundingRect(self):
        size = 16
        return QRectF(0, 0, size, size)

    def paint(self, painter, option, widget):
        brush = QBrush(self._color)
        pen = QPen(Qt.NoPen)

        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawEllipse(self.boundingRect())

        if self._fancyShading:
            painter.setBrush(painter.brush().color().darker(130))
            painter.drawChord(self.boundingRect(), 0 * 16, 180 * 16)
