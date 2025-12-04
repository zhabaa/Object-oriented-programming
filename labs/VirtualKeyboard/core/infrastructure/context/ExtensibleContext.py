from typing import Any, Dict

from core import IContext


class ExtensibleContext(IContext):
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
