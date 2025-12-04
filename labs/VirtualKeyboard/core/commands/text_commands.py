from typing import Any

from core.typing import CommandMetadata
from core.commands import Command


class PrintCharCommand(Command):
    def __init__(self, char: str):
        self.char: str = char

    def execute(self, context: Any) -> CommandMetadata:
        text_buffer = context.get_component("text_buffer")
        case_handler = context.get_component("case_handler")

        actual_char = self.char
        if self.char.isalpha():
            actual_char = (
                self.char.upper() if case_handler.is_upper else self.char.lower()
            )

        text_buffer.append(actual_char)
        return CommandMetadata(type="print", char=actual_char)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        if metadata.char:
            context.get_component("text_buffer").remove_last(len(metadata.char))
        return CommandMetadata(type="undo_print")


class BackspaceCommand(Command):
    def execute(self, context: Any) -> CommandMetadata:
        text_buffer = context.get_component("text_buffer")
        removed = text_buffer.remove_last()
        return CommandMetadata(type="backspace", char=removed)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        if metadata.char:
            context.get_component("text_buffer").append(metadata.char)
        return CommandMetadata(type="undo_backspace")
