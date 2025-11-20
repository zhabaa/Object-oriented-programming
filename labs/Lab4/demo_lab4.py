from lab4 import PropertyChangedHandler, PropertyChangingValidator, Person, Product


changed_handler = PropertyChangedHandler()
validator = PropertyChangingValidator()

person = Person()
product = Product()

person.property_changed += changed_handler
person.property_changing += validator

product.property_changed += changed_handler
product.property_changing += validator

print("=== Тестирование класса Person ===")
person.name = "Иван"        # Корректное значение
person.age = 25             # Корректное значение
person.age = -5             # Некорректное значение (отрицательный возраст)
person.email = ""           # Некорректное значение (пустая строка)

print("\n=== Тестирование класса Product ===")
product.title = "Ноутбук"   # Корректное значение
product.price = 999.99      # Корректное значение
product.price = -100.0      # Некорректное значение (отрицательная цена)
product.quantity = 10       # Корректное значение
product.title = ""          # Некорректное значение (пустая строка)

print("\n=== Отписка от событий и повторная проверка ===")
person.property_changed -= changed_handler
person.property_changing -= validator

person.name = "Петр"        # Изменение без уведомлений

print("\n=== Конец демонстрации ===")
