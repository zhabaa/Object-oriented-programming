from typing import Any, Dict, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from di.injector import Injector


class Scope:
    def __init__(self, injector: "Injector" = None):
        self._injector: "Injector" | None = injector
        self._instances: Dict[Type[Any], Any] = {}

    def get_instance(self, interface_type: Type[Any]) -> Any:
        return self._injector.get_instance(interface_type, scope=self)

    def _get_scoped(self, interface_type: Type[Any]) -> Optional[Any]:
        return self._instances.get(interface_type)

    def _set_scoped(self, interface_type: Type[Any], instance: Any) -> None:
        self._instances[interface_type] = instance

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._instances.clear()
