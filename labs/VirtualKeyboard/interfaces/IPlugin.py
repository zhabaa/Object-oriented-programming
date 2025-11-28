from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import ExtensibleContext
    from keyboard_core import KeyBindingManager
    from keyboard_core import KeyboardStatusProvider


class IPlugin(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def setup(self,context: "ExtensibleContext", binding_manager: "KeyBindingManager", 
              status_provider: "KeyboardStatusProvider") -> None:
        pass

    @abstractmethod
    def teardown(self, context: "ExtensibleContext", binding_manager: "KeyBindingManager",
                 status_provider: "KeyboardStatusProvider") -> None:
        pass
