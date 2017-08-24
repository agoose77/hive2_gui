from contextlib import contextmanager
from functools import partial
from logging import getLogger

from typing import Callable

from .observer import Observable

logger = getLogger(__name__)


class IllegalCommandError(Exception):
    """Exception for command that could not be executed or reversed"""


def raise_invalid_operation(operation):
    raise IllegalCommandError(f"Command cannot perform {operation} in this state")


class Command:
    def __init__(self, execute: Callable, undo: Callable):
        """Command object initialiser
        
        :param execute: execution callback
        :param undo: un-execution callback
        """
        self._execute_func = execute
        self._undo_func = undo

    def __repr__(self):
        return f"Command(execute={self._execute_func}, undo={self._undo_func})"

    def _execute(self):
        """Execute command in forward direction"""
        self.execute = partial(raise_invalid_operation, "execute")
        self.undo = self._undo
        self._execute_func()

    def _undo(self):
        """Execute command in reverse direction"""
        self.execute = self._execute
        self.undo = partial(raise_invalid_operation, "undo")
        self._undo_func()

    undo = _undo
    execute = _execute


class DepthContext:
    """Simple context manager to keep track of depth from initial caller"""

    def __init__(self):
        self._depth = 0

    @property
    def depth(self) -> int:
        return self._depth

    def __bool__(self):
        return bool(self._depth)

    def __enter__(self):
        self._depth += 1

    def __exit__(self, *args):
        self._depth -= 1


class CommandLogManager:
    on_updated = Observable()

    def __init__(self, name: str = '<root>'):
        self._current_history = CommandLog(name)
        # Guards to stop updates being triggered during composite operations,
        # or commands being recorded during undo/redo operations
        self._update_depth_ctx = DepthContext()
        self._push_depth_ctx = DepthContext()

    @property
    def command_id(self) -> int:
        return self._current_history.command_id

    @contextmanager
    def aggregated_commend(self, name: str):
        composite_name = "{}.{}".format(self._current_history.name, name)
        history = CommandLog(name=composite_name)

        self._current_history, old_history = history, self._current_history
        yield self
        self._current_history = old_history

        # If anything useful was performed, record history object
        if history.has_commands:
            self.record_command(history.redo_all, history.undo_all)

    def record_command(self, execute: Callable, undo: Callable):
        """Add reversable operation to history
        
        :param execute: callback to invoke when command is applied
        :param undo: callback to invoke when command is reversed
        """
        if not self._push_depth_ctx:
            self._current_history.record_command(execute, undo)
            self._on_updated()

    def undo(self):
        with self._push_depth_ctx:
            self._current_history.undo()

        self._on_updated()

    def redo(self):
        with self._push_depth_ctx:
            self._current_history.redo()

        self._on_updated()

    def _on_updated(self):
        if self._update_depth_ctx:
            return

        with self._update_depth_ctx:
            self.on_updated(self.command_id)


class CommandLogError(Exception):
    pass


class CommandLog:
    """Linear log of reversible operations"""

    def __init__(self, name="<main>", limit=200):
        self._commands = []
        self._index = -1
        self._limit = limit

        self._name = name

    def __repr__(self):
        return f"CommandLog(name={self._name} limit={self._limit})"

    @property
    def name(self) -> str:
        return self._name

    @property
    def index(self) -> int:
        return self._index

    @property
    def has_commands(self) -> bool:
        return bool(self._commands)

    @property
    def can_redo(self) -> bool:
        return self._index < len(self._commands) - 1

    @property
    def can_undo(self) -> bool:
        return self._index >= 0

    @property
    def command_id(self) -> int:
        if not 0 <= self._index < len(self._commands):
            return id(self)

        command = self._commands[self._index]
        return id(command)

    def undo_all(self):
        while self.can_undo:
            self.undo()

    def redo_all(self):
        while self.can_redo:
            self.redo()

    def undo(self):
        if not self.can_undo:
            raise CommandLogError("Cannot undo any more operations")

        command = self._commands[self._index]
        self._index -= 1

        command.undo()

    def redo(self):
        if not self.can_redo:
            raise CommandLogError("Cannot redo any more operations")

        self._index += 1
        command = self._commands[self._index]

        command.execute()

    def record_command(self, execute: Callable, unexecute: Callable):
        command = Command(execute, unexecute)
        self._add_command(command)

    def _add_command(self, command: Command):
        # If not at end of list, then later commands will be lost, as history must be contiguous in time
        if self._index < len(self._commands) - 1:
            del self._commands[self._index + 1:]
            latest_command = self._commands[-1]

            logger.info(f"Commands after {latest_command} have been lost due to an add command:\n{command!r}")

        self._commands.append(command)
        self._index += 1

        # Limit length to a maximum number of operations
        if len(self._commands) > self._limit:
            # Assume everything atomic, hence only one command to displace
            # Index must be at end, if command list has grown
            self._index -= 1
            del self._commands[0]
