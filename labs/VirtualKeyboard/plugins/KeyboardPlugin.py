from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from VirtualKeyboard import VirtualKeyboard


class KeyboardPlugin(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    def setup(self, keyboard: "VirtualKeyboard") -> None:
        """Вызывается при регистрации плагина"""
        pass

    def teardown(self, keyboard: "VirtualKeyboard") -> None:
        """Вызывается при удалении плагина"""
        pass
