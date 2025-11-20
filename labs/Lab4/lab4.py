from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Self

class EventHandler(ABC):
    @abstractmethod
    def handle(self, sender: Any, args: Any) -> None:
        pass


class Event:
    def __init__(self):
        self._handlers: List[EventHandler] = []

    def __iadd__(self, handler: EventHandler) -> Self:
        if handler not in self._handlers:
            self._handlers.append(handler)
        return self

    def __isub__(self, handler: EventHandler) -> Self:
        if handler in self._handlers:
            self._handlers.remove(handler)
        return self

    def __call__(self, sender: Any, args: Any) -> None:
        for handler in self._handlers:
            handler.handle(sender, args)

@dataclass
class PropertyChangedEventArgs:
    property_name: str


class PropertyChangedHandler(EventHandler):
    def handle(self, sender: Any, args: PropertyChangedEventArgs) -> None:
        print(f"Property '{args.property_name}' of object {type(sender).__name__} has been changed")


class PropertyChangingEventArgs:
    def __init__(self, property_name: str, old_value: Any, new_value: Any):
        self.property_name = property_name
        self.old_value = old_value
        self.new_value = new_value
        self.can_change = True


class PropertyChangingValidator(EventHandler):
    def handle(self, sender: Any, args: PropertyChangingEventArgs) -> None:

        if isinstance(args.new_value, (int, float)) and args.new_value < 0:
            print(f"[Validation]: Cannot set negative value for {args.property_name}")
            args.can_change = False

        elif isinstance(args.new_value, str) and not args.new_value.strip():
            print(f"[Validation]: Property {args.property_name} cannot be empty")
            args.can_change = False


class ObservableObject:
    def __init__(self):
        self.property_changing = Event()
        self.property_changed = Event()

    def _set_property(self, property_name: str, current_value: Any, new_value: Any) -> Any:
        if current_value == new_value:
            return current_value

        changing_args = PropertyChangingEventArgs(property_name, current_value, new_value)
        self.property_changing.__call__(self, changing_args)

        if not changing_args.can_change:
            print(f"Change in the '{property_name}' property has been denied")
            return current_value

        self.property_changed.__call__(self, PropertyChangedEventArgs(property_name))

        return new_value


class Person(ObservableObject):
    def __init__(self):
        super().__init__()
        self._name = ""
        self._age = 0
        self._email = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = self._set_property("name", self._name, value)

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        self._age = self._set_property("age", self._age, value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = self._set_property("email", self._email, value)


class Product(ObservableObject):
    def __init__(self):
        super().__init__()
        self._title = ""
        self._price = 0.0
        self._quantity = 0

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = self._set_property("title", self._title, value)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        self._price = self._set_property("price", self._price, value)

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        self._quantity = self._set_property("quantity", self._quantity, value)
