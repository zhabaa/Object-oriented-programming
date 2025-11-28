from typing import Any

from core.Typing import CommandMetadata
from interfaces import ICommand

class Command(ICommand):
    def execute(self, context: Any) -> CommandMetadata:
        pass

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        pass


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


class ToggleCaseCommand(Command):
    def execute(self, context: Any) -> CommandMetadata:
        case_handler = context.get_component("case_handler")
        case_handler.toggle_case()
        return CommandMetadata(type="toggle", is_upper=case_handler.is_upper)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        context.get_component("case_handler").toggle_case()
        return CommandMetadata(
            type="undo_toggle", is_upper=context.get_component("case_handler").is_upper
        )


class MediaPlayCommand(Command):
    def execute(self, context: Any) -> CommandMetadata:
        context.get_component("media_player").is_playing = True
        return CommandMetadata(type="media_on")

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        context.get_component("media_player").is_playing = False
        return CommandMetadata(type="media_off")


class VolumeUpCommand(Command):
    def __init__(self, step: int = 10):
        self.step: int = step

    def execute(self, context: Any) -> CommandMetadata:
        media_player = context.get_component("media_player")
        new_volume = media_player.volume_up(self.step)
        return CommandMetadata(type="vol_up", step=new_volume)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        context.get_component("media_player").volume_down(self.step)
        return CommandMetadata(type="undo_vol_up")


class VolumeDownCommand(Command):
    def __init__(self, step: int = 10):
        self.step: int = step

    def execute(self, context: Any) -> CommandMetadata:
        media_player = context.get_component("media_player")
        new_volume = media_player.volume_down(self.step)
        return CommandMetadata(type="vol_down", step=new_volume)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        context.get_component("media_player").volume_up(self.step)
        return CommandMetadata(type="undo_vol_down")
