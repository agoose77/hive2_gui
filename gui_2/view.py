from __future__ import print_function, absolute_import

from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPainter, QCursor, QTransform
from PyQt5.QtWidgets import QGraphicsView

from .scene import Scene

SELECT_SIZE = 10


class View(QGraphicsView):
    MOUSE_STEPS = 10

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self._zoom = 1.0
        self._zoomIncrement = 0.05

        self._panning = False
        self._currentCenterPoint = QPointF()
        self._lastPanPoint = QPoint()
        self._hoveredNode = None

        self.setFocusPolicy(Qt.ClickFocus)
        self.setAcceptDrops(True)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setSceneRect(-5000, -5000, 10000, 10000)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setMouseTracking(True)

        scene = Scene(self)
        self.setScene(scene)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    @property
    def mouse_pos(self):
        cursor_pos = QCursor.pos()
        origin = self.mapFromGlobal(cursor_pos)
        scene_pos = self.mapToScene(origin)
        return scene_pos.x(), scene_pos.y()

    def _onBackspaceKey(self):
        self._onDelKey()

    def _onKeyUp(self):
        pass

    def _onKeyDown(self):
        pass

    def _onDelKey(self):
        scene = self.scene()

        selected_nodes = scene.selectedItems()
        self.onNodesDeleted.emit(selected_nodes)

    def setScene(self, new_scene):
        super().setScene(new_scene)

        new_center = QPointF()

        self.centerOn(new_center)
        self._currentCenterPoint = new_center

        self.frameSceneContent()
        self.setZoom(new_scene.zoom())

    def frameSceneContent(self):
        new_center = QPointF(self.scene().itemsBoundingRect().center())
        self.centerOn(new_center)
        self._currentCenterPoint = new_center

    @property
    def center(self):
        return self._currentCenterPoint

    @center.setter
    def center(self, center_point):
        self._currentCenterPoint = center_point
        self.centerOn(self._currentCenterPoint)

    def mousePressEvent(self, event):
        # Handle pan event
        if event.button() == Qt.MiddleButton or \
                (event.button() == Qt.LeftButton and event.modifiers() == Qt.AltModifier):

            if not self._hoveredNode:
                self._lastPanPoint = event.pos()
                self.setCursor(Qt.ClosedHandCursor)
                self._panning = True

        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, mouseEvent):
        if self._panning:
            delta = self.mapToScene(self._lastPanPoint) - self.mapToScene(mouseEvent.pos())
            self._lastPanPoint = mouseEvent.pos()

            self.center += delta
        else:
            QGraphicsView.mouseMoveEvent(self, mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        if self._panning:
            self.setCursor(Qt.ArrowCursor)
            self._lastPanPoint = QPoint()
            self._panning = False
        else:
            QGraphicsView.mouseReleaseEvent(self, mouseEvent)

    def wheelEvent(self, event):
        degrees = event.angleDelta() / 8
        steps = degrees / self.MOUSE_STEPS
        self.setZoom(self.zoom() + self._zoomIncrement * steps.y())

    def keyPressEvent(self, event):
        button = event.key()

        if event.modifiers() in (Qt.NoModifier, Qt.KeypadModifier):
            if button in (Qt.Key_Delete, Qt.Key_Backspace):
                self._onDelKey()
                event.accept()

            elif button == Qt.Key_Up:
                self._onKeyUp()
                event.accept()

            elif button == Qt.Key_Down:
                self._onKeyDown()
                event.accept()

    def zoom(self):
        return self._zoom

    def setZoom(self, zoom):
        self._zoom = zoom

        if zoom >= 1.0:
            self._zoom = 1.0

        elif zoom <= 0.1:
            self._zoom = 0.1

        transform = self.transform()
        new_transform = QTransform.fromTranslate(transform.dx(), transform.dy())
        new_transform.scale(self._zoom, self._zoom)
        self.setTransform(new_transform)

        self.scene().setZoom(self._zoom)

    def zoomIn(self):
        self.setZoom(self._zoom + self._zoomIncrement)

    def zoomOut(self):
        self.setZoom(self._zoom - self._zoomIncrement)
