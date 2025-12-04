"""
Лабораторная работа 7 — Dependency Injection (внедрение зависимостей)
Реализация контейнера-инжектора на Python с поддержкой жизненных циклов:
 - PerRequest: каждый вызов -> новый экземпляр
 - Scoped: один экземпляр внутри scope (контекстного менеджера `with`)
 - Singleton: всегда один и тот же экземпляр

Поддерживается:
 - регистрация интерфейса -> класс
 - регистрация интерфейса -> фабричный метод
 - передача дополнительных параметров для конструктора
 - автоматическое внедрение зависимостей в конструктор по типам параметров
 - типизация, OOP-принципы, комментарии

Файл содержит:
 - enum LifeStyle
 - класс Registration
 - класс Injector
 - класс Scope (контекстный менеджер)
 - 3 интерфейса (Interface1/2/3) и по 2 реализации каждого
 - 2 разные конфигурации регистрации (configure_a / configure_b)
 - демонстрация использования

Запуск: python lab7_di_injector.py
"""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Type, Tuple, get_type_hints
from enum import Enum
from dataclasses import dataclass
import inspect
from abc import ABC, abstractmethod


class LifeStyle(Enum):
    PerRequest = "PerRequest"
    Scoped = "Scoped"
    Singleton = "Singleton"


@dataclass
class Registration:
    # либо concrete_class - тип класса, либо factory - callable
    concrete_class: Optional[Type[Any]] = None
    factory: Optional[Callable[[], Any]] = None
    lifestyle: LifeStyle = LifeStyle.PerRequest
    params: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}


class Scope:
    """Контекст для Scoped объектов.
    Используется как:
        with injector.create_scope() as scope:
            obj = scope.get_instance(Interface1)
    """

    def __init__(self, injector: Injector = None):
        # чтобы избежать forward reference в типах, аннотация выше
        self._injector = injector
        self._instances: Dict[Type[Any], Any] = {}

    def get_instance(self, interface_type: Type[Any]) -> Any:
        return self._injector.get_instance(interface_type, scope=self)

    def _get_scoped(self, interface_type: Type[Any]) -> Optional[Any]:
        return self._instances.get(interface_type)

    def _set_scoped(self, interface_type: Type[Any], instance: Any) -> None:
        self._instances[interface_type] = instance


class Injector:
    """Простой DI контейнер.

    Принципы реализации:
    - Single Responsibility: Injector отвечает только за регистрацию и разрешение зависимостей.
    - Open/Closed: можно добавлять новые регистрации и фабрики,
      не модифицируя основной код разрешения.
    - Dependency Inversion: код использует абстракции (типы/интерфейсы).
    - Liskov / Interface Segregation применимы к интерфейсам в примерах.

    Примечание: В данной реализации внедрение зависимостей происходит по
    аннотациям типов параметров конструктора (PEP 484). Для простоты
    не поддержана циклическая зависимость.
    """

    def __init__(self):
        # registry: mapping interface -> Registration
        self._registry: Dict[Type[Any], Registration] = {}
        # singletons cache
        self._singletons: Dict[Type[Any], Any] = {}

    def register(self,
                 interface_type: Type[Any],
                 class_type: Optional[Type[Any]] = None,
                 life_circle: LifeStyle = LifeStyle.PerRequest,
                 params: Tuple[Any, ...] = (),
                 kwargs: Optional[Dict[str, Any]] = None,
                 factory: Optional[Callable[[], Any]] = None) -> None:
        """Регистрация: можно передать либо class_type, либо factory.
        params/kwargs -- будут переданы в конструктор при создании.
        """
        if factory is None and class_type is None:
            raise ValueError("Нужно указать class_type или factory")

        reg = Registration(concrete_class=class_type,
                           factory=factory,
                           lifestyle=life_circle,
                           params=params,
                           kwargs=kwargs or {})
        self._registry[interface_type] = reg

    def create_scope(self) -> Scope:
        return Scope(injector=self)

    def get_instance(self, interface_type: Type[Any], scope: Scope | None = None) -> Any:
        """Получить экземпляр по интерфейсу.

        Если lifestyle == Scoped, обязательно использовать scope (внутри with).
        Если lifestyle == Singleton, возвращаем кешированный экземпляр.
        Если lifestyle == PerRequest, создаём новый объект каждый раз.
        """
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
        # Factory method
        if reg.factory is not None:
            # фабрика может сама требовать аргументы, но в нашем API фабрика — callable без args
            return reg.factory()

        cls = reg.concrete_class
        assert cls is not None

        # Попытка автоматического внедрения зависимостей через сигнатуру __init__
        constructor = getattr(cls, '__init__', None)
        if constructor is None:
            # класс без конструктора
            return cls(*reg.params, **(reg.kwargs or {}))

        sig = inspect.signature(constructor)
        # Получаем type hints для конструктора. get_type_hints вернёт полный mapping включая позаимствованные generic.
        # Мы хотим читать аннотации для параметров кроме 'self'.
        hints = get_type_hints(constructor)

        args = list(reg.params)
        kwargs = dict(reg.kwargs or {})

        # Перебираем параметры конструктора (skip self)
        for name, param in list(sig.parameters.items()):
            if name == 'self':
                continue
            # если параметр явно указан в kwargs - пропускаем (переопределение вручную)
            if name in kwargs:
                continue
            # если параметр указан в позиционных params и не в kwargs, то пропустим
            # (мы не анализируем позиционные имена)
            # Попробуем внедрить по типу если есть аннотация
            ann = hints.get(name)
            if ann is None:
                # нет аннотации — не внедряем
                continue
            # Если параметр имеет значение по умолчанию, и он не зарегистрирован — тоже пропускаем
            # Но если он обязательный и зарегистрирован — внедрим
            try:
                # рекурсивно запрашиваем зависимость
                dependency = self.get_instance(ann, scope=scope)
                kwargs[name] = dependency
            except KeyError:
                # зависимость не зарегистрирована - пропускаем, оставляем дефолт или пользовательское значение
                continue

        # Наконец создаём экземпляр
        return cls(*args, **kwargs)


# ---- Примеры интерфейсов и реализаций ----
class Interface1(ABC):
    @abstractmethod
    def run(self) -> str:
        pass


class Interface2(ABC):
    @abstractmethod
    def info(self) -> str:
        pass


class Interface3(ABC):
    @abstractmethod
    def compute(self) -> int:
        pass


# Реализации для Interface1
class Class1Debug(Interface1):
    def __init__(self, dep2: Interface2):
        # демонстрируем внедрение зависимости Interface2
        self._dep2 = dep2

    def run(self) -> str:
        return f"Class1Debug -> {self._dep2.info()}"


class Class1Release(Interface1):
    def __init__(self, value: int = 42):
        self._value = value

    def run(self) -> str:
        return f"Class1Release value={self._value}"


# Реализации для Interface2
class Class2Debug(Interface2):
    def __init__(self, dep3: Interface3):
        self._dep3 = dep3

    def info(self) -> str:
        return f"Class2Debug -> compute={self._dep3.compute()}"


class Class2Release(Interface2):
    def info(self) -> str:
        return "Class2Release: production" 


# Реализации для Interface3
class Class3Debug(Interface3):
    def __init__(self, base: int = 1):
        self._base = base

    def compute(self) -> int:
        return self._base * 100


class Class3Release(Interface3):
    def compute(self) -> int:
        return 999
