from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainterPath, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsWidget, QGraphicsLinearLayout, QGraphicsProxyWidget, QLabel, \
    QGraphicsDropShadowEffect

from .colours import Colours
from .enums import IOMode
from .field import Field


class NodeHeaderWidget(QGraphicsWidget):
    def __init__(self, name: str):
        super().__init__()

        layout = QGraphicsLinearLayout(Qt.Vertical)
        self.setLayout(layout)

        self._nameLabel = QLabel(name)
        self._nameLabel.setAlignment(Qt.AlignCenter)
        self._nameLabel.setStyleSheet("QLabel {background-color: rgba(0,0,0,0);}")

        # Setup font
        font = self._nameLabel.font()
        font.setPointSize(20)
        self._nameLabel.setFont(font)

        # Setup label proxy
        label_proxy = QGraphicsProxyWidget()
        label_proxy.setWidget(self._nameLabel)

        # Drop shadow
        dropShadowEffect = QGraphicsDropShadowEffect(self)
        dropShadowEffect.setColor(QColor(0, 0, 0, 50))
        dropShadowEffect.setBlurRadius(0)
        dropShadowEffect.setOffset(1.0, 1.0)
        label_proxy.setGraphicsEffect(dropShadowEffect)

        # Add to layout
        layout.addItem(label_proxy)
        layout.setStretchFactor(label_proxy, 1)

        self._roundness = 2

    def paint(self, painter, option, widget):
        shape = QPainterPath()
        shape.addRoundedRect(self.rect(), self._roundness, self._roundness)

        shapePen = QPen(Qt.NoPen)
        shapePen.setColor(Colours.white)
        shapePen.setWidthF(1.5)

        brush = QBrush(Colours.dark_grey)

        painter.setPen(shapePen)
        painter.setBrush(brush)
        painter.drawPath(shape)


class NodeWidget(QGraphicsWidget):
    def __init__(self, name: str):
        super().__init__()

        layout = QGraphicsLinearLayout(Qt.Vertical)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        header = NodeHeaderWidget(name)
        layout.addItem(header)
        layout.setStretchFactor(header, 1)

        # Effects
        self._dropShadowEffect = QGraphicsDropShadowEffect()
        self.setGraphicsEffect(self._dropShadowEffect)

        self._dropShadowEffect.setOffset(5.0, 5.0)
        self._dropShadowEffect.setBlurRadius(8.0)
        self._dropShadowEffect.setColor(QColor(0, 0, 0, 50))

        self._roundness = 2

    def addField(self, name: str, io_mode: IOMode) -> Field:
        print("ADD F")
        field = Field(name, io_mode)
        print("ADDED F")
        self.layout().addItem(field)
        print("RET F")
        return field

    def fields(self):
        return self.layout().items

    def paint(self, painter, option, widget):
        shape = QPainterPath()
        shape.addRoundedRect(self.rect(), self._roundness, self._roundness)

        shapePen = QPen(Qt.NoPen)
        shapePen.setColor(Colours.white)
        shapePen.setWidthF(1.5)

        brush = QBrush(Colours.light_grey)

        painter.setPen(shapePen)
        painter.setBrush(brush)
        painter.drawPath(shape)
