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

    def execute(self) -> str:
        return self.char

    def undo(self) -> str:
        return "[BACKSPACE]"


class VolumeUpCommand(Command):
    def __init__(self, step: int = 10):
        self.step = step

    def execute(self) -> str:
        return f"volume increased +{self.step}%"

    def undo(self) -> str:
        return f"volume decreased +{self.step}%"


class VolumeDownCommand(Command):
    def __init__(self, step: int = 10):
        self.step = step

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


class KeyboardMemento:
    def __init__(self, key_bindings: Dict[str, Dict[str, Any]]):
        self.key_bindings = key_bindings
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_bindings": self.key_bindings,
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "KeyboardMemento":
        memento = KeyboardMemento(data["key_bindings"])
        memento.timestamp = datetime.fromisoformat(data["timestamp"])
        return memento


class KeyboardStateSaver:
    def __init__(self, filename: str = "keyboard_state.json"):
        self.filename = filename

    def save(self, memento: KeyboardMemento) -> bool:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(memento.to_dict(), f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Error saving state: {e}")
            return False

    def load(self) -> Optional[KeyboardMemento]:
        try:
            if not os.path.exists(self.filename):
                return None

            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            return KeyboardMemento.from_dict(data)

        except Exception as e:
            print(f"Error loading state: {e}")
            return None


class VirtualKeyboard:
    def __init__(self):
        self.key_bindings: Dict[str, Command] = dict()
        self.history: List[Command] = list()
        self.redo_stack: List[Command] = list()
        self.output_text = str()
        self.state_saver = KeyboardStateSaver()

        self.setup_default_bindings()
        self.load_state()

    def setup_default_bindings(self):
        for char in "abcdefghijklmnopqrstuvwxyz":
            self.bind_key(char, PrintCharCommand(char))

        for digit in "0123456789":
            self.bind_key(digit, PrintCharCommand(digit))

        self.bind_key("ctrl++", VolumeUpCommand())
        self.bind_key("ctrl+-", VolumeDownCommand())
        self.bind_key("ctrl+p", MediaPlayerCommand())
        self.bind_key("caps", ToggleCaseCommand())

    def bind_key(self, key_combination: str, command: Command):
        self.key_bindings[key_combination] = command

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
        key_bindings_data = {}

        for key, command in self.key_bindings.items():
            match command:
                case PrintCharCommand():
                    key_bindings_data[key] = {
                        "type": "PrintCharCommand",
                        "char": command.char,
                    }

                case VolumeUpCommand():
                    key_bindings_data[key] = {
                        "type": "VolumeUpCommand",
                        "step": command.step,
                    }

                case VolumeDownCommand():
                    key_bindings_data[key] = {
                        "type": "VolumeDownCommand",
                        "step": command.step,
                    }

                case MediaPlayerCommand():
                    key_bindings_data[key] = {"type": "MediaPlayerCommand"}

                case ToggleCaseCommand():
                    key_bindings_data[key] = {"type": "ToggleCaseCommand"}

                case _:
                    key_bindings_data[key] = {
                        "type": "UnknownCommand",
                        "repr": repr(command),
                    }

            memento = KeyboardMemento(key_bindings_data)
            self.state_saver.save(memento)
            return "State saved successfully"

    def load_state(self):
        memento = self.state_saver.load()
        if memento:
            for key, command_data in memento.key_bindings.items():
                cmd_type = command_data.get("type")

                match cmd_type:
                    case "PrintCharCommand":
                        self.key_bindings[key] = PrintCharCommand(command_data["char"])

                    case "VolumeUpCommand":
                        self.key_bindings[key] = VolumeUpCommand(command_data.get("step", 10))

                    case "VolumeDownCommand":
                        self.key_bindings[key] = VolumeDownCommand(command_data.get("step", 10))

                    case "MediaPlayerCommand":
                        self.key_bindings[key] = MediaPlayerCommand()

                    case "ToggleCaseCommand":
                        self.key_bindings[key] = ToggleCaseCommand()

                    case _:
                        print(f"Warning: Unknown command type '{cmd_type}' for key '{key}'")

    def get_output(self) -> str:
        return self.output_text

    def display_status(self):
        print(f"Current text: '{self.output_text}'")
        print(f"History length: {len(self.history)}, Redo stack: {len(self.redo_stack)}")
        print("Key bindings:", list(self.key_bindings.keys()))
