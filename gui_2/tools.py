from PyQt5.QtWidgets import QGraphicsLayout, QGraphicsLayoutItem

from typing import Iterator

def iter_layout(layout: QGraphicsLayout) -> Iterator[QGraphicsLayoutItem]:
    for i in range(layout.count()):
        yield layout.itemAt(i)
