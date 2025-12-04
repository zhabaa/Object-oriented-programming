from typing import List, Optional, Tuple

from core.commands import Command
from core.typing import CommandMetadata


class CommandHistory:
    def __init__(self):
        self._history: List[Tuple[Command, CommandMetadata]] = []
        self._redo_stack: List[Tuple[Command, CommandMetadata]] = []

    def push(self, command: Command, metadata: CommandMetadata) -> None:
        self._history.append((command, metadata))
        self._redo_stack.clear()

    def pop(self) -> Optional[Tuple[Command, CommandMetadata]]:
        if not self._history:
            return None
        return self._history.pop()

    def push_redo(self, command: Command, metadata: CommandMetadata) -> None:
        self._redo_stack.append((command, metadata))

    def pop_redo(self) -> Optional[Tuple[Command, CommandMetadata]]:
        if not self._redo_stack:
            return None
        return self._redo_stack.pop()

    def clear(self) -> None:
        self._history.clear()
        self._redo_stack.clear()
