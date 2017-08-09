from typing import Iterator

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPalette, QColor, QFontMetrics
from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsLinearLayout, QGraphicsProxyWidget, QLabel, \
    QGraphicsDropShadowEffect, QGraphicsLayout, QGraphicsLayoutItem

from .colours import Colours
from .enums import IOMode
from .socket import Socket
from .tools import iter_layout


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
        label_font.setPointSize(13)
        self._nameLabel.setFont(label_font)

        self._labelProxy = QGraphicsProxyWidget(self)
        self._labelProxy.setWidget(self._nameLabel)

        # Drop shadow
        dropShadowEffect = QGraphicsDropShadowEffect(self)
        dropShadowEffect.setColor(QColor(0, 0, 0, 50))
        dropShadowEffect.setBlurRadius(0)
        dropShadowEffect.setOffset(1.0, 1.0)
        self._labelProxy.setGraphicsEffect(dropShadowEffect)

        # Add socket to connect to
        self._socket = Socket(self, Colours.red)

    def label(self) -> QLabel:
        return self._nameLabel

    def labelBoundingRect(self) -> QRect:
        return QFontMetrics(self._nameLabel.font()).boundingRect(self._nameLabel.text())

    def socket(self) -> Socket:
        return self._socket

    def updateLayout(self, max_label_width: int):
        """Update layout such that socket and label are correctly positioned for a given row width derived from
        longest label length

        :param max_label_width: width of longest label
        """
        label = self._labelProxy
        socket = self._socket
        padding = self._padding

        label_rect = self.labelBoundingRect()
        label_width = label_rect.width()
        assert abs(max_label_width - label_width) > -1e-3

        label_height = label_rect.height()

        socket_width = socket.boundingRect().width()
        socket_height = socket.boundingRect().height()

        socket = self._socket
        socket_pos_y = (label_height - socket_height) / 2.0

        row_width = socket_width / 2 + padding + max_label_width + padding

        # Find socket position
        if self._ioMode == IOMode.OUTPUT:
            socket_pos_x = padding + max_label_width + padding
            label_pos_x = row_width - socket_width / 2 - padding - label_width

        else:
            socket_pos_x = -socket_width / 2
            label_pos_x = socket_width / 2 + padding

        label.setPos(label_pos_x, 0)
        socket.setPos(socket_pos_x, socket_pos_y)

        self.resize(row_width, label_height)
        self.setPreferredSize(row_width, label_height)


class Field(QGraphicsWidget):
    def __init__(self, name: str, io_mode: IOMode):
        super().__init__()

        self._ioMode = io_mode

        layout = QGraphicsLinearLayout(Qt.Vertical)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0.0)
        self.setLayout(layout)

        self._rootRow = self._createRootRow(name)

    def _createRootRow(self, name: str) -> FieldRow:
        row = self.addRow(name, 16)
        palette = row.palette()
        palette.setColor(QPalette.Window, Colours.orange)
        row.setPalette(palette)
        return row

    def addRow(self, name: str, font_size: int=None) -> FieldRow:
        row = FieldRow(name, self._ioMode)

        if font_size is not None:
            font = row.label().font()
            font.setPointSize(font_size)
            row.label().setFont(font)

        self.layout().addItem(row)
        self.updateRowGeometries()
        return row

    def name(self) -> str:
        return self._nameLabel.text()

    def setName(self, name: str):
        self._nameLabel.setText(name)

    def updateRowGeometries(self):
        max_label_with = max(r.labelBoundingRect().width() for r in iter_layout(self.layout()))

        for row in iter_layout(self.layout()):
            row.updateLayout(max_label_with)
