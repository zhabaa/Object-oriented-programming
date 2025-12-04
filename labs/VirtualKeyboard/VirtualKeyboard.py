from typing import List, Optional

from core.infrastructure.context import ExtensibleContext
from core.setup import DefaultComponentSetup, DefaultKeyBindingSetup
from features.keybindings import KeyBindingManager
from features.command_execution import KeyboardCommandInvoker
from features.state_management import StateService
from features.status_display.StatusProvider import StatusProvider
from features.plugins import PluginManager, KeyboardPlugin


class VirtualKeyboard:
    def __init__(self, plugins: Optional[List[KeyboardPlugin]] = None):
        self.context = ExtensibleContext()
        self.plugin_manager = PluginManager()
        self.key_binding_manager = KeyBindingManager()
        self.command_invoker = KeyboardCommandInvoker()
        self.state_service = StateService(
            self.key_binding_manager, self.plugin_manager
        )
        self.status_provider = StatusProvider(self.context)

        # по умолчанию
        DefaultComponentSetup.setup(self.context)
        DefaultKeyBindingSetup.setup(self.key_binding_manager, self.plugin_manager)

        # настройка плагинов
        if plugins:
            for plugin in plugins:
                self.plugin_manager.register_plugin(plugin)

        self.plugin_manager.setup_plugins(
            self.context,
            self.key_binding_manager,
            self.status_provider
        )
        
        self.load_state()

    def register_plugin(self, plugin: KeyboardPlugin) -> None:
        """регистрация плагина"""
        self.plugin_manager.register_plugin(plugin)
        plugin.setup(self.context, self.key_binding_manager, self.status_provider)

    def unregister_plugin(self, plugin_name: str) -> None:
        """удаление плагина"""
        plugin = self.plugin_manager.get_plugin(plugin_name)
        if plugin:
            plugin.teardown(self.context, self.key_binding_manager, self.status_provider)
            self.plugin_manager.unregister_plugin(plugin_name)

    def press_key(self, key: str) -> str:
        command = self.key_binding_manager.get_command(key)
        if command is None:
            return f"Unknown key: {key}"

        metadata = self.command_invoker.execute_command(command, self.context)
        
        return f"Executed: {metadata.type}"

    def undo(self) -> str:
        result = self.command_invoker.undo(self.context)
        if result is None:
            return "Nothing to undo"
        
        return f"Undone: {result.type}"

    def redo(self) -> str:
        result = self.command_invoker.redo(self.context)
        if result is None:
            return "Nothing to redo"
        
        return f"Redone: {result.type}"

    def save_state(self) -> bool:
        return self.state_service.save_state()

    def load_state(self) -> bool:
        return self.state_service.load_state()

    def get_text(self) -> str:
        text_buffer = self.context.get_component("text_buffer")
        return text_buffer.get_text() if text_buffer else ""

    def get_status(self) -> str:
        return self.status_provider.get_status()
