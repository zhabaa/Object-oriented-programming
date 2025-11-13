from lab4 import Event, PropertyChangedEventArgs, PropertyChangingEventArgs

class ObservableObject:
    def __init__(self):
        self.property_changing = Event[PropertyChangingEventArgs]()
        self.property_changed = Event[PropertyChangedEventArgs]()

# 7. Классы с уведомлениями об изменении свойств

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
        if value != self._name:
            # Событие до изменения (валидация)
            changing_args = PropertyChangingEventArgs("name", self._name, value)
            self.property_changing.invoke(self, changing_args)
            
            if changing_args.can_change:
                old_value = self._name
                self._name = value
                # Событие после изменения
                self.property_changed.invoke(self, PropertyChangedEventArgs("name"))
            else:
                print("Изменение имени отменено")
    
    @property
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, value: int) -> None:
        if value != self._age:
            changing_args = PropertyChangingEventArgs("age", self._age, value)
            self.property_changing.invoke(self, changing_args)
            
            if changing_args.can_change:
                old_value = self._age
                self._age = value
                self.property_changed.invoke(self, PropertyChangedEventArgs("age"))
            else:
                print("Изменение возраста отменено")
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        if value != self._email:
            changing_args = PropertyChangingEventArgs("email", self._email, value)
            self.property_changing.invoke(self, changing_args)
            
            if changing_args.can_change:
                old_value = self._email
                self._email = value
                self.property_changed.invoke(self, PropertyChangedEventArgs("email"))
            else:
                print("Изменение email отменено")

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
        if value != self._title:
            changing_args = PropertyChangingEventArgs("title", self._title, value)
            self.property_changing.invoke(self, changing_args)
            
            if changing_args.can_change:
                self._title = value
                self.property_changed.invoke(self, PropertyChangedEventArgs("title"))
            else:
                print("Изменение названия отменено")
    
    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, value: float) -> None:
        if value != self._price:
            changing_args = PropertyChangingEventArgs("price", self._price, value)
            self.property_changing.invoke(self, changing_args)
            
            if changing_args.can_change:
                self._price = value
                self.property_changed.invoke(self, PropertyChangedEventArgs("price"))
            else:
                print("Изменение цены отменено")
    
    @property
    def quantity(self) -> int:
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: int) -> None:
        if value != self._quantity:
            changing_args = PropertyChangingEventArgs("quantity", self._quantity, value)
            self.property_changing.invoke(self, changing_args)
            
            if changing_args.can_change:
                self._quantity = value
                self.property_changed.invoke(self, PropertyChangedEventArgs("quantity"))
            else:
                print("Изменение количества отменено")
