from lab5 import AuthService, UserRepository, User

print("=== ДЕМОНСТРАЦИЯ СИСТЕМЫ АВТОМАТИЧЕСКОЙ АВТОРИЗАЦИИ ===\n")

user_repo = UserRepository("users.json")
auth_service = AuthService(user_repo)

print(f"is auth: {auth_service.is_authorized}")
print(auth_service.current_user)

# auth_service.sign_out()

print(f"is auth: {auth_service.is_authorized}")

user = User(name="qweqwe", login="qweqweqwe", password="qweqweqwe", email=None, address=None)

user_repo.add(user)
