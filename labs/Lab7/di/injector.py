import inspect
from typing import Any, Callable, Dict, Optional, Tuple, Type, get_type_hints

from di.lifestyle import LifeStyle
from di.registration import Registration
from di.scope import Scope


class Injector:
    """
    внедрение зависимостей происходит по аннотациям типов параметров 
    конструктора pep 484
    
    не поддержана циклическая зависимость
    """

    def __init__(self):
        self._registry: Dict[Type[Any], Registration] = {}
        self._singletons: Dict[Type[Any], Any] = {}

    def register(self, interface_type: Type[Any],
                 class_type: Optional[Type[Any]] = None,
                 life_circle: LifeStyle = LifeStyle.PerRequest,
                 params: Tuple[Any, ...] = (),
                 kwargs: Optional[Dict[str, Any]] = None,
                 factory: Optional[Callable[[], Any]] = None) -> None:

        if factory is None and class_type is None:
            raise ValueError("Нужно указать class_type или factory")

        reg = Registration(concrete_class=class_type, factory=factory,
                           lifestyle=life_circle, params=params, kwargs=kwargs or {})

        self._registry[interface_type] = reg

    def create_scope(self) -> Scope:
        return Scope(injector=self)

    def get_instance(self, interface_type: Type[Any], scope: Scope | None = None) -> Any:
        if interface_type not in self._registry:
            raise KeyError(f"Тип {interface_type} не зарегистрирован в контейнере")

        reg = self._registry[interface_type]
        
        # Singleton
        if reg.lifestyle == LifeStyle.Singleton:
            if interface_type not in self._singletons:
                instance = self._create_instance(reg, scope)
                self._singletons[interface_type] = instance

            return self._singletons[interface_type]

        # Scoped
        if reg.lifestyle == LifeStyle.Scoped:
            if scope is None:
                raise RuntimeError("Scoped объект запрошен вне Scope. Используйте with injector.create_scope()")
            
            cached = scope._get_scoped(interface_type)
            
            if cached is None:
                instance = self._create_instance(reg, scope)
                scope._set_scoped(interface_type, instance)
            
                return instance
            
            return cached

        # PerRequest
        return self._create_instance(reg, scope)

    def _create_instance(self, reg: Registration, scope: Scope | None) -> Any:
        if reg.factory is not None:
            return reg.factory()

        cls = reg.concrete_class

        assert cls is not None

        constructor = getattr(cls, '__init__', None)

        if constructor is None:
            return cls(*reg.params, **(reg.kwargs or {}))

        sig = inspect.signature(constructor)
        hints = get_type_hints(constructor)

        args = list(reg.params)
        kwargs = dict(reg.kwargs or {})

        for name, param in list(sig.parameters.items()):
            if name == 'self':
                continue

            if name in kwargs:
                continue

            ann = hints.get(name)
            
            if ann is None:
                continue

            try:
                dependency = self.get_instance(ann, scope=scope)
                kwargs[name] = dependency

            except KeyError:
                continue

        return cls(*args, **kwargs)
