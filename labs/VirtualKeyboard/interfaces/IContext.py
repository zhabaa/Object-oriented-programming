from abc import ABC, abstractmethod
from typing import Any, Dict


class IContext(ABC):
    @abstractmethod
    def register_component(self, name: str, component: Any) -> None:
        pass

    @abstractmethod
    def get_component(self, name: str) -> Any:
        pass

    @abstractmethod
    def get_all_components(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def remove_component(self, name: str) -> bool:
        pass
