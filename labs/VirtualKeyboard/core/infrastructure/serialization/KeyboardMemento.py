from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict

from core.typing import SerializedCommand


class KeyboardMemento:
    def __init__(self, bindings: Dict[str, SerializedCommand]):
        self.bindings = bindings
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bindings": {k: asdict(v) for k, v in self.bindings.items()},
            "timestamp": self.timestamp.isoformat(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "KeyboardMemento":
        bindings = {k: SerializedCommand(**v) for k, v in data["bindings"].items()}
        memento = KeyboardMemento(bindings)
        memento.timestamp = datetime.fromisoformat(data["timestamp"])
        return memento
