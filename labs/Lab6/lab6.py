import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
import string
from typing import Dict, List, Any, Optional, Tuple, Callable, Type
from datetime import datetime


# region Typing
@dataclass
class CommandMetadata:
    type: str
    char: Optional[str] = None
    step: Optional[int] = None
    is_upper: Optional[bool] = None


@dataclass
class SerializedCommand:
    type: str
    char: Optional[str] = None
    step: Optional[int] = None

# endregion

# region PluginSystem

class KeyboardPlugin(ABC):
    """Базовый класс для всех плагинов клавиатуры"""
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    def setup(self, keyboard: 'VirtualKeyboard') -> None:
        """Вызывается при регистрации плагина"""
        pass
    
    def teardown(self, keyboard: 'VirtualKeyboard') -> None:
        """Вызывается при удалении плагина"""
        pass


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
    
    def setup_plugins(self, keyboard: 'VirtualKeyboard') -> None:
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

# endregion

#region Commands

class Command(ABC):
    @abstractmethod
    def execute(self, context: Any) -> CommandMetadata:
        pass

    @abstractmethod
    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        pass


class PrintCharCommand(Command):
    def __init__(self, char: str):
        self.char: str = char

    def execute(self, context: Any) -> CommandMetadata:
        text_buffer = context.get_component("text_buffer")
        case_handler = context.get_component("case_handler")
        
        actual_char = self.char
        if self.char.isalpha():
            actual_char = self.char.upper() if case_handler.is_upper else self.char.lower()
        
        text_buffer.append(actual_char)
        return CommandMetadata(type="print", char=actual_char)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        if metadata.char:
            context.get_component("text_buffer").remove_last(len(metadata.char))
        return CommandMetadata(type="undo_print")


class BackspaceCommand(Command):
    def execute(self, context: Any) -> CommandMetadata:
        text_buffer = context.get_component("text_buffer")
        removed = text_buffer.remove_last()
        return CommandMetadata(type="backspace", char=removed)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        if metadata.char:
            context.get_component("text_buffer").append(metadata.char)
        return CommandMetadata(type="undo_backspace")


class ToggleCaseCommand(Command):
    def execute(self, context: Any) -> CommandMetadata:
        case_handler = context.get_component("case_handler")
        case_handler.toggle_case()
        return CommandMetadata(type="toggle", is_upper=case_handler.is_upper)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        context.get_component("case_handler").toggle_case()
        return CommandMetadata(type="undo_toggle", is_upper=context.get_component("case_handler").is_upper)


class MediaPlayCommand(Command):
    def execute(self, context: Any) -> CommandMetadata:
        context.get_component("media_player").is_playing = True
        return CommandMetadata(type="media_on")

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        context.get_component("media_player").is_playing = False
        return CommandMetadata(type="media_off")


class VolumeUpCommand(Command):
    def __init__(self, step: int = 10):
        self.step: int = step

    def execute(self, context: Any) -> CommandMetadata:
        media_player = context.get_component("media_player")
        new_volume = media_player.volume_up(self.step)
        return CommandMetadata(type="vol_up", step=new_volume)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        context.get_component("media_player").volume_down(self.step)
        return CommandMetadata(type="undo_vol_up")


class VolumeDownCommand(Command):
    def __init__(self, step: int = 10):
        self.step: int = step

    def execute(self, context: Any) -> CommandMetadata:
        media_player = context.get_component("media_player")
        new_volume = media_player.volume_down(self.step)
        return CommandMetadata(type="vol_down", step=new_volume)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        context.get_component("media_player").volume_up(self.step)
        return CommandMetadata(type="undo_vol_down")


# endregion

# region Domain modules


class TextBuffer:
    def __init__(self):
        self._text: str = ""
    
    def append(self, text: str) -> None:
        self._text += text
    
    def remove_last(self, count: int = 1) -> str:
        if count <= 0 or count > len(self._text):
            return ""
        removed = self._text[-count:]
        self._text = self._text[:-count]
        return removed
    
    def get_text(self) -> str:
        return self._text
    
    def clear(self) -> None:
        self._text = ""


class MediaPlayer:
    def __init__(self):
        self._volume: int = 50
        self._is_playing: bool = False
    
    @property
    def volume(self) -> int:
        return self._volume
    
    @volume.setter
    def volume(self, value: int) -> None:
        self._volume = max(0, min(100, value))
    
    @property
    def is_playing(self) -> bool:
        return self._is_playing
    
    @is_playing.setter
    def is_playing(self, state: bool) -> None:
        self._is_playing = state
    
    def volume_up(self, step: int = 10) -> int:
        self.volume = self.volume + step
        return self.volume
    
    def volume_down(self, step: int = 10) -> int:
        self.volume = self.volume - step
        return self.volume


