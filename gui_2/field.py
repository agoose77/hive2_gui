from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsLinearLayout, QGraphicsProxyWidget, QLabel, \
    QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPalette, QColor, QFont, QPainterPath, QPen, QBrush
from .colours import Colours
from .enums import IOMode


class Socket(QGraphicsWidget):

    def __init__(self, parent, colour: QColor, fancy_shading: bool=False):
        super().__init__(parent)

        self._color = colour
        self._fancyShading = fancy_shading

    def color(self):
        return self._color

    def setColor(self, color):
        self._color = color

    def fancyShading(self):
        return self._fancyShading

    def setFancyShading(self, shading):
        self._fancyShading = shading

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


class SubField(QGraphicsWidget):

    def __init__(self, name: str, ioMode: IOMode):
        super().__init__()

        self._ioMode = ioMode
        self._name = name

        # BG styling
        palette = QPalette()
        palette.setColor(QPalette.Window, Colours.dark_grey)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self._nameLabel = QLabel(name)
        self._nameLabel.setStyleSheet("QLabel {background-color: rgba(0,0,0,0);}")

        # Set label font size
        label_font = self._nameLabel.font()
        label_font.setPointSize(15)
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
        self.updateLayout()

    def updateLayout(self):
        self._spacerConstant = 4
        label = self._labelProxy
        height = label.boundingRect().height()
        socket = self._socket

        print(label.boundingRect().width(),
              self.boundingRect().width())
        if self._ioMode == IOMode.OUTPUT:
            hook_y_pos = (height - socket.boundingRect().height()) / 2.0


        else:
            hook_y_pos = (height - socket.boundingRect().height()) / 2.0
            socket.setPos(0.0, hook_y_pos)

        input_width = self._spacerConstant * 2.0
        label.setPos(input_width + self._spacerConstant, 0)

        if self._ioMode == IOMode.OUTPUT:
            socket.setPos(label.pos().x() + label.boundingRect().width() + self._spacerConstant,
                        hook_y_pos)

            self.resize(socket.pos().x() + socket.boundingRect().width(), height)

        else:
            self.resize(label.pos().x() + label.boundingRect().width(), height)

class Field(QGraphicsWidget):

    def __init__(self, name: str, io_mode: IOMode):
        super().__init__()

        layout = QGraphicsLinearLayout(Qt.Vertical)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0.0)
        self.setLayout(layout)

        # Title label
        self._nameLabel = QLabel(name)
        self._nameLabel.setAlignment(Qt.AlignRight if io_mode == IOMode.OUTPUT else Qt.AlignLeft)
        self._nameLabel.setStyleSheet("QLabel {background-color: rgba(0,0,0,0);}")

        # Set label font size
        font = self._nameLabel.font()
        font.setPointSize(20)
        self._nameLabel.setFont(font)

        # Add padding to label
        padding = 6
        self._nameLabel.setContentsMargins(padding, padding, padding, padding)

        label_proxy = QGraphicsProxyWidget()
        label_proxy.setWidget(self._nameLabel)

        # Drop shadow
        dropShadowEffect = QGraphicsDropShadowEffect(self)
        dropShadowEffect.setColor(QColor(0, 0, 0, 50))
        dropShadowEffect.setBlurRadius(0)
        dropShadowEffect.setOffset(1.0, 1.0)
        label_proxy.setGraphicsEffect(dropShadowEffect)

        layout.addItem(label_proxy)

        palette = QPalette()
        palette.setColor(QPalette.Window, Colours.orange)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        sub_rows = ["pre_triggered", "triggered"]
        for row in sub_rows:
            field = SubField(row, io_mode)
            layout.addItem(field)