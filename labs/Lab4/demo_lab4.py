from testClasses import Person, Product
from lab4 import ConsolePropertyChangedHandler, PropertyValidator


# Демонстрация работы
print("=== ДЕМОНСТРАЦИЯ СИСТЕМЫ СОБЫТИЙ И ВАЛИДАЦИИ ===\n")

# Создаем обработчики
console_handler = ConsolePropertyChangedHandler()
validator = PropertyValidator()

# Добавляем правила валидации
validator.add_rule("name", lambda old_val, new_val: len(new_val) >= 2)
validator.add_rule("age", lambda old_val, new_val: 0 <= new_val <= 150)
validator.add_rule("email", lambda old_val, new_val: "@" in new_val)
validator.add_rule("price", lambda old_val, new_val: new_val >= 0)
validator.add_rule("quantity", lambda old_val, new_val: new_val >= 0)

# Создаем объекты
person = Person()
product = Product()

# Подписываемся на события
person.property_changing += validator
person.property_changed += console_handler

product.property_changing += validator
product.property_changed += console_handler

print("1. Тестирование класса Person:")
print("Попытка установить корректное имя:")
person.name = "Иван"

print("\nПопытка установить слишком короткое имя:")
person.name = "Я"

print("\nПопытка установить корректный возраст:")
person.age = 25

print("\nПопытка установить некорректный возраст:")
person.age = -5

print("\nПопытка установить корректный email:")
person.email = "ivan@mail.com"

print("\nПопытка установить некорректный email:")
person.email = "invalid-email"

print("\n2. Тестирование класса Product:")
print("Попытка установить корректную цену:")
product.price = 99.99

print("\nПопытка установить отрицательную цену:")
product.price = -10.0

print("\nПопытка установить корректное количество:")
product.quantity = 50

print("\nПопытка установить отрицательное количество:")
product.quantity = -5

print("\n3. Тестирование отписки от событий:")
# Отписываемся от событий
person.property_changing -= validator
person.property_changed -= console_handler

print("После отписки (изменения не должны валидироваться и логироваться):")
person.name = "Петр"
person.age = 30
