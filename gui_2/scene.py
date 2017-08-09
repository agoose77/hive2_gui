from __future__ import print_function, absolute_import

from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtWidgets import QGraphicsScene


class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

        self._backgroundColor = QColor(50, 55, 60)
        self._gridPen = QPen(self._backgroundColor.lighter(120))
        self._gridPen.setWidth(1)
        self._zoom = 1.0

        self.setItemIndexMethod(QGraphicsScene.NoIndex)  # fixes bug with scene.removeItem()
        self.setBackgroundBrush(self._backgroundColor)
        self.setStickyFocus(True)

    def zoom(self):
        return self._zoom

    def setZoom(self, zoom):
        self._zoom = zoom

    def helpEvent(self, event):
        QGraphicsScene.helpEvent(self, event)

    def mouseReleaseEvent(self, event):
        QGraphicsScene.mouseReleaseEvent(self, event)

    def drawBackground(self, painter, rect):
        if not isinstance(painter, QPainter):
            return

        QGraphicsScene.drawBackground(self, painter, rect)
        painter.setPen(self._gridPen)

        grid_size = 50

        left = int(rect.left()) - (int(rect.left()) % grid_size)
        top = int(rect.top()) - (int(rect.top()) % grid_size)

        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += grid_size

        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += grid_size
