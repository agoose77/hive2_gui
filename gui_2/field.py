from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsLinearLayout, QGraphicsProxyWidget, QLabel, \
    QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPalette, QColor, QFont, QPainterPath, QPen, QBrush, QFontMetrics
from .colours import Colours
from .enums import IOMode


def iter_layout(layout):
    for i in range(layout.count()):
        yield layout.itemAt(i)


class Socket(QGraphicsWidget):

    def __init__(self, parent, colour: QColor, fancy_shading: bool=False):
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
        print("PRINT",self.parentItem()._name)

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


class FieldRow(QGraphicsWidget):

    def __init__(self, name: str, ioMode: IOMode):
        super().__init__()

        self._ioMode = ioMode
        self._name = name

        self._padding = 4

        # BG styling
        palette = QPalette()
        palette.setColor(QPalette.Window, Colours.dark_grey)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self._nameLabel = QLabel(name)
        self._nameLabel.setStyleSheet("QLabel {background-color: rgba(0,0,0,0);}")

        # Set label font size
        label_font = self._nameLabel.font()
        label_font.setPointSize(18)
        self._nameLabel.setFont(label_font)

        self._labelProxy = QGraphicsProxyWidget(self)
        self._labelProxy.setWidget(self._nameLabel)

        # Drop shadow
        dropShadowEffect = QGraphicsDropShadowEffect(self)
        dropShadowEffect.setColor(QColor(0, 0, 0, 50))
        dropShadowEffect.setBlurRadius(0)
        dropShadowEffect.setOffset(1.0, 1.0)
        self._labelProxy.setGraphicsEffect(dropShadowEffect)
        # layout.addItem(self._labelProxy)

        # Add socket to connect to
        self._socket = Socket(self, Colours.red)

    def labelProxy(self):
        return self._labelProxy

    def labelWidth(self):
        return QFontMetrics(self._nameLabel.font()).width(self._nameLabel.text())

    def socket(self):
        return self._socket

    def updateLayout(self, max_label_width):
        """Update layout such that socket and label are correctly positioned for a given row width derived from
        longest label length

        :param max_label_width: width of longest label
        """
        label = self._labelProxy
        socket = self._socket
        padding = self._padding

        label_width = self.labelWidth()
        assert abs(max_label_width - label_width) > -1e-3

        label_height = label.boundingRect().height()

        socket_width = socket.boundingRect().width()
        socket_height = socket.boundingRect().height()

        socket = self._socket
        socket_pos_y = (label_height - socket_height) / 2.0

        row_width = socket_width / 2 + padding + max_label_width + padding

        # Find socket position
        if self._ioMode == IOMode.OUTPUT:
            socket_pos_x = padding + max_label_width + padding
            label_pos_x = row_width - socket_width/2 - padding - label_width

        else:
            socket_pos_x = -socket_width/2
            label_pos_x = socket_width/2 + padding

        label.setPos(label_pos_x, 0)
        socket.setPos(socket_pos_x, socket_pos_y)

        self.resize(row_width, label_height)
        self.setPreferredSize(row_width, label_height)


class Field(QGraphicsWidget):

    def __init__(self, name: str, io_mode: IOMode):
        super().__init__()

        self._ioMode = io_mode

        layout = QGraphicsLinearLayout(Qt.Vertical)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0.0)
        self.setLayout(layout)

        self._rootRow = self.addRow(name)
        p = self._rootRow.palette()
        p.setColor(QPalette.Window, Colours.orange)
        self._rootRow.setPalette(p)

    def addRow(self, name):
        row = FieldRow(name, self._ioMode)
        self.layout().addItem(row)
        self.updateRowGeometries()
        return row

    def name(self):
        return self._nameLabel.text()

    def setName(self, name):
        self._nameLabel.setText(name)

    def updateRowGeometries(self):
        max_label_with = max(r.labelWidth() for r in iter_layout(self.layout()))

        for row in iter_layout(self.layout()):
            row.updateLayout(max_label_with)