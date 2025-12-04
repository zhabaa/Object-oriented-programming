from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Type

from di.lifestyle import LifeStyle


@dataclass
class Registration:
    concrete_class: Optional[Type[Any]] = None
    factory: Optional[Callable[[], Any]] = None
    lifestyle: LifeStyle = LifeStyle.PerRequest

    params: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}
