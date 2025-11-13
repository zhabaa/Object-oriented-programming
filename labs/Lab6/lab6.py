import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime


class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass
    
    @abstractmethod
    def undo(self) -> str:
        pass


class PrintCharCommand(Command):
    def __init__(self, char: str):
        self.char = char
        self.executed = False
    
    def execute(self) -> str:
        self.executed = True
        return self.char
    
    def undo(self) -> str:
        return "[BACKSPACE]"


class VolumeUpCommand(Command):
    def __init__(self, step: int = 10):
        self.step = step
        self.previous_volume = None
    
    def execute(self) -> str:
        return f"volume increased +{self.step}%"
    
    def undo(self) -> str:
        return f"volume decreased +{self.step}%"


class VolumeDownCommand(Command):
    def __init__(self, step: int = 10):
        self.step = step
        self.previous_volume = None
    
    def execute(self) -> str:
        return f"volume decreased +{self.step}%"
    
    def undo(self) -> str:
        return f"volume increased +{self.step}%"


class MediaPlayerCommand(Command):
    def __init__(self):
        self.is_playing = False
    
    def execute(self) -> str:
        self.is_playing = True
        return "media player launched"
    
    def undo(self) -> str:
        self.is_playing = False
        return "media player closed"


class ToggleCaseCommand(Command):
    def __init__(self):
        self.is_upper = False
    
    def execute(self) -> str:
        self.is_upper = not self.is_upper
        mode = "UPPERCASE" if self.is_upper else "lowercase"
        return f"input mode switched to {mode}"
    
    def undo(self) -> str:
        self.is_upper = not self.is_upper
        mode = "UPPERCASE" if self.is_upper else "lowercase"
        return f"input mode switched to {mode}"


class Serializer:
    @staticmethod
    def serialize(obj: Any) -> Dict[str, Any]:
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        
        elif isinstance(obj, dict):
            return {k: Serializer.serialize(v) for k, v in obj.items()}
        
        elif isinstance(obj, list):
            return [Serializer.serialize(item) for item in obj]
        
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        
        else:
            return str(obj)
    
    @staticmethod
    def deserialize(data: Dict[str, Any], class_mapping: Dict[str, type]) -> Any:
        if '_type' in data:
            class_type = class_mapping.get(data['_type'])
        
            if class_type and hasattr(class_type, 'from_dict'):
                return class_type.from_dict(data)
        
        return data


class CommandRepresentation:
    def __init__(self, command_class: type, **kwargs):
        self.command_class = command_class
        self.kwargs = kwargs
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            '_type': self.command_class.__name__,
            'kwargs': self.kwargs
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'CommandRepresentation':
        class_mapping = {
            'PrintCharCommand':     PrintCharCommand,
            'VolumeUpCommand':      VolumeUpCommand,
            'VolumeDownCommand':    VolumeDownCommand,
            'MediaPlayerCommand':   MediaPlayerCommand,
            'ToggleCaseCommand':    ToggleCaseCommand
        }
        
        command_class = class_mapping.get(data['_type'])
        if command_class:
            return CommandRepresentation(command_class, **data.get('kwargs', {}))
        raise ValueError(f"Unknown command type: {data['_type']}")


class KeyboardMemento:
    def __init__(self, key_bindings: Dict[str, CommandRepresentation]):
        self.key_bindings = key_bindings
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            '_type': 'KeyboardMemento',
            'key_bindings': {k: Serializer.serialize(v) for k, v in self.key_bindings.items()},
            'timestamp': self.timestamp.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'KeyboardMemento':
        class_mapping = {
            'CommandRepresentation': CommandRepresentation
        }
        
        key_bindings = {}
        for k, v in data['key_bindings'].items():
            key_bindings[k] = Serializer.deserialize(v, class_mapping)
        
        memento = KeyboardMemento(key_bindings)
        memento.timestamp = datetime.fromisoformat(data['timestamp'])
        return memento


