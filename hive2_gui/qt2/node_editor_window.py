import os
from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QDialog, QMessageBox, QMenu, QMainWindow)

from .configuration_dialogue import ConfigurationDialogue
from .floating_text import FloatingTextWidget
from .node_widget import NodeWidget
from .node_view import NodeView
from ..history import CommandLogManager
from ..inspector import InspectorOption
from ..node import NodeTypes
from ..node_manager import NodeManager
from ..utils import find_file_path_of_hive_path


class NodeEditorWindow(QMainWindow):
    """Qt MainWindow which implements Qt interface to NodeManager state"""
    saveStateUpdated = pyqtSignal(bool)  # has unsaved changes flag

    def __init__(self, project_path=None):
        super().__init__()

        self._filePath = None

        self._history = CommandLogManager()
        self._history.on_updated.subscribe(self._onHistoryUpdated)

        self._nodeView = self._createNodeView()
        self._nodeManager = self._createNodeManager(self._history)

        self.setDockNestingEnabled(True)
        self.setCentralWidget(self._nodeView)

        self._historyID = self._history.command_id
        self._lastSavedID = self._historyID

        self._projectPath = project_path

    def _createNodeView(self):
        # NodeView to node manager
        view = NodeView(self)
        return view

    def _createNodeManager(self, history):
        node_manager = NodeManager(history)
        return node_manager

    def hasUnsavedChanges(self):
        """Check if node manager is dirty (has unsaved state)"""
        return self._lastSavedID != self._history.command_id

    def nodeManager(self):
        return self._nodeManager

    def nodeView(self):
        return self._nodeView

    def filePath(self):
        return self._filePath

    def projectPath(self):
        return self._projectPath

    def selectAll(self):
        self._nodeView.selectAll()

    def undo(self):
        self._nodeManager.history.undo()

    def redo(self):
        self._nodeManager.history.redo()

    def cut(self):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    def paste(self, obj):
        raise NotImplementedError

    def save(self, file_path=None):
        raise NotImplementedError

        if file_path is None:
            file_path = self._filePath
            assert file_path

        if self._filePath is None:
            self._filePath = file_path

        self._lastSavedID = self._history.command_id

    def load(self, file_path=None):
        raise NotImplementedError

        if file_path is None:
            file_path = self._filePath
            assert file_path

        self._filePath = file_path
        self._lastSavedID = self._history.command_id

    def _onHistoryUpdated(self, command_id: int):
        has_unsaved_changes = self.hasUnsavedChanges()
        self.onSaveStateUpdated.emit(has_unsaved_changes)