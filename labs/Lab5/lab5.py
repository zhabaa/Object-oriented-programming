import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, Optional, Sequence, Type, TypeVar

T = TypeVar('T')


@dataclass(order=True)
class User:
    name: str = field(compare=False)
    login: str = field(compare=False)
    password: str = field(compare=False, repr=False)
    id: Optional[int] = field(default=None, compare=True)
    email: Optional[str] = field(default=None, compare=False)
    address: Optional[str] = field(default=None, compare=False)


#region abc classes

class IDataRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> Sequence[T]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def add(self, item: T) -> None:
        pass
    
    @abstractmethod
    def update(self, item: T) -> None:
        pass
    
    @abstractmethod
    def delete(self, item: T) -> None:
        pass


class IUserRepository(IDataRepository[User]):
    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]:
        pass


class IAuthService(ABC):
    @abstractmethod
    def sign_in(self, login: str, password: str) -> bool:
        pass
    
    @abstractmethod
    def sign_out(self) -> None:
        pass
    
    @property
    @abstractmethod
    def is_authorized(self) -> bool:
        pass
    
    @property
    @abstractmethod
    def current_user(self) -> Optional[User]:
        pass

#endregion


class DataRepository(IDataRepository[T]):
    def __init__(self, filename: str, data_class: Type[T]):
        self.filename = filename
        self.data_class = data_class
        self._data: list[T] = []
        self._load_data()
    
    def _load_data(self) -> None:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data_dicts = json.load(f)
                    self._data = [self.data_class(**item) for item in data_dicts]

            except (json.JSONDecodeError, FileNotFoundError):
                self._data = []

        else:
            self._data = []
    
    def _save_data(self) -> None:
        data_dicts = []

        for item in self._data:
            item_dict = item.__dict__.copy()
            data_dicts.append(item_dict)
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data_dicts, f, ensure_ascii=False, indent=2)
    
    def get_all(self) -> Sequence[T]:
        return sorted(self._data) if hasattr(self.data_class, 'name') else self._data
    
    def get_by_id(self, id: int) -> Optional[T]:
        for item in self._data:
            if getattr(item, 'id') == id:
                return item
        return None
    
    def add(self, item: T) -> None:
        if getattr(item, 'id') is None:
            max_id = max([getattr(i, 'id') for i in self._data], default=0)
            setattr(item, 'id', max_id + 1)

        self._data.append(item)
        self._save_data()
    
    def update(self, item: T) -> None:
        item_id = getattr(item, 'id')

        for i, existing_item in enumerate(self._data):
            if getattr(existing_item, 'id') == item_id:
                self._data[i] = item
                self._save_data()
                return

        raise ValueError(f"Item with id {item_id} not found")
    
    def delete(self, item: T) -> None:
        item_id = getattr(item, 'id')
        self._data = [i for i in self._data if getattr(i, 'id') != item_id]
        self._save_data()


class UserRepository(IUserRepository):
    def __init__(self, filename: str = "users.json"):
        self.data_repository = DataRepository(filename, User)
    
    def get_all(self) -> Sequence[User]:
        return self.data_repository.get_all()
    
    def get_by_id(self, id: int) -> Optional[User]:
        return self.data_repository.get_by_id(id)
    
    def get_by_login(self, login: str) -> Optional[User]:
        for user in self.data_repository.get_all():
            if user.login == login:
                return user

        return None
    
    def add(self, user: User) -> None:
        if self.get_by_login(user.login):
            raise ValueError(f"User with login '{user.login}' already exists")
        
        self.data_repository.add(user)
    
    def update(self, user: User) -> None:
        existing_user = self.get_by_login(user.login)

        if existing_user and existing_user.id != user.id:
            raise ValueError(f"User with login '{user.login}' already exists")

        self.data_repository.update(user)
    
    def delete(self, user: User) -> None:
        self.data_repository.delete(user)


class AuthService(IAuthService):
    def __init__(self, user_repository: UserRepository, auth_file: str = "auth_session.json"):
        self.user_repository = user_repository
        self.auth_file = auth_file
        self._current_user: Optional[User] = None
        self._auto_login()
    
    def _auto_login(self) -> None:
        if os.path.exists(self.auth_file):
            try:
                with open(self.auth_file, 'r', encoding='utf-8') as f:
                    auth_data = json.load(f)
                
                user_id = auth_data.get('user_id')
        
                if user_id:
                    user = self.user_repository.get_by_id(user_id)
        
                    if user:
                        self._current_user = user
                        print(f"The user is automatically logged: {user.name}")
        
            except (json.JSONDecodeError, KeyError):
                # os.remove(self.auth_file) хз удадение так себе
                raise Exception("File may be corrupted, please check")

    def _save_auth_session(self) -> None:
        if self._current_user:
            auth_data = {'user_id': self._current_user.id}
            
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                json.dump(auth_data, f)

        elif os.path.exists(self.auth_file):
            os.remove(self.auth_file)
    
    def sign_in(self, login: str, password: str) -> bool:
        user = self.user_repository.get_by_login(login)

        if user and user.password == password:
            self._current_user = user
            self._save_auth_session()
            print(f"Успешная авторизация: {user.name}")
            return True

        else:
            print("Invalid username or password")
            return False
    
    def sign_out(self) -> None:
        if self._current_user:
            print(f"User logged out: {self._current_user.name}")
            self._current_user = None
            self._save_auth_session()
        else:
            print("No authorized user")
    
    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None
    
    @property
    def current_user(self) -> Optional[User]:
        return self._current_user
