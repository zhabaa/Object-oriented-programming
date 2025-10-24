from abc import ABC, abstractmethod

# region without mixin

class DataPropertyChangeListener(ABC):
    @abstractmethod
    def on_property_changed(self, obj: object, prop_name: str) -> None: ...


class SimpleDataPropertyChangeListener(DataPropertyChangeListener):
    def on_property_changed(self, obj: object, prop_name: str) -> None:
        print(f"Property {prop_name} changed in object {obj}")


class DataPropertyChangingListener(ABC):
    @abstractmethod
    def on_property_changing(
        self, obj: object, prop_name: str, old_value: object, new_value: object
    ) -> None: ...


class ColorValidator(DataPropertyChangingListener):
    def on_property_changing(
        self, obj: object, prop_name: str, old_value: object, new_value: object
    ) -> bool:
        if prop_name != "color":
            return True

        return new_value in ["red", "green", "blue"]

# endregion 

class NotifyPropertyChangedMixin:
    def __init__(self):
        self.data_property_changed_listeners: list[DataPropertyChangeListener] = list()

    def add_data_property_changed_listener(
        self, listener: DataPropertyChangeListener
    ) -> None:
        self.data_property_changed_listeners.append(listener)

    def remove_data_property_changed_listener(
        self, listener: DataPropertyChangeListener
    ) -> None:
        self.data_property_changed_listeners.remove(listener)

    def notify_data_property_changed(self, prop_name: str) -> None:
        for listener in self.data_property_changed_listeners:
            listener.on_property_changed(self, prop_name)

    def __setattr__(self, key, value):
        if key in ["data_property_changed_listeners"]:
            super().__setattr__(key, value)
            return

        self.notify_data_property_changed(key)

class NotifyPropertyChangingMixin:
    def __init__(self):
        self.data_property_changing_listeners: list[DataPropertyChangingListener] = (
            list()
        )

    def add_data_property_changing_listener(
        self, listener: DataPropertyChangingListener
    ) -> None:
        self.data_property_changing_listeners.append(listener)

    def remove_data_property_changing_listener(
        self, listener: DataPropertyChangingListener
    ) -> None:
        self.data_property_changing_listeners.remove(listener)

    def notify_data_property_changing(self, prop_name, old_value, new_value):
        return all(
            validator.on_property_changing(self, prop_name, old_value, new_value)
            for validator in self.add_data_property_changing_listeners
        )

    def __setattr__(self, key, value):
        if key in ["data_property_changing_listeners"]:
            super().__setattr__(key, value)
            return

        self.notify_data_property_changing(key)


class Toad(NotifyPropertyChangedMixin, NotifyPropertyChangingMixin):
    def __init__(self, name: str, color: str) -> None:
        NotifyPropertyChangedMixin.__init__(self)
        NotifyPropertyChangingMixin.__init__(self)

        self._name = name
        self._color = color

    # region 123
    # @property
    # def name(self) -> str:
    #     return self._name

    # @name.setter
    # def name(self, name: str) -> None:
    #     self._name = name

    #     for listener in self.data_property_changed_listeners:
    #         listener.on_property_changed(self, "name")

    # @property
    # def color(self) -> str:
    #     return self._color

    # @color.setter
    # def color(self, color: str) -> None: ...

    # def __setattr__(self, key, value):
    #     if key in [
    #         "data_property_changed_listeners",
    #         "data_property_changing_listeners",
    #     ]:
    #         super().__setattr__(key, value)
    #         return

    #     old_value = self.__getattribute__(key)

    #     if self.notify_data_property_changing(key, old_value, value):
    #         return

    #     # self.__dict__[key] == value
    #     super().__setattr__(key, value)

    #     self.notify_data_property_changed(key)
    
    #endregion 

    def __setattr__(self, name, value):
        NotifyPropertyChangingMixin.__setattr__(self, name, value)
        NotifyPropertyChangedMixin.__setattr__(self, name, value)

        # добить
