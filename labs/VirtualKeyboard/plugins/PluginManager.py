from typing import Any, Dict, Type, TYPE_CHECKING

from commands import Command
from plugins import KeyboardPlugin

if TYPE_CHECKING:
    from VirtualKeyboard import VirtualKeyboard


class PluginManager:
    """Управление плагинами клавиатуры"""

    def __init__(self):
        self._plugins: Dict[str, KeyboardPlugin] = {}
        self._component_registries: Dict[str, Any] = {}
        self._command_registries: Dict[str, Type[Command]] = {}

    def register_plugin(self, plugin: KeyboardPlugin) -> None:
        """Регистрация плагина"""
        self._plugins[plugin.get_name()] = plugin

    def unregister_plugin(self, plugin_name: str) -> None:
        """Удаление плагина"""
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]

    def setup_plugins(self, keyboard: "VirtualKeyboard") -> None:
        """Инициализация всех плагинов"""
        for plugin in self._plugins.values():
            plugin.setup(keyboard)

    def register_component_type(self, name: str, component_class: Type) -> None:
        """Регистрация типа компонента для сериализации"""
        self._component_registries[name] = component_class

    def register_command_type(self, name: str, command_class: Type["Command"]) -> None:
        """Регистрация типа команды для сериализации"""
        self._command_registries[name] = command_class

    def get_command_registry(self) -> Dict[str, Type["Command"]]:
        return self._command_registries.copy()
