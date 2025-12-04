from typing import Any

from core.typing import CommandMetadata
from core.commands import Command


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
