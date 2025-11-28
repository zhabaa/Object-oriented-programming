from typing import Optional

from commands import Command
from core import CommandMetadata, CommandHistory, ExtensibleContext


class KeyboardCommandInvoker:
    """Выполнение команд и управление историей"""

    def __init__(self):
        self.history = CommandHistory()

    def execute_command(self, command: Command, 
                        context: ExtensibleContext) -> CommandMetadata:
        metadata = command.execute(context)
        self.history.push(command, metadata)
        return metadata

    def undo(self, context: ExtensibleContext) -> Optional[CommandMetadata]:
        item = self.history.pop()
        if item is None:
            return None

        command, metadata = item
        undo_metadata = command.undo(context, metadata)
        self.history.push_redo(command, metadata)
        return undo_metadata

    def redo(self, context: ExtensibleContext) -> Optional[CommandMetadata]:
        item = self.history.pop_redo()
        if item is None:
            return None

        command, old_metadata = item
        new_metadata = command.execute(context)
        self.history.push(command, new_metadata)
        return new_metadata