class CaseHandler:
    def __init__(self):
        self._is_upper: bool = False
    
    @property
    def is_upper(self) -> bool:
        return self._is_upper
    
    def toggle_case(self) -> None:
        self._is_upper = not self._is_upper
    
    def set_upper_case(self, is_upper: bool) -> None:
        self._is_upper = is_upper


# endregion

# region ExtensibleContext


class ExtensibleContext:
    """Расширяемый контекст для хранения компонентов"""
    
    def __init__(self):
        self._components: Dict[str, Any] = {}
    
    def register_component(self, name: str, component: Any) -> None:
        self._components[name] = component
    
    def get_component(self, name: str) -> Any:
        return self._components.get(name)
    
    def get_all_components(self) -> Dict[str, Any]:
        return self._components.copy()
    
    def remove_component(self, name: str) -> None:
        if name in self._components:
            del self._components[name]


# ==================== HISTORY MANAGEMENT ====================
class CommandHistory:
    def __init__(self):
        self._history: List[Tuple[Command, CommandMetadata]] = []
        self._redo_stack: List[Tuple[Command, CommandMetadata]] = []
    
    def push(self, command: Command, metadata: CommandMetadata) -> None:
        self._history.append((command, metadata))
        self._redo_stack.clear()
    
    def pop(self) -> Optional[Tuple[Command, CommandMetadata]]:
        if not self._history:
            return None
        return self._history.pop()
    
    def push_redo(self, command: Command, metadata: CommandMetadata) -> None:
        self._redo_stack.append((command, metadata))
    
    def pop_redo(self) -> Optional[Tuple[Command, CommandMetadata]]:
        if not self._redo_stack:
            return None
        return self._redo_stack.pop()
    
    def clear(self) -> None:
        self._history.clear()
        self._redo_stack.clear()


# endregion

# region Serialization

class ExtensibleCommandSerializer:
    """Расширяемый сериализатор команд"""
    
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
    
    def serialize(self, cmd: Command) -> SerializedCommand:
        if isinstance(cmd, PrintCharCommand):
            return SerializedCommand(type="PrintCharCommand", char=cmd.char)
        elif isinstance(cmd, (VolumeUpCommand, VolumeDownCommand)):
            return SerializedCommand(type=type(cmd).__name__, step=cmd.step)
        else:
            return SerializedCommand(type=type(cmd).__name__)

    def deserialize(self, data: SerializedCommand) -> Command:
        registry = self.plugin_manager.get_command_registry()
        cls = registry.get(data.type)
        
        if cls is None:
            raise ValueError(f"Unknown command type: {data.type}")
        
        if data.type == "PrintCharCommand":
            return cls(data.char)
        elif data.type in ["VolumeUpCommand", "VolumeDownCommand"]:
            return cls(data.step or 10)
        else:
            return cls()


class KeyboardMemento:
    def __init__(self, bindings: Dict[str, SerializedCommand]):
        self.bindings = bindings
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bindings": {k: asdict(v) for k, v in self.bindings.items()},
            "timestamp": self.timestamp.isoformat()
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "KeyboardMemento":
        bindings = {k: SerializedCommand(**v) for k, v in data["bindings"].items()}
        memento = KeyboardMemento(bindings)
        memento.timestamp = datetime.fromisoformat(data["timestamp"])
        return memento


