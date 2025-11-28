from typing import Dict, Optional

from commands import Command


class KeyBindingManager:
    """Управление привязками клавиш"""

    def __init__(self):
        self._bindings: Dict[str, Command] = {}

    def bind_key(self, key: str, command: Command) -> None:
        self._bindings[key] = command

    def get_command(self, key: str) -> Optional[Command]:
        return self._bindings.get(key)

    def get_all_bindings(self) -> Dict[str, Command]:
        return self._bindings.copy()

    def set_bindings(self, bindings: Dict[str, Command]) -> None:
        self._bindings = bindings
