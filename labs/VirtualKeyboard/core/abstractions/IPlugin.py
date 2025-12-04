from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import ExtensibleContext
    from features import KeyBindingManager
    from features import StatusProvider


class IPlugin(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def setup(self,context: "ExtensibleContext", binding_manager: "KeyBindingManager", 
              status_provider: "StatusProvider") -> None:
        pass

    @abstractmethod
    def teardown(self, context: "ExtensibleContext", binding_manager: "KeyBindingManager",
                 status_provider: "StatusProvider") -> None:
        pass
