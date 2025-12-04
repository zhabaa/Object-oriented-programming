from typing import Any

from core.typing import CommandMetadata
from core.abstractions.ICommand import ICommand

class Command(ICommand):
    def execute(self, context: Any) -> CommandMetadata:
        pass

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        pass