class KeyboardStateSaver:
    def __init__(self, filename: str = "keyboard_state.json"):
        self.filename = filename
    
    def save(self, memento: KeyboardMemento) -> bool:
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(Serializer.serialize(memento), f, indent=2, ensure_ascii=False)
        
            return True
        
        except Exception as e:
            print(f"Error saving state: {e}")
            return False
    
    def load(self) -> Optional[KeyboardMemento]:
        try:
            if not os.path.exists(self.filename):
                return None
            
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            class_mapping = {
                'KeyboardMemento': KeyboardMemento
            }
        
            return Serializer.deserialize(data, class_mapping)
        
        except Exception as e:
            print(f"Error loading state: {e}")
            return None


class VirtualKeyboard:
    def __init__(self):
        self.key_bindings: Dict[str, Command] = {}
        self.history: List[Command] = []
        self.redo_stack: List[Command] = []
        self.output_text = ""
        self.state_saver = KeyboardStateSaver()
        
        self.load_state()
        
        if not self.key_bindings:
            self.setup_default_bindings()
    
    def setup_default_bindings(self):
        self.bind_key('a', PrintCharCommand('a'))
        self.bind_key('b', PrintCharCommand('b'))
        self.bind_key('c', PrintCharCommand('c'))
        self.bind_key('d', PrintCharCommand('d'))
        self.bind_key('ctrl++', VolumeUpCommand())
        self.bind_key('ctrl+-', VolumeDownCommand())
        self.bind_key('ctrl+p', MediaPlayerCommand())
        self.bind_key('caps', ToggleCaseCommand())
    
    def bind_key(self, key_combination: str, command: Command):
        self.key_bindings[key_combination] = command
        self.save_state()
    
    def press_key(self, key_combination: str) -> str:
        if key_combination not in self.key_bindings:
            return f"Unknown key: {key_combination}"
        
        command = self.key_bindings[key_combination]
        result = command.execute()
        
        if isinstance(command, PrintCharCommand):
            self.output_text += result

        elif result == "[BACKSPACE]":
            self.output_text = self.output_text[:-1]
        
        self.history.append(command)
        self.redo_stack.clear()
        
        return result
    
    def undo(self) -> str:
        if not self.history:
            return "Nothing to undo"
        
        command = self.history.pop()
        result = command.undo()
        
        if result == "[BACKSPACE]":
            self.output_text = self.output_text[:-1]
        
        self.redo_stack.append(command)
        return result
    
    def redo(self) -> str:
        if not self.redo_stack:
            return "Nothing to redo"
        
        command = self.redo_stack.pop()
        result = command.execute()
        
        if isinstance(command, PrintCharCommand):
            self.output_text += result
        
        self.history.append(command)
        return result
    
    def save_state(self):
        command_reprs = {}
        for key, cmd in self.key_bindings.items():
            if isinstance(cmd, PrintCharCommand):
                command_reprs[key] = CommandRepresentation(type(cmd), char=cmd.char)

            elif isinstance(cmd, (VolumeUpCommand, VolumeDownCommand)):
                command_reprs[key] = CommandRepresentation(type(cmd), step=cmd.step)

            else:
                command_reprs[key] = CommandRepresentation(type(cmd))
        
        memento = KeyboardMemento(command_reprs)
        self.state_saver.save(memento)
    
    def load_state(self):
        memento = self.state_saver.load()

        if memento:
            self.key_bindings.clear()

            for key, cmd_repr in memento.key_bindings.items():
                command_class = cmd_repr.command_class
                kwargs = cmd_repr.kwargs
                self.key_bindings[key] = command_class(**kwargs)
    
    def get_output(self) -> str:
        return self.output_text
    
    def display_status(self):
        print(f"Current text: '{self.output_text}'")
        print(f"History length: {len(self.history)}, Redo stack: {len(self.redo_stack)}")
        print("Key bindings:", list(self.key_bindings.keys()))
