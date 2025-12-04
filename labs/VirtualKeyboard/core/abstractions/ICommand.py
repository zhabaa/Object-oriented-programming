from abc import ABC, abstractmethod
from typing import Any

from core.typing import CommandMetadata


class ICommand(ABC):
    @abstractmethod
    def execute(self, context: Any) -> CommandMetadata:
        pass

    @abstractmethod
    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        pass
