from lab5 import User, UserRepository, AuthService

print("=== ДЕМОНСТРАЦИЯ СИСТЕМЫ АВТОРИЗАЦИИ ===\n")

# Создание репозитория и сервиса авторизации
user_repo = UserRepository("users.json")
auth_service = AuthService(user_repo)

# Добавление пользователей
print("1. ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ")
users = [
    User(name="Иван Иванов", login="ivan", password="pass123", email="ivan@mail.ru", address="Москва"),
    User(name="Петр Петров", login="petr", password="qwerty", email="petr@yandex.ru"),
    User(name="Мария Сидорова", login="maria", password="123456", address="Санкт-Петербург")
]

for user in users:
    try:
        user_repo.add(user)
        print(f"   Добавлен: {user.name} (логин: {user.login})")
    except ValueError as e:
        print(f"   Ошибка: {e}")

print(f"\n   Всего пользователей: {len(user_repo.get_all())}")

# Авторизация
print("\n2. АВТОРИЗАЦИЯ")
auth_service.sign_in("ivan", "pass123")
print(f"   Авторизован: {auth_service.is_authorized}")
if auth_service.current_user:
    print(f"   Текущий пользователь: {auth_service.current_user.name}")

# Смена пользователя
print("\n3. СМЕНА ПОЛЬЗОВАТЕЛЯ")
auth_service.sign_out()
auth_service.sign_in("maria", "123456")
if auth_service.current_user:
    print(f"   Новый пользователь: {auth_service.current_user.name}")

# Редактирование пользователя
print("\n4. РЕДАКТИРОВАНИЕ ПОЛЬЗОВАТЕЛЯ")
user = user_repo.get_by_login("ivan")
if user:
    user.email = "new_ivan@mail.ru"
    user_repo.update(user)
    print(f"   Обновлен email пользователя: {user.name}")

# Показать всех пользователей (отсортированных по name)
print("\n5. СПИСОК ПОЛЬЗОВАТЕЛЕЙ (отсортирован по имени):")
for user in user_repo.get_all():
    print(f"   {user.id}: {user.name} ({user.login}) - email: {user.email}")

# Выход
print("\n6. ВЫХОД ИЗ СИСТЕМЫ")
auth_service.sign_out()
print(f"   Авторизован: {auth_service.is_authorized}")

print("\n=== ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА ===")


"""Демонстрация автоматической авторизации при повторном запуске"""
print("\n=== ПРОВЕРКА АВТОМАТИЧЕСКОЙ АВТОРИЗАЦИИ ===")

# Создаем новую систему (имитируем повторный запуск)
user_repo = UserRepository("users.json")
auth_service = AuthService(user_repo)

if auth_service.is_authorized:
    print("Автоматическая авторизация выполнена!")
    print(f"Текущий пользователь: {auth_service.current_user.name}")
else:
    print("Автоматическая авторизация не выполнена")