class KeyboardStateManager:
    def __init__(self, filename: str = "keyboard_state.json"):
        self.filename = filename

    def save(self, memento: KeyboardMemento) -> bool:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(memento.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False

    def load(self) -> Optional[KeyboardMemento]:
        if not os.path.exists(self.filename):
            return None
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return KeyboardMemento.from_dict(data)
        except Exception:
            return None

# endregion

#region Keyboard Core

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


class KeyboardCommandInvoker:
    """Выполнение команд и управление историей"""
    
    def __init__(self):
        self.history = CommandHistory()
    
    def execute_command(self, command: Command, context: ExtensibleContext) -> CommandMetadata:
        metadata = command.execute(context)
        self.history.push(command, metadata)
        return metadata
    
    def undo(self, context: ExtensibleContext) -> Optional[CommandMetadata]:
        item = self.history.pop()
        if item is None:
            return None
        
        command, metadata = item
        undo_metadata = command.undo(context, metadata)
        self.history.push_redo(command, metadata)
        return undo_metadata
    
    def redo(self, context: ExtensibleContext) -> Optional[CommandMetadata]:
        item = self.history.pop_redo()
        if item is None:
            return None
        
        command, old_metadata = item
        new_metadata = command.execute(context)
        self.history.push(command, new_metadata)
        return new_metadata


class KeyboardStateService:
    """Сохранение и восстановление состояния клавиатуры"""
    
    def __init__(self, key_binding_manager: KeyBindingManager, plugin_manager: PluginManager):
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


class KeyboardStatusProvider:
    """Предоставление статуса клавиатуры"""
    
    def __init__(self, context: ExtensibleContext):
        self.context = context
        self._status_providers: List[Callable[[], str]] = []
        self._setup_default_providers()
    
    def _setup_default_providers(self):
        """Регистрация провайдеров статуса по умолчанию"""
        self.register_status_provider(self._get_text_status)
        self.register_status_provider(self._get_caps_status)
        self.register_status_provider(self._get_volume_status)
        self.register_status_provider(self._get_media_status)
    
    def _get_text_status(self) -> str:
        text_buffer = self.context.get_component("text_buffer")
        return f"TEXT: {text_buffer.get_text()}" if text_buffer else "TEXT: N/A"
    
    def _get_caps_status(self) -> str:
        case_handler = self.context.get_component("case_handler")
        return f"CAPS: {'ON' if case_handler.is_upper else 'OFF'}" if case_handler else "CAPS: N/A"
    
    def _get_volume_status(self) -> str:
        media_player = self.context.get_component("media_player")
        return f"VOLUME: {media_player.volume}" if media_player else "VOLUME: N/A"
    
    def _get_media_status(self) -> str:
        media_player = self.context.get_component("media_player")
        return f"MEDIA: {'PLAYING' if media_player.is_playing else 'STOPPED'}" if media_player else "MEDIA: N/A"
    
    def register_status_provider(self, provider: Callable[[], str]) -> None:
        self._status_providers.append(provider)
    
    def get_status(self) -> str:
        status_lines = []
        for provider in self._status_providers:
            status_lines.append(provider())
        return "\n".join(status_lines)


class DefaultKeyBindingSetup:
    """Настройка привязок клавиш по умолчанию"""

    @staticmethod
    def setup(binding_manager: KeyBindingManager, 
              plugin_manager: PluginManager) -> None:
        plugin_manager.register_command_type("PrintCharCommand", PrintCharCommand)
        plugin_manager.register_command_type("BackspaceCommand", BackspaceCommand)
        plugin_manager.register_command_type("ToggleCaseCommand", ToggleCaseCommand)
        plugin_manager.register_command_type("MediaPlayCommand", MediaPlayCommand)
        plugin_manager.register_command_type("VolumeUpCommand", VolumeUpCommand)
        plugin_manager.register_command_type("VolumeDownCommand", VolumeDownCommand)

        # Letters
        for ch in string.ascii_lowercase:
            binding_manager.bind_key(ch, PrintCharCommand(ch))

        # Digits
        for d in string.digits:
            binding_manager.bind_key(d, PrintCharCommand(d))

        # Special keys
        binding_manager.bind_key("space", PrintCharCommand(" "))
        binding_manager.bind_key("backspace", BackspaceCommand())
        binding_manager.bind_key("caps", ToggleCaseCommand())
        binding_manager.bind_key("volume_up", VolumeUpCommand())
        binding_manager.bind_key("volume_down", VolumeDownCommand())
        binding_manager.bind_key("media_play", MediaPlayCommand())


class DefaultComponentSetup:
    """Настройка компонентов по умолчанию"""
    
    @staticmethod
    def setup(context: ExtensibleContext) -> None:
        context.register_component("text_buffer", TextBuffer())
        context.register_component("media_player", MediaPlayer())
        context.register_component("case_handler", CaseHandler())

# endregion

# region main keyboard class

class VirtualKeyboard:
    """Координирует работу всех компонентов клавиатуры с поддержкой плагинов"""
    
    def __init__(self, plugins: List[KeyboardPlugin] = None):
        self.context = ExtensibleContext()
        self.plugin_manager = PluginManager()
        self.key_binding_manager = KeyBindingManager()
        self.command_invoker = KeyboardCommandInvoker()
        self.state_service = KeyboardStateService(self.key_binding_manager, self.plugin_manager)
        self.status_provider = KeyboardStatusProvider(self.context)
        
        # Настройка по умолчанию
        DefaultComponentSetup.setup(self.context)
        DefaultKeyBindingSetup.setup(self.key_binding_manager, self.plugin_manager)
        
        # Регистрация и настройка плагинов
        if plugins:
            for plugin in plugins:
                self.plugin_manager.register_plugin(plugin)
        
        self.plugin_manager.setup_plugins(self)
        self.state_service.load_state()

    def register_plugin(self, plugin: KeyboardPlugin) -> None:
        """Динамическая регистрация плагина"""
        self.plugin_manager.register_plugin(plugin)
        plugin.setup(self)

    def unregister_plugin(self, plugin_name: str) -> None:
        """Динамическое удаление плагина"""
        plugin = self.plugin_manager._plugins.get(plugin_name)
        if plugin:
            plugin.teardown(self)
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

# endregion

# region external methods

class BrightnessController:
    def __init__(self):
        self._brightness: int = 50
    
    @property
    def brightness(self) -> int:
        return self._brightness
    
    @brightness.setter
    def brightness(self, value: int) -> None:
        self._brightness = max(0, min(100, value))
    
    def brightness_up(self, step: int = 10) -> int:
        self.brightness = self.brightness + step
        return self.brightness
    
    def brightness_down(self, step: int = 10) -> int:
        self.brightness = self.brightness - step
        return self.brightness


class BrightnessUpCommand(Command):
    def __init__(self, step: int = 10):
        self.step: int = step

    def execute(self, context: ExtensibleContext) -> CommandMetadata:
        brightness_controller = context.get_component("brightness")
        new_brightness = brightness_controller.brightness_up(self.step)
        return CommandMetadata(type="brightness_up", step=new_brightness)

    def undo(self, context: ExtensibleContext, metadata: CommandMetadata) -> CommandMetadata:
        brightness_controller = context.get_component("brightness")
        brightness_controller.brightness_down(self.step)
        return CommandMetadata(type="undo_brightness_up")


class BrightnessDownCommand(Command):
    def __init__(self, step: int = 10):
        self.step: int = step

    def execute(self, context: ExtensibleContext) -> CommandMetadata:
        brightness_controller = context.get_component("brightness")
        new_brightness = brightness_controller.brightness_down(self.step)
        return CommandMetadata(type="brightness_down", step=new_brightness)

    def undo(self, context: ExtensibleContext, metadata: CommandMetadata) -> CommandMetadata:
        brightness_controller = context.get_component("brightness")
        brightness_controller.brightness_up(self.step)
        return CommandMetadata(type="undo_brightness_down")


class BrightnessPlugin(KeyboardPlugin):
    """Пример плагина для управления яркостью"""
    
    def get_name(self) -> str:
        return "brightness"
    
    def setup(self, keyboard: VirtualKeyboard) -> None:
        # Регистрация компонента
        keyboard.context.register_component("brightness", BrightnessController())
        
        # Регистрация команд
        keyboard.plugin_manager.register_command_type("BrightnessUpCommand", BrightnessUpCommand)
        keyboard.plugin_manager.register_command_type("BrightnessDownCommand", BrightnessDownCommand)
        
        # Привязка клавиш
        keyboard.key_binding_manager.bind_key("brightness_up", BrightnessUpCommand())
        keyboard.key_binding_manager.bind_key("brightness_down", BrightnessDownCommand())
        
        # Регистрация провайдера статуса
        def brightness_status_provider():
            brightness_controller = keyboard.context.get_component("brightness")
            return f"BRIGHTNESS: {brightness_controller.brightness}" if brightness_controller else "BRIGHTNESS: N/A"
        
        keyboard.status_provider.register_status_provider(brightness_status_provider)
    
    def teardown(self, keyboard: VirtualKeyboard) -> None:
        # Очистка при удалении плагина
        keyboard.context.remove_component("brightness")
        # Note: В реальной системе нужно также удалить привязки клавиш и провайдеры статуса


# endregion

# ==================== USAGE EXAMPLE ====================
if __name__ == "__main__":
    # Создание клавиатуры с плагином яркости
    keyboard = VirtualKeyboard(plugins=[BrightnessPlugin()])
    
    # Использование как обычно
    keyboard.press_key("a")
    keyboard.press_key("b")
    keyboard.press_key("c")
    keyboard.press_key("caps")
    keyboard.press_key("a")  # Теперь 'A'
    
    # Использование новых функций из плагина
    keyboard.press_key("brightness_up")
    keyboard.press_key("brightness_up")
    
    print(keyboard.get_status())
    # Вывод:
    # TEXT: abcA
    # CAPS: ON
    # VOLUME: 50
    # MEDIA: STOPPED
    # BRIGHTNESS: 70
    
    # Динамическое добавление нового плагина
    # keyboard.register_plugin(SomeOtherPlugin())
