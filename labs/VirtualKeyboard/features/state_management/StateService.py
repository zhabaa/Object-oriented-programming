from core.infrastructure.serialization import KeyboardMemento, KeyboardStateManager, ExtensibleCommandSerializer
from features.keybindings import KeyBindingManager
from features.plugins import PluginManager


class StateService:
    def __init__(self, key_binding_manager: KeyBindingManager, 
                 plugin_manager: PluginManager):
        self.key_binding_manager = key_binding_manager
        self.plugin_manager = plugin_manager
        self.state_manager = KeyboardStateManager()
        self.serializer = ExtensibleCommandSerializer(plugin_manager)

    def save_state(self) -> bool:
        serialized_bindings = {
            key: self.serializer.serialize(command)
            for key, command in self.key_binding_manager.get_all_bindings().items()
        }
        memento = KeyboardMemento(serialized_bindings)
        return self.state_manager.save(memento)

    def load_state(self) -> bool:
        memento = self.state_manager.load()
        if memento is None:
            return False

        try:
            bindings = {}

            for key, cmd_data in memento.bindings.items():
                bindings[key] = self.serializer.deserialize(cmd_data)

            self.key_binding_manager.set_bindings(bindings)
            return True

        except Exception:
            return False
