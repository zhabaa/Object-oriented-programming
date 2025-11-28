import os
import json
from typing import Optional

from serialization import KeyboardMemento


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
