

class Logger:
    def __init__(self, logger_type: str, 
                 file_path: str | None = None,
                 url: str | None = None, 
                 port: int | None = None,
                 login: str | None = None,
                 password: str | None = None) -> None:
        self.logger_type = logger_type
        self.file_path = file_path
        self.url = url
        self.port = port
        self.login = login
        self.password = password

    def log(self, message: str) -> None:
        if self.logger_type == 'console':
            print(message)
        
        elif self.logger_type == 'file':
            try:
                with open('', 'a') as f:
                    f.write(message)
            except Exception:
                pass
        
        elif self.logger_type == 'socket':
            pass

        pass
    

from abc import ABC, abstractmethod
from logging.handlers import SocketHandler
from typing import Collection
from warnings import filters


class ABitBetterLogger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


class ConsoleLogger(ABitBetterLogger):
    def log(self, message: str) -> None:
        print(message)
    

class FileLogger(ABitBetterLogger):
    def __init__(self, file_path) -> None:
        self.file_path = file_path
    
    def log(self, message: str) -> None:
        try:
            with open('', 'a') as f:
                f.write(message)
        except Exception:
            pass

class SocketLogger(ABitBetterLogger):
    def __init__(self, url: str, port: int) -> None:
        self.url = url
        self.port = port
    
    def log(self, message: str) -> None:
        ...
        
class SimpleFilteredLogger(ABitBetterLogger):
    def __init__(self, filter_str: str) -> None:
        self.filter_str = filter_str
    
    def log(self, message: str) -> None:
        if self.filter_str not in message:
            return
    

import re


class RegExFilteredLogger(ABitBetterLogger):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
    
    def log(self, message: str) -> None:
        if re.match(self.pattern, message) is not None:
            return 
        else:
            pass
# -------------------------------------------------
# Наследование

class A:
    ...

class B(A):
    ...

# Агрегация

class A:
    ...
    
class B:
    def __init__(self, a: A) -> None:
        self.a = a
        
a = A()
b = B(a)

# Композиция

class A:
    ...

class B:
    def __init__(self) -> None:
        self.a = A()
        
# -------------------------------------------------
class Filter(ABC):
    @abstractmethod
    def filter(self, message: str) -> None:
        ...
    
class SimpleFilter(Filter):
    def __init__(self, filter_str: str) -> None:
        self.filter_str = filter_str
    
    def filter(self, message: str) -> bool:
        return self.filter_str.lower() in message.lower()
    
class RegExFilter(Filter):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
    
    def filter(self, message: str) -> bool:
        return re.match(self.pattern, message) is not None

class Handler(ABC):
    @abstractmethod
    def handle(self, message: str) -> None:
        print(message)
    

class FilterHandler(Handler):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
    
    def handle(self, message: str) -> None:
        try:
            with open(self.file_path, 'a') as f:
                f.write(message)
        except Exception:
            pass
    
    
class CoolLogger:
    def __init__(self, filters: list[Filter], handlers: list[Handler]) -> None:
        self.filters = filters
        self.handlers = handlers
        self.formatter = FORMATTER # ихменить соо + время не время
    
    def log(self, message: str) -> None:
        if not all(flt.filter(message) for flt in self.filters):
            return
        
        for handle in self.handlers:
            handle.handle(message)

logger = CoolLogger(
    filters = [SimpleFilter('error'),
               RegExFilter('.*')],
    handlers = [ConsoleHandler(),
                FileLogger('file_apth'),
                SocketHandler(host = "localhost",
                              port=8080)]
)