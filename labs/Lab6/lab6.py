import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional, Tuple, Union
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


class Command(ABC):
    @abstractmethod
    def execute(self, context: Any) -> CommandMetadata:
        pass

    @abstractmethod
    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        pass


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


# region mediaplayer


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


class MediaPlayCommand(Command):
    def execute(self, context: Any) -> CommandMetadata:
        media_player: MediaPlayer = context.media_player
        media_player.is_playing = True
        return CommandMetadata(type="media_on")

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        media_player: MediaPlayer = context.media_player
        media_player.is_playing = False
        return CommandMetadata(type="media_off")


class VolumeUpCommand(Command):
    def __init__(self, step: int = 10):
        self.step: int = step
        self._previous_volume: Optional[int] = None

    def execute(self, context: Any) -> CommandMetadata:
        media_player: MediaPlayer = context.media_player
        self._previous_volume = media_player.volume
        new_volume = media_player.volume_up(self.step)
        return CommandMetadata(type="vol_up", step=new_volume)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        media_player: MediaPlayer = context.media_player
        
        if self._previous_volume is not None:
            media_player.volume = self._previous_volume
        
        return CommandMetadata(type="undo_vol_up")


class VolumeDownCommand(Command):
    def __init__(self, step: int = 10):
        self.step: int = step
        self._previous_volume: Optional[int] = None

    def execute(self, context: Any) -> CommandMetadata:
        media_player: MediaPlayer = context.media_player
        self._previous_volume = media_player.volume
        new_volume = media_player.volume_down(self.step)
        return CommandMetadata(type="vol_down", step=new_volume)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        media_player: MediaPlayer = context.media_player
        
        if self._previous_volume is not None:
            media_player.volume = self._previous_volume
        
        return CommandMetadata(type="undo_vol_down")


# endregion


class PrintCharCommand(Command):
    def __init__(self, char: str):
        self.char: str = char

    def execute(self, context: Any) -> CommandMetadata:
        text_buffer: TextBuffer = context.text_buffer
        case_handler: CaseHandler = context.case_handler
        
        actual_char = self.char

        if self.char.isalpha():
            if case_handler.is_upper:
                actual_char = self.char.upper() 
            else:
                actual_char = self.char.lower()
        
        text_buffer.append(actual_char)

        return CommandMetadata(type="print", char=actual_char)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        text_buffer: TextBuffer = context.text_buffer

        if metadata.char:
            text_buffer.remove_last(len(metadata.char))

        return CommandMetadata(type="undo_print")


class BackspaceCommand(Command):
    def execute(self, context: Any) -> CommandMetadata:
        text_buffer: TextBuffer = context.text_buffer
        removed = text_buffer.remove_last()
        return CommandMetadata(type="backspace", char=removed)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        text_buffer: TextBuffer = context.text_buffer
        
        if metadata.char:
            text_buffer.append(metadata.char)
        
        return CommandMetadata(type="undo_backspace")


class ToggleCaseCommand(Command):
    def execute(self, context: Any) -> CommandMetadata:
        case_handler: CaseHandler = context.case_handler
        case_handler.toggle_case()
        return CommandMetadata(type="toggle", is_upper=case_handler.is_upper)

    def undo(self, context: Any, metadata: CommandMetadata) -> CommandMetadata:
        case_handler: CaseHandler = context.case_handler
        case_handler.toggle_case()
        return CommandMetadata(type="undo_toggle", is_upper=case_handler.is_upper)


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


class CommandSerializer:
    _registry: Dict[str, type] = {
        "PrintCharCommand": PrintCharCommand,
        "BackspaceCommand": BackspaceCommand,
        "VolumeUpCommand": VolumeUpCommand,
        "VolumeDownCommand": VolumeDownCommand,
        "MediaPlayCommand": MediaPlayCommand,
        "ToggleCaseCommand": ToggleCaseCommand,
    }

    @staticmethod
    def serialize(cmd: Command) -> SerializedCommand:
        if isinstance(cmd, PrintCharCommand):
            return SerializedCommand(type="PrintCharCommand", char=cmd.char)
        
        elif isinstance(cmd, (VolumeUpCommand, VolumeDownCommand)):
            return SerializedCommand(type=type(cmd).__name__, step=cmd.step)
        
        else:
            return SerializedCommand(type=type(cmd).__name__)

    @staticmethod
    def deserialize(data: SerializedCommand) -> Command:
        cls = CommandSerializer._registry.get(data.type)
        
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


class Context:
    def __init__(self):
        self.text_buffer = TextBuffer()
        self.media_player = MediaPlayer()
        self.case_handler = CaseHandler()


class VirtualKeyboard:
    def __init__(self):
        self.context = Context()
        self.key_bindings: Dict[str, Command] = {}
        self.history = CommandHistory()
        self.state_manager = KeyboardStateManager()
        
        self.setup_default_bindings()
        self.load_state()

    def setup_default_bindings(self) -> None:
        # Letters
        for ch in "abcdefghijklmnopqrstuvwxyz":
            self.bind_key(ch, PrintCharCommand(ch))
        
        # Digits
        for d in "0123456789":
            self.bind_key(d, PrintCharCommand(d))
        
        # Special keys
        self.bind_key("space", PrintCharCommand(" "))
        self.bind_key("backspace", BackspaceCommand())
        self.bind_key("caps", ToggleCaseCommand())
        self.bind_key("volume_up", VolumeUpCommand())
        self.bind_key("volume_down", VolumeDownCommand())
        self.bind_key("media_play", MediaPlayCommand())

    def bind_key(self, key: str, command: Command) -> None:
        self.key_bindings[key] = command

    def press_key(self, key: str) -> str:
        if key not in self.key_bindings:
            return f"Unknown key: {key}"
        
        command = self.key_bindings[key]
        metadata = command.execute(self.context)
        self.history.push(command, metadata)
        
        return f"Executed: {metadata.type}"

    def undo(self) -> str:
        item = self.history.pop()
        if item is None:
            return "Nothing to undo"
        
        command, metadata = item
        undo_metadata = command.undo(self.context, metadata)
        self.history.push_redo(command, metadata)
        
        return f"Undone: {undo_metadata.type}"

    def redo(self) -> str:
        item = self.history.pop_redo()
        if item is None:
            return "Nothing to redo"
        
        command, old_metadata = item
        new_metadata = command.execute(self.context)
        self.history.push(command, new_metadata)
        
        return f"Redone: {new_metadata.type}"

    def save_state(self) -> bool:
        serialized_bindings = {
            key: CommandSerializer.serialize(command) 
            for key, command in self.key_bindings.items()
        }
        memento = KeyboardMemento(serialized_bindings)
        return self.state_manager.save(memento)

    def load_state(self) -> bool:
        memento = self.state_manager.load()
        if memento is None:
            return False
        
        try:
            for key, cmd_data in memento.bindings.items():
                self.key_bindings[key] = CommandSerializer.deserialize(cmd_data)
            return True
        except Exception:
            return False

    def get_text(self) -> str:
        return self.context.text_buffer.get_text()

    def get_status(self) -> str:
        return (f"TEXT: {self.get_text()}\n"
                f"CAPS: {'ON' if self.context.case_handler.is_upper else 'OFF'}\n"
                f"VOLUME: {self.context.media_player.volume}\n"
                f"MEDIA: {'PLAYING' if self.context.media_player.is_playing else 'STOPPED'}")

