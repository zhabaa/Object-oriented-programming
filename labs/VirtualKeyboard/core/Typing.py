from dataclasses import dataclass
from typing import Optional


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
